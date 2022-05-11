
###Shailendra Bhandari 2022#############################
####Machine Learning ACIT4630 Project

import logging

import pandas as pd

from falldetection.extract_features import extract_features
from falldetection.sensor_file_reader import read_sensor_file
from falldetection.window_around_maximum_total_acceleration import get_window_around_maximum_total_acceleration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureExtractor:

    def __init__(self, autocovar_num, dft_amplitudes_num) -> None:
        self.autocovar_num = autocovar_num
        self.dft_amplitudes_num = dft_amplitudes_num

    def extract_features(self, sensorFile):
        logger.debug('default_feature_extractor(%s)', sensorFile)
        return self.flatten_data_frame(
            extract_features(
                df=self.sensor_file_2_df(sensorFile),
                autocovar_num=self.autocovar_num,
                dft_amplitudes_num=self.dft_amplitudes_num))

    @staticmethod
    def sensor_file_2_df(sensorFile):
        return get_window_around_maximum_total_acceleration(
            read_sensor_file(sensorFile),
            half_window_size=50,
            index_error_msg=sensorFile)

    @staticmethod
    def flatten_data_frame(df):
        df_flattened = df.T.stack()
        index_flattened = FeatureExtractor.__flatten_2level_index(df_flattened.index)
        return pd.DataFrame(data=df_flattened.values, index=index_flattened).T

    @staticmethod
    def __flatten_2level_index(index):
        return pd.Index(['_'.join(levels) for levels in index.tolist()])
