import os
import pandas as pd
from src.config import DATA_PATH
from src.preprocess import Preprocessor
from sklearn.ensemble import IsolationForest


class ForestWrapper:
    def __init__(self, n_estimators=200,
                 contamination=0.2, **kwargs):
        self.estimator = IsolationForest(
            n_estimators=n_estimators, contamination=contamination,
            random_state=123, **kwargs
        )
        self.is_fitted = False

    def fit(self, df):
        self.estimator.fit(df)
        self.is_fitted = True

    def predict(self, df):
        if not self.is_fitted:
            raise RuntimeError("Trying to apply unfitted estimator")
        preds = self.estimator.predict(df)
        return preds

    def fit_predict(self, df):
        self.fit(df)
        preds = self.predict(df)
        return preds


class BotDetector:
    def __init__(self, clf, preprocessor: Preprocessor, input_keys=None):
        self.clf = clf
        self.preprocessor = preprocessor
        if input_keys is None:
            input_keys = self.preprocessor.input_keys
        self.input_keys = input_keys
        self.preprocessor.update_input_keys(input_keys)

    def predict(self, file_path, compression=None,
                sep=',', save_to_disk=False):
        if not os.path.exists(DATA_PATH / file_path):
            raise OSError('File not found in file_path')
        df = pd.read_csv(
            DATA_PATH / file_path, compression=compression,
            sep=sep, parse_dates=[self.input_keys.TIME_KEY]
        )
        final_df = self.preprocessor.transform(df)
        preds = self.clf.predict(
            final_df.drop(columns=self.input_keys.PRIMARY_KEY)
        )
        final_df['IS_BOT'] = (preds < 0).astype(int)
        if save_to_disk:
            final_df[
                [self.input_keys.PRIMARY_KEY, 'IS_BOT']
            ].to_csv(DATA_PATH / (file_path.split('.')[0] + 'result.csv'))
        else:
            return final_df[[self.input_keys.PRIMARY_KEY, 'IS_BOT']]
