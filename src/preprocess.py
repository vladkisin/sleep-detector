import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


class Preprocessor:
    def __init__(self, input_keys, agg_trns):
        self.ohe = OneHotEncoder(sparse=False)
        self.is_fitted = False
        self.input_keys = input_keys
        self.agg_trns = agg_trns
        self.hours = list(range(24))

    def update_input_keys(self, new_input_keys):
        self.input_keys = new_input_keys

    def fit_transform(self, df):
        df = df.copy()
        df.sort_values(
            [self.input_keys.PRIMARY_KEY, self.input_keys.TIME_KEY], inplace=True
        )
        df.reset_index(drop=True, inplace=True)
        df = self._extract_times(
            df, transformation=self.ohe.fit_transform
        )  # Extract time diffs and hour sum
        self.is_fitted = True
        df_feats = self._apply_transforms(df)  # Apply feature transformation defined in config
        df_hours, df_norm, df_cumulated_norm = self._apply_time_transforms(df)
        final_df = self._concatenate_dfs(
            df_feats, df_hours, df_norm, df_cumulated_norm
        )
        return final_df

    def transform(self, df):
        df = df.copy()
        if not self.is_fitted:
            raise RuntimeError("Trying to apply unfitted preprocessor")
        df.sort_values(
            [self.input_keys.PRIMARY_KEY, self.input_keys.TIME_KEY], inplace=True
        )
        df.reset_index(drop=True, inplace=True)
        df = self._extract_times(
            df, transformation=self.ohe.transform
        )  # Extract time diffs and hour sum
        df_feats = self._apply_transforms(df)  # Apply feature transformation defined in config
        df_hours, df_norm, df_cumulated_norm = self._apply_time_transforms(df)
        final_df = self._concatenate_dfs(
            df_feats, df_hours, df_norm, df_cumulated_norm
        )
        return final_df

    def _extract_times(self, df, transformation):
        df['HOUR'] = df[self.input_keys.TIME_KEY].dt.hour
        df = pd.concat(
            (
                df, pd.DataFrame(transformation(df[['HOUR']]))
            ),
            axis=1
        )
        df['TIME_DIFF'] = np.where(
            df[self.input_keys.PRIMARY_KEY] == df[self.input_keys.PRIMARY_KEY].shift(1),
            df[self.input_keys.TIME_KEY].diff(), np.timedelta64(None)
        )
        df['TIME_DIFF'] = df['TIME_DIFF'].dt.total_seconds()
        return df

    def _apply_transforms(self, df):
        df_feats = df.groupby(
            self.input_keys.PRIMARY_KEY, as_index=False
        ).agg(self.agg_trns.transforms)
        return df_feats

    def _apply_time_transforms(self, df):
        # Plain hours stats: number of zero active hours and total requests a day
        df_hours = df.groupby(
            self.input_keys.PRIMARY_KEY, as_index=False
        )[self.hours].agg('sum')
        df_hours['ZERO_ACTIVE_HOURS'] = (df_hours == 0).sum(axis=1)
        df_hours['TOTAL_REQS'] = df_hours[self.hours].sum(axis=1)

        # Normalized stats: max peak in percentage, std of hourly percentage distribution
        df_norm = df_hours[self.hours].div(
            df_hours[self.hours].sum(axis=1), axis=0
        )
        df_norm['HOURS_STD'] = df_norm[self.hours].std(axis=1)
        df_norm['MAX_PEAK'] = df_norm[self.hours].max(axis=1) - df_norm[self.hours].min(axis=1)

        # Cumulated normalized counts
        df_cumulated = df_hours[self.hours].cumsum(axis=1)
        df_cumulated_norm = df_cumulated[self.hours].div(
            df_cumulated[23], axis=0
        )

        return df_hours, df_norm, df_cumulated_norm

    def _concatenate_dfs(self, df_feats, df_hours,
                         df_norm, df_cumulated_norm):
        final_df = pd.concat(
            (
                df_hours, df_norm.add_prefix('NORM_'), df_cumulated_norm.add_prefix('CUMNORM_'),
                df_feats.drop(columns=self.input_keys.PRIMARY_KEY)
            ),
            axis=1
        )
        final_df.drop(
            columns=self.input_keys.unused_columns, errors='ignore', inplace=True
        )
        return final_df
