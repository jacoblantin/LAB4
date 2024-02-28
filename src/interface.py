"""!
@file interface.py
This file is modified from the interface submitted from Lab00 for use in Lab03.

Namely, this file is modified for use in conjuction with Lab03's main.py, encoder_reader.py, and motor_driver.py.
The graphical interface runs the control loop given a set Kp and graphs the results onto the GUI.
The Kp is modified by manually changing the Kp in main.py's run file.

@author Jacob Lantin, Devon Lau, Filippo Maresca Denini
@date 21-Feb-2024

"""
# import modules
import math
import time
import tkinter

# import modules pt.2
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# function to read serial port output
def serial_read(port, baudrate=9600, timeout=3):
    """!
    @param port The serial port indicated by this Windows Laptop ('COM9' in this case)
    @param baudrate A specified baudrate of 9600 bits/second
    @param timeout A timeout of 2 seconds
    """
    
    ser = Serial(port, baudrate, timeout=timeout)
    ser.write(b'\x04')    
    data = ser.readlines()
    ser.close()
    return data


# function to read and interpret serial data and plot values
def plot_function(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    """
    
    # Read data through USB-serial port, process to make two lists
    serial_port = 'COM9'
    
    serial_data = serial_read(serial_port)
    
    decoded_data = [line.decode('utf-8') for line in serial_data]
    
    csv_data = [line.strip().split(',') for line in decoded_data if ',' in line]
    
    time_values = [int(row[0]) for row in csv_data]
    
    encoder_values = [float(row[1]) for row in csv_data]

    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(time_values, encoder_values)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program.
if __name__ == "__main__":
    tk_matplot(plot_function,
               xlabel="Time (ms)",
               ylabel="Position",
               title="Step Response of One Revolution")

