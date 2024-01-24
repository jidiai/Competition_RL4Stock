from backtest.policies import base_taker_policy
from backtest.utils import time_format_conversion
from envs.utils import Order


def backtest_oneday(environment, logdir, backtest_mode, TEST_WHITE_CORE_STRATEGY, backtest_datas):
    obs, done, info = environment.reset()
    while True:

        if ((53820 - time_format_conversion(obs['eventTime'])) / 5) < (
                abs(environment.code_net_position - 0) + 1):

            # Close positions near the market close.
            if backtest_mode == 'oneSide':
                order = Order(side=2, volume=min(
                    1, obs['bv0']), price=obs['bp0'] - 0.1)
            elif backtest_mode == 'twoSides':
                if environment.code_net_position > 0:
                    order = Order(side=2, volume=min(
                        1, obs['bv0']), price=obs['bp0'] - 0.1)
                elif environment.code_net_position < 0:
                    order = Order(side=0, volume=min(
                        1, obs['av0']), price=obs['ap0'] + 0.1)
                else:
                    order = Order(side=1, volume=0, price=0)
        else:
            order = base_taker_policy(obs, info)

        obs, done, info = environment.step(order)

        if done == 2:
            # done == 2 indicates the end of trading for a particular stock on that day;
            # after reset, trading begins for the next stock
            obs, done, info = environment.reset()

        if done == 1:
            # done == 1 indicates the completion of trading for all stocks on that day.
            break

    backtest_datas.append(environment.get_backtest_metric())

    # # Save the back test information locally
    # environment.dump(f"{logdir}/backtest_{backtest_mode}/{environment.date}.json")
