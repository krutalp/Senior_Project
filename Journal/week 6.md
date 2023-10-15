# Week 6 Updates

### Continued LP formulation - Approach 1 (Analytical Solutions)

Consider the following constants/variables:
- $B_{i,j,p}^{t}$ ~ {1 - if plane p flies route (i,j) at time t, 0 otherwise}
- $\tau_{i,j}$ ~ flight duration between airport i and airport j
- $D_{i,j}^{t}$ ~ Number of passengers with origin i and final destination j
- $K_{i}^{t}$ ~ airport capcacity / number of additional aircraft at time t
- $C_{i,j}^{t}$ ~ operational cost for route (i,j)
- $L_{p}$ ~ capacity of plane p
- $\delta_{i}$ ~ transfer time at airport i
- $P = {p_{1}, p_{2}, . . ., p_{N}}$ ~ set of aircraft in the fleet
- N ~ total number of aircraft in the fleet

We wish to minimize the total travel time for passengers.

Let's fix t = 0, the variable $D_{i,j}^{t=0}$ tells us the total number of passengers that wish to travel from airport i to the final destination at airport j.
There are two cases:
1. There exists a direct route between airports i and j in our network
2. There does not exist a direct route between airprots i and j in our network and passengers have to make M connections

Objective Funtion: minimize total travel time for passengers

Split into two cases
We iterate through each plane to get a running sum of travel time for all planes active at given time t. 

1. Direct flight exists between airport i and j (0 stops): $T_{i,j}^{t,0} = \sum_{p} D_{i,j}^{t} \tau_{i,j} (B_{i,j,p}^{t} + (1 - B_{i,j,p}^{t})M  )$
   This expression consider several things:
     - all planes p are active at given time t --> which is why we iterate through each plane
     - If a plane p is active on route i,j and the corresponding B variable is 1, then all other instances of B with that specified p must be 0 (since a plane can be operational on only one route at a time)
     - A penalty term M is added to account for nonexist routes operated by some aircraft p. This helps avoid the trivial solution of having 0 operational flights at time t

2. Consider flights with one stop at airport k
   - Additional factors to consider: time spent at transfer airport, each flight leg duration, whether or not a new aircraft p exists at the intermediate airport k
   - $T_{i,j}^{t,1} = \sum_{k} T_{i,k}^{t,1} + (t^{'}) + T_{k,j}^{t^{'} , 1} $
     where $t^{'} = t + \tau_{i,k} + \delta_{k}$
   - Note $T_{k,j}$ 

Objective function: For all routes i,j compute: min {T_{i,j}^{t,0}, T_{i,j}^{t,1}}
Questions
1. Instead of iterating through each plane p, would it make more sense to iterate through each route and then have the LP select whether that route should be operated by a direct flight or a 1-stop connecting flight?



Constraints
1. All planes in the fleet should be used at time t

   $\sum_{p} B_{i,j,p}^{t} = 1$   $\forall i,j,t$
   
2. If a plane p is active on route (i,j) then $B_{i,j,p} = 1$ at time t but $B_{i,j,p} = 0$ for all other i,j routes

3. Budget Constraints

   $\sum_{t,i,j,p} C_{i,j}^{t} B_{i,j,p}^{t}$ $\leq$ BUDGET

5. Airport Capacity

   $\sum_{p} B_{i,j,p}^{t} \leq K_{j} $  $\forall j$

6. $B_{i,j,p}^{t}$ = {0,1}

7. Flight Availability

   $\sum_{i,j} B_{i,j,p}^{t} \leq 1 \forall t,p $


Gameplan moving forward
1. edit up objective function and constraints
2. create sample data to test
3. Run on gurobi using sample data
4. gather real world data: cleaning; preprocessing
5. run on gurobi using real world data
6. run bayesian method and compare network models
7. create visualization dashboard
8. brief report / summary of project - manuscript 



Follow up on data sources:
1. https://www.cirium.com/solutions/schedules-and-routes/
2. https://aviation-edge.com/premium-api/ 

   

   

# Week 6 Updates

### Continued LP formulation - Approach 1 (Analytical Solutions)

Consider the following constants/variables:
- $B_{i,j,p}^{t}$ ~ {1 - if plane p flies route (i,j) at time t, 0 otherwise}
- $\tau_{i,j}$ ~ flight duration between airport i and airport j
- $D_{i,j}^{t}$ ~ Number of passengers with origin i and final destination j
- $K_{i}^{t}$ ~ airport capcacity / number of additional aircraft at time t
- $C_{i,j}^{t}$ ~ operational cost for route (i,j)
- $L_{p}$ ~ capacity of plane p
- $\delta_{i}$ ~ transfer time at airport i
- $P = {p_{1}, p_{2}, . . ., p_{N}}$ ~ set of aircraft in the fleet
- N ~ total number of aircraft in the fleet

We wish to minimize the total travel time for passengers.

Let's fix t = 0, the variable $D_{i,j}^{t=0}$ tells us the total number of passengers that wish to travel from airport i to the final destination at airport j.
There are two cases:
1. There exists a direct route between airports i and j in our network
2. There does not exist a direct route between airprots i and j in our network and passengers have to make M connections

Objective Funtion: minimize total travel time for passengers

Split into two cases
We iterate through each plane to get a running sum of travel time for all planes active at given time t. 

1. Direct flight exists between airport i and j (0 stops): $T_{i,j}^{t,0} = \sum_{p} D_{i,j}^{t} \tau_{i,j} (B_{i,j,p}^{t} + (1 - B_{i,j,p}^{t})M  )$
   This expression consider several things:
     - all planes p are active at given time t --> which is why we iterate through each plane
     - If a plane p is active on route i,j and the corresponding B variable is 1, then all other instances of B with that specified p must be 0 (since a plane can be operational on only one route at a time)
     - A penalty term M is added to account for nonexist routes operated by some aircraft p. This helps avoid the trivial solution of having 0 operational flights at time t

2. Consider flights with one stop at airport k
   - Additional factors to consider: time spent at transfer airport, each flight leg duration, whether or not a new aircraft p exists at the intermediate airport k
   - $T_{i,j}^{t,1} = \sum_{k} T_{i,k}^{t,1} + (t^{'}) + T_{k,j}^{t^{'} , 1} $
     where $t^{'} = t + \tau_{i,k} + \delta_{k}$
   - Note $T_{k,j}$ 

Objective function: For all routes i,j compute: min {T_{i,j}^{t,0}, T_{i,j}^{t,1}}
Questions
1. Instead of iterating through each plane p, would it make more sense to iterate through each route and then have the LP select whether that route should be operated by a direct flight or a 1-stop connecting flight?



Constraints
1. All planes in the fleet should be used at time t

   $\sum_{p} B_{i,j,p}^{t} = 1$   $\forall i,j,t$
   
2. If a plane p is active on route (i,j) then $B_{i,j,p} = 1$ at time t but $B_{i,j,p} = 0$ for all other i,j routes

3. Budget Constraints

   $\sum_{t,i,j,p} C_{i,j}^{t} B_{i,j,p}^{t}$ $\leq$ BUDGET

5. Airport Capacity

   $\sum_{p} B_{i,j,p}^{t} \leq K_{j} $  $\forall j$

6. $B_{i,j,p}^{t}$ = {0,1}

7. Flight Availability

   $\sum_{i,j} B_{i,j,p}^{t} \leq 1 \forall t,p $


Gameplan moving forward
1. edit up objective function and constraints
2. create sample data to test
3. Run on gurobi using sample data
4. gather real world data: cleaning; preprocessing
5. run on gurobi using real world data
6. run bayesian method and compare network models
7. create visualization dashboard
8. brief report / summary of project - manuscript 



Follow up on data sources:
1. https://www.cirium.com/solutions/schedules-and-routes/
2. https://aviation-edge.com/premium-api/ 

   

   
