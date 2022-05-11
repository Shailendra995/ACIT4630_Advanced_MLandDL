
###Shailendra Bhandari 2022#############################
####Machine Learning ACIT4630 Project ###############################################3


import numpy as np

from falldetection.feature_extractor import FeatureExtractor
from falldetection.sensor_files_provider import SensorFilesProvider
from falldetection.sensor_files_to_exclude import get_sensor_files_to_exclude_for
from falldetection.time_series_extractor import TimeSeriesExtractor


class TimeSeriesExtractorWorkflow:

    def __init__(self, timeSeriesExtractor):
        self.timeSeriesExtractor = timeSeriesExtractor

    def extract_time_series(self, sensorFiles):
        X, y = self.__unzip(map(self.__extract_time_series_4_sensorFile, sensorFiles))
        return np.array(X), np.array(y)

    def __extract_time_series_4_sensorFile(self, sensorFile):
        X, y = self.timeSeriesExtractor.extract_time_series(sensorFile)
        return X, [y]

    def __unzip(self, X_y_pairs):
        X, y = zip(*X_y_pairs)
        return X, y


def extract_time_series(sensor, baseDir, columns):
    def createTimeSeriesExtractor():
        return TimeSeriesExtractor(
            sensor_file_2_df=FeatureExtractor.sensor_file_2_df,
            columns=columns)

    def createTimeSeriesExtractorWorkflow():
        return TimeSeriesExtractorWorkflow(createTimeSeriesExtractor())

    def createSensorFilesProvider():
        return SensorFilesProvider(
            baseDir,
            sensor,
            get_sensor_files_to_exclude_for(sensor))

    def get_sensor_files():
        return createSensorFilesProvider().provide_sensor_files()

    return createTimeSeriesExtractorWorkflow().extract_time_series(get_sensor_files())
