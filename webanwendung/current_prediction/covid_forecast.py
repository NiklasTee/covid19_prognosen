import json
import numpy as np
import pandas as pd
from rki_function1 import CountyCasesAggregator
from rki_function2 import DateCasesAggregator
from rki_function3 import LagCreator
from rki_function4 import CalendarAdder
from tensorflow import keras

start_time = pd.to_datetime('2020-03-01')
end_time = pd.to_datetime('2021-07-06') # !!!LETZTES DATUM IM DATENSATZ !!!
case_dates = pd.date_range(start_time, end_time, freq='D')
prediction_time = pd.date_range(end_time+pd.to_timedelta(1, unit='d'), end_time+pd.to_timedelta(7, unit='d'), freq='D')


berliner_ids = [11001, 11002, 11003, 11004, 11005, 11006, 11007, 11008, 11009, 11010, 11011, 11012]


data1 = pd.read_csv(r'RKI_COVID19.csv', encoding='cp1252')
data2 = pd.read_csv(r'landkreise_bundesland_id.csv', delimiter=';')

df = pd.DataFrame(data1)
landkreise_df = pd.DataFrame(data2)
landkreise_df.set_index('IdLandkreis', drop=True, inplace=True)
landkreise_df['Fallzahlen_Aktuell'] = np.nan
landkreise_df['Fallzahlen_Vortag'] = np.nan
landkreise_df['Fallzahlen_Vorzweitag'] = np.nan
landkreise_df['Fallzahlen_Vordreitag'] = np.nan
landkreise_df['Fallzahlen_Vorviertag'] = np.nan
landkreise_df['Fallzahlen_Vorfünftag'] = np.nan
landkreise_df['Fallzahlen_Vorsechstag'] = np.nan
landkreise_df['Fallzahlen_Prognose'] = None
landkreise_df['Fallzahlen_Prognose'] = landkreise_df['Fallzahlen_Prognose'].astype(object)

landkreise_df['Bevölkerung'] = landkreise_df['Bevölkerung'].astype(int)

model = keras.models.load_model('rnn.h5')

with open("fallzahlen_minmax.json", "rb") as infile:
    fallzahlen_minmax = json.load(infile)

df['AnzahlFall'].replace(-1, 0, inplace=True)

df = DateCasesAggregator(df, start_time, end_time)
df = CountyCasesAggregator(df, berliner_ids, 11000)
df = LagCreator(df)
df = CalendarAdder(df)

test_rnn = df[['AnzahlFall', 'AnzahlFall_Vortag', 'AnzahlFall_Vorzweitag', 'AnzahlFall_Vordreitag', 'AnzahlFall_Vorviertag', 'AnzahlFall_Vorfünftag', 'AnzahlFall_Vorsechstag', 'AnzahlFall_Vorwoche']]

kreis_ids = test_rnn.index.get_level_values(0).unique()

test_rnn.reset_index(inplace=True, drop=False)

for kreis_id in kreis_ids:
    kreis_min = fallzahlen_minmax[f'{kreis_id}'][0]
    kreis_max = fallzahlen_minmax[f'{kreis_id}'][1]

    kreis_test_df = test_rnn.loc[test_rnn['IdLandkreis'] == kreis_id]

    kreis_test_df[
        ['AnzahlFall', 'AnzahlFall_Vortag', 'AnzahlFall_Vorzweitag', 'AnzahlFall_Vordreitag', 'AnzahlFall_Vorviertag',
         'AnzahlFall_Vorfünftag', 'AnzahlFall_Vorsechstag', 'AnzahlFall_Vorwoche']] = kreis_test_df[
        ['AnzahlFall', 'AnzahlFall_Vortag', 'AnzahlFall_Vorzweitag', 'AnzahlFall_Vordreitag', 'AnzahlFall_Vorviertag',
         'AnzahlFall_Vorfünftag', 'AnzahlFall_Vorsechstag', 'AnzahlFall_Vorwoche']].apply(
        lambda x: (x - kreis_min) / (kreis_max - kreis_min), axis=1)

    test_rnn.loc[test_rnn['IdLandkreis'] == kreis_id] = kreis_test_df


test_rnn = test_rnn.groupby(['IdLandkreis', 'Meldedatum']).last()



for kreis_id in kreis_ids:

    # Daten Vorbereitung Vorhersage
    df_pred = test_rnn.xs(kreis_id)
    df_pred = df_pred.loc[end_time]

    kreis_min = fallzahlen_minmax[f'{kreis_id}'][0]
    kreis_max = fallzahlen_minmax[f'{kreis_id}'][1]


    currrent_cases = df_pred['AnzahlFall']
    vortag_cases = df_pred['AnzahlFall_Vortag']
    vorzweitag_cases = df_pred['AnzahlFall_Vorzweitag']
    vordreitag_cases = df_pred['AnzahlFall_Vordreitag']
    vorviertag_cases = df_pred['AnzahlFall_Vorviertag']
    vorfünftag_cases = df_pred['AnzahlFall_Vorfünftag']
    vorsechstag_cases = df_pred['AnzahlFall_Vorsechstag']
    vorsiebentag_cases = df_pred['AnzahlFall_Vorwoche']
    predictions = []

    for date in prediction_time:
        row_values = df_pred[:-1]
        X_pred = row_values.to_xarray()
        X_pred = X_pred.transpose()
        X_pred = X_pred.values
        X_pred = np.expand_dims(X_pred, axis=1)
        X_pred = np.expand_dims(X_pred, axis=0)

        prediction = model.predict(X_pred)
        predictions.append(prediction[0][0]*(kreis_max - kreis_min)+kreis_min)

        df_pred['AnzahlFall_Vortag'] = df_pred['AnzahlFall']
        df_pred['AnzahlFall_Vorzweitag'] = df_pred['AnzahlFall_Vortag']
        df_pred['AnzahlFall_Vordreitag'] = df_pred['AnzahlFall_Vorzweitag']
        df_pred['AnzahlFall_Vorviertag'] = df_pred['AnzahlFall_Vordreitag']
        df_pred['AnzahlFall_Vorfünftag'] = df_pred['AnzahlFall_Vorviertag']
        df_pred['AnzahlFall_Vorsechstag'] = df_pred['AnzahlFall_Vorfünftag']
        df_pred['AnzahlFall_Vorwoche'] = df_pred['AnzahlFall_Vorsechstag']
        df_pred['AnzahlFall'] = prediction[0][0]


    landkreise_df.at[kreis_id, 'Fallzahlen_Prognose'] = predictions
    landkreise_df.at[kreis_id, 'Fallzahlen_Aktuell'] = currrent_cases

    landkreise_df.at[kreis_id, 'Fallzahlen_Vortag'] = vortag_cases*(kreis_max - kreis_min)+kreis_min
    landkreise_df.at[kreis_id, 'Fallzahlen_Vorzweitag'] = vorzweitag_cases*(kreis_max - kreis_min)+kreis_min
    landkreise_df.at[kreis_id, 'Fallzahlen_Vordreitag'] = vordreitag_cases*(kreis_max - kreis_min)+kreis_min
    landkreise_df.at[kreis_id, 'Fallzahlen_Vorviertag'] = vorviertag_cases*(kreis_max - kreis_min)+kreis_min
    landkreise_df.at[kreis_id, 'Fallzahlen_Vorfünftag'] = vorfünftag_cases*(kreis_max - kreis_min)+kreis_min
    landkreise_df.at[kreis_id, 'Fallzahlen_Vorsechstag'] = vorsechstag_cases*(kreis_max - kreis_min)+kreis_min


landkreise_df.loc[:, 'Fallzahlen_Prognose_1'] = landkreise_df['Fallzahlen_Prognose'].map(lambda x: x[0])
landkreise_df.loc[:, 'Fallzahlen_Prognose_2'] = landkreise_df['Fallzahlen_Prognose'].map(lambda x: x[1])
landkreise_df.loc[:, 'Fallzahlen_Prognose_3'] = landkreise_df['Fallzahlen_Prognose'].map(lambda x: x[2])
landkreise_df.loc[:, 'Fallzahlen_Prognose_4'] = landkreise_df['Fallzahlen_Prognose'].map(lambda x: x[3])
landkreise_df.loc[:, 'Fallzahlen_Prognose_5'] = landkreise_df['Fallzahlen_Prognose'].map(lambda x: x[4])
landkreise_df.loc[:, 'Fallzahlen_Prognose_6'] = landkreise_df['Fallzahlen_Prognose'].map(lambda x: x[5])
landkreise_df.loc[:, 'Fallzahlen_Prognose_7'] = landkreise_df['Fallzahlen_Prognose'].map(lambda x: x[6])

landkreise_df[['Fallzahlen_Vorsechstag', 'Fallzahlen_Vorfünftag', 'Fallzahlen_Vorviertag', 'Fallzahlen_Vordreitag', 'Fallzahlen_Vorzweitag', 'Fallzahlen_Vortag', 'Fallzahlen_Aktuell', 'Fallzahlen_Prognose_1', 'Fallzahlen_Prognose_2', 'Fallzahlen_Prognose_3', 'Fallzahlen_Prognose_4', 'Fallzahlen_Prognose_5', 'Fallzahlen_Prognose_6', 'Fallzahlen_Prognose_7']] = landkreise_df[['Fallzahlen_Vorsechstag', 'Fallzahlen_Vorfünftag', 'Fallzahlen_Vorviertag', 'Fallzahlen_Vordreitag', 'Fallzahlen_Vorzweitag', 'Fallzahlen_Vortag', 'Fallzahlen_Aktuell', 'Fallzahlen_Prognose_1', 'Fallzahlen_Prognose_2', 'Fallzahlen_Prognose_3', 'Fallzahlen_Prognose_4', 'Fallzahlen_Prognose_5', 'Fallzahlen_Prognose_6', 'Fallzahlen_Prognose_7']].round(0).astype(int)
landkreise_df = landkreise_df[['Landkreis', 'Bundesland', 'Bevölkerung', 'Fallzahlen_Vorsechstag', 'Fallzahlen_Vorfünftag', 'Fallzahlen_Vorviertag', 'Fallzahlen_Vordreitag', 'Fallzahlen_Vorzweitag', 'Fallzahlen_Vortag', 'Fallzahlen_Aktuell', 'Fallzahlen_Prognose_1', 'Fallzahlen_Prognose_2', 'Fallzahlen_Prognose_3', 'Fallzahlen_Prognose_4', 'Fallzahlen_Prognose_5', 'Fallzahlen_Prognose_6', 'Fallzahlen_Prognose_7']]

print(landkreise_df)

#landkreise_df[['Fallzahlen_Vorsechstag', 'Fallzahlen_Vorfünftag', 'Fallzahlen_Vorviertag', 'Fallzahlen_Vordreitag', 'Fallzahlen_Vorzweitag', 'Fallzahlen_Vortag', 'Fallzahlen_Aktuell', 'Fallzahlen_Prognose_1', 'Fallzahlen_Prognose_2', 'Fallzahlen_Prognose_3', 'Fallzahlen_Prognose_4', 'Fallzahlen_Prognose_5', 'Fallzahlen_Prognose_6', 'Fallzahlen_Prognose_7']].clip(lower=0, inplace=True)
landkreise_df['Fallzahlen_Prognose_1'] = landkreise_df['Fallzahlen_Prognose_1'].clip(lower=0)
landkreise_df['Fallzahlen_Prognose_2'] = landkreise_df['Fallzahlen_Prognose_2'].clip(lower=0)
landkreise_df['Fallzahlen_Prognose_3'] = landkreise_df['Fallzahlen_Prognose_3'].clip(lower=0)
landkreise_df['Fallzahlen_Prognose_4'] = landkreise_df['Fallzahlen_Prognose_4'].clip(lower=0)
landkreise_df['Fallzahlen_Prognose_5'] = landkreise_df['Fallzahlen_Prognose_5'].clip(lower=0)
landkreise_df['Fallzahlen_Prognose_6'] = landkreise_df['Fallzahlen_Prognose_6'].clip(lower=0)
landkreise_df['Fallzahlen_Prognose_7'] = landkreise_df['Fallzahlen_Prognose_7'].clip(lower=0)

print(landkreise_df)

landkreise_df['SiebenTageInzidenz_Aktuell'] = landkreise_df['Fallzahlen_Aktuell'] + landkreise_df['Fallzahlen_Vortag'] + landkreise_df['Fallzahlen_Vorzweitag'] + landkreise_df['Fallzahlen_Vordreitag'] + landkreise_df['Fallzahlen_Vorviertag'] + landkreise_df['Fallzahlen_Vorfünftag'] + landkreise_df['Fallzahlen_Vorsechstag']
landkreise_df['SiebenTageInzidenz_Prognose1'] = landkreise_df['Fallzahlen_Aktuell'] + landkreise_df['Fallzahlen_Vortag'] + landkreise_df['Fallzahlen_Vorzweitag'] + landkreise_df['Fallzahlen_Vordreitag'] + landkreise_df['Fallzahlen_Vorviertag'] + landkreise_df['Fallzahlen_Vorfünftag'] + landkreise_df['Fallzahlen_Prognose_1']
landkreise_df['SiebenTageInzidenz_Prognose2'] = landkreise_df['Fallzahlen_Aktuell'] + landkreise_df['Fallzahlen_Vortag'] + landkreise_df['Fallzahlen_Vorzweitag'] + landkreise_df['Fallzahlen_Vordreitag'] + landkreise_df['Fallzahlen_Vorviertag'] + landkreise_df['Fallzahlen_Prognose_2'] + landkreise_df['Fallzahlen_Prognose_1']
landkreise_df['SiebenTageInzidenz_Prognose3'] = landkreise_df['Fallzahlen_Aktuell'] + landkreise_df['Fallzahlen_Vortag'] + landkreise_df['Fallzahlen_Vorzweitag'] + landkreise_df['Fallzahlen_Vordreitag'] + landkreise_df['Fallzahlen_Prognose_3'] + landkreise_df['Fallzahlen_Prognose_2'] + landkreise_df['Fallzahlen_Prognose_1']
landkreise_df['SiebenTageInzidenz_Prognose4'] = landkreise_df['Fallzahlen_Aktuell'] + landkreise_df['Fallzahlen_Vortag'] + landkreise_df['Fallzahlen_Vorzweitag'] + landkreise_df['Fallzahlen_Prognose_4'] + landkreise_df['Fallzahlen_Prognose_3'] + landkreise_df['Fallzahlen_Prognose_2'] + landkreise_df['Fallzahlen_Prognose_1']
landkreise_df['SiebenTageInzidenz_Prognose5'] = landkreise_df['Fallzahlen_Aktuell'] + landkreise_df['Fallzahlen_Vortag'] + landkreise_df['Fallzahlen_Prognose_5'] + landkreise_df['Fallzahlen_Prognose_4'] + landkreise_df['Fallzahlen_Prognose_3'] + landkreise_df['Fallzahlen_Prognose_2'] + landkreise_df['Fallzahlen_Prognose_1']
landkreise_df['SiebenTageInzidenz_Prognose6'] = landkreise_df['Fallzahlen_Aktuell'] + landkreise_df['Fallzahlen_Prognose_6'] + landkreise_df['Fallzahlen_Prognose_5'] + landkreise_df['Fallzahlen_Prognose_4'] + landkreise_df['Fallzahlen_Prognose_3'] + landkreise_df['Fallzahlen_Prognose_2'] + landkreise_df['Fallzahlen_Prognose_1']
landkreise_df['SiebenTageInzidenz_Prognose7'] = landkreise_df['Fallzahlen_Prognose_7'] + landkreise_df['Fallzahlen_Prognose_6'] + landkreise_df['Fallzahlen_Prognose_5'] + landkreise_df['Fallzahlen_Prognose_4'] + landkreise_df['Fallzahlen_Prognose_3'] + landkreise_df['Fallzahlen_Prognose_2'] + landkreise_df['Fallzahlen_Prognose_1']

landkreise_df['SiebenTageInzidenz_Aktuell'] = (landkreise_df['SiebenTageInzidenz_Aktuell']/landkreise_df['Bevölkerung'])*100000
landkreise_df['SiebenTageInzidenz_Prognose1'] = (landkreise_df['SiebenTageInzidenz_Prognose1']/landkreise_df['Bevölkerung'])*100000
landkreise_df['SiebenTageInzidenz_Prognose2'] = (landkreise_df['SiebenTageInzidenz_Prognose2']/landkreise_df['Bevölkerung'])*100000
landkreise_df['SiebenTageInzidenz_Prognose3'] = (landkreise_df['SiebenTageInzidenz_Prognose3']/landkreise_df['Bevölkerung'])*100000
landkreise_df['SiebenTageInzidenz_Prognose4'] = (landkreise_df['SiebenTageInzidenz_Prognose4']/landkreise_df['Bevölkerung'])*100000
landkreise_df['SiebenTageInzidenz_Prognose5'] = (landkreise_df['SiebenTageInzidenz_Prognose5']/landkreise_df['Bevölkerung'])*100000
landkreise_df['SiebenTageInzidenz_Prognose6'] = (landkreise_df['SiebenTageInzidenz_Prognose6']/landkreise_df['Bevölkerung'])*100000
landkreise_df['SiebenTageInzidenz_Prognose7'] = (landkreise_df['SiebenTageInzidenz_Prognose7']/landkreise_df['Bevölkerung'])*100000

landkreise_df['SiebenTageInzidenz_Aktuell'] = landkreise_df['SiebenTageInzidenz_Aktuell'].round(1)
landkreise_df['SiebenTageInzidenz_Prognose1'] = landkreise_df['SiebenTageInzidenz_Prognose1'].round(1)
landkreise_df['SiebenTageInzidenz_Prognose2'] = landkreise_df['SiebenTageInzidenz_Prognose2'].round(1)
landkreise_df['SiebenTageInzidenz_Prognose3'] = landkreise_df['SiebenTageInzidenz_Prognose3'].round(1)
landkreise_df['SiebenTageInzidenz_Prognose4'] = landkreise_df['SiebenTageInzidenz_Prognose4'].round(1)
landkreise_df['SiebenTageInzidenz_Prognose5'] = landkreise_df['SiebenTageInzidenz_Prognose5'].round(1)
landkreise_df['SiebenTageInzidenz_Prognose6'] = landkreise_df['SiebenTageInzidenz_Prognose6'].round(1)
landkreise_df['SiebenTageInzidenz_Prognose7'] = landkreise_df['SiebenTageInzidenz_Prognose7'].round(1)


landkreise_df = landkreise_df[['Landkreis', 'Bundesland', 'Bevölkerung', 'SiebenTageInzidenz_Aktuell', 'SiebenTageInzidenz_Prognose1', 'SiebenTageInzidenz_Prognose2', 'SiebenTageInzidenz_Prognose3', 'SiebenTageInzidenz_Prognose4', 'SiebenTageInzidenz_Prognose5', 'SiebenTageInzidenz_Prognose6', 'SiebenTageInzidenz_Prognose7']]

print(landkreise_df)

landkreise_df.to_csv('covid_forecast.csv', index=True, sep=';')

