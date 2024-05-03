import datetime

import pandas as pd


def Postprocess(output_file, forecast, gt):
    forecast = forecast.pd_dataframe()["solarGeneration"]
    out = pd.DataFrame({          
        "solarGeneration":forecast,
    })
    out_1 = out.reset_index()
    frames = [gt, out_1]
    result = pd.concat(frames, join='outer')
    result["datetime"] = result["datetime"].apply(lambda x: int(datetime.datetime.timestamp(x)*1000))
    result["solarGeneration"] = result["solarGeneration"].apply(lambda x: round(x, 4))
    result = result.rename(columns={"datetime":"timestamp"})
    print(result)
    result.to_csv(output_file, index = False)