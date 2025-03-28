#!/usr/bin/env python3
import datetime
from controllers.SondeControl import SondeControl
from controllers.JsonController import JsonController
from controllers.ParserController import ParserController

def main():
    # timestamp
    now = datetime.datetime.now().isoformat()
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    year = datetime.datetime.now().strftime("%Y")
    # init des controllers
    sc = SondeControl()
    jcl = JsonController("/home/titiplex/ams/logs/sondesLogs", day)
    jcc = JsonController("/home/titiplex/ams/logs/certLogs", year)
    parser = ParserController()
    # collecte
    print("1")
    sysInfo = sc.collectSysInfo(now)
    certInfo = parser.getLastAlert(now)
    print("2")
    # clean des logs
    jcl.clean(now, 7)
    jcc.clean(now, 365)
    print("3")
    # json
    jcl.printLogs(day + ".json", sysInfo)
    if not jcc.exists("title", certInfo["title"]):
        jcc.printLogs(year + ".json", certInfo)
        jcc.print("### New Cert Alert ###")
    # terminal
    print("\n")
    sc.printTerminal()
    jcl.printTerminal("### JsonControl ###")

if __name__ == "__main__":
    main()
