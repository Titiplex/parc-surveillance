import subprocess

class MailController:
    def __init__(self, suject, content, destination):
        self.subject = suject
        self.content = content
        self.destination = destination
        self.origin = "titouan.johanny@alumni.univ-avignon.fr"
        self.resultat = ""
    
    def send_mail(self):
        commande = f"source /home/titiplex/ams/controllers/modules/mail.sh && send_mail '{self.content}' '{self.subject}' '{self.origin}' '{self.destination}'"
        self.resultat = subprocess.run(["bash", "-c", commande], capture_output=True, text=True)
    
    def get_result(self):
        return {"output": self.resultat.stdout, "error": self.resultat.stderr}