#!/usr/bin/env python3

import sys

def printPythonVer():
    print("Python version")
    print (sys.version)

def checkPythonMinVer(major,minor):
    if (sys.version_info[0] <  major):
        print ("Found python ver " , sys.version_info[0], " with a minor version ", sys.version_info[1])
        raise Exception("Must be using Python ", major,".",minor)
    elif (sys.version_info[0] >= major and sys.version_info[1] < minor):
        print ("Found python ver " , sys.version_info[0], " with a minor version ", sys.version_info[1])
        raise Exception("Must be using Python ", major,".",minor)
