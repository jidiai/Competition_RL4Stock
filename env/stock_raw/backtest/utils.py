import dill
import gc
import json
import math
import os
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from envs.utils import JsonFile


def time_format_conversion(event_time):
    h = event_time // 10000000
    m = (event_time - h * 10000000) // 100000
    s = (event_time - h * 10000000 - m * 100000) // 1000
    ss = event_time - h * 10000000 - m * 100000 - s * 1000
    return h * 3600 + m * 60 + s


class File(ABC):
    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        self.__filename = filename

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @data.deleter
    def data(self):
        del self.__data

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def dump(self):
        pass

    def purge(self):
        del self.data
        gc.collect()


class DillFile(File):
    def load(self, custom=None):
        try:
            with open(custom if custom else self.filename, "rb") as f:
                self.data = dill.load(f)
        except Exception as e:
            print("e={} filename={}".format(e, self.filename))

    def dump(self, custom=None):
        with open(custom if custom else self.filename, "wb") as f:
            dill.dump(self.data, f, dill.HIGHEST_PROTOCOL)


class CsvFile(File):
    def load(self, custom=None):
        self.data = pd.read_csv(
            custom if custom else self.filename, index_col=0, parse_dates=True)

    def dump(self, custom=None):
        self.data.to_csv(custom if custom else self.filename)


class ParquetFile(File):
    def load(self, custom=None):
        self.data = pd.read_parquet(
            path=custom if custom else self.filename
        )

    def dump(self, custom=None):
        self.data.columns = self.data.columns.astype(str)
        self.data.to_parquet(
            path=custom if custom else self.filename,
            engine="pyarrow"
        )


class BacktestMetrics(CsvFile):
    FILENAME = 'backtest_metrics.csv'

    def __init__(self, envs, backtest_data):
        self.filename = self.FILENAME
        self.envs = envs
        self.backtest_datas = backtest_data
        self.metrics = []

    def make(self, logdir):
        for backtest_datas in self.backtest_datas:
            data = pd.DataFrame(backtest_datas, index=['date'])
            self.metrics.append(data)

        # # Read the file from the local file and calculate the average return if you have saved
        # # the test information locally in line 45 of backtest_oneday.py
        # for environment in self.envs:
        #     # date = environment.date
        #     with open(f'{logdir}/backtest_{self.backtest_mode}/{environment.date}.json') as f:
        #         content = json.load(f)
        #         data = pd.DataFrame(content, index=['date'])
        #         self.metrics.append(data)

        self.data = pd.concat([metric for metric in self.metrics])


class BacktestStats(JsonFile):
    FILENAME = 'backtest_stats.csv'

    def __init__(self, metrics):
        self.filename = self.FILENAME
        self.metrics = metrics

    def make(self):
        df = self.metrics
        stats = {}

        is_traded_day = df['day_total_orders_volume'] != 0
        days_traded = df.loc[is_traded_day, 'day_pnl'].count()
        days_win = sum(df.loc[:, 'day_pnl'] > 0)

        stats['day_pnl_mean'] = df.loc[:, 'day_pnl'].mean()
        stats['daily_return_mean'] = df.loc[:, 'daily_return'].mean()
        stats['code_nums_mean'] = df.loc[:, 'code_nums'].mean()
        stats['day_total_orders_volume_mean'] = df.loc[:,
                                                'day_total_orders_volume'].mean()

        has_traded = days_traded != 0
        stats['win_rate'] = days_win / float(days_traded) if has_traded else 0
        pnl_total_sum = df.loc[:, 'day_pnl'].sum()
        stats['day_traded_pnl_mean'] = pnl_total_sum / \
                                       days_traded if has_traded else 0
        pnl_std = df.loc[:, 'day_pnl'].std(ddof=0)

        std_net_pnl = df.loc[:, 'day_pnl'].std(ddof=0)
        std_net_pnl_notnan = not math.isnan(std_net_pnl)
        std_net_pnl_is_valid = std_net_pnl_notnan and has_traded and std_net_pnl != 0
        stats['sharpe'] = math.sqrt(
            250) * stats['day_pnl_mean'] / pnl_std if std_net_pnl_is_valid else 1

        fee_sum = df.loc[:, 'day_handling_fee'].sum()
        stats['day_handling_fee_mean'] = fee_sum / \
                                         days_traded if has_traded else 0
        if stats['day_pnl_mean'] >= 0:
            stats['daily_return_mean_sharped'] = stats['daily_return_mean'] * \
                                                 min(10, stats['sharpe']) / 10
            stats['daily_pnl_mean_sharped'] = stats['day_pnl_mean'] * \
                                              min(10, stats['sharpe']) / 10
        else:
            stats['daily_return_mean_sharped'] = stats['daily_return_mean']
            stats['daily_pnl_mean_sharped'] = stats['day_pnl_mean']
        self.data = stats
