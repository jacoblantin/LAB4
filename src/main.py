"""!
@file main.py
    This file contains the main file, modified from basic_tasks.py, to run two tasks sequentially in
    a real-time scheduler. Each task is the main file from the previous Lab, Lab03 - control loop. The
    tasks are modified as generator files, and the main file in this task runs each task after one another.

@author Jacob Lantin, Devon Lau, Filippo Maresca Denini
@date   2024-Feb-27

"""

import gc
import pyb

import cotask
import task_share

from control import CLPControl

# task 1
def task1_fun():
    """!
    This task runs the control loop with the first motor/encoder, with a Kp set to 6 and 5 revoultions.
    """
    
    while True:
        # (motor A) A10, B4, B5, timer 3
        pinE = pyb.Pin.board.PA10
        pinA = pyb.Pin.board.PB4
        pinB = pyb.Pin.board.PB5
        timer1 = 3

        # encoder 1 pins
        pin1 = pyb.Pin.board.PC6
        pin2 = pyb.Pin.board.PC7
        timer2 = 8

        # initalize controller class
        CLP = CLPControl(pinE, pinA, pinB, timer1, pin1, pin2, timer2)

        # set Kp (1 to 100)
        CLP.set_Kp(6)

        # set setpoint, we assume a full rotation of ~16000 (from testing encoder)
        CLP.set_setpoint(5*16000)

        # run
        CLP.run()

        # disable motor
        CLP.disable_motor()      
        
        yield 0
    


# task 2
def task2_fun():
    """!
    This task runs the control loop with the second motor/encoder, with a Kp set to 6 and 1 revoultion.
    """
    
    while True:
        # (motor B) C1, A0, A1, timer 5    
        pinE = pyb.Pin.board.PC1
        pinA = pyb.Pin.board.PA0
        pinB = pyb.Pin.board.PA1
        timer1 = 5
        
        # encoder 2 pins
        pin1 = pyb.Pin.board.PB6
        pin2 = pyb.Pin.board.PB7
        timer2 = 4
        
        # initalize controller class
        CLP = CLPControl(pinE, pinA, pinB, timer1, pin1, pin2, timer2)
        
        # set Kp (1 to 100)
        CLP.set_Kp(6)
        
        # set setpoint, we assume a full rotation of ~16000 (from testing encoder)
        CLP.set_setpoint(1*16000)
        
        # run
        CLP.run()
        
        # disable motor
        CLP.disable_motor()
        
        yield 0


if __name__ == "__main__":
        
    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False, name="Queue 0")

    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=10, profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=10, profile=True, trace=False, shares=(share0, q0))
    
    # Append tasks to list
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()
    
    # Run the scheduler with the rr_sched scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.rr_sched()     
        except KeyboardInterrupt:
            break

