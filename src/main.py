"""
Created on Jan 25 16:42 2019

@author: nishit
"""
import json
import sys

from src.http_ofw import Http_ofw
import optparse
#from src.config_input import input as input_file
from src.endpoint_inputs import Inputs
from src.photovoltaic import PV
from src.EV import EV
from src.local_battery import ESS
from src.EV import Charger
from src.load import Load
from src.utils import Utils
import logging, os, time


logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


if __name__ == '__main__':
    """
       
    """

    utils = Utils()
    host="localhost"
    port=8001
    id="92206fa729de"
    number_km = 10

    # creating the ESS system
    ESS_capacity = 70  # kWh
    Max_Charging_Power = 33
    Max_Discharging_Power = 33
    ESS_SoC_Start = 0.5
    local_ESS = ESS(ESS_capacity, ESS_SoC_Start, Max_Charging_Power, Max_Discharging_Power)

    # creating PV system
    PVs={}
    PVs["PV_90"] = PV(90)
    PVs["PV_50"] = PV(50)

    #creating Load object
    Load_1= Load()

    #creatiing Evs
    EV_Battery_Capacity = 18.7# kWh
    consumption_pro_100_km =  11.7 / 100
    EVs={}
    EVs["ev1"] = EV(1, EV_Battery_Capacity, 0.2, consumption_pro_100_km)
    EVs["ev2"] = EV(2, EV_Battery_Capacity, 0.2, consumption_pro_100_km)
    EVs["ev3"] = EV(3, EV_Battery_Capacity, 0.2, consumption_pro_100_km)
    EVs["ev4"] = EV(4, EV_Battery_Capacity, 0.2, consumption_pro_100_km)
    EVs["ev5"] = EV(5, EV_Battery_Capacity, 0.2, consumption_pro_100_km)

    #creating chargers
    Chargers={}
    Chargers["Charger1"] = Charger(7)
    Chargers["Charger2"] = Charger(7)
    Chargers["Charger3"] = Charger(7)
    Chargers["Charger4"] = Charger(22)
    Chargers["Charger5"] = Charger(22)


    #scenarios_list=["scenario1","scenario2", "scenario3", "scenario4", "scenario5", "scenario6", "scenario7", "scenario8", "scenario9", "scenario10", "scenario11", "scenario12", "scenario13"]
    scenarios_list = ["scenario2"]



    for scenario in scenarios_list:
        logger.debug("###################################")
        logger.debug("scenario " + str(scenario))
        logger.debug("###################################")
        #from src.config_input import input as input_file

        config_path = "H:/Doktorarbeit/UCC/Linksmart/stochastic-simulator-paper/src/config_input.py"
        with open(config_path, "r") as in_file:
            input_file=json.loads(in_file.read())
        logger.debug("input_file "+str(input_file))

        path_results = "results/logs"
        #path_results="/home/vinoth/ofw/optimization-framework/logs"
        #path_scenarios = "/home/garagon/stochastic/src/scenarios/"+str(scenario)+".xlsx"
        path_scenarios = "scenarios/" + str(scenario) + ".xlsx"
        logger.debug("path scenarios "+str(path_scenarios))
        path_output="results/output_"+str(scenario)+".csv"
        #path_output = "/home/garagon/stochastic/src/results/output_"+str(scenario)+".csv"
        logger.debug("path output " + str(path_output))
        utils.del_file_if_existing(path_output)
        #path_input = "/home/garagon/stochastic/src/results/input_"+str(scenario)+".csv"
        path_input = "results/input_" + str(scenario) + ".csv"
        logger.debug("path input " + str(path_input))
        utils.del_file_if_existing(path_input)



        #SoC_EV_start={"1":20,"2":20,"3":20,"4":20,"5":20}
        #SoC_EV_start = input_file["PROFEV"]["VAC_SoC_Value"]
        #SoC_bat_start = input_file["ESS"]["SoC_Value"]

        unit_consumption = utils.calculate_unit_consumption(number_km)
        logger.debug("unit_consumption "+str(unit_consumption))
        #input_file["PROFEV"]["Unit_Consumption_Assumption"]=unit_consumption


        command_to_execute = {"host":host,"port":port}
        http = Http_ofw(command_to_execute)
        ofw=Inputs(http)


        logger.debug("Starting the loop")

        #SoC_bat_next_timestep = SoC_bat_start
        Pev={}



        for time_sim in range(24):
            logger.debug("##################################################################")
            logger.debug("Time "+str(time_sim))
            logger.debug("##################################################################")

            #time_sim = 7

            #EV_SoC_aggregated =  utils.get_SoC_aggregated(EVs)
            #logger.debug("EV_SoC_aggregated " + str(EV_SoC_aggregated))

            #get the SoC of the local ESS
            local_ESS_SoC = local_ESS.get_SoC()
            logger.debug("Local_ESS_Soc " + str(local_ESS_SoC))
            # changing input_file for PROFEV
            input_file["ESS"]["SoC_Value"] = local_ESS_SoC


            PV_forecast={}
            #get the PV forcast starting from this timestep
            for name, pv in PVs.items():
                PV_forecast[name]=pv.get_forecast(time_sim)
            logger.debug(str(PV_forecast))
            input_file["photovoltaic"]["P_PV"] = PV_forecast["PV_50"]

            #get the Load forecast starting from this timestep
            Load_forecast = Load_1.get_forecast(time_sim)
            logger.debug(str(Load_forecast))
            input_file["load"]["P_Load"] = Load_forecast

            #get the cars connected to the charging statons following the scenario
            charging_stations = utils.get_Cars_in_Chargers_for_Timestep(path_scenarios, Chargers, EVs, time_sim)
            logger.debug("charging stations " + str(charging_stations))

            input_file["Chargers"] = charging_stations


            inputs = {}
            inputs["ESS_SoC"] = local_ESS_SoC
            inputs["VAC_SoC"] = EV_SoC_aggregated
            for name, ev in EVs.items():
                inputs[name]=ev.get_SoC()
            logger.debug("Inputs to file: "+str(inputs))
            logger.debug("Storing inputs")
            utils.store_input_optimization(path_input, inputs, time_sim)


            logger.debug("Input_file "+str(json.dumps(input_file, indent=4, sort_keys=True)))

            # logger.debug("New input file for the simulation " + str(json.dumps(input_file, indent=4, sort_keys=True)))
            ofw.register_input(input_file, id)

            # run simulation
            ofw.run_simulation(id)
            status = "running"
            status = ofw.get_status(id)
            logger.debug("status " + str(status))
            first_sleep = True
            while not ofw.get_status(id) == "stopped":

                logger.debug("waiting time " + str(time_sim) + " for scenario " + str(scenario))
                if first_sleep:
                    first_sleep = False
                    time.sleep(720)  # waits 14 min
                else:
                    time.sleep(30)
                # status = ofw.get_status(id)
                
            outputs_stochastic = ofw.get_outputs(id)
            logger.debug("Outputs "+str(outputs_stochastic))


            sys.exit(0)


            outputs=utils.calculate_powers_first_grid(outputs_stochastic)
            logger.debug("after outputs "+str(outputs))

            #reads results for Pev from the optimization output [kW]
            Pev = utils.get_Pev_from_optimization(outputs)
            logger.debug("Pev "+str(Pev))
            #logger.debug("Car_SoC_dict "+str(Car_SoC_dict))

            SoC_EV_next_timestep = utils.calculate_S0C_EV_next_timestep(SoC_EV_next_timestep, Pev, number_km)
            logger.debug("SoC EV next timestep " + str(SoC_EV_next_timestep))
            Car_SoC_dict = utils.get_SoC_approximation(SoC_EV_next_timestep, 2.5)
            logger.debug("SoC EV next timestep approximated" + str(Car_SoC_dict))

            # calculate Pbat for next timestep
            Pbat = utils.get_Pbat_from_optimization(outputs)
            logger.debug("Pbat " + str(Pbat))

            #SoC_bat arrives in percentage so we divided it to 100
            SoC_bat_next_timestep = (utils.calculate_S0C_bat_next_timestep(SoC_bat_next_timestep/100, Pbat))*100
            logger.debug("SoC bat next timestep "+str(SoC_bat_next_timestep))
            SoC_bat = utils.get_SoC_approximation(SoC_bat_next_timestep/100, 10)
            logger.debug("SoC bat next timestep approximated " + str(SoC_bat))


            #saves results into a file

            utils.store_output_optimization(path_output, outputs, Pev, time_sim)


            #if time_sim == 7:
                #sys.exit(0)




