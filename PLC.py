#!/usr/bin/env python

## Water Tank Simulator
## Simulates the operation of PLC, which communicate with two sensors, a pump and a valve
## It acts as a Modbus TCP client and Modbus TCP server 

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import time
import threading
import csv

class modbusPLC:
    def __init__(self, Address, Port, option):
        ##Option 1 is used to create a server instance
        if option == 1:
            #Create the server
            self.server = modbus_tcp.TcpServer(address=Address,port=Port)
            #create a slave object
            self.slave = self.server.add_slave(255)
            #adding 100 HOLDING_REGISTERS, values = 0
            self.slave.add_block('0', cst.HOLDING_REGISTERS, 1, 100)
            #adding 100 COILS, values = 0
            self.slave.add_block('1', cst.COILS, 1, 100)
            # create socket, bind and listen
            self.server._do_init()
            
        ## Option 2 is used to create a client instance
        elif option == 2:       
            self.target_Address=Address
            self.target_port=Port
    
    ##Starts the server
    def start(self):
        try:
            ##The servers runs infinitely
            while True:
                self.server._do_run()
        except modbus_tk.modbus.ModbusError as exc:
                print "%s- Code=%d"%(exc, exc.get_exception_code())
    
    ## This method is used for the client instances in order to make read queries to the sensors
    def processing_s(self, id):
        sensor_state=self.read_Query(id,cst.READ_HOLDING_REGISTERS,1,1)
        return sensor_state[0]

    def read_Query(self,UID,function_Code,start_Address,number_Registers):
        try:
            ## Connects to the slave
            master = modbus_tcp.TcpMaster(host=self.target_Address,port=self.target_port)
            ## Executes the command
            response=master.execute(UID,function_Code,start_Address,number_Registers)
        except modbus_tk.modbus.ModbusError as exc:
            print "%s- Code=%d"%(exc, exc.get_exception_code())
        return response
    
    ## This method is used for the client instances in order to make write queries to the actuators (pump and valve)
    def processing_a(self, id, value):
        self.write_Single_Query(id,cst.WRITE_SINGLE_REGISTER,1,value)

    def write_Single_Query(self,UID,function_Code,start_Address,write_Value):
        try:
            ## Connects to the slave
            master = modbus_tcp.TcpMaster(host=self.target_Address,port=self.target_port)
            ## Executes the command
            response=master.execute(UID,function_Code,start_Address,output_value=write_Value)
        except modbus_tk.modbus.ModbusError as exc:
            print "%s- Code=%d"%(exc, exc.get_exception_code())
        return response

##Sensors method
def sensors(client_H,  client_L):
    while True:
        ##Calls the methods of the clients, which return the state of every sensor
        sensor_H = client_H.processing_s(255)
        sensor_L = client_L.processing_s(255)

        ##Computes the state of the tank
        if sensor_H == 0 and sensor_L == 0:
            state = 0
        elif sensor_H == 0 and sensor_L == 1:
            state = 1
        elif sensor_H == 1 and sensor_L == 1:
            state = 2
        
        ##Saves the state of the tank in the Register 1
        plc.slave.set_values('0',1,state)
        #print "sL=%d and sH=%d, state=%d"%(sensor_L, sensor_H, state)
        
        ## Reads the values of register 2 and 3 in which the SCADA writes the values of the actuators
        ##
        pump = plc.slave.get_values('0',2)[0]
        valve = plc.slave.get_values('0',3)[0]
        
        #print "Pump=%d and Valve=%d"%(Pump, Valve)
        #print "-----------------"
        
        ##Opens a file and writes the state of the tank on it. The graph will use this value
        state_w =  open('Tank/plc_tank_state.csv', 'wb')
        st_writer = csv.writer(state_w)
        st_writer.writerow([state])
        
        ##Closes the file
        state_w.close()
        
        ##Sleeps for one second
        time.sleep(1)

##Actuators method
def actuators(client_p,  client_v):
    while True:
        ##Reads the values that SCADA has written in the registers 2 and 3
        pump = plc.slave.get_values('0',2)[0]
        valve = plc.slave.get_values('0',3)[0]
        
        ##Uses the processing_a method of the instance in order to send these values to the actuators
        client_p.processing_a(255, pump)
        client_v.processing_a(255, valve)
        
        ##Sleeps for one second
        time.sleep(1)

if __name__ == "__main__":
    ## The address and the port that the PLC listen as server
    address="10.1.2.3"
    listen_port=502
    
    ## Creates a server instance
    plc = modbusPLC(address, listen_port, 1)

    ## Creates four clients instance
    ## The PLC acts as client when communicates with these servers: Sensor_H, Sensor_L, Pump, Valve
    client_Sen_H=modbusPLC("10.1.1.5",listen_port, 2)
    client_Sen_L=modbusPLC("10.1.1.6",listen_port, 2)
    client_Pump=modbusPLC("10.1.1.4",listen_port, 2)
    client_Valve=modbusPLC("10.1.1.7",listen_port, 2)
    
    ##Declare three threads
    ##Thread 1: starts the server to listen
    t1 = threading.Thread(target=plc.start, args=() )
    
    ##Thread 2: Calls the sensor method
    t2 = threading.Thread(target = sensors, args=(client_Sen_H,client_Sen_L))
    
    ##Thread 3: Calls the actuator method
    t3 = threading.Thread(target = actuators, args=(client_Pump,client_Valve))

    ##Adds the threads to the daemon in order to be able to stop the program with ctrl+C
    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    
    print "PLC is running"
    
    ##Starts the two threads
    t1.start()
    t2.start()
    t3.start()
    
    ##The main thread runs infinitely 
    while True:
        time.sleep(0)
