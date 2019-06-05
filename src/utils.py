
import logging, os, sys
import glob
import time

import pandas as pd
import json
import math
from pandas import ExcelWriter
import xlsxwriter



logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class Utils:

    def __init__(self):
        self.previous_file=""
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

    def is_new_file(self, folder_path):
        logger.debug("previous file "+str(self.previous_file))
        folder_path = self.get_path(folder_path)
        folder = folder_path + "/*"
        # logger.debug("folder path " + str(folder))
        list_of_files = glob.glob(folder)  # * means all if need specific format then *.csv
        list_of_files_new = []
        for file in list_of_files:
            if "output" in file:
                list_of_files_new.append(file)
        logger.debug("len latest file "+str(len(list_of_files_new)))
        if len(list_of_files_new) > 0:
            latest_file = max(list_of_files_new, key=os.path.getctime)
            logger.debug("latest file " + str(latest_file))
            if latest_file == self.previous_file:
                return False
            else:
                return True
        else:
            return False

    def get_latest_file(self, folder_path):
        folder_path = self.get_path(folder_path)
        folder=folder_path+"/*"
        #logger.debug("folder path " + str(folder))
        list_of_files = glob.glob(folder)  # * means all if need specific format then *.csv
        list_of_files_new=[]
        for file in list_of_files:
            if "output" in file:
                list_of_files_new.append(file)
        latest_file = max(list_of_files_new, key=os.path.getctime)
        if latest_file == self.previous_file:
            return None
        else:
            self.previous_file=latest_file
            logger.debug("latest file " + str(latest_file))
            return latest_file

    def read_data_from_xlsx(self, filepath):
        """Reads data from excel config file, parses it, and returns it as dict

        Arguments:
            filepath {str} -- Filepath to the excel config file

        Returns:
            dict -- Python dict of inputs, outputs, and start config
        """
        filepath = self.get_path(filepath)
        #logger.debug("filepath "+str(filepath))
        if not os.path.isfile(filepath):
            logger.error("Error: Excel file is missing")
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

    def get_car_number(self, name):
        if name=="Car1":
            return 1
        elif name=="Car2":
            return 2
        elif name=="Car3":
            return 3
        elif name=="Car4":
            return 4
        elif name=="Car5":
            return 5
        else:
            return "No car with this name"

    def get_SoC_aggregated(self, SoC_dict, Cars_dict):
        SoC_list=[]
        for car, soc in SoC_dict.items():
            SoC_list.append(soc)

        Battery_Capacity_list=[]
        for car, value in Cars_dict.items():
            Battery_Capacity_list.append(value["Battery_Capacity_kWh"])
        VAC=sum(Battery_Capacity_list)
        return sum([a * b for a, b in zip(SoC_list, Battery_Capacity_list)])/VAC


        #sum(soc*capacity)/
    def get_results_from_optimization(self, folderpath):
        while not self.is_new_file(folderpath):
            time.sleep(2)

        filepath = self.get_latest_file(folderpath)
        # logger.debug("This is the latest file " + str(filepath))

        try:
            with open(filepath, "r") as myfile:
                optimization_result = myfile.read()
            # logger.debug("File: " + str(optimization_result)+" type "+str(type(optimization_result)))
            P_data = json.loads(optimization_result)
            return P_data
        except Exception as e:
            logger.debug("File path not existing")
            logger.error(e)
            sys.exit(0)

    def get_Pev_from_optimization(self, data):
        logger.debug("data for Pev "+str(data))
        try:
            P_ev_return={}
            for charging_stations, power in data["p_ev"].items():
                P_ev_return[str(int(charging_stations)+1)]=power
            for i in range(1,6):
                if not str(i) in P_ev_return.keys():
                    P_ev_return[str(i)]= -1
            return P_ev_return
        except Exception as e:
            logger.debug("Data not existing")
            logger.error(e)
            sys.exit(0)

    def get_Pbat_from_optimization(self, data):
        logger.debug("data for Pbat " + str(data))
        try:
            P_bat_return=data["p_ess"]
            return P_bat_return
        except Exception as e:
            logger.debug("Data not existing")
            logger.error(e)
            sys.exit(0)

    def get_possible_ESS_power(self,SoC_bat, SoC_to_reach):
        Capacity = 70  # kWh
        P_max = Capacity*abs(SoC_bat-SoC_to_reach)/1 #h
        if P_max > 33:
            P_max = 33
        return P_max

    def calculate_powers_first_ess(self, data, ess_soc):
        id=data["id"]
        p_pv= data["p_pv"]
        p_grid = data["p_grid"]
        p_ess = data["p_ess"]
        p_vac = data["p_vac"]
        p_feasible_ev_charging = data["feasible_ev_charging_power"]
        p_ev = data["p_ev"]
        exec_time=data["execution_time"]

        logger.debug("p_grid "+str(p_grid)+" p_VAC "+str(p_vac)+" feas "+str(p_feasible_ev_charging)+" p_pv "+str(p_pv)+" p_ess "+str(p_ess))

        #leftover_vac_charging_power = p_grid - p_ess - p_pv - p_feasible_ev_charging
        leftover_vac_charging_power = p_vac - p_feasible_ev_charging
        logger.debug("leftover vac "+str(leftover_vac_charging_power))


        #if leftover then goes primarly to the ess
        P_max_ess = self.get_possible_ESS_power(ess_soc, 1)
        logger.debug("p_max ess " + str(P_max_ess))
        possible_ess = p_ess - leftover_vac_charging_power
        logger.debug("possible ess "+str(possible_ess))

        #max because p_ess is negative for charging
        p_ess_return= max(possible_ess,-1*P_max_ess)
        logger.debug("p_ess_return " + str(p_ess_return))

        # if lefover bigger than max ess power, rest goe to the grid
        p_grid_return = p_feasible_ev_charging - p_pv - p_ess_return
        logger.debug("p_grid_return " + str(p_grid_return))

        data_to_return= {"id": id, "p_pv":p_pv, "p_grid":p_grid_return,"p_ess":p_ess_return,"p_vac":p_vac, "feasible_ev_charging_power": p_feasible_ev_charging,
                         "p_ev":p_ev,"execution_time":exec_time}
        return data_to_return

    def calculate_powers_first_grid(self, data, ess_soc):
        id=data["id"]
        p_pv= data["p_pv"]
        p_grid = data["p_grid"]
        p_ess = data["p_ess"]
        p_vac = data["p_vac"]
        p_feasible_ev_charging = data["feasible_ev_charging_power"]
        p_ev = data["p_ev"]
        exec_time=data["execution_time"]

        logger.debug("p_grid "+str(p_grid)+" p_VAC "+str(p_vac)+" feas "+str(p_feasible_ev_charging)+" p_pv "+str(p_pv)+" p_ess "+str(p_ess))


        p_grid_return = p_feasible_ev_charging - p_pv - p_ess
        logger.debug("p_grid_return " + str(p_grid_return))


        data_to_return= {"id": id, "p_pv":p_pv, "p_grid_before":p_grid, "p_grid":p_grid_return,"p_ess":p_ess,"p_vac":p_vac, "feasible_ev_charging_power": p_feasible_ev_charging,
                         "p_ev":p_ev,"execution_time":exec_time}
        return data_to_return

    def calculate_S0C_bat_next_timestep(self, SoC_before, P_bat):
        #todo calculate the cars that are not there
        Capacity = 70  # kWh
        dT=1 #hours
        SoC_now={}

        logger.debug("SoC before "+str(SoC_before))
        logger.debug("P_bat_result "+str(P_bat))
        value=(SoC_before - ((P_bat*dT)/Capacity)) # - because with positive Pbat it gives energy

        if value < 0:
            value=0
        elif value > 1:
            value=1

        SoC_now = value
        return SoC_now

    def calculate_unit_consumption(self, number_km_per_hour):
        number_cars=5
        consumption_per_ev = (11.7 * number_km_per_hour) / 100  # 11.7 kwh/100km consumption for VW Eup
        Capacity = 18.700  # kWh
        VAC_Capacity= number_cars * Capacity
        #consumption_per_ev = number_km_per_hour * consumption_for_x_km
        unit_consumption= (consumption_per_ev * 100) / VAC_Capacity
        return unit_consumption




    #def get_charger_connected(self, timestep):
    def calculate_S0C_EV_next_timestep(self, SoC_before, P_ev, number_km_per_hour):
        #number_km = 5
        consumption_for_x_km=(11.7 * number_km_per_hour) / 100 #11.7 kwh/100km consumption for VW Eup
        #logger.debug("consumption for " +str(number_km)+" is "+str(consumption_for_x_km))
        #todo calculate the cars that are not there
        Capacity = 18.700  # kWh
        SoC_now={}
        #logger.debug("SoC before "+str(SoC_before))
        #logger.debug("P_ev_results "+str(P_ev))
        if isinstance(P_ev, dict) and isinstance(SoC_before,dict):
            for car, power in P_ev.items():
                if power == -1:
                    #logger.debug("car " + str(car) + " power " + str(power))
                    value = (SoC_before[car] - (consumption_for_x_km / Capacity))
                    #logger.debug("value "+str(value))
                    if value < 0:
                        value=0
                else:
                    #logger.debug("car "+str(car)+" power "+str(power))
                    value=(SoC_before[car] + (P_ev[car]/Capacity))
                    if value > 1:
                        value = 1
                SoC_now[car] = value
        return SoC_now

    def calculate_S0C_EV_for_sim(self, SoC_before, P_ev, connections, number_km_per_hour):
        #number_km = 10
        consumption_for_x_km=(11.7 * number_km_per_hour) / 100 #11.7 kwh/100km consumption for VW Eup
        Capacity = 18.700  # kWh
        SoC_now=[]
        #logger.debug("SoC "+str(SoC_before))
        #logger.debug("P_Ev "+str(P_ev))
        if isinstance(P_ev, list) and isinstance(SoC_before,list):
            #logger.debug("connections "+str(connections))
            if connections:
                power=P_ev[-1]
                value = (SoC_before[-1] + (power / Capacity))
                if value > 1:
                    value = 1
            else:
                value = (SoC_before[-1] - (consumption_for_x_km / Capacity))
                # logger.debug("value "+str(value))
                if value < 0:
                    value = 0
            #SoC_before.append(value)

        return value

    def get_SoC_approximation(self, dict_values, step):

        if isinstance(dict_values, dict):
            SoC_dict = {}
            for number, SoC in dict_values.items():
                #logger.debug("number "+str(number)+" SoC "+str(SoC))
                SoC_dict[number]=(round((SoC*100)/step)*step)/100
                #frac, whole = math.modf(SoC)
                #logger.debug("frac ev" + str(frac) + " whole " + str(whole))
                #SoC_dict[number] = (round(SoC*100))/100

        else:
            #approximation for bat in steps of 10
            if dict_values > 1:
                dict_values = 1
            #frac, whole = math.modf(dict_values*10)
            #logger.debug("frac " + str(frac) + " whole " + str(whole))
            SoC_dict = round((dict_values*100)/step)*step
        return SoC_dict

    def set_SoC_in_EVs(self, charging_stations, SoC_dict):
        charging_stations_return=charging_stations
        for charger, value in charging_stations_return.items():
            #logger.debug("value "+str(value))
            if "Hosted_Car" in value.keys():
                charger_number = str(self.get_charger_number(charger))
                charging_stations_return[charger]["SoC"]=SoC_dict[charger_number]
        return charging_stations_return

    def get_Car_SoCs(self,charger_with_cars_dict):
        Car_SoC_dict={}
        for charger, value in charger_with_cars_dict.items():
            if len(value) == 3:
                Car_SoC_dict[str(self.get_car_number(value["Hosted_Car"]))] = value["SoC"]
        return Car_SoC_dict
        #logger.debug("Car_SoC_dict "+str(Car_SoC_dict))

    def complete_SoCs(self, Car_Soc_dict):
        random_soc=0.4
        for car_number in range(1,6) :
            if not str(car_number) in Car_Soc_dict.keys():
                Car_Soc_dict[str(car_number)] = random_soc
        return Car_Soc_dict

    def get_Cars_in_Chargers_for_Timestep(self, filepath, timestep):
        charging_stations = {
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
        # Extract inputs sheet
        filepath=self.get_path(filepath)
        logger.debug("filepath "+str(filepath))
        excel_data= self.read_data_from_xlsx(filepath)
        #inputs = excel_data["Car2"]
        #logger.debug("excel inputs "+str(inputs))
        #logger.debug("charging stations "+str(charging_stations))
        #charging_stations_return=charging_stations.copy()
        charging_stations_return={}
        for charger, value in charging_stations.items():
            charging_stations_return[charger]=value
            charger_number=self.get_charger_number(charger)
            #logger.debug("excel_data[Car1]"+str(excel_data["Car1"][timestep]))
            if excel_data["Car1"][timestep]==charger_number:
                charging_stations_return[charger]["Hosted_Car"]="Car1"
            elif excel_data["Car2"][timestep]==charger_number:
                charging_stations_return[charger]["Hosted_Car"]="Car2"
            elif excel_data["Car3"][timestep]==charger_number:
                charging_stations_return[charger]["Hosted_Car"]="Car3"
            elif excel_data["Car4"][timestep]==charger_number:
                charging_stations_return[charger]["Hosted_Car"]="Car4"
            elif excel_data["Car5"][timestep]==charger_number:
                charging_stations_return[charger]["Hosted_Car"]="Car5"
        #logger.debug("charging statins return "+str(charging_stations_return))
        #logger.debug("self charging stations " + str(charging_stations))
        return charging_stations_return

    def is_ev_connected(self,filepath, timestep):
        filepath = self.get_path(filepath)
        logger.debug("filepath " + str(filepath))
        excel_data = self.read_data_from_xlsx(filepath)
        ev_connected_return = {}

        for i in range(1,6):
            if excel_data["Car"+str(i)][timestep] == i:
                ev_connected_return["Car"+str(i)] = True
            else:
                ev_connected_return["Car"+str(i)] = False


        # logger.debug("charging statins return "+str(charging_stations_return))
        # logger.debug("self charging stations " + str(charging_stations))
        return ev_connected_return

    def read_csv_data(self, filepath):
        filepath = self.get_path(filepath)
        #logger.debug("filepath "+str(filepath))
        if not os.path.isfile(filepath):
            logger.debug("No CSV file present")
            return None

        # Read file
        data = pd.read_csv(filepath)
        #logger.debug(data["P_EV1"])
        return data

    def del_file_if_existing(self,filepath):
        filepath=self.get_path(filepath)
        logger.debug("filepath "+str(filepath))
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            print("Error while deleting file ", filepath)

    def store_simulation(self, filepath, p_grid, p_pv,p_ess, p_vac, p_ev):
        #logger.debug("data to store "+str(data_to_store))
        #logger.debug("data to store soc ev " + str(soc_ev))
        #logger.debug("data to store approximated" + str(soc_ev_approximated))
        data_to_pd={}
        data_to_pd["P_Grid"]=p_grid
        data_to_pd["P_PV"]=p_pv
        data_to_pd["P_ESS"] = p_ess
        data_to_pd["P_VAC"]=p_vac
        for i in range(1,6):
            data_to_pd["P_EV"+str(i)]=p_ev[str(i)]
            #logger.debug("len PEV"+str(i)+" "+str(len(data_to_pd["P_EV"+str(i)])))

        logger.debug("data to pandas " + str(data_to_pd))

        df = pd.DataFrame(data_to_pd)
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        #df.to_csv(filepath)

    def store_simulation_soc(self, filepath,soc_bat,soc_ev):
        logger.debug("data to store "+str(soc_bat))
        logger.debug("data to store soc ev " + str(soc_ev))
        #logger.debug("data to store approximated" + str(soc_ev_approximated))
        data_to_pd={}
        data_to_pd["SoC_ESS"]=soc_bat
        for i in range(1,6):
            data_to_pd["SoC_EV"+str(i)]=soc_ev[str(i)]
            #logger.debug("len PEV"+str(i)+" "+str(len(data_to_pd["P_EV"+str(i)])))

        logger.debug("data to pandas " + str(data_to_pd))

        df = pd.DataFrame(data_to_pd)
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def store_input_optimization(self, filepath, data_to_store, soc_ev, soc_ev_approximated, time):

        data=self.read_csv_data(filepath)
        #logger.debug("data to store "+str(data_to_store))
        #logger.debug("data to store soc ev " + str(soc_ev))
        #logger.debug("data to store approximated" + str(soc_ev_approximated))
        SoC_EV = {}
        for i in range(1, 6):
            SoC_EV["SoC_EV" + str(i)] = soc_ev[str(i)]
        data_to_pd = {**data_to_store, **SoC_EV}
        SoC_EV_appr = {}
        for i in range(1, 6):
            SoC_EV_appr["SoC_EV" + str(i) + "_appr"] = soc_ev_approximated[str(i)]
        data_to_pd = {**data_to_pd, **SoC_EV_appr}
        #logger.debug("data to pandas " + str(data_to_pd))

        if data is None:
            df = pd.DataFrame(data_to_pd, index=[time])
            #logger.debug(df["SoC_EV1"])
            df.to_csv(filepath)
        else:
            df2 = pd.DataFrame(data_to_pd, index=[time])
            new_data = pd.concat([data, df2], ignore_index=False)
            #logger.debug(new_data["SoC_EV1"])
            new_data.to_csv(filepath)



    def store_output_optimization(self, filepath, data_to_store, p_ev, time):
        data=self.read_csv_data(filepath)
        data_to_store.pop("p_ev")
        EV = {}
        for i in range(1, 6):
            if p_ev[str(i)] == -1:
                EV["P_EV" + str(i)] = 0
            else:
                EV["P_EV" + str(i)] = p_ev[str(i)]
        # data_to_pd.append({**data_to_store, **EV})
        data_to_pd = {**data_to_store, **EV}
        if data is None:
            #logger.debug("data to pandas "+str(data_to_pd))
            df = pd.DataFrame(data_to_pd, index=[time])
            #logger.debug(df["P_EV1"])
            df.to_csv(filepath)
        else:
            #logger.debug("data to pandas " + str(data_to_pd))
            df2 = pd.DataFrame(data_to_pd, index=[time])
            new_data=pd.concat([data, df2],ignore_index=False)
            #logger.debug(new_data["P_EV1"])
            new_data.to_csv(filepath)



