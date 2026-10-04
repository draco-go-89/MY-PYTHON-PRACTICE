import time
import subprocess

seconds = int(input("\n Enter Seconds: "))

while seconds > 0:
    print("Second", seconds)
    time.sleep(1)
    seconds -= 1

print("\n - [ Your Time is Over] \n")

subprocess.run([
    "Powershell",
    "-Command",
    "Add-Type -AssemblyName System.Speech;"
    "$S = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
    "$S.Speak('Your time is over ! your time is over ! Get Out ! your time is over! your time is over!')"
])