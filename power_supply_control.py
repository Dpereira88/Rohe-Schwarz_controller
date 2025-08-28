# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 13:56:39 2022

@author: Dpereira88
"""
import serial
import sys
import serial.tools.list_ports as p
from time import sleep
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich import print as rprint
import pyvisa
import time

console = Console()


def get_com_port_name():
        value = None
        try:
            ports = p.comports()
            tree = Tree("COM Port Tree")
            for port in ports:
                console.log(port)
                tree.add(f"[bold green]Port: [white]{port.device}").add(f"[bold blue]Serial Number: [white]{port.serial_number}") 
                if "VCP" in port.serial_number: #Power supply ROHDE&SCHWARZ
                    value = (port.device)
                    return(value)
                    #break
            #tree for debug 
        except:     
            None
            return(value)
        console.log(tree)  
        return(value)


com_port = get_com_port_name()

def power_supply(str_ComPort, value, output_port_value, voltage, current):
    output_port = f'INST OUT{output_port_value}'
    output_sel =  f'OUTP:SEL {output_port_value}'
    appl = f'APPL {voltage},{current}'
    
    if str_ComPort is not None:
        #console.log(f"[bold green]{str_ComPort}")
        str_ComPort = str_ComPort.replace('COM','ASRL')
        print(str_ComPort) #port com that the powerSupply is connected
        #Visa protocol initiation resources 
        try:
            rm = pyvisa.ResourceManager("C:\\Windows\\System32\\visa64.dll")
            #console.log(rm.list_resources()) #list of resources available
            #name of the port for the Visa protocol
            my_instrument = rm.open_resource(f'{str_ComPort}::INSTR') 
            #power on 1 select out1 with Volts=13.5v and Current=9A and active output
            power_on_OUT1 = (f'{output_port}',f'{appl}','OUTP ON',f'{output_sel}')
            #power off 1 select out1
            power_off_OUT1 = (f'{output_port}','OUTP:SEL 0')
            #need to be created a function
            rprint(f"value:[bold green]{value}")
            if "on" in value.lower():
                for arg in power_on_OUT1: #run commands from tuple 
                    (my_instrument.write(arg))
                    
                #my_instrument.write(output_port)
                time.sleep(2.5)
                value = my_instrument.query('MEAS:CURR?')
                value = float(value)*1000
                rprint(f'{voltage} V | {value:0.2f} mA')
            elif "off" in value.lower():
                for arg in power_off_OUT1: #run commands from tuple 
                    (my_instrument.write(arg))

        except Exception as e:
            rprint(e)
    else:
        rprint("[bold red]No Power Supply Connected")

try:
    power_supply_command = sys.argv[1]
    out = sys.argv[2]
    volt = sys.argv[3]
    curr = sys.argv[4]
    #rprint(f"<{power_supply_command}>")
except IndexError:
    rprint("[b]Usage:[/] python power_supply_control.py <ON> or <OFF>")
else:
    power_supply(com_port,power_supply_command, out, volt, curr)






