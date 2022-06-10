import pandas as pd


def CalendarAdder (df_name):

    df_name['date'] = df_name.index.get_level_values('Meldedatum')
    df_name['Monat'] = df_name['date'].dt.month
    df_name['Wochentag'] = df_name['date'].dt.dayofweek
    df_name.drop('date', axis=1, inplace=True)

    return df_name