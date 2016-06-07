#!/usr/bin/env python
import threading
import csv
import time

lock = threading.Lock()

def sensor_write():
    ##Thes sensor data array, with the states of the sensors
    sensor_data = ["0,0".split(","),  "1,0".split(","),  "1,1".split(",")]
    
    ##Gets the current time and sets it as the zero point
    t0 = time.time()
    
    ##The initial state of pump and valve is zero and they will be changed when the program reads the files
    valve = 0
    pump = 0
    
    while True:
        lock.acquire()
        ##Opens and read the file of pump
        actuator_p =  open('Tank/pump.csv', 'rb')
        act_p_reader = csv.reader(actuator_p)
        
        ##Reads the value of the file, which is the state of the pump
        for row in act_p_reader:
            pump = int(row[0])
        
        ## Closes the file
        actuator_p.close()
        lock.release()

        ##While the state of the pump is 1 , the process is repeated
        while (pump == 1):
            lock.acquire()
            ##Opens the file of the sensors in order to write their states
            sensor_w =  open('Tank/sensor.csv', 'wb')
            writer = csv.writer(sensor_w, delimiter=',')

            ##Computes how many seconds have passed after the beginning of the program
            t1 = int(time.time() -t0)
            
            ##Depending on the seconds, the state of the tank is changed
            if (t1<=1):
                writer.writerow(sensor_data[0])
            if (t1 >1 and t1<15 ):
                writer.writerow(sensor_data[1])
            elif (t1 >= 15):
                writer.writerow(sensor_data[2])
            
            ##Opens the pump file
            actuator_p =  open('Tank/pump.csv', 'rb')
            act_p_reader = csv.reader(actuator_p)
            
            ##Reads the new state of the pump
            for row in act_p_reader:
                pump = int(row[0])
            
            ##Closes the files
            actuator_p.close()
            sensor_w.close()
            lock.release()

            ##Sleeps for one second
            time.sleep(1)
        
        
        lock.acquire()
        
        ##Opens and read the file of pump
        actuator_v =  open('Tank/valve.csv', 'rb')
        act_v_reader = csv.reader(actuator_v)
        
        ##Reads the value of the file, which is the state of the valve
        for row in act_v_reader:
            valve = int(row[0])

        ## Closes the file
        actuator_v.close()
        lock.release()
        
        ## Initiate the starting time again
        t0 = time.time()
        
        ##While the state of the valve is 1 , the process is repeated
        while (valve == 1):
            lock.acquire()
            
            ##Opens the file of the sensors in order to write their states
            sensor_w =  open('Tank/sensor.csv', 'wb')
            writer = csv.writer(sensor_w, delimiter=',')
            
            ##Computes the new second
            t2 = int(time.time() -t0)
            
            ##Checks the seconds and computes the state of the tank
            if (t2<=1):
                writer.writerow(sensor_data[2])
            if (t2 >1 and t2 <15):
                writer.writerow(sensor_data[1])
            elif (t2>=15):
                writer.writerow(sensor_data[0])
            
            ##Opens the valve file
            actuator_v =  open('Tank/valve.csv', 'rb')
            act_v_reader = csv.reader(actuator_v)
            
            ##Reads the new state of the valve
            for row in act_v_reader:
                valve = int(row[0])
            
            ##Closes the files
            actuator_v.close()
            sensor_w.close()
            lock.release()

            ##Sleeps for one second
            time.sleep(1)
            
        ##Initiate the time again
        t0 = time.time()

def main():
    print "Tank process is running..."
    sensor_write()

if __name__=="__main__":
    main()
