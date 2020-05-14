import requests
import pandas as pd
import numpy as np
from tqdm import tqdm

class Options:

    def __init__(self, currency="BTC"):
        """
        Initializing Options.

        Parameters
        ----------
        currency: string ("BTC" or "ETH")
            The cryptocurrency that will be used to retrieve all option
            and volatility related data. The default parameter is "BTC".

        Example
        ---------
        >>> import deribit_data as dm
        >>> data = dm.Options(currency = "ETH")
        """
        self.url = 'https://www.deribit.com/api/v2/public/'
        self.currency = currency.lower()

    def get_hist_vol(self, save_csv=False):
        """
        Retrieves the asset's annualised historical volatility measured
        every hour for the past 15 days.

        Parameters
        -------------
        save_csv: boolean
            Select True to save the historical volatility to a csv file.

        Returns
        -------------
        dataframe:
            A time-series dataframe

        csv:
            A csv file will be saved if save_csv is set to True

        Example
        -------------
        >>> df = data.get_hist_vol()
        >>> df.tail()
        date                    btc_hist_vol
        2020-05-13 21:00:00     95.228999
        2020-05-13 22:00:00     95.501434
        2020-05-13 23:00:00     95.553333
        2020-05-14 00:00:00     95.572422
        2020-05-14 01:00:00     95.564853
        """
        data = {"currency": self.currency}
        d = requests.get(self.url + "get_historical_volatility?", data)
        df = pd.DataFrame(d.json()['result'])
        df.columns = ['date', str(self.currency.lower())+'_hist_vol']
        df['date'] = pd.to_datetime(df.date, unit='ms')
        df = df.set_index("date")
        if save_csv == True:
            df.to_csv(str(self.currency) + "_hist_vol.csv")
        return df

    def get_options_list(self):
        """
        This method is used to retrive the option type and instrument name.
        The output of this method is used as an input to the `get_option_stats`
        method.

        Returns
        -------------
        dataframe:
            A dataframe with relevant information which is fed into the
            `get_option_stats` method.

        Example
        -------------
        >>> df = data.get_options_list()
        >>> df.head()
        expiration_timestamp option_type instrument_name strike
        0	1590134400000	put	    BTC-22MAY20-9250-P  9250.0
        1	1590134400000	call	BTC-22MAY20-12000-C	12000.0
        2	1593158400000	call	BTC-26JUN20-8000-C	8000.0
        3	1589443200000	call	BTC-14MAY20-8875-C	8875.0
        4	1601020800000	put	    BTC-25SEP20-9000-P  9000.0
        """
        data = {'currency': self.currency, 'kind': 'option'}
        r = requests.get(self.url + 'get_instruments', data)
        df = pd.DataFrame(r.json()['result'])
        cols = ['expiration_timestamp', 'option_type', 'instrument_name', 'strike']
        return df[cols]

    def get_options_stats(self, save_csv=False):
        """
        Retrieves the price, implied volatility, volume, open interest, greeks
        and other relevant data for all options of the selected asset.

        Parameter:
        ------------
        save_csv: boolean
            Select True to save the options data to a csv file

        Returns
        -------------
        dataframe:
            A dataframe with corresponding statistics for each option

        csv:
            A csv file will be saved if save_csv is set to True

        Example
        -------------
        >>> df = data.get_options_stats()
        >>> df.columns
        Index(['expiration_timestamp', 'option_type', 'instrument_name', 'strike',
               'underlying_price', 'underlying_index', 'timestamp', 'stats', 'state',
               'settlement_price', 'open_interest', 'min_price', 'max_price',
               'mark_price', 'mark_iv', 'last_price', 'interest_rate',
               'instrument_name', 'index_price', 'greeks', 'estimated_delivery_price',
               'change_id', 'bids', 'bid_iv', 'best_bid_price', 'best_bid_amount',
               'best_ask_price', 'best_ask_amount', 'asks', 'ask_iv'],
                dtype='object')

        >>> df[['instrument_name', 'last_price', 'mark_iv', 'open_interest']].head()
            instrument_name	  last_price mark_iv open_interest
        0	BTC-22MAY20-9250-P	0.0460	77.72	138.8
        1	BTC-22MAY20-12000-C	0.0050	112.28	110.6
        2	BTC-26JUN20-8000-C	0.1825	90.26	771.0
        3	BTC-14MAY20-8875-C	0.0410	90.65	24.7
        4	BTC-25SEP20-9000-P	0.1770	83.37	266.9
        """
        storage = []
        options_list = self.get_options_list()
        iv_url = self.url + 'get_order_book?instrument_name='
        for option in tqdm(range(len(options_list))):
            data = iv_url + options_list.instrument_name.values[option]
            storage.append(requests.get(data).json()['result'])
        iv = pd.DataFrame(storage)
        df = pd.concat([options_list, iv], axis=1)
        df = df.loc[:,~df.columns.duplicated()]
        if save_csv == True:
            df.to_csv("options_data.csv")
        return df
