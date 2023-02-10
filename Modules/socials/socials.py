
import datetime, os
from Modules.functions.functions import *

class Match():
    def match(text, output=False):
        out = Texts.best(f"{os.getcwd()}/Modules/socials/data/vocabulary.ini", text)
        if output: return eval(out[1])
        else: return out[0]

class Data():
    def update(timer):
        pass

class Socials():
    def ahoj(text):
        time = int(datetime.datetime.now().strftime('%H%M'))
        if time < 1000: return "Dobré ráno pane"
        elif time >= 1000 and time <= 1800: return "Dobrý den pane"
        elif time > 1800: return "Dobrý večer pane"
        else: return f"Time error ({time})"

class Bus():
    pass