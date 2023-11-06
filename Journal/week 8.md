# Week 8 Updates

### Continued LP formulation - Approach 1 (Analytical Solutions)

Consider the following constants/variables:
- $X_{i,j,p}^{t}$ ~ {1 - if plane p flies route (i,j) at time t, 0 otherwise}
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


**Objective function**: 

$T_{i,j}^{t,0} (X) =   \tau_{i,j} (X_{i,j,p}^{t} + (1 - X_{i,j,p}^{t})M  )$

consider what happens with plane p 
consider dropping plane p 

$T_{i,j,p}^{t,1}(x) = min_{k, t^{'}} \, \,  (t^{'} + \tau_{k,j} - t)$ for $k \neq i,j$



- Condition: $t^{'} - t \geq \tau_{i,k} + \delta_{k} \forall \, \, t,i,k$
  
    Treat $t^{'}$ as a function of X

------
### Possible Idea
To represent the condition $t' - t \geq \tau_{i,k} + \delta_k$ as a linear constraint in the problem, can we add additional binary decision variables and constraints. 

Let $Y_{i,j,k}^{t,t'}$ indicate whether flight (i, j) with aircraft k departs at time t and arrives at time t'. 

$Y_{i,j,k}^{t,t'} = 1$ if flight (i, j) with aircraft k departs at time t and arrives at time t'.

$Y_{i,j,k}^{t,t'} = 0$ otherwise.

Time Condition Constraints: 
To ensure that $t' - t \geq \tau_{i,k} + \delta_k$, add constraints like the following for all i, j, k, t, and t' where flight (i, j) is possible:

$Y_{i,j,k}^{t,t'} \geq X_{i,j,k}^{t} - X_{i,j,k}^{t'} - X_{i,j,p}^{t'}$ for all p , i,j ≠ k


If $X_{i,j,k}^{t} = 1$ and $X_{i,j,k}^{t'} = 1$, it implies that flight (i, j) with aircraft k departs at both time t and time t', which is not allowed. 
Therefore, $Y_{i,j,k}^{t,t'}$ must be set to 0 to satisfy this constraint.

If $X_{i,j,k}^{t} = 1$ and $X_{i,j,p}^{t'} = 1$ for some other aircraft p ≠ k, it implies that aircraft k cannot depart at time t and arrive at time t'. 
Therefore, $Y_{i,j,k}^{t,t'}$ must be set to 0 to satisfy this constraint.

----



For all routes i,j and fixed t (define this time as the earliest departure time) compute: $min ({T_{i,j}^{t,0}, T_{i,j}^{t,1}})$

**Simplications/Assumptions**
1. Fix a time t, treat this as a single time period; fixed network model
2. Fix time t when computing the min passenger travel time for each
3. Assume availability of routes, accepting unbounded number of aircrafts operating that route

**Constraints**
1. All planes in the fleet should be used at time t. This means that exactly one $X_{i,j,p}^{t} \leq 1$ since plane p can only be active on a single route (i,j) at fixed time t.

    This also captures the condition: If a plane p is active on route (i,j) then $X_{i,j,p} = 1$ at time t but $X_{i,j,p} = 0$ for all other i,j routes

    $\sum_{i} \sum_{j}   X_{i,j,p}^{t} \leq 1$   $\forall \, \, t, p$
   

   treat time t as intervals discretized by the min 

2. Budget Constraints
   
   This condition ensures us that the selected $X_{i,j,p}^{t}$ decision variables statisfy cost associated with each route over time. 

   Once again, we are now treating t as a continuous time r.v.

   $\sum_{t,i,j,p} C_{i,j}^{t} X_{i,j,p}^{t}$ $\leq$ BUDGET

3. Airport Capacity

   Ensure that for each destination airport j (from every route at time t), we do not exceed airport j's plane p capacity (which is fixed over time t)

   $\sum_{i} \sum_{p} X_{i,j,p}^{t} \leq K_{j}$  $\forall j, t$

4. $X_{i,j,p}^{t}$ = {0,1}


5. A plane p can only be used for a route (i,j) at time t, if at the previous time, that plane operated a route (i,j) 
    i.e. the destination must match the origin of the next flight 

In other words, $X_{i,l,p}^{t} = 1$ if and only if $X_{l,j,p}^{t^{'}} = 1$ $\forall$ p, t, $t^{'}, i,j, l$, where $t^{'} > t + \tau_{i,j}$


## Fix Time t / Simplification
**Objective function**: 

In the following, we consider the total travel time for a passenger traveling nonstop between their origin airport i and their final destination airport j. 
Note, this value will be very large if the corresponding direct route (i,j) does not exist in the network or $\tau_{i,j}$, the duration of the direct flight (i,j) if this route exists in the network.

$T_{i,j}^{0} (X) =   \tau_{i,j} (X_{i,j,p} + (1 - X_{i,j,p})M  )$

Now consider the second option which is a connecting stop for a passenger traveling between airport i and j. 

$T_{i,j,p}^{1}(X) = min_{k} \, \,  (t^{'} + \tau_{k,j} - t)$ for $k \neq i,j$



We compute $\forall$ direct route pairs $(i,j)$: $min $




   

   
