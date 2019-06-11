import logging, os, json

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class EV:

    def __init__(self,ev_number, Battery_Capacity, SoC, consumption_pro_100_km):
        self.Battery_Capacity = Battery_Capacity
        self.consumption = consumption_pro_100_km
        self.Soc = SoC
        self.ev_number = ev_number
        logger.debug("EV "+str(self.ev_number)+" created")

    def get_SoC(self):
        return self.Soc

    def set_SoC(self, value):
        if value < 0 or value >1:
            return 0
        else:
            self.Soc = value
            return 1

    def get_Battery_Capacity(self):
        return self.Battery_Capacity

    def calculate_S0C_next_timestep(self, P_ev, number_km_driven):
        #number_km = 5
        number_km = number_km_driven
        #consumption_for_x_km = (11.7 * number_km) / 100  # 11.7 kwh/100km consumption for VW Eup
        consumption_for_x_km = self.consumption * number_km
        # logger.debug("consumption for " +str(number_km)+" is "+str(consumption_for_x_km))
        #Capacity = 18.700  # kWh
        if P_ev == -1:
            # logger.debug("car " + str(car) + " power " + str(power))
            value = (self.Soc - (consumption_for_x_km / self.Battery_Capacity))
            # logger.debug("value "+str(value))
            if value < 0:
                value = 0
        else:
            # logger.debug("car "+str(car)+" power "+str(power))
            value = (self.Soc + (P_ev / self.Battery_Capacity))
            if value > 100:
                value = 100
        SoC_now = value
        return SoC_now


class Charger:
    def __init__(self, Max_Capacity):
        self.Max_Capacity = Max_Capacity

    def set_EV_connected(self, EV_connected):
        self.EV_connected = EV_connected

    def get_EV_connected(self):
        return  self.EV_connected

    def get_Max_Capacity(self):
        return self.Max_Capacity