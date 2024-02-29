"""!
Real-Time Serial Data Plotter with Tkinter and Matplotlib

Authors: Conor Schott, Fermin Moreno, Berent Baysal

Description:
This script provides a user-friendly interface for real-time plotting of data received from a serial device using Tkinter and Matplotlib. It allows users to visualize data from the serial device and customize plotting parameters.

Requirements:
- Python 3.x
- Tkinter
- Matplotlib
- PySerial

Instructions:
1. Adjust the 'serial_port' and 'baud_rate' variables according to your serial device settings.
2. Customize the stop condition within the 'plot_example' function.
3. Run the script and click 'Run Test' to start plotting.
4. Click 'Clear' to clear the plot.
5. Click 'Quit' to exit the application.
"""

import tkinter
from tkinter.simpledialog import askfloat
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import serial
import threading

def plot_example(plot_axes, plot_canvas, xlabel, ylabel, kp, setpoint):
    """!
    Plot data received from a serial device.

    Args:
    - plot_axes: Matplotlib axes object for plotting
    - plot_canvas: Matplotlib canvas object for updating plot
    - xlabel: Label for the x-axis
    - ylabel: Label for the y-axis
    - kp: Proportional gain for the controller
    - setpoint: Setpoint for the control system
    """
    serial_port = 'COM9'  # Adjust the serial port accordingly
    baud_rate = 115200  # Adjust baud rate if needed
    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    ser.write(b'\x02')  # Send control-B
    ser.write(b'\x03')  # Send control-C
    ser.write(b'\x04')  # Send control-D
    
    # Read data from the serial device for motor1
    time_data = []
    position_data = []
    while not ser.inWaiting():
        if not plot_canvas.running_flag:
            break
    print("Start reading data...")
    line = ser.readline().rstrip().decode('utf-8')  # Read a line of text
    stop_condition = 0
    while stop_condition <= 150:  # Adjust the condition as needed
        try:
            print("Received line:", line)  # Print received line for debugging
            
            if "," in line:  # Check if the line contains a comma
                time_data_str, position_data_str = line.split(",")  # Split the line into parts
                time_data_float = float(time_data_str)
                position_data_float = float(position_data_str)
            
                time_data.append(time_data_float)
                position_data.append(position_data_float)
        except ValueError as e:
            print("ValueError:", e)
        except Exception as e:
            print("Exception:", e)
        finally:
            line = ser.readline().rstrip().decode('utf-8')
            stop_condition += 1
            if not plot_canvas.running_flag:
                break

    print("Data read complete.")
    
    # Plot data for motor1
    plot_axes.plot(time_data, position_data)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()
    ser.close()

class PlotCanvas(FigureCanvasTkAgg):
    def __init__(self, master=None, **kwargs):
        super().__init__(Figure(), master=master, **kwargs)
        self.running_flag = True

def tk_matplot(plot_function, input_fun, xlabel, ylabel, title):
    """!
    Create a Tkinter GUI for real-time plotting.

    Args:
    - plot_function: Function to execute for plotting
    - input_fun: Function to retrieve input values
    - xlabel: Label for the x-axis
    - ylabel: Label for the y-axis
    - title: Title for the plot window
    """
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    plot_canvas = PlotCanvas(master=tk_root)
    axes = plot_canvas.figure.add_subplot()

    toolbar = NavigationToolbar2Tk(plot_canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=lambda: quit_plot(tk_root, plot_canvas))
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or plot_canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: start_plot(plot_function, axes, plot_canvas,
                                                              xlabel, ylabel,
                                                              *input_fun()))

    plot_canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)
    toolbar.grid(row=1, column=0, columnspan=4)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=3)

    tkinter.mainloop()

def start_plot(plot_function, axes, plot_canvas, xlabel, ylabel, kp, setpoint):
    """!
    Start a new thread for real-time plotting.

    Args:
    - plot_function: Function to execute for plotting
    - axes: Matplotlib axes object for plotting
    - plot_canvas: Matplotlib canvas object for updating plot
    - xlabel: Label for the x-axis
    - ylabel: Label for the y-axis
    - kp: Proportional gain for the controller
    - setpoint: Setpoint for the control system
    """
    plot_canvas.running_flag = True
    thread = threading.Thread(target=plot_function, args=(axes, plot_canvas, xlabel, ylabel, kp, setpoint))
    thread.start()

def quit_plot(root, plot_canvas):
    """!
    Quit the application and stop plotting.

    Args:
    - root: Tkinter root window
    - plot_canvas: Matplotlib canvas object
    """
    plot_canvas.running_flag = False
    root.destroy()

if __name__ == "__main__":
    tk_matplot(plot_example, lambda: (0.003, 50000),
               xlabel="Time (ms)",
               ylabel="Position (Encoder Counts)",
               title="Step Response")
