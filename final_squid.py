from gpiozero import LED, OutputDevice
from time import sleep
import cv2
import urllib.request
import numpy as np
import imagej
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import gsm_pi
import serial
import time

# pins
# step_motor_pin_1 = 17
# step_motor_pin_2 = 27
# step_motor_pin_3 = 22
# step_motor_pin_4 = 10

flashlight_pin = 12
water_pump_pin = 17

us_delay = 9000     # delay between each step in microseconds
step_per_revo = 2048 # number of half steps per 1 revolution

''' stepper motor '''
# r1 = OutputDevice(step_motor_pin_1) 
# r2 = OutputDevice(step_motor_pin_2)
# r3 = OutputDevice(step_motor_pin_3)
# r4 = OutputDevice(step_motor_pin_4)

flashlight = OutputDevice(flashlight_pin)
water_pump = OutputDevice(water_pump_pin)
water_pump.on()

''' image sending '''
url='http://10.42.0.35/cam-hi.jpg' # CHANGE TO ACTUAL IP
# cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)


''' mpact '''
# img_count = int, refers to image name       
ij = imagej.init('sc.fiji:fiji')
# img_name = str(img_count) + ".png"

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

def flashlight_power(status):
    # status = bool
    if status:
        flashlight.on()
    else:
        flashlight.off()
    return


def get_water(status):
    # somehow the inputs are flipped, on = off, off = on, possibly due to the pin
    if not status:
        water_pump.on()
    else:
        water_pump.off()


def get_image(count):
    img_resp=urllib.request.urlopen(url)	# get image from url
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
    
    # cv2.imshow("live transmission", frame)
    
    key=cv2.waitKey(1)		# wait 1000 ms
    # count+=1
    
    t=str(count)+'.png'		# name of image
    cv2.imwrite(t,frame)	# save image frame
    print("image saved as: "+t)
    return


def mp_act(img_count):
    
    macro = """
#@ String name
//MP-ACT (Microplastics Automated Counting Tool) v1.0
//Created by J.C.Prata, V. Reis, J. Matos, J.P.da Costa, A.Duarte, T.Rocha-Santos 2019

macro "MPACT Action Tool - Cd61D32D72D92Da2Db2Dc2D33D43D63D73D93Dd3D34D54D74D94Dd4D35D55D75D95Da5Db5Dc5D36D76D96D37D77D97D3aD4aD5aD7aD8aD9aDbaDcaDdaD3bD5bD7bDcbD3cD4cD5cD7cDccD3dD5dD7dDcdD3eD5eD7eD8eD9eDce"{

open(name);
//8-bit conversion and automatic threshold

run("Invert");
run("8-bit");

run("Threshold...");
setThreshold(0,150);
setOption("BlackBackground", false);
run("Convert to Mask");
run("Set Measurements...", "area shape feret's display redirect=None decimal=3");

//title
title = getTitle();
setBatchMode(true);
mpshape = newArray ("Fibers", "Fragments", "Particles");
for (i = 0; i < mpshape.length; i++) {
selectWindow(title);
run("Duplicate...", " ");
rename(mpshape[i]);
}
run("Tile");

//Analyze Fibers
selectWindow(mpshape[0]);
run("Analyze Particles...", "size=3-1000000 pixel circularity=0.0-0.3 display");

//Analyze Fragments
selectWindow(mpshape[1]);
run("Analyze Particles...", "size=3-1000000 pixel circularity=0.3-0.6 display");

//Analyze Particles
selectWindow(mpshape[2]);
run("Analyze Particles...", "size=3-1000000 pixel circularity=0.6-1.0 display");

//Get results and save to excel
for (i = 0; i < mpshape.length; i++) {
    close(mpshape[i]);
}
run("Original Scale");

dir = File.directory; 
name = File.nameWithoutExtension; 
saveAs("results",  name + "_act2_results.csv"); 

}
"""
    # img_count = int, refers to image name       
    img_name = str(img_count) + ".png"
    
    args = {}
    args = {'name':img_name}
    image = ij.io().open(img_name)

    ij.py.run_script("ijm",macro,args)
    # ij.py.show(image)
    macro = """ """
    ij.py.run_script("ijm",macro,args)

    result_name = os.path.splitext(args['name'])[0] + "_act2_results.csv"
    print(result_name)
    data = pd.read_csv(result_name)
    ferets = data.loc[:,['FeretX', 'FeretY']]
    print(ferets)

    # display image
    #im = Image.open(img_name)
    fig, ax = plt.subplots()        # Create figure and axes
    for index, row in ferets.iterrows():
        rect = patches.Rectangle((row['FeretX']-3.6, row['FeretY']-3.6), 10, 10, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    ax.imshow(im)                   # Display the image
    plt.show()

    return (data.shape[0], (data["Label"]=='Fibers').sum(), (data["Label"]=='Fragments').sum(), (data["Label"]=='Particles').sum())

ser = serial.Serial('/dev/serial0')
def SIM800(command):
    AT_command = command + "\r\n"
    ser.write(str(AT_command).encode('ascii'))
    sleep(1)
    if ser.inWaiting() > 0:
        echo = ser.readline() #waste the echo
        response_byte = ser.readline()
        response_str = response_byte.decode('ascii')
        return (response_str)
    else:
        return ("ERROR")

def send_msg(message):
    # message = string
    print(SIM800("AT+CMGF=1"))
    ser.write(str('AT+CMGS="+639279977811"\r\n').encode('ascii'))
    sleep(1) # VERY IMPORTANT
    print(SIM800(message + "\x1A\r\n"))
    return
    
            
if __name__ == "__main__":

     count+=1
     get_water(True)
     sleep(4)
     get_water(False)

     for i in range(1,6):
         sleep(600) # wait 10 minutes
         img_name = str(count) + "_" + str(i)
         flashlight_power(True)
         sleep(5)
         get_image(img_name)
         flashlight_power(False)
         sleep(5)
         mp_count = mp_act(img_name)    
         send_msg("there are " + str(mp_count[0]) + " microplastics in this sample, " \
                + str(mp_count[1]) + " Fibers, " \
                + str(mp_count[2]) + " Fragments, " \
                + str(mp_count[3]) + " Particles, ")
 