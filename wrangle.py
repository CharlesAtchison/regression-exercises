import pandas as pd
from acquire import *
from prepare import *


def wrangle_zillow():
    df = get_zillow_data()
    
    ## Uncomment this to print all dict features
    # target_dict, feature_dict = fetch_data_dict(df, 'taxvaluedollarcnt')

    # print(df.shape)
    # print(df.describe().T.to_markdown())
    # print(feature_dict)
    # print(target_dict)
    # print(df.isnull().sum().to_markdown())

    final_df = prepare_data(df)
    return final_df