import os
import subprocess
import time

from winappdbg import Debug, EventHandler


def CreateFileA_handler(event, ra, lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes,
                        dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile):
    print("CreateFileA called with parameters:")
    print("File: ", lpFileName)
    print("Desired access: ", dwDesiredAccess)
    print("Share mode: ", dwShareMode)
    print("Security attributes: ", lpSecurityAttributes)
    print("Creation disposition: ", dwCreationDisposition)
    print("Flags and attributes: ", dwFlagsAndAttributes)
    print("Template file: ", hTemplateFile)


def create_process(event):
    process = event.get_process()
    if process.get_filename().endswith("virus.exe"):
        process.suspend()
        process.hook_function(process.get_module("kernel32.dll").resolve("CreateFileA"), CreateFileA_handler)
        process.resume()
        print("got here")


class MyEventHandler(EventHandler):
    pass


import psutil


def get_pid(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc.pid
    return None


subprocess.Popen(["virus.exe"])
pid = get_pid("virus.exe")
print(pid)

time.sleep(5) # wait for process to start

debug = Debug()
try:
    debug.attach(pid)
    debug.loop()
finally:
    debug.stop()
