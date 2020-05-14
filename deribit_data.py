import requests
import time
import pandas as pd
import numpy as np
from tqdm import tqdm

class OptionsData:

    def __init__(self, currency):
        self.url = 'https://www.deribit.com/api/v2/public/'
        self.currency = currency

    def get_histvol_data(self):
        data = {"currency": self.currency}
        d = requests.get(self.url + "get_historical_volatility?", data)
        df = pd.DataFrame(d.json()['result'])
        df.columns = ['date', str(self.currency.lower())+'_hist_vol']
        df['date'] = pd.to_datetime(df.date, unit='ms')
        df = df.set_index("date")
        return df

    def get_options_list(self):
        data = {'currency': self.currency,
               'kind': 'option'}
        r = requests.get(self.url + 'get_instruments', data)
        df = pd.DataFrame(r.json()['result'])
        df['time_to_maturity'] = ((df.expiration_timestamp/1000) - time.time())/(60*24*24)
        cols = ['expiration_timestamp', 'option_type', 'instrument_name', 'strike', 'time_to_maturity']
        df = df[cols]
        return df

    def get_options_stats(self):
        storage = []
        options_list = self.get_options_list()
        iv_url = self.url + 'get_order_book?instrument_name='
        for option in tqdm(range(len(options_list))):
            data = iv_url + options_list.instrument_name.values[option]
            storage.append(requests.get(data).json()['result'])
        iv = pd.DataFrame(storage)
        df = pd.concat([options_list, iv], axis=1)
        return df
