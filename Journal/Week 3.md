# Week 3 Notes / Planning

### Background Research

From The Traffic Flow Management Rerouting Problem in Air Traffic Control: A DynamicNetwork Flow Approach - DIMITRIS BERTSIMAS & PATTERSON

"
The problem of dynamically rerouting aircraft has not been addressed to the best of our knowledge in the literature. We propose an integrated mathemat-ical programming approach that consists of severalmethodologies and that determines how to adjustthe release times of flights into the network, control flight speed once they are airborne, and rerouteflights. 
"

Background on Airline rerrouting practices
Source: BTS, FAA
1. Airport gate availability is dependent on type of aircraft, time of day of aircraft arrival, airport hub denotation, airport slot recommendations
2. There isn't often a consideration of connecting passengers when rerouting flights
3. Many flights are often cancelled ahead of 
4. Remote parking and passenger accomdations allow for a few flights off schedule to land at airports given certain factors - FAA
5. Previous research highlight the poor network recovery after airport closures - increased delay times and further cancellations


### Research Problem / Investigation

1. Analyzing network resilence in P2P and HS network topologies 
2. Studying current network resilience properties
3. Case study with Southwest Airlines & United Airlines Networks

### Reinforcment Learning Notes
Source: towardsDataScience

The Reinforcement Learning problem involves an agent exploring an unknown environment to achieve a goal - In this case, exploring different network topologies or configurations.

The known hypothesis is that all goals can be described by the maximization of expected cumulative reward. Our reward function would be the running sum of total passenger travel time, or airline operating costs (we would want to minimize both)

The agent must learn to extract the state of the environment using its actions to derive maximal reward. (inverse of above functions?)

The formal framework for RL borrows from the problem of optimal control of Markov Decision Processes (MDP).

The main elements of an RL system are:

- The agent or the learner
- The environment the agent interacts with
- The policy that the agent follows to take actions
- The reward signal that the agent observes upon taking actions

Problems
1. High dimensional state space: many route combinations / complete graph considerations?
2. Reward system may not work well given the various constraints specified
3. Many data factors to consider and implement into the RL system
   
alternate approaches?

### Gurobi - Applications
Source: https://www.gurobi.com/solutions/gurobi-optimizer/

LP optimization solver

Provide
- list of variables (in our problem, binary variables of the presence of a new route from airport i to airport j)
- objective functions (minimize avg total travel time for passengers, operational costs for airlines)  dual program?


## Data Collection updates
1. reviewed flightstats, OAG, and flightaware rest APIs for data
2. Large costs associated with API keys
3. Turned to open source data 
   1. BTS, TSA, FlightStats, Airline databases 

## Proposed Methods / Ideas
List of variables to account for / Data Collection:
1. Airport capacity at a given time t
2. Passenger data for each flight $f_{i}$ in the network
3. US airports data
4. Aircraft type on each route including feul capacity/availbility 
5. Connecting passengers data


**Linear Programming Approach**

Objective Function: minimize total travel time for passengers and total operating cost to the airline

Given $n$ total flights at a given time $t$:

-> We track the various candidate routes that can be added (rerouting to new airports)

$A$ ~ set of airports in network
$R$ ~ set of all flight routes in network: each element r = (i,j)

Objective function:

$\sum_{i\in A}\sum_{j\in A}$ $X_{i,j} * T_{i,j}$ + $\sum_{i\in A}\sum_{j\in A}$ $C_{i,j} * X_{i,j}$

where $X_{i,j}$~ binary variable: 1 if route (i,j) is included in network, 0 otherwise, $T_{i,j}$ ~ avg remaining travel time for passengers after route $X_{i,j}$, $C_{i,j}$ ~ operating cost for this route.

Constraints

1. For all airports $e \in A$, $\sum_{j = e} X_{i,j}$ (if j = e) < K - This ensures that no more than a certain number of aircraft can be redirected to airport e at the same time  (airport capacity)
2. Fuel constraints for each rerouted aircraft
3. Only propose a single new route despite model containing all possible routes after an airport removal (from origin airport)



**Bayesian Paradigm Approach**


For each affected route in the network, define a set of candidate airports for which the aircraft can be redirected to: $[a_{1}, a_{2}, ..., a_{n}]$

Output the probability of rerouting to each of the respective airports given historical data and current factors (contributing to the likelihood function)

1. Prior Probability Distribution:
   
   Define a prior probability distribution over the candidate airports for rerouting. This could be based on historical rerouting data, airport statistics, or any relevant prior information.

2. Likelihood function that models the probability of rerouting to a specific airport given certain factors. 
    These factors include:
    - Airport proximity to the closed airport.
    - Historical rerouting patterns.
    - Flight schedule compatibility.
    - Passenger preferences.
    - Airport capacity.

Leverage Bayesian Updating procedure:

$P(A_{i}|D) = \frac{P(A_{i})  P(D|A_{i})}{C}$

$P(A_{i})$ ~ prior probability of rerouting to airport i

$P(A_{i}|D)$ ~ posterior probability of rerouting to airport i given data

$P(D|A_{i})$ ~ likelihood function probability of rerouting to airport i given various network factors 

Example:

$P(D|A_{i})$ = P(Connecting passengers | $A_{i}$) P(Route operating costs | $A_{i}$) P(Airport capacity | $A_{i}$) P(Airport capacity | $A_{i}$) ....



