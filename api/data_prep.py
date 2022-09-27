import pandas as pd
import pickle
import numpy as np



# Load imputer
with open('./model/imputer.pkl','rb') as impute:
    imputer = pickle.load(impute)

# Load scaler
with open('./model/scaler.pkl','rb') as scaler:
    std_scaler = pickle.load(scaler)

#NOTE: For production, OneHotEncoder() is a better option for encoding categorical variables. Most of the code in prep_data takes care of the downside of using get_dummies().
def prep_data(df):
    

    all_variables = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10',
       'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20',
       'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30',
       'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40',
       'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50',
       'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x60',
       'x61', 'x62', 'x63', 'x64', 'x65', 'x66', 'x67', 'x68', 'x69', 'x70',
       'x71', 'x72', 'x73', 'x74', 'x75', 'x76', 'x77', 'x78', 'x79', 'x80',
       'x81', 'x82', 'x83', 'x84', 'x85', 'x86', 'x87', 'x88', 'x89', 'x90',
       'x91', 'x92', 'x93', 'x94', 'x95', 'x96', 'x97', 'x98', 'x99']


    # 1. Fixing the money and percents
    if 'x12' in df.columns:
        df['x12'] = df['x12'].str.replace('$', '')
        df['x12'] = df['x12'].str.replace(',', '')
        df['x12'] = df['x12'].str.replace(')', '')
        df['x12'] = df['x12'].str.replace('(', '-')
        df['x12'] = df['x12'].astype(float)
    if 'x63' in df.columns:
        df['x63'] = df['x63'].str.replace('%', '')
        df['x63'] = df['x63'].astype(float)

    # 2. Creating NaN value if variable is missing from raw data
    for var in all_variables:
        if var not in df.columns:
            df[var] = np.nan

    # 3. Scale and impute new data with trained imputer and std_scaler 

    df_imputed = pd.DataFrame(imputer.transform(df.drop(columns=['x5', 'x31', 'x81', 'x82'])),
                              columns=df.drop(columns=['x5', 'x31', 'x81', 'x82']).columns)
    df_imputed_std = pd.DataFrame(std_scaler.transform(df_imputed), columns=df_imputed.columns)

    # 4. create dummies

    dumb5 = pd.get_dummies(df['x5'], drop_first=False, prefix='x5', prefix_sep='_', dummy_na=True)
    df_imputed_std = pd.concat([df_imputed_std, dumb5], axis=1, sort=False)

    dumb31 = pd.get_dummies(df['x31'], drop_first=False, prefix='x31', prefix_sep='_', dummy_na=True)
    df_imputed_std = pd.concat([df_imputed_std, dumb31], axis=1, sort=False)

    dumb81 = pd.get_dummies(df['x81'], drop_first=False, prefix='x81', prefix_sep='_', dummy_na=True)
    df_imputed_std = pd.concat([df_imputed_std, dumb81], axis=1, sort=False)

    dumb82 = pd.get_dummies(df['x82'], drop_first=False, prefix='x82', prefix_sep='_', dummy_na=True)
    df_imputed_std = pd.concat([df_imputed_std, dumb82], axis=1, sort=False)


    del dumb5, dumb31, dumb81, dumb82

    variables = ['x5_saturday', 'x81_July', 'x81_December', 'x31_japan',
                 'x81_October', 'x5_sunday', 'x31_asia', 'x81_February',
                 'x91', 'x81_May', 'x5_monday', 'x81_September', 'x81_March',
                 'x53', 'x81_November', 'x44', 'x81_June', 'x12', 'x5_tuesday',
                 'x81_August', 'x81_January', 'x62', 'x31_germany', 'x58', 'x56']

    # 5. Accounting for missing dummy variables
    for var in variables:
        if var not in df_imputed_std.columns:
            df_imputed_std[var] = 0

    return df_imputed_std[variables]
