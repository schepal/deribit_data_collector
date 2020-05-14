# Deribit Data Scraper
A library that can be used to download the entire BTC and ETH option chain data on Deribit.

## Example
``` python
import deribit_data as dm
btc_data = dm.OptionsData("BTC")


# Get realised historical volatility
btc_data.get_histvol_data()

>>                     btc_hist_vol
date                             
2020-04-28 03:00:00     53.861539
2020-04-28 03:00:00     53.861539
2020-04-28 04:00:00     53.830579
2020-04-28 05:00:00     53.759275
2020-04-28 06:00:00     53.763557
...                           ...
2020-05-13 21:00:00     95.228999
2020-05-13 22:00:00     95.501434
2020-05-13 23:00:00     95.553333
2020-05-14 00:00:00     95.572422
2020-05-14 01:00:00     95.564853

# Retrieve all options pricing and greeks data - note this may take several minutes to download
btc_data.get_options_stats()

>>      expiration_timestamp  ...  ask_iv
0           1590134400000  ...   87.56
1           1590134400000  ...  115.93
2           1593158400000  ...   93.25
3           1589443200000  ...  204.46
4           1601020800000  ...   85.01
..                    ...  ...     ...
305         1590134400000  ...  125.95
306         1608883200000  ...   86.53
307         1601020800000  ...   86.94
308         1608883200000  ...    0.00
309         1589529600000  ...  500.00

```
