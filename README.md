## WATER TANK SIMULATOR
#### with the use of DETERLAB

How to run the WATER TANK Simulator in DeterLAB

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

### 2. Swap in the experiment
### 3. Components
    Install:
    - python-setuptools
    - modbus_tk in every node (except of Tank and Attacker nodes). 
    - ettercap (manually the last version) and tcpdump in attacker node

    If you want to run the monitors, install in SCADA or PLC node:
    - python-matplotlib
    - tightvncserver
    - Export documents as Markdown, HTML and PDF
