import logging, os, json

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


class PV:

    def __init__(self, Max_Power):
        self.Max_Power = Max_Power
        self.PV_forecast = [i * (Max_Power / 50.0) for i in self.PV]
        logger.debug("PV created")

    def get_forecast(self, init_time):
        return self.PV_forecast[init_time:init_time+23]

    PV = [
        0,
        0,
        0,
        0,
        0,
        0.39367,
        4.75361,
        15.1473,
        15.867,
        31.79674,
        38.73189,
        33.29914,
        14.63464,
        24.09385,
        10.87046,
        20.06198,
        10.99505,
        2.28806,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0.44908,
        5.68837,
        8.98529,
        26.33816,
        15.66616,
        28.97914,
        41.16202,
        8.14226,
        10.0315,
        8.41445,
        15.84856,
        2.32287,
        1.95342,
        0,
        0,
        0,
        0,
        0,
        0
    ]






