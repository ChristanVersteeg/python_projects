import pyautogui
import time

schools = [
    "Acht dagen rotzomer",
    "Das Droog en de zaak van Zusje Pinguïn",
    "De boom die alles zag",
    "De meedogenloze detectives",
    "De Super Squishy Club - De Squishy’s nemen het over!",
    "De twee levens van Kaia",
    "Durf",
    "Er was eens een beer",
    "Gewoon Keet",
    "Gieren met de pinguïns",
    "Kampioen in je hoofd",
    "Konijntjes op het kerkhof",
    "Lisa en de ontsnapte letters",
    "Wat de blaadjes vertellen",
    "Willem Zoetelief, koning van Aloeka"
]

time.sleep(3)

for name in schools:
    pyautogui.write(name)
    
    for _ in range(3):
        pyautogui.press('tab')