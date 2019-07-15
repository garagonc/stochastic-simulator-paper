"""
Created on Jan 25 16:42 2019

@author: nishit
"""
import ast
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
    host="s4g.fit.fraunhofer.de"
    port=8001
    id="fa339df7aee1"
    number_km = 10

    # creating the ESS system
    ESS_capacity = 70  # kWh
    Max_Charging_Power = 33
    Max_Discharging_Power = 33
    ESS_SoC_Start = 0.4
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
    Chargers["charger1"] = Charger(7, None)
    Chargers["charger2"] = Charger(7, None)
    Chargers["charger3"] = Charger(7, None)
    Chargers["charger4"] = Charger(22, None)
    Chargers["charger5"] = Charger(22, None)


    #scenarios_list=["scenario1","scenario2", "scenario3", "scenario4", "scenario5", "scenario6", "scenario7", "scenario8", "scenario9", "scenario10", "scenario11", "scenario12", "scenario13"]
    scenarios_list = ["scenario1"]



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
            #time_sim = 8
            logger.debug("##################################################################")
            logger.debug("Time "+str(time_sim))
            logger.debug("##################################################################")

            #time_sim = 7

            EV_SoC_aggregated =  utils.get_SoC_aggregated(EVs)
            logger.debug("EV_SoC_aggregated " + str(EV_SoC_aggregated))

            #get the SoC of the local ESS
            local_ESS_SoC = local_ESS.get_SoC()
            logger.debug("Local_ESS_Soc " + str(local_ESS_SoC))
            # changing input_file for PROFEV
            input_file["ESS"]["SoC_Value"] = local_ESS_SoC #* 100


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

            input_file["chargers"] = charging_stations


            inputs = {}
            inputs["ESS_SoC"] = local_ESS_SoC
            inputs["VAC_SoC"] = EV_SoC_aggregated
            inputs["time_sim"] = time_sim
            for name, ev in EVs.items():
                inputs[name]=ev.get_SoC()
            #logger.debug("Inputs to file: "+str(inputs))
            logger.debug("Storing inputs")
            utils.store_input_optimization(path_input, inputs)


            logger.debug("Input_file "+str(json.dumps(input_file, indent=4, sort_keys=True)))

            # logger.debug("New input file for the simulation " + str(json.dumps(input_file, indent=4, sort_keys=True)))
            ofw.register_input(input_file, id)

            # run simulation
            ofw.run_simulation(id)
            status = "running"
            logger.debug("status " + str(status))

            logger.debug("waiting time " + str(time_sim) + " for scenario " + str(scenario))
            time_to_sleep= 9*60
            time.sleep(time_to_sleep)
            while not ofw.get_status(id) == "stopped":
                logger.debug("waiting time " + str(time_sim) + " for scenario " + str(scenario))
                time.sleep(30)
                
            outputs_stochastic = ofw.get_outputs(id)
            logger.debug("Outputs "+str(outputs_stochastic))

            



            """outputs_stochastic= { 'feasible_ev_charging_power': {'1562148133.0': 0.0}, 'p_ess': {'1562148133.0': 28.0}, 'p_grid': {'1562148133.0': -28.0}, 'p_pv': {'1562148133.0': 0.0}, 'p_vac': {'1562148133.0': 0.0}}
            outputs_stochastic = {
"feasible_ev_charging_power": {
"1560262735.0": 0
},
"p_ess": {
"1560262735.0": 28
},
"chargers/charger1/ev1/p_ev": {
"1560262735.0": 0
},
"chargers/charger2/ev2/p_ev": {
"1560262735.0": 3
},
"chargers/charger3/ev3/p_ev": {
"1560262735.0": 4
},
"chargers/charger4/ev4/p_ev": {
"1560262735.0": 4
},
"chargers/charger5/ev5/p_ev": {
"1560262735.0": 5
},
"p_grid": {
"1560262735.0": -28
},
"p_pv": {
"1560262735.0": 0
},
"p_vac": {
"1560262735.0": 0
}
}"""

            logger.debug("outputs_stochastic "+str(outputs_stochastic))
            outputs=utils.create_output_message(outputs_stochastic)
            logger.debug("outputs "+str(outputs))

            for i in range(1,6):
                logger.debug("Charger"+str(i)+" "+str(Chargers["charger"+str(i)].EV_connected))
            utils.set_SoC_with_Pev(outputs,Chargers, EVs, number_km)

            # calculate Pbat for next timestep
            Pbat = outputs["p_ess"]
            logger.debug("Pbat " + str(Pbat))

            SoC_ESS = local_ESS.calculate_S0C_next_timestep(Pbat, 3600)
            local_ESS.set_SoC(SoC_ESS)
            logger.debug("SoC_ESS "+str(local_ESS.get_SoC()))

            # saves results into a file
            outputs["time_sim"]=time_sim
            utils.store_output_optimization(path_output, outputs)








            if time_sim == 10:
                sys.exit(0)




