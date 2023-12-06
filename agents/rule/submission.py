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
    side = [0,1,0]
    volumn = min(1, obs['av0'])
    price = obs['ap0']+0.1
    return [side, [volumn], [price]]

