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
    portdesc = []
    for port, desc, hwid in sorted(ports):
        #print(port)
        portdesc = port.desc
    
    
    
    setting_column = [
        [sg.Text("Port", size=(10,1))], 
        [sg.Listbox(values=portdesc, size=(30,6), enable_events=True, key='-PORTLIST-'), sg.Button("Connect", size=(10,6))],
        [sg.Text('_' * 40)],
        [sg.Text("Total Time", size=(10,1)), sg.Input(key='-RUNTIME-', size=(10,1)), sg.Text("Minutes")],
        [sg.Text("Interval", size=(10,1)), sg.Input(key='-INTER-',size=(10,1)), sg.Text("Seconds")],
        [sg.Text("File"), sg.Input(key='-FILE')],
        [sg.Button("RUN")]
    ]
    result_column = [
        #[plot]
        [sg.Output(size=(80, 10))]

    ]

    layout = [
        [
            sg.Column(setting_column),
            sg.VSeparator(),
            sg.Column(result_column)
        ]
    ]

    window = sg.Window("Powder Flow Measurement", layout)


    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):                # always check for closed window
            break
        if event == '-PORTLIST-':
            port = values['-PORTLIST-']
        





"""
class ScaleKern:
    bdrate = 9600
    timeout = 0.3
    runtime = 0

    def __init__(self):

    def connect(port):

    def start():

    def setduration():
    
    def setinter():
    
    def setfile():    
"""



"""
    s = serial.Serial(p, 9600, timeout=0.3) 
    s.reset_input_buffer()      #clear buffer
    # device type s.write(b'w')
    device = s.readline()
    if device == 'Kern':
        self.port = p
        print("Kern scale on " + p)
        return 

print("connect to Kern failed")
return   #end of the program
"""





if __name__ == '__main__':
    main()






