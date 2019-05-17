from LIS3DH import LIS3DH
from time import sleep
import matplotlib.pyplot as plt
import datetime as dt
import serial

ser = serial.Serial('/dev/rfcomm0', baudrate=9600)
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

def average(lst):
	return int(sum(lst) / len(lst))


if __name__ == '__main__':
    sensor = LIS3DH(debug=True)
    sensor.setRange(LIS3DH.RANGE_2G)
    sensor.setClick(LIS3DH.CLK_DOUBLE, 200, mycallback=clickcallback)
    
    xs = []
    ys = []
    if ser.readline() == string_byte:
        while True:        
            z = sensor.getZ()*10
            print(z)
            sleep(.1)        
            if z >10:
                while z > 10:
                    z = sensor.getZ()*10 
                    ys.append(z)
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
        
		
	      
    

    #print("Starting stream")
    #while True:

        #x = sensor.getX()
        #y = sensor.getY()
        #z = sensor.getZ()

        # raw values
        #print("\rX: %.6f\tY: %.6f\tZ: %.6f" % (x, y, z))
        #sleep(0.1)

    # click sensor if polling & not using interrupt
    #        click = sensor.getClick()
    #        if (click & 0x30) :
    #            print "Click detected (0x%2X)" % (click)
    #            if (click & 0x10): print " single click"
#            if (click & 0x20): print " double click"
