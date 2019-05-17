from LIS3DH import LIS3DH
from time import sleep
import matplotlib.pyplot as plt
import datetime as dt
import serial

#Creates serial monitor
ser = serial.Serial('/dev/rfcomm0', baudrate=9600)

#Defines string that will be read from phone
string = "ready\r\n"
string_byte = string.encode()

def clickcallback(channel):
    # interrupt handler callback
    print("Interrupt detected")
    click = sensor.getClick()
    print("Click detected (0x%2X)" % (click))
    if (click & 0x10):
        print(" single click")
    if (click & 0x20):
        print(" double click")

#Definition for finding average of an array
def average(lst):
	return int(sum(lst) / len(lst))


if __name__ == '__main__':
	
	#Initialize sensor
    sensor = LIS3DH(debug=True)
    sensor.setRange(LIS3DH.RANGE_2G)
    sensor.setClick(LIS3DH.CLK_DOUBLE, 200, mycallback=clickcallback)
    
    #Initialize arrays for sensor data and x-axis for graphs
    xs = []
    ys = []
    
    #Waits to hear from phone for ready signal
    if ser.readline() == string_byte:
        while True:
			
			#Read sensor data and multiplies by 10 to conver to meters        
            z = sensor.getZ()*10
            print(z)
            sleep(.1)
            #Records once z-acceleration is greater than gravity        
            if z >10:
                while z > 10:
                    z = sensor.getZ()*10 
                    #Adds value to array
                    ys.append(z)
                    #Adds time to array
                    xs.append(dt.datetime.now().strftime('%S.%F'))
                    print(z)
                    sleep(0.1)
                avg = average(ys)
                print(avg)
                ser.write("Acceleration is ".encode())
                ser.write(str(avg).encode())
                ser.write('\n'.encode())
                plt.plot(xs,ys)
         
                plt.show()
        
		
	      
    

    

