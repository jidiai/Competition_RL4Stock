import random
import os
import sys
from pathlib import Path
CURRENT_PATH = str(Path(__file__).resolve().parent.parent)
taxing_path = os.path.join(CURRENT_PATH)
sys.path.append(taxing_path)
print(CURRENT_PATH)
stock_path = os.path.join(CURRENT_PATH, 'env/stock_raw')
sys.path.append(stock_path)


import numpy as np
import pandas as pd
import math

from .stock_raw.envs.stock_base_env_cython import StockBaseEnvCython
from .stock_raw.backtest.utils import ParquetFile
from .stock_raw.mock_market_common.mock_market_data_cython import MockMarketDataCython
from .stock_raw.utils import Order

from .utils.box import Box
from .utils.discrete import Discrete
from .simulators.game import Game



class KaFangStock(Game):
    def __init__(self, conf,seed=None):
        super(KaFangStock, self).__init__(conf['n_player'], conf['is_obs_continuous'], conf['is_act_continuous'],
                                               conf['game_name'], conf['agent_nums'], conf['obs_type'])
        self.seed = seed
        self.set_seed()
        file = ParquetFile()
        self.env_core_list = []

        signal_file_original_rootpath = os.path.join(stock_path, 'data')
        self.dateList = [name for name in os.listdir(signal_file_original_rootpath) if
                    os.path.isdir(os.path.join(signal_file_original_rootpath, name))]
        self.dateList.sort()
        for date in self.dateList[:]:
            file.filename = os.path.join(stock_path, "./data/" + date + '/train_data.parquet')
            file.load()
            df = file.data
            code_list = []
            for item in df['code'].unique():
                code_list.append(float(item))
            df = np.array(df)
            mock_market_data = MockMarketDataCython(df)
            env = StockBaseEnvCython(date, code_list, mock_market_data)

            self.env_core_list.append(env)

        self.init_info = ''
        self.done = False
        self.step_cnt = 0
        self.won = {}
        self.reset()

        self.backtest_mode = 'twoSides'
        # self.metrics = []


    @staticmethod
    def create_seed():
        seed = random.randrange(1000)
        return seed

    def set_seed(self, seed=None):
        if not seed:        #use previous seed when no new seed input
            seed = self.seed
        else:               #update env global seed
            self.seed = seed
        random.seed(seed)
        np.random.seed(seed)

    def joint_action_space(self):
        return [self.get_single_action_space(0)]

    def get_single_action_space(self, player_idx):
        return [Discrete(3), Box(low=0, high=100, shape=(1,)), Box(low=2000, high=10000, shape=(1,))]

    def reset(self):
        self.init_info = None
        self.step_cnt = 0
        self.total_r = 0
        self.current_game = 0
        self.total_game = len(self.env_core_list)

        obs, done, info = self.env_core_list[self.current_game].reset()
        self.all_observes = [{"observation": obs, "new_game": True}]
        return self.all_observes

    def reset_game(self):
        self.current_game += 1
        obs, done, info = self.env_core_list[self.current_game].reset()
        self.all_observes = [{"observation": obs, "new_game": True}]
        return self.all_observes


    def is_valid_action(self, joint_action):
        if len(joint_action) != self.n_player:          #check number of player
            raise Exception("Input joint action dimension should be {}, not {}".format(
                self.n_player, len(joint_action)))
        if len(joint_action[0][0]) != 3:
            raise Exception("Input action dimension should be {}, not {}".format(
                3, len(joint_action[0][0])
            ))

    def convert_action(self, action):
        """
        Possible action format:
        [[x], [x], [x]]
        [x, x, x]
        """
        side, volume, price = action[0], action[1], action[2]
        if isinstance(side, list):
            if len(side)==3:
                side = side.index(1)
            elif len(side)==1:
                side = side[0]
        else:
            side = self.get_single_action_space(0)[0].sample()

        if isinstance(volume, list):
            volume = volume[0]
        elif isinstance(volume, np.ndarray):
            volume = volume[0]
        elif isinstance(volume, float):
            volume = volume
        else:
            volume = self.get_single_action_space(0)[1].sample()

        if isinstance(price, list):
            price = price[0]
        elif isinstance(price, np.ndarray):
            price = price[0]
        elif isinstance(price, float):
            price = price
        else:
            price = self.get_single_action_space(0)[2].sample()

        return Order(side = side,
                      volume=volume,
                      price = price)


    def step(self, action):
        """
        Action format:
        [side, volume, price]
        """
        self.is_valid_action(action)
        action_array = action[0]
        decoded_order = self.convert_action(action_array)

        # side = 2  ##random.choice([0,1,2])
        # volume = min(1, self.all_observes[0]['bv0'])#random.randrange(0,2)
        # price = self.all_observes[0]['bp0']-0.1

        info_before = None

        try:
            obs,done,info = self.env_core_list[self.current_game].step(decoded_order)
        except ValueError as v:
            print(f'Current game terminate early due to error {v}')
            done = True
            obs = {}
            info = None

        # self.all_observes = [obs]
        self.step_cnt += 1

        if done and (self.current_game<self.total_game-1):
            obs = self.reset_game()
            self.all_observes = obs
        elif done and (self.current_game==self.total_game-1):
            self.done = True
            self.all_observes = [{"observation": obs, "new_game": False}]
        else:
            self.all_observes = [{"observation": obs, "new_game": False}]


        if self.done:
            self._load_backtest_data()
            self.compute_final_stats()
            self.set_n_return()

        return self.all_observes, 0, done, info_before, ''

    def is_terminal(self):
        return self.done



    def set_n_return(self):
        self.n_return = [self.stats['daily_pnl_mean_sharped']]

    def check_win(self):
        return '-1'


    def _load_backtest_data(self):
        metric_list = []
        for env in self.env_core_list:
            env_metric = env.get_backtest_metric()
            env_metric_dataframe = pd.DataFrame(env_metric, index=['date'])

            metric_list.append(env_metric_dataframe)

        self.backtest_metric = pd.concat([metric for metric in metric_list])

    def compute_final_stats(self):
        df = self.backtest_metric        #backtest_metric_data
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

        self.stats = stats

