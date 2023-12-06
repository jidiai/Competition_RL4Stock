<img src="imgs/Jidi%20logo.png" width='300px'> 

# RLChina Competition - Gui Mao Summer Season

This repo provide the source code for the [RLChina Competition - Gui Mao Summer Season](http://www.jidiai.cn/compete_detail?compete=41)



## Multi-Agent Game Evaluation Platform --- Jidi (及第)
Jidi supports online evaluation service for various games/simulators/environments/testbeds. Website: [www.jidiai.cn](www.jidiai.cn).

A tutorial on Jidi: [Tutorial](https://github.com/jidiai/ai_lib/blob/master/assets/Jidi%20tutorial.pdf)


## Environment
The competition environment is a 2-player grid game where each agent plays as a delivery man sending orders from restaurant to customers as quick as possible.

<img src='imgs/delivery.gif' width=300>


### Delivery

#### map

- You are positioned in a 16x16 grid map with 10 restaurants, 20 customers randomly located. The grid map has path along which the agent can move at each time-step

<img src='imgs/delivery_map.png' width=250>

#### Restaurant
- The restaurant will receive an order each 10 time-steps. 
- Each restaurant will hold maximally 10 orders and orders that are not picked by the rider in time will be dropped.

#### Order
- The order contain information of the restaurant, the customer and the time for arrival.
- The arrival time is computed as the order generating time plusing a random number between restuarant-customer distance and 16x16.
- When the order is picked by the rider, a picking time between **D** and **2D** (D is the restaurant-rider distance). 

#### Rider
- At each time-step, the game will dispatch (maximum 20) to each riders orders that are closed enough to pick up (within distance 5).
- Rider can choose to accept any of the dispatched orders in each time-step.
- If multiple riders accept the orders at the same time, the game will assign randomly.
- Rider will automatically pick up the accepted orders once arriving at the specific restaurant.
- Each rider can have maximum 5 orders (including the accepted and the picked).
- Rider need to deliver the order it has picked to specific customer. Rider will receive rewards if the order is delievered in time (reward equals to the distance between the customer and the restaurant).
- Rider will get penality if any accepted order has exceeded the time limit. The penality is half of the distance between the restaurant and the customer.

#### Observation, action and reawrd
- Observation: 
  - agents: all riders' information such as the position and the accepted orders;
  - restaruant: information of all restaurants such as the position and the available orders;
  - customer: position of all customers;
  - roads: coordinates of all roads;
  - controlled_player_index: the index of current controlled agent;
- Action:
  - movement: dimension 5, agent can move up, down, right, left or stay still.
  - pick up orders: dimension 20, 1 represents for picking up the order in the current restaurant;
  - deliver orders: dimension 5, whether to deliver the orders at current location, 5 is the maximum capacity for each rider, 1 represent for yes and 0 for no.
  - accept orders: dimension 10, whether to accept the generated orders (maximum 10) at current time-step.
- Reward:
  - positive reward for the order that is successfully delivered in time, the value is equal to the restaurant-customer distance;
  - negative reward for the accepted order that exceeds time limit, the value is equal to half of the restaurant-customer distance.

## Quick Start

You can use any tool to manage your python environment. Here, we use conda as an example.

```bash
conda create -n deliver-venv python==3.7  
conda activate deliver-venv
```

Next, clone the repository and install the necessary dependencies:
```bash
git clone https://github.com/jidiai/Competition_Delivery.git
cd Competition_Delivery
pip install -r requirements.txt
```

Finally, run the game by executing:
```bash
python run_log.py
```


## Navigation

```
|-- Competition_OvercookedAI               
	|-- agents                              // Agents that act in the environment
	|	|-- random                      // A random agent demo
	|	|	|-- submission.py       // A ready-to-submit random agent file
	|-- env		                        // scripts for the environment
	|	|-- config.py                   // environment configuration file
	|	|-- delivery.py  // The environment wrapper		  
	|-- rl_train
	|       |-- tools.py                    //some helper function for feature engineering  
	|-- utils               
	|-- run_log.py		                // run the game with provided agents (same way we evaluate your submission in the backend server)
```



## How to test submission

- You can train your own agents using any framework you like as long as using the provided environment wrapper. 

- For your ready-to-submit agent, make sure you check it using the ``run_log.py`` scrips, which is exactly how we 
evaluate your submission.

- ``run_log.py`` takes agents from path `agents/` and run a game. For example:

>python run_log.py --my_ai "random" --opponent "random"

set both agents as a random policy and run a game.

- You can put your agents in the `agent/` folder and create a `submission.py` with a `my_controller` function 
in it. Then run the `run_log.py` to test:

>python run_log.py --my_ai your_agent_name --opponent xxx

- If you pass the test, then you can submit it to the Jidi platform. You can make multiple submission and the previous submission will
be overwritten.


