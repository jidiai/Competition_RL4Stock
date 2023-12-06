<img src="imgs/Jidi%20logo.png" width='300px'> 

# KaFang Technology - Stock Trading Reinforcement Learning Challenge

This repo provide the source code for the [KaFang Technology - Stock Trading Reinforcement Learning Challenge](http://www.jidiai.cn/compete_detail?compete=45)

"RL4Stock (Stock Trading Reinforcement Learning Challenge) is hosted by KAFANG Technology Co., Ltd. It is a reinforcement learning competition tailored for real stock trading scenarios. The competition aims to provide a platform for researchers interested in reinforcement learning to develop effective stock trading strategies. Participants are encouraged to explore various innovative ideas and approaches in this competition, and we have prepared substantial rewards for participants. We welcome everyone to join.


## Multi-Agent Game Evaluation Platform --- Jidi (及第)
Jidi supports online evaluation service for various games/simulators/environments/testbeds. Website: [www.jidiai.cn](www.jidiai.cn).

A tutorial on Jidi: [Tutorial](https://github.com/jidiai/ai_lib/blob/master/assets/Jidi%20tutorial.pdf)


## Environment
The competition environment is a single-player stock prediction game. In this code repository, we have provided some foundational materials necessary for participating in the competition.

To develop effective trading strategies, you can build upon these foundations. Firstly, we offer a real trading environment encapsulated in a `.so` file, similar to the gym format, which can be found in the `./envs/stock_raw/envs` directory.

You can refer to the usage in `./envs/stock_raw/test.py` to incorporate it into your work. Additionally, we provide a simple trading strategy located in the `.envs/stock_raw/backtest/policies.py` file. You can evaluate its performance by running `python ./envs/stock_raw/test.py`.

<img src='imgs/env_img.jpg' width=300>


## Quick Start

You can use any tool to manage your python environment. Here, we use conda as an example.

```bash
conda create -n stock-venv python==3.7.5  
conda activate stock-venv
```

Next, clone the repository and install the necessary dependencies:
```bash
git clone https://github.com/jidiai/Competition_RL4Stock.git
cd Competition_RL4Stock
pip install -r requirements.txt
```

Finally, run the game by executing:
```bash
python run_log.py
```


## Navigation

```
|-- Competition_RL4Stock               
	|-- agents                              // Agents that act in the environment
	|	|-- random                      // A random agent demo
	|	|	|-- submission.py       // A ready-to-submit random agent file
	|-- env                                 // Environment
	|	|-- stock_raw                   // Raw environment
	|	|	|-- data.py             // Testing data
	|	|-- config.py                   // environment configuration file
	|	|-- kafang_stock.py             // The environment wrapper		  
	|-- run_log.py		                // run the game with provided agents (same way we evaluate your submission in the backend server)
```

## Training data 

百度网盘

Link：https://pan.baidu.com/s/1KNw9QYDY4g5EyYGzTP0F-A 

Code：oic4 


## How to test submission

- You can train your own agents using any framework you like as long as using the provided environment wrapper. 

- For your ready-to-submit agent, make sure you check it using the ``run_log.py`` scrips, which is exactly how we 
evaluate your submission.

- ``run_log.py`` takes agents from path `agents/` and run a game. For example:

>python run_log.py --my_ai "random" 

set both agents as a random policy and run a game.

- You can put your agents in the `agent/` folder and create a `submission.py` with a `my_controller` function 
in it. Then run the `run_log.py` to test:

>python run_log.py --my_ai your_agent_name --opponent xxx

- If you pass the test, then you can submit it to the Jidi platform. You can make multiple submission and the previous submission will
be overwritten.


