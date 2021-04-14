import os
import json
import requests
import math

cmdr = "YOURCMDRNAMEHERE"
path = r'C:\Users\YOURUSERNAMEHERE\Saved Games\Frontier Developments\Elite Dangerous'

url = "https://www.edsm.net/api-v1/system?&showPrimaryStar=0&showCoordinates=1&systemName="
bodurl = "https://www.edsm.net/api-system-v1/bodies?systemName="
files = os.listdir(path)
files.sort()
systemname = ""
csv = open(path + "\elws.csv", "a")

for f in files:
    if f[-3:] == 'log' and f[:7] == 'Journal':
        l = open(path + "\\" + f, "r", encoding="utf8")
        journal = l.readlines()
        entrycount= 0
        dupechecker = [""]
        for entry in journal:
            entryj = json.loads(entry)
            if entryj["event"] == "FSDJump":
                population = entryj["Population"]
                systemname = entryj["StarSystem"]
            if "PlanetClass" in entryj:
                if entryj["PlanetClass"] == "Earthlike body" and population == 0:
                    bodyname = entryj["BodyName"].replace(systemname + " ", "")
                    if bodyname not in dupechecker:
                        dupechecker[entrycount]=bodyname
                        response = requests.request("GET", url + systemname)
                        responsej = json.loads(response.text)
                        x=responsej["coords"]["x"]
                        y=responsej["coords"]["y"]
                        z=responsej["coords"]["z"]
                        dts = int(math.sqrt(x ** 2 + y ** 2 + z ** 2))

                        response = requests.request("GET", bodurl + systemname)
                        responsej = json.loads(response.text)
                        edsmurl=responsej["url"]

                        count=0
                        systemStar="\""
                        for x in responsej["bodies"]:
                            if x["type"] == "Star":
                                if count > 0:
                                    systemStar = systemStar + ","
                                if x["spectralClass"] is not None:
                                    systemStar = systemStar + x["spectralClass"] + " " + x["luminosity"]
                                else:
                                    systemStar = systemStar + x["subType"]
                                count += 1
                        systemStar = systemStar + "\""
                        print(systemname + ',' + bodyname + ',' + str(dts) + ',' + cmdr + ',' + systemStar + ',' + edsmurl + ',' + f)
                        csv.write(systemname + ',' + bodyname + ',' + str(dts) + ',' + cmdr + ',' + systemStar + ',' + edsmurl + ',' + f + '\n')


csv.close()
