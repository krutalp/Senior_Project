# Week 4 Updates

1. LP formulation - Approach 1 (Analytical Solutions)

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
2. There does not exist a direct route between airprots i and j in our network and 
   


3. Network Passenger Flow (Simulation-based approach)

   

   
