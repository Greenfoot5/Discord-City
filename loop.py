#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os
import time

g_command = "git pull".split(' ')
b_start = "python3 DiscordCity.py".split(' ')
stopfile = "shutdown"

if os.path.isfile(stopfile):
    try:
        _ = subprocess.call(["rm","-f", stopfile])
        print("success - linux \n\n")
    except Exception as e:
        print(e)
        
    
    try:
        _ = subprocess.call(["del", stopfile], shell=True)
        print("success - windows \n\n")
    except Exception as e:
        print(e)
        
        
while 1:
    print("getting latest version")

    callback = subprocess.call(g_command)
    if callback != 0:
        break
    print("\nstarting bot...\n\n")
    try:
        callback = subprocess.call(b_start)
    except Exception as e:
        print(e)
        break
    
    #check if there is a stopfile
    if os.path.isfile(stopfile):
        break
    time.sleep(2)
    
