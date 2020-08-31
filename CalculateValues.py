import numpy as np

def calculate_values(TB, tw_settings, current, voltage):
    active_traps = tw_settings[tw_settings['Enabled?']=='X'][':Trap #'].to_list()
    discharge_times = tw_settings[tw_settings['Enabled?']=='X']['Discharge Instant'].to_list()
    pulse_widths = tw_settings[tw_settings['Enabled?']=='X']['Pulse Width'].to_list()

    # TODO: Allow for some enabled traps not to show up in the current because they're cut off
    # current_range = [current['Time (s)'].iloc[0],current['Time (s)'].iloc[-1]]
    # in_range = [1 if x < current_range[1] and x> current_range[0] else 0 for x in discharge_times]


    all_active_traps = tw_settings[tw_settings['Enabled?']=='X'][':Trap #'].to_list()
    all_discharge_times = tw_settings[tw_settings['Enabled?']=='X']['Discharge Instant'].to_list()
    all_pulse_widths = tw_settings[tw_settings['Enabled?']=='X']['Pulse Width'].to_list()
    
    active_traps = [x for x in all_active_traps if x%16==TB]
    discharge_times = [y for x,y in zip(all_active_traps, all_discharge_times) if x%16==TB]
    pulse_widths = [y for x,y in zip(all_active_traps, all_pulse_widths) if x%16==TB]

    #default to prevent an error if no trap is chosen
    chosen_trap = active_traps[0] 
    chosen_index = active_traps.index(chosen_trap)
    
    def get_closest(val, lst, region):
        for x in range(len(lst)):
            if lst[x] > val and lst[x-1] < val:
                if region=='start':
                    return max(x-25, 0) #add a buffer to improve graph
                elif region=='end':
                    return min(x+10,len(lst)-1) #add a buffer to improve graph
    
    starts = [get_closest(x, current['Time (s)'].to_list(), 'start') for x in discharge_times]
    ends = [get_closest(x+y, current['Time (s)'].to_list(), 'end') for x,y in zip(discharge_times, pulse_widths)]
    maxima = [max(current['Current (A)'].to_list()[x:y]) for x,y in zip(starts, ends)]   
    
    from scipy.signal import savgol_filter
    smooth_current = savgol_filter(np.ravel(current['Current (A)'].values), 153, 3)
    dif_current = np.diff(smooth_current)
    
    starts_shifted_up = [0] + starts[:len(starts)-1]
    starts_shifted_down = starts[1:] + [len(current)-1] # list of the start of the next pulse
    starts_shifted = zip(starts_shifted_up, starts_shifted_down)
    meas_starts = [np.argmax(dif_current[x:y]) for x,y in starts_shifted]
    meas_ends = [np.argmin(dif_current[x:y]) for x,y in starts_shifted]
    
    baseline = current['Current (A)'].values[:starts[0]//2].mean()
    cuts = [0] + [(x+y)//2 for x,y in zip(starts[1:], ends[:len(ends)-1])]
    meas_starts = []
    meas_ends = []
    for cut in cuts:
        for x in range(len(current[cut:])-10):
            if current['Current (A)'].values[cut+x+10] > baseline + 10 and current['Current (A)'].values[cut+x] < baseline + 10:
                meas_starts.append(cut+x)
                break
        for x in range(len(current[cut:])-10):
            if current['Current (A)'].values[cut+x+10] < baseline + 10 and current['Current (A)'].values[cut+x] > baseline + 10:
                meas_ends.append(cut+x)
                break

    pulse_widths = [current['Time (s)'].to_list()[y]-current['Time (s)'].to_list()[x] for x,y in zip(meas_starts, meas_ends)]
    
    return active_traps, pulse_widths, maxima, starts, ends

