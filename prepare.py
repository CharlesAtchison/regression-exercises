import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (MinMaxScaler, StandardScaler,
                                   RobustScaler, QuantileTransformer)

def show_histplots(df, target):
    '''Takes train and target and returns violin plots for all metrics
    '''
    col_names = [col for col in df.columns]
    x_len = (len(col_names) // 2) + 1
    fig, axes = plt.subplots(x_len, 2, figsize=(16, 40))
    
    target_df = df[target].replace({0:'No', 1:'Yes'})
    for n, col in enumerate(col_names):
        fig_row = n // 2
        fig_col = n % 2
        sns.histplot(ax=axes[fig_row, fig_col], x=df[col], bins=40)
        axes[fig_row, fig_col].set_title(f'{col.capitalize()} Plot')

def remove_outliers(df: pd.DataFrame, col_list: list, k=1.5):
    ''' Will remove outliers from within a specified threshold.

    The value for k is a constant that sets the threshold. 
    Usually, you’ll see k start at 1.5, or 3 or less, depending on how many outliers you want to keep. 
    The higher the k, the more outliers you keep. Recommend not going beneath 1.5, but this is worth using, 
    especially with data w/ extreme high/low values.
    '''
    
    for col in col_list:

        q1, q3 = df[col].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df

def prepare_data(df):
    '''
    '''
    # Rename the columns 
    rename_key = {'bedroomcnt': 'bedroom', 'bathroomcnt': 'bathroom', 'calculatedfinishedsquarefeet': 'sqft',
                'taxvaluedollarcnt': 'tax_val', 'yearbuilt': 'year', 'taxamount':'tax_amt'}
    df.rename(columns=rename_key, inplace=True)

    # This will fill every column's null values with that column's mean value
    imputer = SimpleImputer(strategy='mean')
    for col in df.columns:
        df[[col]] = imputer.fit_transform(df[[col]])

    # Convert fips to object/str so it can be categorical
    df.fips = df.fips.astype('int').astype('object')
    df.year = df.year.astype('int').astype('object')

    # Remove outliers reducing observations from 2,152,864 to 1,802,511
    df = remove_outliers(df, [col for col in df.columns if col not in ['fips']])

    # # Use this to print the histplot distributions
    # show_histplots(df, 'tax_val')

    return df

def scale_data(train, validate, test, scaler, target):
    '''Takes split dataframes and defined scaler, and returns the df scaled and split into x/y of each 
    along with a visualization of the change.
    '''
    x_cols = [col for col in train.columns if col != target]
    x_train = train[[*x_cols]]
    y_train = train[[target]]
    x_validate = validate[[*x_cols]]
    y_validate = validate[[target]]
    x_test = test[[*x_cols]]
    y_test =test[[target]]

    scaler.fit(x_train)

    x_train_scaled = scaler.transform(x_train)
    x_validate_scaled = scaler.transform(x_validate)
    x_test_scaled = scaler.transform(x_test)

    name = str(type(scaler)).split('.')[-1][:-2]

    plt.figure(figsize=(13, 6))
    plt.subplot(121)
    plt.hist(x_train, ec='black', label=x_cols)
    plt.title('Original')
    plt.legend()
    plt.subplot(122)
    plt2 = plt.hist(x_train_scaled, ec='black', label=x_cols)
    plt.title(name)
    plt.legend()

    return x_train_scaled, y_train, x_validate_scaled, y_validate, x_test_scaled, y_test

