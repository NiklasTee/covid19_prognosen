import pandas as pd

def LagCreator (df_name):
    df_name['AnzahlFall_Vortag'] = df_name['AnzahlFall'].shift(periods=1)
    df_name['AnzahlFall_Vorzweitag'] = df_name['AnzahlFall'].shift(periods=2)
    df_name['AnzahlFall_Vordreitag'] = df_name['AnzahlFall'].shift(periods=3)
    df_name['AnzahlFall_Vorviertag'] = df_name['AnzahlFall'].shift(periods=4)
    df_name['AnzahlFall_Vorfünftag'] = df_name['AnzahlFall'].shift(periods=5)
    df_name['AnzahlFall_Vorsechstag'] = df_name['AnzahlFall'].shift(periods=6)
    df_name['AnzahlFall_Vorwoche'] = df_name['AnzahlFall'].shift(periods=7)
    df_name['AnzahlFall_Vortagwoche'] = df_name['AnzahlFall'].shift(periods=8)
    df_name.fillna(0, inplace=True)
    df_name['AnzahlFall_Vortag'] = df_name['AnzahlFall_Vortag'].astype(int)
    df_name['AnzahlFall_Vorzweitag'] = df_name['AnzahlFall_Vorzweitag'].astype(int)
    df_name['AnzahlFall_Vordreitag'] = df_name['AnzahlFall_Vordreitag'].astype(int)
    df_name['AnzahlFall_Vorviertag'] = df_name['AnzahlFall_Vorviertag'].astype(int)
    df_name['AnzahlFall_Vorfünftag'] = df_name['AnzahlFall_Vorfünftag'].astype(int)
    df_name['AnzahlFall_Vorsechstag'] = df_name['AnzahlFall_Vorsechstag'].astype(int)
    df_name['AnzahlFall_Vorwoche'] = df_name['AnzahlFall_Vorwoche'].astype(int)
    df_name['AnzahlFall_Vortagwoche'] = df_name['AnzahlFall_Vortagwoche'].astype(int)

    return df_name