from time import sleep
from colorama import Fore, Style
import requests
import random
import string
import os

class SapphireGen:
    def __init__(self):
        self.session = requests.Session()
        self.DISCORD_WEBHOOK_URL = self.get_webhook_url()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_webhook_url(self):
        self.clear_screen()
        return input("Bienvenue ! Veuillez entrer l'URL du Webhook Discord: ")

    def send_to_discord_webhook(self, message, mention_everyone=False):
        payload = {
            "content": message,
            "allowed_mentions": {
                "parse": ["everyone"] if mention_everyone else []
            }
        }
        response = requests.post(self.DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            self.cleanup_webhook_messages()

    def cleanup_webhook_messages(self):
        response = requests.get(self.DISCORD_WEBHOOK_URL)
        if response.status_code == 200:
            messages = response.json()
            for message in messages:
                content = message.get("content", "")
                if "https://discord.gift/" in content:
                    content_parts = content.split(" | ")
                    gift_url = content_parts[0]
                    message_id = message.get("id")
                    delete_url = f"{self.DISCORD_WEBHOOK_URL}/messages/{message_id}"
                    requests.delete(delete_url)
                    self.send_to_discord_webhook(gift_url, mention_everyone=True)
                    self.send_to_discord_webhook(message, mention_everyone=False)

    def generate_code(self):
        code_length = 24
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(code_length))

    def check_code_status(self, code):
        try:
            req = self.session.get(
                f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                timeout=10,
            ).status_code
            return req
        except requests.RequestException as e:
            return str(e)

    def display_message(self, message, color=Fore.WHITE, style=Style.NORMAL):
        print(f"{style}{color}{message}{Style.RESET_ALL}")

    def welcome_message(self):
        self.clear_screen()
        self.display_message("""
        GGGGGGGGGGGGG     OOOOOOOOO               JJJJJJJJJJJ     OOOOOOOOO     
     GGG::::::::::::G   OO:::::::::OO             J:::::::::J   OO:::::::::OO   
   GG:::::::::::::::G OO:::::::::::::OO           J:::::::::J OO:::::::::::::OO 
  G:::::GGGGGGGG::::GO:::::::OOO:::::::O          JJ:::::::JJO:::::::OOO:::::::O
 G:::::G       GGGGGGO::::::O   O::::::O            J:::::J  O::::::O   O::::::O
G:::::G              O:::::O     O:::::O            J:::::J  O:::::O     O:::::O
G:::::G              O:::::O     O:::::O            J:::::J  O:::::O     O:::::O
G:::::G    GGGGGGGGGGO:::::O     O:::::O            J:::::j  O:::::O     O:::::O
G:::::G    G::::::::GO:::::O     O:::::O            J:::::J  O:::::O     O:::::O
G:::::G    GGGGG::::GO:::::O     O:::::OJJJJJJJ     J:::::J  O:::::O     O:::::O
G:::::G        G::::GO:::::O     O:::::OJ:::::J     J:::::J  O:::::O     O:::::O
 G:::::G       G::::GO::::::O   O::::::OJ::::::J   J::::::J  O::::::O   O::::::O
  G:::::GGGGGGGG::::GO:::::::OOO:::::::OJ:::::::JJJ:::::::J  O:::::::OOO:::::::O
   GG:::::::::::::::G OO:::::::::::::OO  JJ:::::::::::::JJ    OO:::::::::::::OO 
     GGG::::::GGG:::G   OO:::::::::OO      JJ:::::::::JJ        OO:::::::::OO   
        GGGGGG   GGGG     OOOOOOOOO          JJJJJJJJJ            OOOOOOOOO 
""", Fore.CYAN, Style.BRIGHT)

    def goodbye_message(self):
        self.display_message("Merci d'avoir utilisé le nitro gen de fr41tr42. À bientôt !", Fore.CYAN, Style.BRIGHT)

    def generate(self):
        self.welcome_message()

        self.display_message(f"URL du Webhook configurée : {self.DISCORD_WEBHOOK_URL}", Fore.MAGENTA, Style.BRIGHT)

        while True:
            try:
                code = self.generate_code()
                req = self.check_code_status(code)

                message = f"https://discord.gift/{code}"

                if req == 200:
                    self.display_message(message, Fore.GREEN, Style.BRIGHT)
                    self.send_to_discord_webhook(message, mention_everyone=True)
                elif req == 404:
                    self.display_message(message, Fore.RED, Style.BRIGHT)
                    self.send_to_discord_webhook(message)
                elif req == 429:
                    self.display_message(message, Fore.YELLOW, Style.BRIGHT)
                    self.send_to_discord_webhook(message)
                else:
                    self.display_message(f"Erreur : {message}", Fore.RED, Style.BRIGHT)

            except Exception as e:
                self.display_message(f"Erreur : {e}", Fore.RED, Style.BRIGHT)

if __name__ == "__main__":
    SapphireGen().generate()
