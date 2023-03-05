import numpy as np
import pandas as pd
from sklearn import preprocessing
import os
import zipfile

def process(data): 
    data["diff_lat"] = abs(data["pickup_latitude"] - data["dropoff_latitude"])
    data["diff_lon"] = abs(data["pickup_longitude"] - data["dropoff_longitude"])
    
    data["dist"] = np.sqrt(np.power(data["diff_lat"],2) + np.power(data["diff_lon"],2))

    data["pickup_datetime"] = pd.to_datetime(data["pickup_datetime"])
    
    data["pickup_year"] = data["pickup_datetime"].dt.year
    data["pickup_month"] = data["pickup_datetime"].dt.month
    data["pickup_day"] = data["pickup_datetime"].dt.day
    data["pickup_dow"] = data["pickup_datetime"].dt.dayofweek
    data["pickup_hour"] = data["pickup_datetime"].dt.hour
    data["pickup_min"] = data["pickup_datetime"].dt.minute
    data["pickup_sec"] = data["pickup_datetime"].dt.second
    
    data = data.drop(["diff_lat", "diff_lon", "pickup_longitude", "pickup_latitude", "dropoff_latitude", "dropoff_longitude", "id", "pickup_datetime"], axis = 1)
    data = data.drop(["dropoff_datetime"], axis = 1)

    le = preprocessing.LabelEncoder()
    data["store_and_fwd_flag"] = le.fit_transform(data["store_and_fwd_flag"])
    return data


def download_datasets():
    base_dir = "nyc-taxi-trip-duration"
    try:
        if not os.path.exists(os.path.join(base_dir)):
            base_file = base_dir + ".zip"
            with zipfile.ZipFile(base_file,"r") as z:
                z.extractall(base_dir)
            os.remove(os.path.join(base_dir, "sample_submission.zip"))
            os.remove(os.path.join(base_dir, "test.zip"))

            train_dir = os.path.join(base_dir, "train.zip")
            with zipfile.ZipFile(train_dir,"r") as z:
                z.extractall(base_dir)
            os.remove(train_dir)
    except:
        raise Exception("""Download dataset in current dir from 
                  https://www.kaggle.com/competitions/nyc-taxi-trip-duration/data
                  """)
    return base_dir