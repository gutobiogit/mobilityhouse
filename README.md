<h1 align="center"> mobilityhouse </h1>




<img src="images/12_14hrs.png" alt="Image0" width="50%" height="20%"><img src="images/12_14hrs_2.png" alt="Image1" width="50%" height="20%">
<img src="images/12_14hrs_3.png" alt="Image2" width="50%" height="20%"><img src="images/12_14hrs_4.png" alt="Image3" width="50%" height="20%">


<h1 align="center"> What is it?</h1>
This programs are part of the mobilityhouse PV Simulator Challenge.

* **meter_sender.py** is a client program which produces a random value between 0 and 9000 simulating energy consumption, it send to RabbitMq broker

* **magic_table.csv** PV_simulator.py need to load a certain profile of energy production(PV). The solution I found was to download the data from https://data.open-power-system-data.org/time_series/, pick only the german production during summer and map the numbers with the test draw. The result is very close to real, but we have only data every 15 min. For a better view maybe next step is to distribute this data throut this 15 min.l

* **PV_simulator.py** is a program which load data from the broker and print a graphic. The program also looks in magic_table for the PV production during the day.
It output a file named "Data_recorded.csv" which has a timestamp ,meter data, PV simulator, meter data + PV simulator.

<h1 align="center"> What I need?</h1>

* **http://www.pyqtgraph.org/**  
```python 
pip3 install pyqtgraph```

