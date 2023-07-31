import requests
from datetime import date
import os
class XMLFEED:
    __AUTHTOKEN = 'C36DE09079464F7085BC4C0122B81887'
    AUTHTOKEN = '?authtoken=' + __AUTHTOKEN
    URL = 'https://xmlfeed.directemployers.org/'
    CURSOR = None
    TODAY = date.today()

    def __init__(self: None) -> None:
        self.GetList()
        self.VerifyStructure()



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
        with open(str(self.TODAY) + "\\MANIFEST.TXT", "w") as f:
            for x in self.__SPLIT__:
                f.write(x[0] + "," + x[1])
                if x != self.__SPLIT__[-1]:
                        f.write("\n")

XMLFEED()
