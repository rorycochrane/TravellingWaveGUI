import pandas as pd

def read_settings(settings_file):
    tw_settings = pd.read_csv(settings_file)
    tw_settings.columns = tw_settings.iloc[3]
    tw_settings = tw_settings[4:]
    tw_settings[':Trap #'] = tw_settings[':Trap #'].apply(lambda x: x.strip(':')).astype('int')
    tw_settings['Discharge Instant'] = tw_settings['Discharge Instant'].astype('float')/1000/1000
    tw_settings['Pulse Width'] = tw_settings['Pulse Width'].astype('float')/1000/1000
    return tw_settings

def read_current(current_file):
    current = pd.read_csv(current_file)
    current = current[7:]
    current.columns = ['Time (s)', 'Current (A)']
    current['Current (A)'] = current['Current (A)'].astype(float)
    current['Time (s)'] = current['Time (s)'].astype(float)
    return current


def read_voltage(voltage_file):
    voltage = pd.read_csv(voltage_file)
    voltage = voltage[7:]
    voltage.columns = ['Time (s)', 'Voltage (V)']
    voltage['Voltage (V)'] = voltage['Voltage (V)'].astype(float)
    voltage['Time (s)'] = voltage['Time (s)'].astype(float)
    return voltage