# Real-Time Process Monitoring Dashboard
A graphical dashboard that displays real-time information about process states, CPU usage, and memory consumption. The tool should allow administrators to manage processes efficiently and identify potential issues promptly

## Features:-
 - Visualize Cpu usage and memory usage in real-time by using a line chart.
 - Update the the information within every 2 sec.
 - Display the list of all processes running, including detailos like name, CPU usage and memory usage.
 - A feature of kill button that kill the process from dashboard.

## Working:- 

1. Data Collection:
   - The data_collection.py script gathers the system data like CPU, memory and processes using psutil library.
   - The data collected by data_collection.py script saved into system_matrics.json file so that dashboard can access.

3. Dashboard:-
   - The dashboard.py script reads the data from system.matrics.json file and show on dashboard.
   - User can can see the running process and CPU usage details on the deshboard in a interactive way.
