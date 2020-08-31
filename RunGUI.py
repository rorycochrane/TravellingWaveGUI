import ReadCSV
from CalculateValues import calculate_values
from LaunchGUI import *

def run_GUI(TB, settings_file, current_file, voltage_file=None):
    # read csv files
    tw_settings = ReadCSV.read_settings(settings_file)
    current = ReadCSV.read_current(current_file)
    if voltage_file:
        voltage = ReadCSV.read_voltage(voltage_file)
    else:
        voltage = None

    # calculate values to plot
    active_traps, pulse_widths, maxima, starts, ends = calculate_values(TB, tw_settings, current, voltage)
    
    # launch GUI
    app = Tonyapp(
        active_traps, 
        maxima, 
        pulse_widths, 
        current, 
        voltage,
        starts,
        ends
        )
    app.mainloop()

