# RL4Stock

<center class =>
<img src="logo_kafang.png" width = 40%>
</center>

"RL4Stock (Stock Trading Reinforcement Learning Challenge) is hosted by KAFANG Technology Co., Ltd. It is a reinforcement learning competition tailored for real stock trading scenarios. The competition aims to provide a platform for researchers interested in reinforcement learning to develop effective stock trading strategies. Participants are encouraged to explore various innovative ideas and approaches in this competition, and we have prepared substantial rewards for participants. We welcome everyone to join.

In this code repository, we have provided some foundational materials necessary for participating in the competition. To develop effective trading strategies, you can build upon these foundations. Firstly, we offer a real trading environment encapsulated in a `.so` file, similar to the gym format, which can be found in the `./envs/` directory. You can refer to the usage in `test.py` to incorporate it into your work. Additionally, we provide a simple trading strategy located in the `./backtest/policies.py` file. You can evaluate its performance by running `python test.py`.

## Installation
To facilitate the smooth testing of your submitted work on the testing platform, we recommend using `Python 3.7.*` and installing some of your dependencies according to the `requirements.txt` file.
```bash
cd RL4Stock
conda create -n RL4Stock python=3.7
conda activate RL4Stock
```

### Install dependency packages

```bash
pip install -r requirements.txt
```

## Usage
### Backtest the white-box strategy
Set TEST_WHITE_CORE_STRATEGY to True in the test.py file, and then run 'python test.py'.

```bash
python test.py
```
