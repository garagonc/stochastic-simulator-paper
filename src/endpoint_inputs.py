import sys
import logging, os
import json

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

class Inputs:

    def __init__(self, connection):
        self.connection =connection


    def register_input(self, input_data, id=None):
        logger.debug("Adding inputs")
        logger.debug("id "+str(id))

        # normal working
        payload =json.dumps(input_data, indent=4, sort_keys=True)
        #logger.debug("payload "+str(payload))

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        # if id was present PUT
        if id is not None:
            endpoint = "v1/inputs/dataset/" +str(id)
            #logger.debug("endpoint "+str(endpoint))
            response =self.connection.send_request("PUT", endpoint, payload, headers)
            logger.debug(json.dumps(response, indent=4, sort_keys=True))

    def run_simulation(self,  id=None):
        logger.debug("Starting simulation")
        logger.debug("id "+str(id))

        # normal working
        payload = {
                "control_frequency": 30,
                "horizon_in_steps": 24,
                "dT_in_seconds":3600,
                "model_name": "CarParkModel",
                "repetition": 1,
                "solver": "ipopt"
        }
        #logger.debug("payload "+str(payload))

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        # if id was present PUT
        if id is not None:
            endpoint = "v1/optimization/start/" +str(id)
            #logger.debug("endpoint "+str(endpoint))
            response =self.connection.send_request("PUT", endpoint, payload, headers)
            logger.debug(json.dumps(response, indent=4, sort_keys=True))

    def get_status(self, id):
        logger.debug("Getting status")
        logger.debug("id " + str(id))

        # normal working
        payload = ""
        status=""
        #logger.debug("payload " + str(payload))

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        # if id was present PUT
        if id is not None:
            endpoint = "v1/optimization/status"
            #logger.debug("endpoint " + str(endpoint))
            response = self.connection.send_request("GET", endpoint, payload, headers)
            #logger.debug(json.dumps(response, indent=4, sort_keys=True))
            if response:
                for ids in response["status"].keys():
                    if ids == id:
                        status = response["status"][id]["status"]

                if not status:
                    status = "id not present"
            else:
                status = "id not present"

        return status