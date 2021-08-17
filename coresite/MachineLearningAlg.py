import joblib

import pandas as pd
import numpy as np

import os
from django.conf import settings

def rf_COVID (matrix):

    loaded_model = joblib.load(open(os.path.join(settings.MEDIA_ROOT, 'RF_COVID'), "rb"))
    df_raw = pd.read_csv(os.path.join(settings.MEDIA_ROOT, "AI_Matrix_predictions.csv"))

    rows, columns = df_raw.shape

    dose_1 = matrix["first_dose"]
    dose_2 = matrix["second_dose"]
    connect_covid = matrix["CONNECT_lag"]

    df_to_predict = df_raw.copy()

    df_to_predict['Dose_1_cumul_Pct'] = dose_1
    df_to_predict['Dose_2_cumul_Pct'] = dose_2
    df_to_predict['CONNECT_COVID_LAG'] = connect_covid

    df_id = df_to_predict.iloc[:, [0]]

    region = np.array(df_id).ravel()

    df_x = df_to_predict.iloc[:, 1:columns]

    prediction = loaded_model.predict(df_x)

    rf_result = {"region_id":region, "Alerte": prediction}

    df_result = pd.DataFrame.from_dict(rf_result)

    return df_result