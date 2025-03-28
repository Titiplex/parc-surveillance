#!/usr/bin/env python3
import datetime
from controllers.SondeControl import SondeControl
from controllers.JsonController import JsonController
from controllers.ParserController import ParserController

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
        print("No new cert alert")

def main():
    # timestamp
    now = datetime.datetime.now().isoformat()
    
    manage_sondes(now)
    manage_cert(now)

if __name__ == "__main__":
    main()