
from subprocess import *
import os, sys

def GetPIDByProcessName(aProcessName):
	for proc in psutil.process_iter():
		if proc.name == aProcessName:
			return proc.pid

def OpenNotepadAndSuspend(spyManager):
	print ("Starting Notepad...")
	notepadPath = os.path.join(os.environ['WINDIR'],"syswow64\\notepad.exe")
	notepad, continueEvent = spyManager.CreateProcess(notepadPath, True)
	if notepad is None:
		notepadPath = os.path.join(os.environ['WINDIR'],"system32\\notepad.exe")
		notepad, continueEvent = spyManager.CreateProcess(notepadPath, True)
	if notepad is None:
		print ("Cannot launch Notepad")
		sys.exit(0)
	return notepad, continueEvent

def HookFunctionForProcess(spyManager, functionModuleAndName, notepadPID):
	print ("Hooking function " + functionModuleAndName + " for Notepad...")
	hook = spyManager.CreateHook(functionModuleAndName, 0)
	hook.Attach(notepadPID, True)
	hook.Hook(True)
	print ("Notepad successfully hooked")
	return hook

def StartNotepadAndHook(spyManager):
	notepad, continueEvent = OpenNotepadAndSuspend(spyManager)
	hook = HookFunctionForProcess(spyManager, "kernel32.dll!CreateFileW", notepad.Id)
	spyManager.ResumeProcess(notepad, continueEvent)
	return notepad
