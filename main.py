#!/usr/bin/env python3
import datetime
from controllers.SondeControl import SondeControl
from controllers.JsonController import JsonController
from controllers.ParserController import ParserController
from controllers.CrisisController import CrisisController
from controllers.GraphController import GraphController

def manage_sondes(now):
    # var needed
    day = datetime.datetime.now().strftime("%Y-%m-%d")

    # controllers
    sc = SondeControl()
    jcl = JsonController("/home/titiplex/ams/logs/sondesLogs", day)
    jcl.clean(now, 7)

    # harvest
    sysInfo = sc.collectSysInfo(now)

    # logs (json)
    jcl.printLogs(day + ".json", sysInfo)

    # logs (cron)
    print("\n")
    sc.printTerminal()
    jcl.printTerminal("### JsonControl ###")

    return sysInfo

def manage_cert(now):
    # var needed
    year = datetime.datetime.now().strftime("%Y")
    
    # controllers
    jcc = JsonController("/home/titiplex/ams/logs/certLogs", year)
    parser = ParserController()
    jcc.clean(now, 365)

    # collecte
    certInfo = parser.getLastAlert(now)

    if not jcc.exists("title", certInfo["title"]):

        # logs (json)
        jcc.printLogs(year + ".json", certInfo)

        # logs (cron)
        jcc.print("### New Cert Alert ###")
    else:
        print("### No new cert alert### ")

def manage_crisis(now):
    seuils = {}
    seuils["cpuPercent"] = 75
    seuils["diskUsagePercent"] = 85
    seuils["memoryPercent"] = 85
    seuils["processCount"] = 200

    cc = CrisisController("/home/titiplex/ams/logs/sondesLogs", seuils)
    result = cc.checkseuils()

    jci = JsonController("/home/titiplex/ams/logs/crisisLogs", now)
    jci.clean(now, 7)
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    jci.printLogs(day + ".json", result)
    jci.printTerminal("### Crisis Info ###")

def main():
    # timestamp
    now = datetime.datetime.now().isoformat()
    
    manage_sondes(now)
    manage_cert(now)
    print("1")
    manage_crisis(now)
    print("2")

    sonde_name = "cpuPercent"
    output_path = f"/home/titiplex/ams/logs/graphs/{now}.svg"
    gc = GraphController(sonde_name)
    gc.generate_svg_graph(output_path)

if __name__ == "__main__":
    main()