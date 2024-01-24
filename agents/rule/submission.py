# -*- coding:utf-8  -*-

"""
# =================================== Important =========================================
Notes:
1. this agent is rule agent that keep the env running , which can fit any env in Jidi platform.
2. if you want to load .pth file, please follow the instruction here:
https://github.com/jidiai/ai_lib/blob/master/examples/demo
"""


def my_controller(observation, action_space, is_act_continuous=False):
    obs = observation['observation']
    
    if obs['signal0'] > 0.8:

        # Long opening
        price = (obs['ap0'] + obs['bp0']) / 2 * (1 + (obs['signal0'] * 0.0001))
        if price < obs['ap0']:
            side = [0, 1, 0]
            volumn = 0
            price = 0
        elif obs['ap0'] <= price:
            side = [1, 0, 0]
            volumn = min(obs['av0'], 300 - obs['code_net_position'])
            price = price
    elif obs['signal0'] < -0.8:

        # Short opening
        price = (obs['ap0'] + obs['bp0']) / 2 * (1 + (obs['signal0'] * 0.0001))
        if price > obs['bp0']:
            side = [0, 1, 0]
            volumn = 0
            price = 0
        elif obs['bp0'] >= price:
            side = [0, 0, 1]
            volumn = min(obs['bv0'], 300 + obs['code_net_position'])
            price = price
    else:
        side = [0, 1, 0]
        volumn = 0
        price = 0

    return [side, [volumn], [price]]

