import logging, os, json

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class ESS:

    def __init__(self, Battery_Capacity, start_SoC, max_charging_power, max_discharging_power):
        #Enter battery capacity in KWh
        self.Battery_Capacity = Battery_Capacity
        self.SoC = start_SoC
        self.max_charging_power = max_charging_power
        self.max_discharging_power = max_discharging_power
        logger.debug("Local ESS created")


    def get_SoC(self):
        return self.SoC

    def set_SoC(self, value):
        self.SoC = value

    def get_Battery_Capacity(self):
        return self.Battery_Capacity

    def get_max_charging_power(self):
        return self.max_charging_power

    def get_max_discharging_power(self):
        return self.max_discharging_power

    def calculate_S0C_next_timestep(self, SoC_before, P_bat, timestep_in_sec):
        logger.debug("SoC before " + str(SoC_before))
        logger.debug("P_bat_result " + str(P_bat))
        value = (SoC_before + ((P_bat * timestep_in_sec)/ (self.Battery_Capacity * 3600)))

        if value < 0:
            value = 0
        elif value > 100:
            value = 100

        SoC_now = value
        return SoC_now