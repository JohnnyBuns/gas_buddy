import time
from etherscan_api import etherscan_api

class gas_updater:
    '''
        gas_updater class will periodically update the gas fees and date
    '''

    def __init__(self):
        self.suggested_gas_base         = 0
        self.suggested_time_estimate    = 0
        self.safe_gas_price             = 0
        self.safe_time_estimate         = 0
        self.fast_gas_price             = 0
        self.fast_time_estimate         = 0
        self.data_points_count          = 0
        self.data_points                = []
        self.base_gas_average           = 0
        self.etherscan_api              = etherscan_api()

    async def gas_update(self, notify_event):
        '''
            gas_update updates the gas fees using data from etherscan

            Arguments:
                notify_event	-   event for meeting criteria (currently below 90 gwei) so we can notify subscribers

        '''
        try:

            gas_fees = self.etherscan_api.get_gas_fees()
            self.suggested_gas_base         = gas_fees[0]
            self.suggested_time_estimate    = self.etherscan_api.confirmation_time_estimator(self.suggested_gas_base)

            self.safe_gas_price             = gas_fees[1]
            self.safe_time_estimate         = self.etherscan_api.confirmation_time_estimator(self.safe_gas_price)

            self.fast_gas_price             = gas_fees[2]
            self.fast_time_estimate         = self.etherscan_api.confirmation_time_estimator(self.fast_gas_price)

            print(self.suggested_gas_base)

            self.data_points.append(self.suggested_gas_base)
            self.data_points_count += 1

            date_points_total = sum(self.data_points)
            self.base_gas_average = date_points_total/self.data_points_count

            base_diff = abs(self.suggested_gas_base - self.base_gas_average)
            base_diff_percent = base_diff/self.base_gas_average

            print(f"average is {self.base_gas_average}, base percent difference is {base_diff_percent}")

            if self.suggested_gas_base <= 90:
                await notify_event()

        except Exception as error:
            time.sleep(5)
            print(error)
