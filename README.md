## WATER TANK SIMULATOR
    Implemented by: Jasdheer Maan, Michail Kapsalakis, and Tho Le Phuoc
    Instructor: Davide Fauri
    
    For the IST Seminar in Technology University of Eindhoven
    2016

### How to run the WATER TANK Simulator in DeterLAB
### 1. Create an experiment
    Copy the model.ns file to generate the topology with these 8 nodes:
    - SCADA
    - PLC
    - Valve
    - Pump
    - SensorH
    - SensorL
    - Tank
    - Attacker
    
    Upload the files in your home folder (/users/$USER)
    Change the IPs in each node in order to be similar to your nodes' IPs

### 2. Swap in the experiment
### 3. Connect to each node
### 4. Components
    Install:
    - python-setuptools
    - modbus_tk in every node (except of Tank and Attacker nodes). 
    - ettercap (manually the last version) and tcpdump in attacker node

    If you want to run the monitors, install in SCADA or PLC node:
    - python-matplotlib
    - tightvncserver
    - Export documents as Markdown, HTML and PDF

### 5. Run the python files
    Get root privileges in each node and run the python files.
    Run the files in this order:
        1. Sensor_H.py
        2. Sensor_L.py
        3. Pump.py
        4. Valve.py
        5. PLC.py
        6. SCADA.py
        7. tanksim.py
        
#### NOTE: Before run the tanksim.py, set the sensors' state to 0:
```sh
$ echo '0,0' > Tank/sensor.csv
```
#### PLC and SCADA print information about the state of tank, sensors, and actuators

### 6. Attack to the system
    In attacker node:
        - Root privileges
        - Run: ettercap -C
        - Sniff -> Unified sniffing
        - Set the correct network interface (e.g. eth4)
        - Targets -> Select Targets
        - Add the targets like that:
            Target 1: /10.1.1.2/
            Target 2: /10.1.1.3/
        - Hosts -> Scan for hosts
        - Mitm -> ARP poisoning
        - In the pop-up window write:
            remote
        - Start -> Start sniffing
        - View -> Connections
        - Filters -> Load a filter
            Select the filter that you want to run
        - If you want to stop the filter:
            Filters -> Stop filtering

### 7. Generate the datasets
Open a new attacker node. Run the tcpdump
```sh
tcpdump -i [network_interface] -w [filename].pcap
```
