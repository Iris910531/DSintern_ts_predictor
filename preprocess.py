import requests
import pandas as pd
import time


def Preprocess(time_stamp):
    ###requests API
    struct_time = time.localtime(time_stamp) # 轉成時間元組
    timeString = time.strftime("%Y%m%d%H%M%S", struct_time)

    path = 'http://61.220.250.198:3000/getPingfongFamiSolarGeneration/?hour=600&unit=kwh&endTime='
    response = requests.get(path + timeString)
    if response.status_code != 200:
        print(response.status_code)
        raise AssertionError(f"database query error")
    
    list_of_dicts = response.json()
    dd = []
    solar = []
    for i in range(len(list_of_dicts)):
        solar.append(list_of_dicts[i][0])
        dd.append(list_of_dicts[i][1])
    SG_dict = {
        "solarGeneration": solar,
        "datetime": dd,
    }
    SG = pd.DataFrame(SG_dict)
    ###del_microsec
    SG['datetime'] = pd.to_datetime(SG['datetime'])
    SG['datetime'] = SG['datetime'].apply(lambda x: x.replace(microsecond=0))
    SG = SG.groupby('datetime').first().reset_index()
    
    ###per unit time electricity
    SG["solarGeneration"] = SG["solarGeneration"].diff().fillna(0)
    
    ###half per hour sum
    SG["datetime"] = pd.to_datetime(SG["datetime"])
    SG["datetime"] = SG["datetime"].apply(lambda x: x.replace(second = 0))

    thirty = SG["datetime"].apply(lambda x: x.minute)
    SG["datetime_30"] = 0
    SG["datetime_30"][thirty < 30] = SG["datetime"].apply(lambda x: x.replace(minute = 0))
    SG["datetime_30"][thirty >= 30] = SG["datetime"].apply(lambda x: x.replace(minute = 30))
    SG = SG.groupby('datetime_30').sum().reset_index()
    SG.rename(columns = {'datetime_30':'datetime'}, inplace = True)

    ##miss value 插值
    expected_range = pd.date_range(start=SG['datetime'][SG.index.min()], end=pd.to_datetime(timeString), freq='30T', closed = 'left')
    nan_SG = SG.set_index('datetime').reindex(expected_range)
    SG_interpolate = nan_SG.interpolate(method = 'linear')
    SG = SG_interpolate.reset_index()
    nan_SG = nan_SG.reset_index()
    nan_SG.rename(columns = {'index':'datetime'}, inplace = True)
    SG.rename(columns = {'index':'datetime'}, inplace = True)
    
    return SG, nan_SG, timeString
    