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
    PV_90 = PV(90)
    logger.debug("Time 1 "+str(PV_90.get_forecast(1)))
    logger.debug(str(len(PV_90.get_forecast(1))))
    PV_50 = PV(50)

    sys.exit(0)
    #scenarios_list=["scenario1","scenario2", "scenario3", "scenario4", "scenario5", "scenario6", "scenario7", "scenario8", "scenario9", "scenario10", "scenario11", "scenario12", "scenario13"]
    scenarios_list = ["scenario4","scenario13","scenario8", "scenario9", "scenario10", "scenario11", "scenario12"]



    for scenario in scenarios_list:
        logger.debug("###################################")
        logger.debug("scenario " + str(scenario))
        logger.debug("###################################")
        #from src.config_input import input as input_file

        with open("/home/garagon/stochastic/src/config_input.py", "r") as in_file:
            input_file=json.loads(in_file.read())
        logger.debug("input_file "+str(input_file))

        #path_results = "results/logs"
        path_results="/home/vinoth/ofw/optimization-framework/logs"
        path_scenarios = "/home/garagon/stochastic/src/scenarios/"+str(scenario)+".xlsx"
        logger.debug("path scenarios "+str(path_scenarios))
        # path_output="./src/results/scenario1_output.csv"
        path_output = "/home/garagon/stochastic/src/results/output_"+str(scenario)+".csv"
        logger.debug("path output " + str(path_output))
        utils.del_file_if_existing(path_output)
        path_input = "/home/garagon/stochastic/src/results/input_"+str(scenario)+".csv"
        logger.debug("path input " + str(path_input))
        utils.del_file_if_existing(path_input)
        number_cars = 5


        #SoC_EV_start={"1":20,"2":20,"3":20,"4":20,"5":20}
        SoC_EV_start = input_file["PROFEV"]["VAC_SoC_Value"]
        SoC_bat_start = input_file["ESS"]["SoC_Value"]

        unit_consumption = utils.calculate_unit_consumption(number_km)
        logger.debug("unit_consumption "+str(unit_consumption))
        #input_file["PROFEV"]["Unit_Consumption_Assumption"]=unit_consumption
        logger.debug("input_file " + str(input_file))

        command_to_execute = {"host":host,"port":port}
        http = Http_ofw(command_to_execute)
        ofw=Inputs(http)


        logger.debug("Starting the loop")

        SoC_bat_next_timestep = SoC_bat_start
        Pev={}



        for time_sim in range(24):
            logger.debug("##################################################################")
            logger.debug("Time "+str(time_sim))
            logger.debug("##################################################################")
            # set simulation time
            input_file["PROFEV"]["Start_Time"] = time_sim

            #get the cars connected to the charging statons following the scenario
            charging_stations = utils.get_Cars_in_Chargers_for_Timestep(path_scenarios, time_sim)
            logger.debug("charging stations " + str(charging_stations))
            #calculates the SoC for this timestep

            if time_sim == 0:
                Car_SoC_dict=utils.get_Car_SoCs(input_file["PROFEV"]["CarPark"]["Charging_Station"])
                if not len(Car_SoC_dict) == number_cars:
                    #Cars that are not connected at the beginning receive a SoC value of 0.4
                    Car_SoC_dict =  utils.complete_SoCs(Car_SoC_dict)
                SoC_EV_next_timestep=Car_SoC_dict
                logger.debug("Car_SoC_dict " + str(Car_SoC_dict))

                Cars_Capacity = input_file["PROFEV"]["CarPark"]["Cars"]
                #*100 because soc aggregatted is between 0 and 1
                SoC_aggregated = (utils.get_SoC_aggregated(Car_SoC_dict, Cars_Capacity))*100
                logger.debug("Aggregated SoC " + str(SoC_aggregated) + "%")
                SoC_aggregated_approximated = utils.get_SoC_approximation(SoC_aggregated/100, 2.5)
                logger.debug("Aggregated SoC approximated " + str(SoC_aggregated_approximated) +"%")
                is_EV_Connected = utils.is_ev_connected(path_scenarios,time_sim)
                logger.debug("is_EV_connected "+str(is_EV_Connected))
                input_file["PROFEV"]["VAC_SoC_Value"] = SoC_aggregated_approximated

                SoC_bat = SoC_bat_start
                logger.debug("SoC bat " + str(SoC_bat)+"%")
                input_file["ESS"]["SoC_Value"] = SoC_bat
            else:
                charging_stations = utils.set_SoC_in_EVs(charging_stations, Car_SoC_dict)
                logger.debug("New charging stations "+str(charging_stations))
                input_file["PROFEV"]["CarPark"]["Charging_Station"] = charging_stations

                #is it possible to send any aggregated soc?
                Cars_Capacity=input_file["PROFEV"]["CarPark"]["Cars"]
                logger.debug("SoC next timestep "+str(SoC_EV_next_timestep))
                SoC_aggregated = utils.get_SoC_aggregated(SoC_EV_next_timestep, Cars_Capacity)
                logger.debug("VAC SoC aggregated "+str(SoC_aggregated))
                SoC_aggregated_approximated = utils.get_SoC_approximation(SoC_aggregated, 2.5)
                logger.debug("VAC SoC aggregated aproximated " + str(SoC_aggregated_approximated))
                is_EV_Connected = utils.is_ev_connected(path_scenarios, time_sim)
                logger.debug("is_EV_connected " + str(is_EV_Connected))
                input_file["PROFEV"]["VAC_SoC_Value"] = SoC_aggregated_approximated

                logger.debug("SoC bat " + str(SoC_bat) + "%")
                input_file["ESS"]["SoC_Value"] = SoC_bat

            inputs = {}
            inputs["ESS_SoC"] = SoC_bat_next_timestep
            inputs["ESS_SoC_appr"] = SoC_bat
            inputs["VAC_SoC"]=SoC_aggregated
            inputs["VAC_SoC_appr"] = SoC_aggregated_approximated
            logger.debug("Storing inputs")
            utils.store_input_optimization(path_input, inputs, SoC_EV_next_timestep, Car_SoC_dict, time_sim)


            #logger.debug("New input file for the simulation " + str(json.dumps(input_file, indent=4, sort_keys=True)))
            ofw.register_input(input_file, id)
    
            #run simulation
            ofw.run_simulation(id)
            status="running"
            status = ofw.get_status(id)
            logger.debug("status "+str(status))
            first_sleep = True
            while not ofw.get_status(id) == "stopped":
    
                logger.debug("waiting time "+str(time_sim)+" for scenario " + str(scenario))
                if first_sleep:
                    first_sleep=False
                    time.sleep(720) #waits 14 min
                else:
                    time.sleep(30)
                #status = ofw.get_status(id)

            outputs_stochastic = utils.get_results_from_optimization(path_results)
            outputs=utils.calculate_powers_first_grid(outputs_stochastic, SoC_bat_next_timestep)
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




