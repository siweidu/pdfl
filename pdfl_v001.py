#######################
# Automated continuous weight measurement.
# from weighing scale KERN 572
# for powder flow rate measurement.  
# 
#   KERN 572
#       t Tare.
#       w a weighing value (or unstable) is sent via RS 232 interface.
#       s a stable weighing value is sent via RS 232 interface.
#
# 
#
#######################

#from random import random

from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import time
from time import sleep
from PySimpleGUI.PySimpleGUI import VSeparator
import serial
from serial.tools.list_ports import comports
import PySimpleGUI as sg


def main():
    ports = serial.tools.list_ports.comports()
    px = []
    py = []
    pyrate = []



    setting_column = [
        [sg.Text("Ports", size=(10,1))], 
        [sg.Listbox(values=ports, size=(50,6), enable_events=True, key='-PORTLIST-'), sg.Button("Connect", size=(10,6), key='-CONNECT-')],
        [sg.Text('_' * 65)],
        [sg.Text("Total Time", size=(10,1)), sg.Input(key='-TIME-', enable_events=True, size=(10,1)), sg.Text("Minutes")],
        [sg.Text("Interval", size=(10,1)), sg.Input(key='-INTER-', enable_events=True, size=(10,1)), sg.Text("Seconds")],
        [sg.Text("File", size=(10,1)), sg.Input(key='-FILE-', enable_events=True, size=(40,1)), sg.SaveAs(target='-FILE-')],
        [sg.Button("RUN", key='-RUN-')],
        [sg.Text('_' * 65)],
        [sg.Output(size=(65, 10))]

    ]
    result_column = [
        [sg.Canvas(key='-CANVAS-', size=(80, 40))]
        
    ]

    layout = [
        [
            sg.Column(setting_column),
            sg.VSeparator(),
            sg.Column(result_column)
        ]
    ]

    window = sg.Window("Powder Flow Measurement", layout, finalize=True)

    # fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas
    
    
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("Powder flow rate (g/s)")
    ax.grid()
    fig_agg = draw_figure(canvas, fig)

    enable_run = False       #change to False after test
    enable_connect = False  
    ttime = interval = 0
    filename = 'tempfile'

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
        elif event == '-TIME-':
            if values['-TIME-'].isnumeric(): 
                ttime = int(values['-TIME-'])
                print("Total measure time set to " + values['-TIME-'] + " minutes")
        elif event == '-INTER-':
            if values['-INTER-'].isnumeric(): 
                interval = int(values['-INTER-'])
                print("Interval set to " + values['-INTER-'] + " seconds")
        elif event == '-FILE-':
            filename = values['-FILE-']
            #print (filename)
        elif event == '-RUN-' and enable_run:
            if filename != '' and ttime>0 and interval>0:
                enable_connect=False
                
                runtime=0
                f = open(filename, 'w')
                scale.tare()          # dis comment after test

                #start timer
                tstart = time.perf_counter()
                
                while runtime < ttime*60:
                    sleep(interval)
                    weight = scale.read() # float or string  dis comment after test
                    #weight = test()
                    runtime += interval
                    realtimer = time.perf_counter() - tstart
                    print(f'{runtime}, {realtimer:.2f}, {weight}')
                    f.write(str(runtime).replace("b", " ") + ',' + str(realtimer) + ',' + str(weight)+'\n') #write time and weight into text file
                    px.append(realtimer) #time
                    py.append(weight) # weight float   
                    




                f.close()
                pyrate = np.gradient(py,px) #rate
                pymean = np.mean(pyrate) 
                pystd = np.std(pyrate)
                #ax.cla()                    # clear the subplot
                #ax.grid()                   # draw the grid
                ax.plot(px, pyrate, 'x', label = 'Powder flow rate')
                fig_agg.draw()
                print('Measurement completed. \n    Average flow rate: {0} (g/s) \n    Standard deviation: {1} (g/s)' .format(pymean, pystd))



def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

"""
def test():
    return random()
"""



if __name__ == '__main__':
    main()




class ScaleKern:

    def __init__(self, port, baudrate):
        self.port = port
        self.bdrate = baudrate
        self.timeout = 0.3

    def connect(self):
        s = serial.Serial(self.port, self.bdrate, timeout=self.timeout) 
        s.reset_input_buffer()      #clear buffer
        s.write(b'w')
        msg = s.readline()
        if msg != "":
            print("Kern scale connected on " + self.port)
            return 0
        else:
            print("Kern scale NOT connected")
            s.close()
            return 1

    def tare(self):
        self.s.write(b't')
    

    def read(self):
        self.s.reset_input_buffer()      #clear buffer
        self.s.write(b'w')
        strweight = self.s.readline()   
        nweight = strweight.translate({ord(i): None for i in 'bg\\rn\' '})
        return nweight


    def __del__(self):
        self.s.close()  






