from controllers.MailController import MailController
import os, json

class CrisisController:
    def get_latest_log(self):
        try:
            files = sorted(
                [f for f in os.listdir(self.logs_path) if f.endswith(".json")]
            )
            if not files:
                return None
            
            latest_file = os.path.join(self.logs_path, files[-1])
            with open(latest_file, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                elif isinstance(data, list) and data:
                    return data[-1]
        except Exception as e:
            print(f"Log writing error : {e}")
            return None

    def __init__(self, logs_path, seuils: dict):
        self.logs_path = logs_path
        self.sondes = self.get_latest_log()
        self.seuils = seuils
    
    def checkseuils(self):
        alerts = {}
        result = {}
        for cle, valeur in self.seuils.items():
            if float(self.sondes[cle]) > float(valeur):
                alerts[cle] = self.sondes[cle]
        
        if len(alerts)!=0:
            subject = f"!! Alert System, Machine {self.sondes['machineName']}"
            content = "Voici les problèmes trouves :\r\n"
            email = "titouan.johanny@alumni.univ-avignon.fr"

            content += str(alerts)
            mc = MailController(subject, content, email)
            mc.send_mail()
            result.update(mc.get_result())
        else:
            result.update({"code": 1})
        
        return result