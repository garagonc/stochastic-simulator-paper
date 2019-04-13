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


    host="simplon.fit.fraunhofer.de"
    port=8000
    #id="a2be69a7d65f"  #this is the one that works
    id="ee350b341a3f"
    path_results="results/logs"
    path_scenarios="./scenarios/scenario1.xlsx"

    SoC_EV_start={"1":0.2,"2":0.2,"3":0.2,"4":0.2,"5":0.2}
    SoC_bat_start = 0.8


    command_to_execute = {"host":host,"port":port}
    http = Http_ofw(command_to_execute)
    ofw=Inputs(http)
    utils=Utils()

    logger.debug("Starting the loop")

    first_sleep=True
    first_timestep=True
    SoC_EV_next_timestep_approximated = SoC_EV_start
    SoC_bat_next_timestep_approximated = SoC_bat_start
    Pev={}

    for time in range(24):
        logger.debug("Time "+str(time))
        # set simulation time
        input_file["PROFEV"]["Start_Time"] = time
        #logger.debug("Input file " + str(input_file))

        #get the cars connected to the charging statons following the scenario
        charging_stations = utils.get_Cars_in_Chargers_for_Timestep(path_scenarios, time)
        logger.debug("charging stations " + str(charging_stations))
        #calculates the SoC for this timestep

        charging_stations = utils.set_SoC_in_EVs(charging_stations, SoC_EV_next_timestep_approximated)
        logger.debug("New charging stations "+str(charging_stations))

        new_SOC_aggregated = utils.get_SoC_aggregated(charg)
        #set the new parameters
        input_file["PROFEV"]["CarPark"]["Charging_Station"] = charging_stations
        logger.debug("New input file for the simulation " + str(input_file))
        """ofw.register_input(input_file, id)

        #run simulation
        ofw.run_simulation(id)

        while ofw.get_status(id) is not "stopped":
            if first_sleep:
                time.sleep(720) #waits 12 min
            else:
                time.sleep(30)"""

        #reads results for Pev and Pbat from the optimization output
        Pev = utils.get_Pev_from_optimization(path_results)
        logger.debug("Pev "+str(Pev))
        Pbat = utils.get_Pbat_from_optimization(path_results)
        logger.debug("Pbat "+str(Pbat))

        #calculate Pev and Pbat for next timestep
        SoC_EV_next_timestep = utils.calculate_S0C_EV_next_timestep(SoC_EV_next_timestep_approximated, Pev)
        logger.debug("SoC EV next timestep " + str(SoC_EV_next_timestep))
        SoC_EV_next_timestep_approximated = utils.get_SoC_approximation(SoC_EV_next_timestep)
        logger.debug("SoC EV next timestep approximated" + str(SoC_EV_next_timestep_approximated))

        SoC_bat_next_timestep = utils.calculate_S0C_bat_next_timestep(SoC_bat_next_timestep_approximated, Pbat)
        logger.debug("SoC bat next timestep "+str(SoC_bat_next_timestep))
        SoC_bat_next_timestep_approximated = utils.get_SoC_approximation(SoC_bat_next_timestep)
        logger.debug("SoC bat next timestep approximated " + str(SoC_bat_next_timestep_approximated))


        #saves results into a file

        if time == 2:
            sys.exit(0)



