
import datetime, os

class Match():
    def match(text, output=False):
        return 0

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