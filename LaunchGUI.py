import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk#Agg
from matplotlib.figure import Figure

LARGE_FONT = ("Verdana", 12)
    
class Tonyapp(tk.Tk):

    def __init__(self, active_traps, maxima, pulse_widths, current, voltage, starts, ends, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, CustomPage, GraphPage): 
            frame = F(container, self, active_traps, maxima, pulse_widths, current, voltage, starts, ends)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller, active_traps, maxima, pulse_widths, current, voltage, starts, ends):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Start Page', font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        # NAVIGATION BUTTONS
        graph_button = tk.Button(self, text="Compare All Pulses", 
                            command = lambda: controller.show_frame(GraphPage))
        graph_button.pack()
        
        custom_button = tk.Button(self, text="Compare Select Pulses",
                                    command = lambda: controller.show_frame(CustomPage))
        custom_button.pack()

        f = Figure(figsize=(10,6))#, dpi=100)
        gs = f.add_gridspec(3, 2)

        a = f.add_subplot(gs[0, 0])
        a.scatter(active_traps,maxima)
        a.set_title('Peak Current vs Trap Number')
        a.set_xlabel('Trap Number')
        a.set_ylabel('Peak Curennt (A)')
        a.set_ylim([0,1.1*max(maxima)]) #1.1 for visibility

        b = f.add_subplot(gs[0,1])
        b.scatter(active_traps,pulse_widths+[0]*(len(active_traps)-len(pulse_widths)))
        b.set_title('Pulse Width vs Trap Number')
        b.set_xlabel('Trap Number')
        b.set_ylabel('Pulse Width (s)')
        b.set_ylim([0,1.1*max(pulse_widths)]) #1.1 for visibility

        c = f.add_subplot(gs[1,:])
        c.scatter(current['Time (s)'].apply(lambda x: x*1000*1000).to_list(),current['Current (A)'].to_list()) 
        c.set_title('Current vs Time')
        c.set_xlabel('Time (us)')
        c.set_ylabel('Current (A)')
        
        
        d = f.add_subplot(gs[2,:])
        d.scatter(voltage['Time (s)'].apply(lambda x: x*1000*1000).to_list(),voltage['Voltage (V)'].to_list())
        d.set_title('Voltage vs Time')
        d.set_xlabel('Time (us)')
        d.set_ylabel('Voltage (V)')

        f.tight_layout()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class GraphPage(tk.Frame):

    def __init__(self, parent, controller, active_traps, maxima, pulse_widths, current, voltage, starts, ends):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Graph Page', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # NAVIGATION BUTTONS
        home_button = tk.Button(self, text="Back to Home", 
                            command = lambda: controller.show_frame(StartPage))
        home_button.pack()
        
        custom_button = tk.Button(self, text="Compare Select Pulses", 
                                    command = lambda: controller.show_frame(CustomPage))
        custom_button.pack()

        f = Figure(figsize=(5,5))#, dpi=100)
        a = f.add_subplot(111)
        for start, end in zip(starts, ends):
            mod_start, mod_end = 0, end -start
            a.scatter(current['Time (s)'].to_list()[mod_start:mod_end], current['Current (A)'].to_list()[start:end])
        #a.scatter(current['Time (s)'].to_list()[start:end], current['Current (A)'].to_list()[start:end])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class CustomPage(tk.Frame):

    def __init__(self, parent, controller, active_traps, maxima, pulse_widths, current, voltage, starts, ends):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Choose Which Pulses to Compare', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # NAVIGATION BUTTONS
        home_button = tk.Button(self, text="Back to Home", 
                            command = lambda: controller.show_frame(StartPage))
        home_button.pack()
        
        graph_button = tk.Button(self, text="Compare All Pulses",
                            command = lambda: controller.show_frame(GraphPage))
        graph_button.pack()

        # LIST BOX
        listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        tk.Label(self, text="Choose a trap").pack()
        listbox.pack()

        for x,item in enumerate(active_traps):
            listbox.insert(x, item)

        #PLOT GRAPH
        def plot_graph():
            selected = listbox.curselection()
            selected_traps = [active_traps[x] for x in selected]
            selected_starts = [starts[x] for x in selected]
            selected_ends = [ends[x] for x in selected]
            f = Figure(figsize=(5,5))#, dpi=100)
            a = f.add_subplot(111)
            for start, end in zip(selected_starts, selected_ends):
                mod_start, mod_end = 0, end -start
                a.scatter(current['Time (s)'].to_list()[mod_start:mod_end], current['Current (A)'].to_list()[start:end])
            a.legend(selected_traps)
            #a.scatter(current['Time (s)'].to_list()[start:end], current['Current (A)'].to_list()[start:end])

            def clear_graph():
                canvas._tkcanvas.pack_forget()
                canvas.get_tk_widget().pack_forget()
                toolbar.pack_forget()
                b.pack_forget()

            b = tk.Button(self, text="Clear Graph", command=clear_graph)
            b.pack()

            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            toolbar = NavigationToolbar2Tk(canvas, self)
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        plot_button = tk.Button(self, text="Plot Graph", command = plot_graph)
        plot_button.pack()


        
        