
import logging, os, sys
import glob
import pandas as pd
import json
import math

from src.config_input import input as input_file

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class Utils:

    def __init__(self):
        self.charging_stations={
                "Charger1": {
                    "Max_Charging_Power_kW": 7,

                },
                "Charger2": {
                    "Max_Charging_Power_kW": 7,

                },
                "Charger3": {
                    "Max_Charging_Power_kW": 7
                },
                "Charger4": {
                    "Max_Charging_Power_kW": 22,

                },
                "Charger5": {
                    "Max_Charging_Power_kW": 22
                }
            }

    def get_path(self, relative_path):
        path_to_send = os.path.abspath(relative_path)
        return path_to_send

    def get_folder_path(self, path):
        return os.path.dirname(os.path.abspath(path))

    def get_latest_file(self, folder_path):
        folder_path = self.get_path(folder_path)
        folder=folder_path+"\*"
        logger.debug("folder path " + str(folder))
        list_of_files = glob.glob(folder)  # * means all if need specific format then *.csv
        latest_file = min(list_of_files, key=os.path.getctime)
        return latest_file

    def read_data_from_xlsx(self, filepath):
        """Reads data from excel config file, parses it, and returns it as dict

        Arguments:
            filepath {str} -- Filepath to the excel config file

        Returns:
            dict -- Python dict of inputs, outputs, and start config
        """
        filepath = self.get_path(filepath)
        logger.debug("filepath "+str(filepath))
        if not os.path.isfile(filepath):
            logger.error(f"Error: Excel file at {filepath} is missing")
            return

        # Read file
        excel_data = pd.read_excel(filepath, sheet_name="Tabelle1")
        #logger.debug(excel_data)
        return excel_data

    def get_charger_number(self, name):
        if name=="Charger1":
            return 1
        elif name=="Charger2":
            return 2
        elif name=="Charger3":
            return 3
        elif name=="Charger4":
            return 4
        elif name=="Charger5":
            return 5
        else:
            return "No charging station with this name"


    def get_Pev_from_optimization(self, folderpath):
        filepath = self.get_latest_file(folderpath)
        logger.debug("This is the latest file " + str(filepath))

        try:
            with open(filepath, "r") as myfile:
                optimization_result = myfile.read()
            #logger.debug("File: " + str(optimization_result)+" type "+str(type(optimization_result)))
            P_data=json.loads(optimization_result)
            P_ev_return={}
            for charging_stations, power in P_data["p_ev"].items():
                P_ev_return[str(int(charging_stations)+1)]=power
            for i in range(1,6):
                if not str(i) in P_ev_return.keys():
                    P_ev_return[str(i)]= -1
            return P_ev_return
        except Exception as e:
            logger.debug("File path not existing")
            logger.error(e)
            sys.exit(0)

    def get_Pbat_from_optimization(self, folderpath):
        filepath = self.get_latest_file(folderpath)
        logger.debug("This is the latest file " + str(filepath))

        try:
            with open(filepath, "r") as myfile:
                optimization_result = myfile.read()
            #logger.debug("File: " + str(optimization_result)+" type "+str(type(optimization_result)))
            P_data=json.loads(optimization_result)
            P_bat_return=P_data["p_ess"]
            return P_bat_return
        except Exception as e:
            logger.debug("File path not existing")
            logger.error(e)
            sys.exit(0)

    def calculate_S0C_bat_next_timestep(self, SoC_before, P_bat):
        #todo calculate the cars that are not there
        Capacity = 2.43  # kWh
        SoC_now={}
        logger.debug("SoC before "+str(SoC_before))
        logger.debug("P_bat_result "+str(P_bat))
        value=(SoC_before + (P_bat/Capacity))*100
        if value < 0:
            value=0
        elif value > 100:
            value=100

        SoC_now = value
        return SoC_now

    #def get_charger_connected(self, timestep):
    def calculate_S0C_EV_next_timestep(self, SoC_before, P_ev):
        number_km = 5
        consumption_for_x_km=(11.7 * number_km) / 100 #11.7 kwh/100km consumption for VW Eup
        logger.debug("consumption for " +str(number_km)+" is "+str(consumption_for_x_km))
        #todo calculate the cars that are not there
        Capacity = 18.700  # kWh
        SoC_now={}
        logger.debug("SoC before "+str(SoC_before))
        logger.debug("P_ev_results "+str(P_ev))
        if isinstance(P_ev, dict) and isinstance(SoC_before,dict):
            for car, power in P_ev.items():
                if power == -1:
                    #logger.debug("car " + str(car) + " power " + str(power))
                    value = (SoC_before[car] - (consumption_for_x_km / Capacity)) * 100
                    if value < 0:
                        value=0
                else:
                    #logger.debug("car "+str(car)+" power "+str(power))
                    value=(SoC_before[car] + (P_ev[car]/Capacity))*100
                    if value > 100:
                        value = 100
                SoC_now[car] = value
        return SoC_now

    def get_SoC_approximation(self, dict_values):

        if isinstance(dict_values, dict):
            SoC_dict = {}
            for number, SoC in dict_values.items():
                #logger.debug("number "+str(number)+" SoC "+str(SoC))
                frac, whole = math.modf(SoC)
                #logger.debug("frac " + str(frac) + " whole " + str(whole))
                if frac >= 0.5:
                    SoC_dict[number] = math.ceil(SoC) / 100
                else:
                    SoC_dict[number] = math.floor(SoC) / 100
        else:
            frac, whole = math.modf(dict_values)
            # logger.debug("frac " + str(frac) + " whole " + str(whole))
            if frac >= 0.5:
                SoC_dict = math.ceil(dict_values) / 100
            else:
                SoC_dict = math.floor(dict_values) / 100
        return SoC_dict

    def set_SoC_in_EVs(self, charging_stations, SoC_dict):
        charging_stations_return=charging_stations
        for charger, value in charging_stations_return.items():
            #logger.debug("value "+str(value))
            if "Hosted_Car" in value.keys():
                charger_number = str(self.get_charger_number(charger))
                charging_stations_return[charger]["SoC"]=SoC_dict[charger_number]
        return charging_stations_return

    def get_Cars_in_Chargers_for_Timestep(self, filepath, timestep):
        # Extract inputs sheet
        excel_data= self.read_data_from_xlsx(filepath)
        #inputs = excel_data["Car2"]
        #logger.debug("excel inputs "+str(inputs))
        #logger.debug("charging stations "+str(self.charging_stations))
        for charger, value in self.charging_stations.items():
            charger_number=self.get_charger_number(charger)
            if excel_data["Car1"][timestep]==charger_number:
                value["Hosted_Car"]="Car1"
            elif excel_data["Car2"][timestep]==charger_number:
                value["Hosted_Car"]="Car2"
            elif excel_data["Car3"][timestep]==charger_number:
                value["Hosted_Car"]="Car3"
            elif excel_data["Car4"][timestep]==charger_number:
                value["Hosted_Car"]="Car4"
            elif excel_data["Car5"][timestep]==charger_number:
                value["Hosted_Car"]="Car5"
        return self.charging_stations


