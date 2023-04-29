from gpiozero import LED, OutputDevice
from time import sleep

us_delay = 9000     # delay between each step in microseconds
step_per_revo = 2048 # number of half steps per 1 revolution

''' stepper motor '''
r1 = OutputDevice(17) 
r2 = OutputDevice(27)
r3 = OutputDevice(22)
r4 = OutputDevice(10)
    
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


    
            
if __name__ == "__main__":
    step_move(-5)
    print("hello world")

        
    
    
        

        
        

