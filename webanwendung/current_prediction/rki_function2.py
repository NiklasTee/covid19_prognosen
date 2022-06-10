import pandas as pd


def DateCasesAggregator(df_name, start_date, end_date):
    sub_df = df_name[['IdLandkreis', 'AnzahlFall', 'AnzahlTodesfall', 'AnzahlGenesen', 'Meldedatum']]
    sub_df['Meldedatum'] = pd.to_datetime(sub_df['Meldedatum'], format='%Y/%m/%d %H:%M:%S')
    sub_df = sub_df.groupby(['IdLandkreis', 'Meldedatum']).sum()
    case_dates = pd.date_range(start_date, end_date, freq='D')
    sub_df = sub_df.loc[(slice(None), case_dates), :]
    sub_df = sub_df.reindex(pd.MultiIndex.from_product([sub_df.index.levels[0], case_dates], names=['IdLandkreis', 'Meldedatum']), fill_value=0)

    return sub_df