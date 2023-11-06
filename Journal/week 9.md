# Week 9

## "Simplified" LP Approach and Formulation

### Case 1: Assume we have only a single plane p

Let $G(A,R)$ ~ a **directed** airline network at a given time interval

Consider a set of airports $A = [a_{1}, a_{2}, ..., a_{n}]$, and set of routes $R$, $|R| = M$

$\text{Routes}= \{(i,j) \in A \times A \}$: Set of all allowed routes


- $X_{i,j}^{t}$ ~ {1 - if the plane flies route (i,j) at time t, 0 otherwise}
- $\tau_{i,j}$ ~ flight duration between airport i and airport j
- $D_{i,j}$ ~ Number of passengers with origin i and final destination j
- $C_{i,j}$ ~ operational cost for route (i,j)
- $\delta_{i}$ ~ transfer time at airport i

Objective function is to minimize total passenger travel time:

#### Decision Variables
$X_{i, j}^{t} \in \{0, 1\}$: This variable is equal to 1, if we decide to connect airport $i$ with airport $j$ at time t. Otherwise, the decision variable is equal to zero.

Let t simply be discrete time steps: $t=1, t=2, t=3, ...$

### Objective Function
- **Shortest Travel Time**. Minimize the total travel time of a route for passengers. A route is a sequence of airports where the single plane p travels through, dropping off passengers and picking up new passengers. 


**stuck here**
\begin{equation}
\text{Min} \quad    T = \sum_{t}   \sum_{(i,j) \in \text{Routes}}     d_{i,j} \cdot x_{i,j}^{t}
\tag{0}
\end{equation}


### Constraints/Assumptions

1. Flight duration between any two airports is the same in either direction $\tau_{i,j} = \tau_{j,i}$
2. Operational cost between any two airports is the same in either direction $C_{i,j} = C_{j,i} $
3. Passenger Demand may not be the same between two airports given the direction
4. Ensure the path is connected; i.e. if the plane enters an airport i, it should leave that airport
   
   $\sum_{(i,j) \in \text{Routes}}x_{i,j} = 2 \quad \forall  i \in A$   Does this apply in the directed graph setting?

5. $\forall t  \sum_{(i,j) \in Routes} X_{i,j}^{t} = 1$  - For a single plane, only one route can be flown

6. If at some time t, $\forall j \in A$, $X_{(i,j)}^{t} = 1$, then at time t + 1, $X_{(j,k)}^{t+1} = 1$  Ensure network flow




**Ref. Traveling Salesman optimization problem



### Worked through Example 

Let $A = [a_{1}, a_{2}, a_{3}]$

All possible routes: $R_{all} = [(a_{1}, a_{2}), (a_{1}, a_{3}), (a_{2}, a_{1}), (a_{2}, a_{3}), (a_{3},a_{2}), (a_{3}, a_{1}) ]$

Thus, in general, if $|A| = N$, $|R_{all}| = N^{2} - N$

Suppose we have the following data where the columns are [Origin airport, destination airport, flight duration, passenger demand (count)]:

| Route | Duration $\tau_{i,j}$ | Passenger Demand $D_{i,j}$ |
| -------- | ------- | ------- |
| $a_{1}$ -> $a_{2}$ | 8 | 6
| $a_{1}$ -> $a_{3}$ | 5 | 2
| $a_{2}$ -> $a_{1}$ | 8 | 4
| $a_{2}$ -> $a_{3}$ | 10 | 15
| $a_{3}$ -> $a_{1}$ | 5 | 2
| $a_{3}$ -> $a_{2}$ | 10 | 3

Our goal is to now determine the best path (aka. set of routes) for a plane p so that we minimize the total travel time among the passengers, while considering a set of constraints$

**suppose** the optimal path is determined to be [$a_{1}, a_{2}, a_{3}, a_{2}, a_{1}$]

The corresponding decision variables will then be


| $t = 1$ | $t = 2$ | $t = 3$ | $t = 4$ |
| -------- | ------- | ------- | ------ |
| $X_{(a_{1},a_{2})}^{t=1} = 1$|  $X_{(a_{1},a_{2})}^{t=2} = 0$ | $X_{(a_{1},a_{2})}^{t=3} = 0$ | $X_{(a_{1},a_{2})}^{t=4} = 0$ | 
| $X_{(a_{1},a_{3})}^{t=1} = 0$|$X_{(a_{1},a_{3})}^{t=2} = 0$ |$X_{(a_{1},a_{3})}^{t=3} = 0$ |$X_{(a_{1},a_{3})}^{t=4} = 0$ |
| $X_{(a_{2},a_{1})}^{t=1} = 0$| $X_{(a_{2},a_{1})}^{t=2} = 0$ | $X_{(a_{2},a_{1})}^{t=3} = 0$ | $X_{(a_{2},a_{1})}^{t=4} = 1$ |
| $X_{(a_{2},a_{3})}^{t=1} = 0$|$X_{(a_{2},a_{3})}^{t=2} = 1$ |$X_{(a_{2},a_{3})}^{t=3} = 0$ |$X_{(a_{2},a_{3})}^{t=4} = 0$ |
| $X_{(a_{3},a_{2})}^{t=1} = 0$| $X_{(a_{3},a_{2})}^{t=2} = 0$ | $X_{(a_{3},a_{2})}^{t=3} = 1$ | $X_{(a_{3},a_{2})}^{t=4} = 0$ |
| $X_{(a_{3},a_{1})}^{t=1} = 0$|$X_{(a_{3},a_{1})}^{t=2} = 0$ |$X_{(a_{3},a_{1})}^{t=3} = 0$ |$X_{(a_{3},a_{1})}^{t=4} = 0$ |

So, given this how do we formulate an objective function that considers the routes for each passenger
