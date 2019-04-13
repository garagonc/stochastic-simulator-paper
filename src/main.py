"""
Created on Jan 25 16:42 2019

@author: nishit
"""
import sys

from src.http_ofw import Http_ofw
import optparse
from src.config_input import input as input_file
from src.endpoint_inputs import Inputs
from src.utils import Utils
import logging, os, time


logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


if __name__ == '__main__':
    """
       
    """

    utils = Utils()
    host="simplon.fit.fraunhofer.de"
    port=8000
    #id="a2be69a7d65f"  #this is the one that works
    id="ee350b341a3f"
    path_results="results/logs"
    path_scenarios="./scenarios/scenario1.xlsx"
    path_output="./results/scenario1_output.csv"
    utils.del_file_if_existing(path_output)
    path_input = "./results/scenario1_input.csv"
    utils.del_file_if_existing(path_input)
    number_cars=5

    #SoC_EV_start={"1":20,"2":20,"3":20,"4":20,"5":20}
    SoC_EV_start = input_file["PROFEV"]["VAC_SoC_Value"]
    SoC_bat_start = input_file["ESS"]["SoC_Value"]


    command_to_execute = {"host":host,"port":port}
    http = Http_ofw(command_to_execute)
    ofw=Inputs(http)


    logger.debug("Starting the loop")

    first_sleep=True
    first_timestep=True

    SoC_bat_next_timestep = SoC_bat_start
    Pev={}

    for time in range(24):
        logger.debug("##################################################################")
        logger.debug("Time "+str(time))
        logger.debug("##################################################################")
        # set simulation time
        input_file["PROFEV"]["Start_Time"] = time

        #get the cars connected to the charging statons following the scenario
        charging_stations = utils.get_Cars_in_Chargers_for_Timestep(path_scenarios, time)
        logger.debug("charging stations " + str(charging_stations))
        #calculates the SoC for this timestep

        if time == 0:
            Car_SoC_dict=utils.get_Car_SoCs(input_file["PROFEV"]["CarPark"]["Charging_Station"])
            if not len(Car_SoC_dict) == number_cars:
                #Cars that are not connected at the beginning receive a SoC value of 0.4
                Car_SoC_dict =  utils.complete_SoCs(Car_SoC_dict)
            SoC_EV_next_timestep=Car_SoC_dict
            logger.debug("Car_SoC_dict " + str(Car_SoC_dict))

            Cars_Capacity = input_file["PROFEV"]["CarPark"]["Cars"]
            SoC_aggregated_approximated = utils.get_SoC_aggregated(Car_SoC_dict, Cars_Capacity)
            SoC_aggregated=SoC_aggregated_approximated
            logger.debug("Aggregated SoC " + str(SoC_aggregated_approximated) +"%")
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
            SoC_aggregated = utils.get_SoC_aggregated(SoC_EV_next_timestep, Cars_Capacity)
            SoC_aggregated_approximated = utils.get_SoC_approximation(SoC_aggregated)
            logger.debug("Aggregated SoC " + str(SoC_aggregated_approximated))
            input_file["PROFEV"]["VAC_SoC_Value"] = SoC_aggregated_approximated

            logger.debug("SoC bat " + str(SoC_bat) + "%")
            input_file["ESS"]["SoC_Value"] = SoC_bat

        inputs = {}
        inputs["ESS_SoC"] = SoC_bat
        inputs["Aggregated_SoC"]=SoC_aggregated
        inputs["Aggregated_SoC_appr"] = SoC_aggregated_approximated
        utils.store_input_optimization(path_input, inputs, SoC_EV_next_timestep, Car_SoC_dict, time)


        logger.debug("New input file for the simulation " + str(input_file))
        ofw.register_input(input_file, id)

        #run simulation
        ofw.run_simulation(id)

        while ofw.get_status(id) is not "stopped":
            if first_sleep:
                time.sleep(720) #waits 12 min
            else:
                time.sleep(30)

        #reads results for Pev from the optimization output
        Pev = utils.get_Pev_from_optimization(path_results)
        logger.debug("Pev "+str(Pev))
        logger.debug("Car_SoC_dict "+str(Car_SoC_dict))

        SoC_EV_next_timestep = utils.calculate_S0C_EV_next_timestep(SoC_EV_next_timestep, Pev)
        logger.debug("SoC EV next timestep " + str(SoC_EV_next_timestep))
        Car_SoC_dict = utils.get_SoC_approximation(SoC_EV_next_timestep)
        logger.debug("SoC EV next timestep approximated" + str(Car_SoC_dict))

        # calculate Pbat for next timestep
        Pbat = utils.get_Pbat_from_optimization(path_results)
        logger.debug("Pbat " + str(Pbat))

        SoC_bat_next_timestep = utils.calculate_S0C_bat_next_timestep(SoC_bat_next_timestep, Pbat)
        logger.debug("SoC bat next timestep "+str(SoC_bat_next_timestep))
        SoC_bat = utils.get_SoC_approximation(SoC_bat_next_timestep)
        logger.debug("SoC bat next timestep approximated " + str(SoC_bat))


        #saves results into a file
        outputs=utils.get_results_from_optimization(path_results)
        utils.store_output_optimization(path_output, outputs, Pev, time)


        if time == 23:
            sys.exit(0)



