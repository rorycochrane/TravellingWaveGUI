# TravellingWaveGUI
This is a project I put together using tkinter for [the Momose group](https://www.chem.ubc.ca/takamasa-momose) as a part of their travelling wave decelerator project. 
The goal was to allow them to better visualize and compare high frequency current signals. It reads a settings file and two data files.
The settings file is a summary of the instructions given to the decelerator indicating which 'traps' on the decelerator will be activated, when they will be activated, and how long they will be activated for. 
The data files are the current and voltage read out at a specific point on the decelerator as a function of time.


The GUI is broken up into several pages. The start page displays graphs of current and voltage vs time as well as the peak amplitude and pulse width of the current vs trap number. 
The graphs can be manipulated and saved for future reference. This page was included to allow users to take a quick glance at the data.
![StartPage](/images/StartPage.png)

Another page provides a graph with all the current pulses lined up to allow a user to qickly look for outliers.
![GraphPage](/images/AllPulsesGraphPage.png)

The final page allows a user to select one or more traps, and plot their respective current pulses for a closer look.
![CustomPage](/images/CustomPulsesGraphPage.png)
