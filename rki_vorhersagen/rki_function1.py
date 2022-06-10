import pandas as pd

def CountyCasesAggregator(df_name, from_ids, to_id):
    sub_df = df_name.loc[from_ids]
    sub_df = sub_df.groupby(['Meldedatum']).sum()
    sub_df = pd.concat([sub_df], keys=[to_id], names=['IdLandkreis'])
    df_name = df_name.append(sub_df)
    df_name.drop(from_ids, axis=0, inplace=True)
    df_name.sort_index(inplace=True)

    return df_name