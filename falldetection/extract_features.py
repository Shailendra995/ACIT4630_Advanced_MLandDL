
###Shailendra Bhandari 2022#############################
####Machine Learning ACIT4630 Project
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acovf  ###(https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.acovf.html)


def extract_features(df, autocovar_num, dft_amplitudes_num):
    features = pd.DataFrame(columns=df.columns, dtype=np.float64)

    def add_2_features(index, df):
        def order_by_column(series):
            return series[features.columns].values

        features.loc[index, :] = order_by_column(df)

    def add_autocovariance_of_df_2_features():
        def autocovariance_of_df(lag):
            return df.apply(lambda col: acovf(col)[lag], axis='index')

        for lag in range(1, autocovar_num + 1):
            add_2_features('autocovar_lag_' + str(lag), autocovariance_of_df(lag=lag))

    def add_dft_amplitudes_of_df_2_features():
        def dft_amplitudes_of_df(num):

            return df.apply(lambda col: np.abs(np.fft.fft(col))[num], axis='index')

        for num in range(1, dft_amplitudes_num + 1):
            add_2_features('dft_amplitude_' + str(num), dft_amplitudes_of_df(num - 1))

####there are 6 9min, max, mean, var, skewness, and kurtosos and 11 other autocovariance) Altogether 17 features

    add_2_features('min', df.min())
    add_2_features('max', df.max())
    add_2_features('mean', df.mean())
    add_2_features('var', df.var(ddof=0))
    add_2_features('skew', df.skew())
    add_2_features('kurtosis', df.kurtosis())
    add_autocovariance_of_df_2_features()
    add_dft_amplitudes_of_df_2_features()
    return features
