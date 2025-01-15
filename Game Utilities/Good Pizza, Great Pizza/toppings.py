import pyautogui; pyautogui.PAUSE = 0.01
import keyboard

points = [
    (1855, 1165),
    (1864, 1018),
    (1993, 1088),
    (1934, 1289),
    (2066, 1214),
    (2064, 1358),
    (1854, 1405),
    (1988, 1481),
    (1861, 1559),
    (1708, 1567),
    (1720, 1405),
    (1589, 1488),
    (1517, 1364),
    (1657, 1281),
    (1522, 1213),
    (1721, 1174),
    (1600, 1085),
    (1724, 1010),
    (1719, 1012)
]

def place_toppings(_):
    for x, y in points:
        pyautogui.click(x, y)
keyboard.on_press_key("t", place_toppings)

keyboard.wait()