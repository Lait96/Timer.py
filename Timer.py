from tkinter import *
from functools import partial
import pygame


SettingList = []
file = open('Time.txt', 'r')
for line in file:
    SettingList.append(int(line))
file.close()
for _ in range(2):
    SettingList.append(True)
pygame.mixer.init()


def finish(SettingList):
    TimerCount['foreground'] = '#D5D5D5'
    TimerCount.place(x=35, y=-3)
    TimerCount['text'] = str("ʕ ᵔᴥᵔ ʔ")
    play_sound(SettingList)

def play_sound(SettingList):
    if SettingList[1] == 100:
        VolumeLevelInDef = 1
    else:
        VolumeLevelInDef = float(str("0" + "." + str(SettingList[1])))
    pygame.mixer.music.set_volume(VolumeLevelInDef)
    pygame.mixer.music.load("tada.mp3")
    pygame.mixer.music.play()

def stop(SettingList):
    SettingList[2] = False
    TimerCount['foreground'] = '#D5D5D5'
    TimerCount.place(x=17, y=-3)
    TimerCount['text'] = str("¯\_(ツ)_/¯")
stopDef = partial(stop, SettingList)

def start(SettingList):
    SettingList[2] = True
    SettingList[3] = True
    TimerCount['foreground'] = '#D5D5D5'
    TimerCount['text'] = str("")
    TimerCount.place(x=40, y=-3)
    Timer(SettingList[0], SettingList)
StartDef = partial(start, SettingList)

def Timer(TimerCounter, SettingList=SettingList):
    if not SettingList[2]:
        return None
    minute = TimerCounter // 60
    second = TimerCounter % 60
    if second < 10:
        second = '0' + str(second)
    TimerCount['text'] = str('0' + str(minute) + ':' + str(second))
    if TimerCounter != 0 and SettingList[2]:
        if 10 < TimerCounter <= 30:
            TimerCount['foreground'] = '#FF9218'
        if TimerCounter <= 10:
            TimerCount['foreground'] = '#ff3318'
        TimerCounter -= 1
        window.after(1000, Timer, TimerCounter)
    if TimerCounter == 0 and SettingList[3]:
        SettingList[3] = False
        window.after(1000, finish, SettingList)


def drag(event):
    window_class = event.widget.winfo_class()
    if window_class in ("Tk", "Toplevel", "Frame", "Label"):
        x = window.winfo_pointerx() - window.offsetx
        y = window.winfo_pointery() - window.offsety
        window.geometry('+{x}+{y}'.format(x=x,y=y))

def click(event):
    window.offsetx = event.x
    window.offsety = event.y


def setting(SettingList):
    def TimeForTimer(SettingList=SettingList):
        TimeM = str(MinuteEntry.get())
        TimeS = str(SecondEntry.get())

        if TimeM.isdigit() or TimeS.isdigit():
            SettingList[0] = 0
            if TimeM.isdigit():
                SettingList[0] += int(TimeM) * 60
            if TimeS.isdigit():
                SettingList[0] += int(TimeS)

    def TransparencyOff():
        window.attributes('-alpha', 1)

    def TransparencyOn():
        window.attributes('-alpha', 0.75)

    def get_val_motion(event, SettingList=SettingList):
        SettingList[1] = VolumeLevelScale.get()

    def on_closing(settingDef):
        file = open('Time.txt', 'w')
        file.write(str(SettingList[0]) + '\n' + str(SettingList[1]) + '\n')
        file.close()
        settingWindow.destroy()
    on_closingDef = partial(on_closing, settingDef)

    settingWindow = Toplevel(window)
    settingWindow.geometry('200x100')

    ForVolumeLevelLabel = Label(settingWindow, font="Colatemta 8")
    ForVolumeLevelLabel.grid()
    ForVolumeLevelLabel['text'] = 'Громкость звука'

    VolumeLevelScale = Scale(settingWindow, orient=HORIZONTAL, length=100, from_=0, to=100,
                             tickinterval=50, resolution=1)
    VolumeLevelScale.bind("<B1-Motion>", get_val_motion)
    VolumeLevelScale.grid()
    VolumeLevelScale.set(SettingList[1])

    MinuteLabel = Label(settingWindow, font="Colatemta 8")
    MinuteLabel.grid()
    MinuteLabel['text'] = 'Введите минуты:'

    MinuteEntry = Entry(settingWindow, width=5)
    MinuteEntry.grid()

    SecondLabel = Label(settingWindow, font="Colatemta 8")
    SecondLabel.grid()
    SecondLabel['text'] = 'Введите секунды:'

    SecondEntry = Entry(settingWindow, width=5)
    SecondEntry.grid()

    TimeButton = Button(settingWindow, text='Обновить время', command=TimeForTimer)
    TimeButton.grid()

    TransparencyOnButton = Button(settingWindow, text='Включить прозрачность', command=TransparencyOn)
    TransparencyOnButton.grid()

    TransparencyOffButton = Button(settingWindow, text='Убрать прозрачность', command=TransparencyOff)
    TransparencyOffButton.grid()

    settingWindow.protocol("WM_DELETE_WINDOW", on_closingDef)
settingDef = partial(setting, SettingList)

window = Tk()
window.title("Таймер")
window.geometry('150x87')
window['bg'] = "gray22"

TimerCount = Label(font="Colatemta 19")
TimerCount['bg'] = "gray22"

ButtonStart = Button(window, text="Старт", command=StartDef, padx="10", pady="0")
ButtonStart.place(x=7, y=30)
ButtonStart['bg'] = "gray16"

ButtonStop = Button(window, text="Стоп", command=stopDef, padx="12", pady="0")
ButtonStop.place(x=82, y=30)
ButtonStop['bg'] = "gray16"

ButtonSetting = Button(window, text='Настройки', command=settingDef)
ButtonSetting.place(x=38.5, y=57.5)
ButtonSetting['bg'] = "gray16"

ButtonClose = Button(window, text='X', command=window.destroy)
ButtonClose.place(x=136, y=0, height=13, width=13)
ButtonClose['bg'] = "gray16"
ButtonClose['foreground'] = '#ff3318'


window.bind('<Button-1>', click)
window.bind('<B1-Motion>', drag)
window.overrideredirect(1)
window.wm_attributes("-transparentcolor", "white")
window.attributes('-alpha', 0.75)
window.call('wm', 'attributes', '.', '-topmost', '1')
window.mainloop()
