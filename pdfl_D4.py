#######################
# KERN 572
# t Tare.
# w a weighing value (or unstable) is sent via RS 232 interface.
# s a stable weighing value is sent via RS 232 interface.
#
#
#######################


import os
import sys
import glob
import argparse
from PySimpleGUI.PySimpleGUI import VSeparator
import serial
from serial.tools.list_ports import comports
import PySimpleGUI as sg


def main():
    ports = serial.tools.list_ports.comports()
    
    setting_column = [
        [sg.Text("Ports", size=(10,1))], 
        [sg.Listbox(values=ports, size=(50,6), enable_events=True, key='-PORTLIST-'), sg.Button("Connect", size=(10,6), key='-CONNECT-')],
        [sg.Text('_' * 40)],
        [sg.Text("Total Time", size=(10,1)), sg.Input(key='-RUNTIME-', enable_events=True, size=(10,1)), sg.Text("Minutes")],
        [sg.Text("Interval", size=(10,1)), sg.Input(key='-INTER-', enable_events=True, size=(10,1)), sg.Text("Seconds")],
        [sg.Text("File"), sg.Input(key='-FILE')],
        [sg.Button("RUN", enable_events=False, key='-RUN-')]
    ]
    result_column = [
        #[plot]
        #[sg.Output(size=(80, 10))]

    ]

    layout = [
        [
            sg.Column(setting_column),
            sg.VSeparator(),
            sg.Column(result_column)
        ]
    ]

    window = sg.Window("Powder Flow Measurement", layout)

    enable_run = enable_connect = False
    runtime = interval = 0
    

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):                # always check for closed window
            break
        if event == '-PORTLIST-' and len(values['-PORTLIST-'])==1:
            port = values['-PORTLIST-'][0].name
            print(port + " selected")
            enable_connect=True
        elif event == '-CONNECT-' and enable_connect:
            try:
                scale = ScaleKern(port, 9600)
                if scale.connect():
                    enable_run = True
                    enable_connect = False                    
            except:
                print("No connection")
        elif event == '-RUNTIME-':
            if values['-RUNTIME-'].isnumeric(): 
                runtime = int(values['-RUNTIME-'])
                # scale.setruntime(int(values['-RUNTIME-']))
                print("Run time set to " + values['-RUNTIME-'] + " minutes")
        elif event == '-INTER-':
            if values['-INTER-'].isnumeric(): 
                interval = int(values['-INTER-'])
                print("Interval set to " + values['-INTER-'] + " seconds")
        elif event == '-RUN-' and enable_run:
            scale.start()










if __name__ == '__main__':
    main()




class ScaleKern:

    def __init__(self, port, baudrate):
        self.port = port
        self.bdrate = baudrate
        self.timeout = 0.3
        self.runtime = 0
        self.inter = 0

    def connect(self):
        s = serial.Serial(self.port, self.bdrate, timeout=self.timeout) 
        s.reset_input_buffer()      #clear buffer
        s.write(b'w')
        msg = s.readline()
        if msg != "":
            print("Kern scale connected on " + self.port)
            return 1
        else:
            print("Kern scale NOT connected")
            s.close()
            return 0
"""
    def setruntime(self,runtime):
        self.runtime = runtime
        print("Run time set to " + runtime + " minutes")
    
    def setinter(self, inter):
        self.inter = inter
        print("Interval set to " + inter + " seconds")
"""    
    #def start():
    
    #def setfile():    23



