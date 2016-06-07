#!/usr/bin/env python
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import threading
import csv
import time

lock = threading.Lock()

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
        print "Valve is running..."

    ##Starts the server.
    def start(self):
        try:
            ##The servers runs infinitely
            while True:
                self.server._do_run()
        except modbus_tk.modbus.ModbusError as exc:
                print "%s- Code=%d"%(exc, exc.get_exception_code())
    
    ##The server receives data from the client
    ##which are stored in the register 1
    ##Reads the data of register 1
    ##Stores them in the csv file
    def actuatorData(self):
        while True:
            ##Acquire the file for this thread session
            lock.acquire()
            
            ##Reads the value of the register 1          
            vR = self.slave.get_values('0',1)
            #print "vR=%d"%(vR)
            
            ##Opens the csv file in write mode
            actuator_w =  open('Tank/valve.csv', 'wb')
            act_writer = csv.writer(actuator_w)
            
            ##Writes the state of actuator (pump) to the file
            act_writer.writerow(vR)
            
            ##Closes the file
            actuator_w.close()
            
            ##Releases the file
            lock.release()
            
            ##Sleep for one second and repeat
            time.sleep(1)

if __name__ == "__main__":
    ##The listen address and the listen port of the client
    address="10.0.1.7"
    listen_port=502
    
    ##Creates a server instance
    server=modbusServer(address,listen_port)

    ##Declare two threads
    ##Thread 1: Starts the server to listen
    t1 = threading.Thread(target=server.start, args=())
    ##Thread 2: Writes the values of the pump to the csv file
    t2 = threading.Thread(target = server.actuatorData, args=() )
  
    ##Adds the threads to the daemon in order to be able to stop the program with ctrl+C
    t1.daemon = True
    t2.daemon = True
    
    ##Starts the two threads
    t1.start()
    t2.start()
    
    ##The main thread runs infinitely 
    while True:
        time.sleep(0)
