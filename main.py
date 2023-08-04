import requests
from datetime import date
import os
from time import time
import multiprocessing as mp
import threading
from queue import Queue
import copy
class read(object):
    def __new__(cls, filename: str, delim: str = None, Encoding : str ="ISO-8859-1", Remove: list = ['\r', '\t']) -> open:
        cls.Encoding = Encoding
        cls.Remove = Remove
        if delim != None:
            return cls.fileread(cls, filename).split(delim)
        return cls.fileread(cls, filename)
    def fileread(self, filename: str) -> open:
        with open(filename, "rb") as f:
            var = f.read().decode(self.Encoding)
            if self.Remove:
                for x in self.Remove:
                    var = var.replace(x, "")
        return var

class XMLFEED:
    __AUTHTOKEN = 'C36DE09079464F7085BC4C0122B81887'
    AUTHTOKEN = '?authtoken=' + __AUTHTOKEN
    URL = 'https://xmlfeed.directemployers.org'
    CURSOR = None
    TODAY = date.today()
    MANIFEST = None
    THREADS = []
    def __init__(self: None) -> None:


        self.VerifyStructure()
        
        self.Cleanup()
        #print(self.MANIFEST)
        self.Threader()
    def Cleanup(self):
        NEWMAN = []
        FileList = os.listdir(str(self.TODAY) + "\\DATA")
        
        for x in self.MANIFEST:
            #print(x[1])
            if x[1] in FileList:
                if os.path.getsize(str(self.TODAY) + "\\DATA\\" + x[1]) == 0:
                    #print(x[1])
                    NEWMAN.append(['/feeds/'+x[1], x[1]])
            else:
                NEWMAN.append(['/feeds/'+x[1], x[1]])
        self.MANIFEST = NEWMAN


    def GetList(self: None):
        self.CURSOR = requests.get(self.URL)
        with open("out.html", "wb") as f:
            f.write(self.CURSOR.content)
        print(self.CURSOR.status_code)

        self.__SPLIT__= str(self.CURSOR.content).split('<td><a href="')
        del self.__SPLIT__[0]
        for x in range(len(self.__SPLIT__)):
            self.__SPLIT__[x] = self.__SPLIT__[x].split('</a></td>')[0].replace('"', '').split(">")
        #print(self.__SPLIT__)

    def VerifyStructure(self: None):
        if not os.path.exists(str(self.TODAY)):
            os.mkdir(str(self.TODAY))

        if not os.path.exists(str(self.TODAY) + "\\DATA"):
            os.mkdir(str(self.TODAY) + "\\DATA")
        if not os.path.exists(str(self.TODAY) + "\\MANIFEST.TXT"):
            self.GetList()
            with open(str(self.TODAY) + "\\MANIFEST.TXT", "w") as f:
                for x in self.__SPLIT__:
                    f.write(x[0] + "," + x[1])
                    if x != self.__SPLIT__[-1]:
                            f.write("\n")
            
            self.VerifyStructure()
        else:
            self.MANIFEST = read(str(self.TODAY) + "\\MANIFEST.TXT", "\n")
            for x in range(len(self.MANIFEST)):
                self.MANIFEST[x] = self.MANIFEST[x].split(",")


    def Threader(self):
        self.Q = Queue()
        for x in range(100):
            l = threading.Thread(target=self.downloadMANIFEST)
            #l.daemon = True
            self.THREADS.append(l)

        for x in self.MANIFEST:
            self.Q.put(x)

        for x in self.MANIFEST:
            self.Q.put(None)
        for x in self.THREADS:
            x.start()

        for x in self.THREADS:		
            x.join()
    def downloadMANIFEST(self):

        while True:
            #print("h")
            __TEMP__ = self.Q.get()
            if __TEMP__ == None:
                break
            print(__TEMP__[1])
            with open(str(self.TODAY) + "\\DATA\\" + __TEMP__[1] + "", "wb") as f:
                __QQ = requests.get(self.URL + __TEMP__[0] + self.AUTHTOKEN)
                for chunk in __QQ.iter_content(chunk_size=8192): 
                    f.write(chunk)
            self.Q.task_done()
XMLFEED()
