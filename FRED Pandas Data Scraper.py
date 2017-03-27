import numpy as np
import datetime 
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import warnings
import glob
warnings.filterwarnings("ignore")

# START AT JAN 1 2007 SO WE HAVE 10 YEARS OF DATA

file1 = '/path0/'
file2 = '/path to csvs/'
out1 = '/path to output/'
filestox = '/path to csvs to merge with web scraped data/'


forex = ['DEXUSEU','DEXUSUK','DEXUSNZ','DEXUSAL',
         'DEXSZUS','DEXCHUS','DEXMXUS','DEXJPUS','DEXCAUS']

# S&P5000, EURO CURRENCY,  DJIA, NASDAQ 100, Russell 2000, 
vixes = [ 'VIXCLS','EVZCLS','VXDCLS','VXNCLS', 'RVXCLS']

idxs= ['SP500', 'DEXUSEU','DJIA', 'NASDAQ100','RU2000PR']
       
# other SP: S%P 100, 3-month S&P
vixsp = ['VXOCLS','VXVCLS']

# GOOG, APL, Amazon, IBM, Goldman Sachs
vixstx = ['VXGOGCLS','VXAPLCLS','VXAZNCLS','VXIBMCLS','VXGSCLS']
         



fred_codes = np.concatenate([idxs, vixes])

fred_codes2 = np.concatenate([ forex, idxs, vixes, vixstx])
fred_codes2 = np.concatenate([ forex, idxs, vixes])


data = pd.DataFrame()
start = datetime.datetime(2008, 1, 1)
end = datetime.datetime(2017, 3, 25) # today




def creator(fred_codes):
    names = fred_codes
    start = datetime.datetime(2007, 1, 1)
    end = datetime.datetime(2017, 3, 25) # today

    yo = web.DataReader(names[0], "fred", start, end)
    data = pd.DataFrame(yo)

    cdates = data.index
    print(data.shape)

    for i in range(1,len(fred_codes)): # FIRST RUN: CREATE TIME DICTIONARY
        current_code = fred_codes[i]
        
        yo = web.DataReader(current_code, "fred", start, end)
        data = pd.concat([data,yo],axis=1)
        print(data.shape)
        
    for filename in glob.glob(filestox+'*csv'):
        yo = pd.read_csv(filename)
        yo['Date'] = pd.to_datetime( yo['Date'] )
        yo = yo.set_index('Date')
        data = pd.concat([data,yo],axis=1)
        print(data.shape)
        print(filename)

    to_reverse = ['DEXSZUS','DEXCHUS','DEXMXUS','DEXJPUS','DEXCAUS']

    for i in to_reverse:
        data[i] = 1 / data[i] #normalize Forex rates
        
    
    data = data.fillna(method='ffill')
    data = data.dropna()
    data.to_csv(out1)
    #print(data.head(40))
    print(data.shape)

creator(fred_codes2)
