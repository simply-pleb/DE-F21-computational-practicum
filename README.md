 # Differential Equations Practicum

This program aims to compare the precision of 3 different numerical methods for solving differential equations

1. Euler method
1. Improved Euler method 
1. Runge-Kutta method

The criterions of comparison are 

- GTE (global truncation error)
- LTE (local truncation error)
- GTE on an interval of number of steps

The specifics are described in the report pdf file attached here.

logic.py includes all the methods and generates several .csv files that the plotter uses.

index.py and app.py are the interface of the plotter and they require _dash plotly_. 

app.py starts a local server.


