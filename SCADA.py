#!/usr/bin/env python

## Water Tank Simulator
## Simulates the SCADA System, which receives the state of the tank from the PLC and changes the state of pump and valve

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import time
import csv

##Makes query to modbus server via target_address:port
class modbusClient: 
    def __init__(self,target_Address,target_port):
        self.target_Address=target_Address
        self.target_port=target_port
        print "SCADA is running..."

    def read_Query(self,UID,function_Code,start_Address,number_Registers):
        try:
            ## Connects to the slave
            master = modbus_tcp.TcpMaster(host=self.target_Address,port=self.target_port)
            ## Executes the command
            response=master.execute(UID,function_Code,start_Address,number_Registers)
        except modbus_tk.modbus.ModbusError as exc:
            print "%s- Code=%d"%(exc, exc.get_exception_code())
        return response
    
    ## We don't use it
    def write_Signle_Query(self,UID,function_Code,start_Address,write_Value):
        try:
            ## Connects to the slave
            master = modbus_tcp.TcpMaster(host=self.target_Address,port=self.target_port)
            response=master.execute(UID,function_Code,start_Address,output_value=write_Value)
        except modbus_tk.modbus.ModbusError as exc:
            print "%s- Code=%d"%(exc, exc.get_exception_code())
        return response
    
    
    def write_Multiple_Query(self,UID,function_Code,start_Address,write_Value):
        try:
            ##Connect to the slave
            master = modbus_tcp.TcpMaster(host=self.target_Address,port=self.target_port)

            ## Executes the command
            response=master.execute(UID,function_Code,start_Address,output_value=write_Value)
        except modbus_tk.modbus.ModbusError as exc:
           print "%s- Code=%d"%(exc, exc.get_exception_code())

        return response
    
    
    def processing(self):
        ##Make a query to the PLC and reads the state of the tank
        state=self.read_Query(255,cst.READ_HOLDING_REGISTERS,1,1)
        
        #print "state = %d"%(state[0])
        #print "------"
        
        ##Opens a file and writes the state. The graph will use this value
        state_w =  open('SCADA/state.csv', 'w')
        st_writer = csv.writer(state_w)
        st_writer.writerow([state[0]])
        state_w.close()
        
        ##Opens two files for pump and valve in order to write their state. This values will be used by graph
        pump_w =  open('SCADA/pump.csv', 'w')
        valve_w =  open('SCADA/valve.csv', 'w')
        pump_writer = csv.writer(pump_w)
        valve_writer = csv.writer(valve_w)

        ## If the state of the tank is 0 then the SCADA makes a query to the PLC
        ## and writes the Registers 2 and 3 with the values 1 and 0
        ## Register 2 is the pump
        ## Register 3 is the valve
        if state[0] == 0:
            self.write_Multiple_Query(255,cst.WRITE_MULTIPLE_REGISTERS,2,[1,0])
            pump_writer.writerow([1])
            valve_writer.writerow([0])
        ## If the state of the tank is 0 then the SCADA makes a query to the PLC
        ## and writes the Registers 2 and 3 with the values 0 and 1
        ## Register 2 is the pump
        ## Register 3 is the valve
        elif state[0] == 2:
            self.write_Multiple_Query(255,cst.WRITE_MULTIPLE_REGISTERS,2,[0, 1])
            pump_writer.writerow([0])
            valve_writer.writerow([1])
        
        ##Closes the files
        pump_w.close()
        valve_w.close()


if __name__ == "__main__":
    ##The target address and the target port of the client
    target_address="10.1.2.3"
    target_port=502
    
    ##Creates a client instance
    client=modbusClient(target_address,target_port)
    
    ##Runs the code infinitely until keyboard interruption
    while True:
        ##Calls the processing method of client
        st = client.processing()
        
        ##Sleep for one second
        time.sleep(1)
