from pattern.web import URL
import pandas as pd
import os
import sys

def extract_data(stock_ticker):
    url_base = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t='
    url_end = '&region=usa&culture=en-US&cur=&order=asc'
    # May add more exchanges later on, but these cover the main US stock exchanges: Nasdaq, New York SE, and Pink Sheets (OTC stocks), respectively
    # Loops through main stock exchanges to get proper URL for data extraction
    stock_exchange_list = ['XNAS:','XNYS:','PINX:'] 
    for exchange in stock_exchange_list:
        test = URL(url_base+exchange+stock_ticker+url_end)
        if sys.getsizeof(test.download()) > 35: #A broken URL produces an empty string, which has memory size 33; size 35 allows for minor variation in the size
            break
    temp_data = 'C:/Users/Owner/Documents/temp.csv'
    f = open(temp_data, mode='w')
    try:
        f.write(test.download())
    except:
        raise IOError('There was an error processing this data')
        sys.exit(1)
    f.close()
    try:
        stock_data_df =  pd.read_csv(temp_data, header=2,thousands =',',index_col=0,skiprows=[19,20,31,41,42,43,48,58,53,64,65,72,73,95,101,102])
    except:
        raise IOError('Problem downloading files')
        os.remove(temp_data)
        sys.exit(1)
    os.remove(temp_data)
    stock_data_df = stock_data_df.transpose()
    return(stock_data_df)