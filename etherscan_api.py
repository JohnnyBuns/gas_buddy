import json
import requests
from gas_exception import gasException

class etherscan_api:
    '''
        etherscan_api class handles all calls to the etherscan api
    '''
    def __init__(self):
        self.key                    = "PPI13U7W1W35PBPSKF7ZDBEA3QSUNEFA1M"
        self.oracle_endpoint        = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={self.key}"
        self.estimation_endpoint    = f"https://api.etherscan.io/api?module=gastracker&action=gasestimate&gasprice=%d&apikey={self.key}"
        self.gwei_to_wei            = 1000000000

    def get_gas_fees(self):
        '''
            Gets base, safe, and fast gas fees

            Returns:
                suggested_gas_base  - Suggested base
                safe_gas_price	    - The safe gase price
                fast_gas_price	    - Price for quickly completing a transaction
        '''
        suggested_gas_base  = 0
        safe_gas_price      = 0
        fast_gas_price	    = 0

        try:

            response = requests.get(self.oracle_endpoint)
            response_json = response.json()

            print(response_json)
            result = response_json['result']
            suggested_gas_base = float(result['suggestBaseFee'])
            safe_gas_price     = float(result['SafeGasPrice'])
            fast_gas_price     = float(result['FastGasPrice'])
            print(suggested_gas_base)

        except Exception as error:
            raise gasException(f"Failed to get gas fees\n{error}")

        return (suggested_gas_base, safe_gas_price, fast_gas_price)

    def confirmation_time_estimator(self, gas):
        '''
            estimates the amount of time a transaction will be confirmed given a set amount of gas

            Arguments:
                gas             - The given gas for the transaction

            Returns:
                estimated_time  - The time in seconds estimated to complete the transaction
        '''
        time = 0

        try:
            endpoint = self.estimation_endpoint%(int(float(gas)*self.gwei_to_wei))
            print(endpoint)
            response = requests.get(endpoint)
            response_json = response.json()

            print(response_json)
            time = response_json['result']

            if int(time) > 60:
                time = str(float(time)/60.0 ) + ' m'
            else:
                time += ' s'

        except Exception as error:
            raise gasException(f"Failed to get time confirmation\n{error}")

        return time



