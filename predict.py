import pandas as pd
import time
from darts import TimeSeries
import datetime as dt
from darts.models import RandomForest

def zero_out(data:TimeSeries):
    data = data.pd_dataframe()
    start_time = pd.Timestamp('05:30:00')
    end_time = pd.Timestamp('18:30:00')
    data.loc[data["solarGeneration"] < 0, "solarGeneration"] = 0
    data.loc[((data.index.time < start_time.time()) | (data.index.time > end_time.time())), 'solarGeneration'] = 0
    return TimeSeries.from_dataframe(data.reset_index(), time_col="datetime")["solarGeneration"]


def eval_model(model, train):
    model.fit(train)
    forecast = zero_out(model.predict(13))
    return forecast

def split_df_date(df, start_date, end_date):
    DAY = []
    SG_DAY = []
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df['datetime'] = pd.to_datetime(df['datetime'])
    for i in range(len(df['datetime'])):
        if df['datetime'][i] >= start_date and df['datetime'][i] < end_date:
            DAY.append(i)
    SG_DAY = df.iloc[DAY]
    SG_DAY = SG_DAY.reset_index()
    SG_DAY = SG_DAY.drop(columns = ["index"])
    return SG_DAY


def Predict(timeString, SG, nan_SG):
    timeDate = pd.to_datetime(timeString)
    HoursBefore = (timeDate - dt.timedelta(hours = 3))
    parse = split_df_date(nan_SG, HoursBefore, timeString)
    ts_gt = TimeSeries.from_dataframe(SG, time_col="datetime", fill_missing_dates=True, freq=None)
    forecast = eval_model(RandomForest(lags=24), ts_gt)
    
    return forecast, parse