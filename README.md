# Senior_Project
Airline Networking Rewiring and Data Analysis Project 

![Alt text](image.png)



#### INTRODUCTION

The global aviation industry is an intricate web of interconnected routes, airports, and flights that enable the efficient movement of passengers and resources. There are two main airline network topologies: the Hub and Spoke topology (HS) and the Point-to-Point topology (PP). In the H&S model, there exists a set of “hub” airports which serve as transit and connection points for passengers. Many of the airlines’ flights originate out of one of their hub airports, where passengers can transfer flights to reach their destination. In contrast, the P2P network topology offers direct routes between different origins and destinations. Each route is independent from the other routes as there is limited need for passengers to connect flights to reach their destination.

However, this intricate network is vulnerable to disruptions caused by unforeseen events such as adverse weather conditions, airport closures, or other unexpected crises. There have many been previous studies investigating the network resilience of PP and HS models during unforeseen events. Such sudden closures of airports and cancellation of flights can cause significant cancellations and delays across the network, affecting passengers, airline costs, and operations.

During airport closures, Airlines often rebook passengers on later flights or to nearby airports if the closure is known of well in advance. However, in many cases, closures are sudden and unpredictable, and many airlines are forced to cancel all inbound and outbound flights to the affected airports. This can cause massive operational delays and cancellations. 

To address this critical issue, this research project seeks to develop a novel probabilistic model to determine real time alternative destinations for affected routes in the network due to airport closure(s). The objective is to proactively rewire the airline network in response to airport closures, with the overarching goal of minimizing passenger travel time and maintaining operational cost-efficiency. This model aims to contribute not only to the resilience of airline networks but also to the seamless travel experience of millions of passengers worldwide, even in the face of unexpected disruptions.


#### PROJECT COMPONENTS


Survey Study and Analysis of Network Resilience 
1.	Conducted large scale network analysis on various airline networks. Compare network statistics across HS and PP network topologies. 
2.	Study network resilience properties across different Airline network topologies. Study network metrics under different network conditions.
3.	Simulate edge and node removal affects network topologies. Compare the results between HS and PP models.

Network Rewiring given single Airport Removal
1.	Given a real time closure of an airport, develop a probabilistic model using the Bayesian paradigm to predict alternate airports where flights should be redirected. This model considers various factors including number of connecting passengers, operational costs, gate availability, passenger demand, remaining fuel, and total passenger travel time. 
2.	A second model using reinforcement learning will be developed (Q-learning for Route Prediction). As an initial approach, the reward function will be based on minimizing total passenger travel time. This algorithm will learn from scheduled flight routes data given any set of airport closures. 

Data Visualization and Dashboard
1.	Construct an interactive dashboard highlighting statistics and findings for the survey analysis. Display relevant figures to highlight key results. Illustrate statistical differences between route optimization in the HS and PP models. 
2.	Deploy algorithm and allow for user testing via interactive dashboard, where users can select airports to remove from the network and see the alternate routes live. 
