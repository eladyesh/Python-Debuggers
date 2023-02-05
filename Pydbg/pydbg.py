import psutil

# An attempt to hook the CreateFileA function

def get_pid(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc.pid
    return None

import pydbg
import pydbg.defines as defines


def CreateFileA_handler(dbg):
    print("CreateFileA called with parameters:")
    print("File: ", dbg.context.Eax)
    print("Desired access: ", dbg.context.Ecx)
    print("Share mode: ", dbg.context.Edx)
    print("Security attributes: ", dbg.context.Ebx)
    print("Creation disposition: ", dbg.context.Esp)
    print("Flags and attributes: ", dbg.context.Ebp)
    print("Template file: ", dbg.context.Esi)
    return dbg.defines.DBG_CONTINUE


dbg = pydbg.pydbg()
pid = input("Enter the PID of the process to attach to: ")
dbg.attach(int(pid))
dbg.bp_set(dbg.func_resolve("kernel32.dll", "CreateFileA"), handler=CreateFileA_handler)
dbg.run()
