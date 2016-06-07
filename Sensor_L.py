#!/usr/bin/env python

## Water Tank Simulator
## It simulates the operation of a Sensor that controls the lowest level of the tank
## It acts as a Modbust TCP Server

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import threading
import csv
import time

class modbusServer:
    def __init__(self,listen_Address, listen_Port):
        ##Creates the server
        self.server = modbus_tcp.TcpServer(address=listen_Address,port=listen_Port)
        ##Creates a slave object
        self.slave = self.server.add_slave(255)
        ##Adding 10 HOLDING_REGISTERS, values = 0
        self.slave.add_block('0', cst.HOLDING_REGISTERS, 1, 10)
        ##Adding 100 COILS, values = 0
        #self.slave.add_block('1', cst.COILS, 1, 100)
        ##Creates socket, bind and listen
        self.server._do_init()
        print "Sensor_L is running..."

    ##Starts the server.
    def start(self):
        try:
            ##The servers runs infinitely
            while True:
                self.server._do_run()
        except modbus_tk.modbus.ModbusError as exc:
                print "%s- Code=%d"%(exc, exc.get_exception_code())

    ##Reads the data from a csv files
    ##which is the lowest level sensor's data
    def sensorData(self):
        sL=0 ##The sensor state variable
        while True:
            ##Opens the file
            sensor_file = open('Tank/sensor.csv','rb')
            
            ##Reads the rows of the file (actually one row)
            reader = csv.reader(sensor_file)

            ##Gets the first value of the row
            ##which is the state of the sensor
            for row in reader:
                sL = int(row[0])

            #print "sL=%d"%(sL)
            ##Closes the file
            sensor_file.close();
            
            ##Sets the value of register 1 with the state of sensor
            self.slave.set_values('0',1,sL)

            ##Sleep for one second
            time.sleep(1)

if __name__ == "__main__":
    ##The listen address and the listen port of the client
    address="10.0.1.6"
    listen_port=502
    
    ##Creates a server instance
    server=modbusServer(address,listen_port)
    
    ##Declare two threads
    ##Thread 1: Starts the server to listen
    t1 = threading.Thread(target=server.start, args=() )
    ##Thread 2: Reads the values of the sensor from the csv file
    t2 = threading.Thread(target = server.sensorData, args=())
    
    ##Adds the threads to the daemon in order to be able to stop the program with ctrl+C
    t1.daemon = True
    t2.daemon = True
    
    ##Starts the two threads
    t1.start()
    t2.start()
    
    ##The main thread runs infinitely 
    while True:
        time.sleep(0)
