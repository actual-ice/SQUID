from gpiozero import LED, OutputDevice
from time import sleep
import cv2
import urllib.request
import numpy as np


# pins
step_motor_pin_1 = 17
step_motor_pin_2 = 27
step_motor_pin_3 = 22
step_motor_pin_4 = 10

flashlight_pin = 23
water_pump_pin = 24

us_delay = 9000     # delay between each step in microseconds
step_per_revo = 2048 # number of half steps per 1 revolution

''' stepper motor '''
r1 = OutputDevice(step_motor_pin_1) 
r2 = OutputDevice(step_motor_pin_2)
r3 = OutputDevice(step_motor_pin_3)
r4 = OutputDevice(step_motor_pin_4)

flashlight = OutputDevice(flashlight_pin)
water_pump = OutputDevice(water_pump_pin)

''' image sending '''
url='http://10.42.0.35/cam-hi.jpg' # CHANGE TO ACTUAL IP
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
count=0


    
def delay_step():
    sleep(us_delay / 1000000)
    return
        
def step_move(degree):
    step_list = [r1, r2, r3, r4]
    steps = (degree/360) * step_per_revo # number of steps needed

    if steps < 0:      # determines the direction of rotation, clockwise or counter clockwise
        # direction = -1 # clockwise
        step_list.reverse()
    i = 0

    while i <= abs(steps):                         
        for step in range(len(step_list)): 
            step_list[step].on()                       # turn on one step 
            step_list[step -2].off()   # turn off step two sequences ago 
            delay_step() # delay step
            i += 1 # one step done 
            
    
    for step in step_list:
        step.off()
    return

def flashlight_power(status){
    # status = bool
    if status:
        flashlight.on()
    elif not status:
        flashlight.off()
    return
}

def get_water(){
    pump_duration = 2 # two seconds
    water_pump.on()
    sleep(pump_duration)
    water_pump.off()
}

def get_image(){
    img_resp=urllib.request.urlopen(url)	# get image from url
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
    
    cv2.imshow("live transmission", frame)
    
    key=cv2.waitKey(1000)		# wait 1000 ms
    count+=1
    
    t=str(count)+'.png'		# name of image
    cv2.imwrite(t,frame)	# save image frame
    print("image saved as: "+t)
}

    
            
if __name__ == "__main__":
    step_move(-5)
    print("hello world")

        
    
    
        

        
        


