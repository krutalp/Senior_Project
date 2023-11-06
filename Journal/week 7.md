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

1. Direct flight exists between airport i and j (0 stops): $T_{i,j}^{t,0} =  D_{i,j}^{t} \tau_{i,j} (B_{i,j,p}^{t} + (1 - B_{i,j,p}^{t})M  )$
   This expression consider several things:
     - all planes p are active at given time t --> which is why we iterate through each plane
     - If a plane p is active on route i,j and the corresponding B variable is 1, then all other instances of B with that specified p must be 0 (since a plane can be operational on only one route at a time)
     - A penalty term M is added to account for nonexistent routes operated by some aircraft p. This helps avoid the trivial solution of having 0 operational flights at time t

2. Consider flights with one stop at airport k
   - Additional factors to consider: time spent at transfer airport, each flight leg duration, whether or not a new aircraft p exists at the intermediate airport k
   - $T_{i,j}^{t,1} = \sum_{k} T_{i,k}^{t,1} + (\tau_{i,k} + \delta_{k}) + T_{k,j}^{t^{'} , 1}$
     where $t^{'} = t + \tau_{i,k} + \delta_{k}$
   - Note $\delta_{k}$ ~ the additional time / error 

**Objective function**: 

$T_{i,j}^{t,0} (x) =   \tau_{i,j} (B_{i,j,p}^{t} + (1 - B_{i,j,p}^{t})M  )$

consider what happens with plane p 
consider dropping plane p 

$T_{i,j,p}^{t,1}(x) = min_{k, t^{'}} \, \,  (t^{'} + \tau_{k,j} - t)$ for $k \neq i,j$



- Condition: $t^{'} - t \geq \tau_{i,k} + \delta_{k} \forall \, \, t,i,k$
Treat $t^{'}$ as a function of x
- Switch all B decision variables with x decision variables 










consider largest time difference - interval 


For all routes i,j and fixed t (define this time as the earliest departure time) compute: $min ({T_{i,j}^{t,0}, T_{i,j}^{t,1}})$

**Simplications/Assumptions**
1. Assume continuous time instead of discrete time intervals, allowing for analysis of a single network throughout the full time period.
2. Fix time t when computing the min passenger travel time for each
3. Assume availability of routes, accepting unbounded number of aircrafts operating that route

**Constraints**
1. All planes in the fleet should be used at time t. This means that exactly one $B_{i,j,p}^{t} \leq 1$ since plane p can only be active on a single route (i,j) at fixed time t.

    This also captures the condition: If a plane p is active on route (i,j) then $B_{i,j,p} = 1$ at time t but $B_{i,j,p} = 0$ for all other i,j routes

    $\sum_{i} \sum_{j}   B_{i,j,p}^{t} \leq 1$   $\forall \, \, t, p$
   

   treat time t as intervals discretized by the min 

2. Budget Constraints
   
   This condition ensures us that the selected $B_{i,j,p}^{t}$ decision variables statisfy cost associated with each route over time. 

   Once again, we are now treating t as a continuous time r.v.

   $\sum_{t,i,j,p} C_{i,j}^{t} B_{i,j,p}^{t}$ $\leq$ BUDGET

3. Airport Capacity

   Ensure that for each destination airport j (from every route at time t), we do not exceed airport j's plane p capacity (which is fixed over time t)

   $\sum_{i} \sum_{p} B_{i,j,p}^{t} \leq K_{j}$  $\forall j, t$

4. $B_{i,j,p}^{t}$ = {0,1}


5. A plane p can only be used for a route (i,j) at time t, if at the previous time, that plane operated a route (i,j) 
    i.e. the destination must match the origin of the next flight 

In other words, $B_{i,l,p}^{t} = 1$ if and only if $B_{l,j,p}^{t^{'}} = 1$ $\forall$ p, t, $t^{'}, i,j, l$, where $t^{'} > t + \tau_{i,j}$



Gameplan moving forward
1. edit up objective function and constraints
2. create sample data to test
3. Run on gurobi using sample data
4. gather real world data: cleaning; preprocessing
5. run on gurobi using real world data
6. run bayesian method and compare network models
7. create visualization dashboard
8. brief report / summary of project - manuscript 



   

   
