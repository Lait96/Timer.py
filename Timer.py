from tkinter import *
import pygame

InTimer = True
MusicOneTime = True

file = open('Time.txt', 'r')
TimerTime = int(file.read())
file.close()

pygame.mixer.init()


def play_sound():
    pygame.mixer.music.load("tada.mp3")
    pygame.mixer.music.play()
    TimerCount['foreground'] = '#D5D5D5'
    TimerCount.place(x=35, y=-3)
    TimerCount['text'] = str("ʕ ᵔᴥᵔ ʔ")


def stop():
    global InTimer
    InTimer = False
    TimerCount['foreground'] = '#D5D5D5'
    TimerCount.place(x=17, y=-3)
    TimerCount['text'] = str("¯\_(ツ)_/¯")


def start():
    global InTimer
    global MusicOneTime
    global TimerTime
    InTimer = True
    MusicOneTime = True
    TimerCount['foreground'] = '#D5D5D5'
    TimerCount['text'] = str("")
    TimerCount.place(x=40, y=-3)
    Timer(TimerTime)


def Timer(TimerTime):
    global InTimer
    global MusicOneTime
    if not InTimer:
        return None
    minute = TimerTime // 60
    second = TimerTime % 60
    if second < 10:
        second = '0' + str(second)
    TimerCount['text'] = str('0' + str(minute) + ':' + str(second))
    if TimerTime != 0 and InTimer:
        if 10 < TimerTime <= 30:
            TimerCount['foreground'] = '#FF9218'
        if TimerTime <= 10:
            TimerCount['foreground'] = '#ff3318'
        TimerTime -= 1
        window.after(1000, Timer, TimerTime)
    if TimerTime == 0 and MusicOneTime:
        MusicOneTime = False
        window.after(1000, play_sound)


def drag(event):
    window_class = event.widget.winfo_class()
    if window_class in ("Tk", "Toplevel", "Frame", "Label"):
        x = window.winfo_pointerx() - window.offsetx
        y = window.winfo_pointery() - window.offsety
        window.geometry('+{x}+{y}'.format(x=x,y=y))

def click(event):
    window.offsetx = event.x
    window.offsety = event.y


def setting():
    def TimeForTimer():
        global TimerTime

        TimeM = str(MinuteEntry.get())
        TimeS = str(SecondEntry.get())

        if TimeM.isdigit() or TimeS.isdigit():
            TimerTime = 0
            if TimeM.isdigit():
                TimerTime += int(TimeM) * 60
            if TimeS.isdigit():
                TimerTime += int(TimeS)

            file = open('Time.txt', 'w')
            file.write(str(TimerTime))
            file.close()

    def alphaOff():
        window.attributes('-alpha', 1)

    def alphaOn():
        window.attributes('-alpha', 0.75)


    settingWindow = Toplevel(window)
    settingWindow.geometry('200x100')

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

    AlphaOnButton = Button(settingWindow, text='Включить прозрачность', command=alphaOn)
    AlphaOnButton.grid()

    AlphaOffButton = Button(settingWindow, text='Убрать прозрачность', command=alphaOff)
    AlphaOffButton.grid()


window = Tk()
window.title("Таймер")
window.geometry('150x87')
window['bg'] = "gray22"


TimerCount = Label(font="Colatemta 19")
TimerCount['bg'] = "gray22"

ButtonStart = Button(window, text="Старт", command=start, padx="10", pady="0")
ButtonStart.place(x=7, y=30)
ButtonStart['bg'] = "gray16"

ButtonStop = Button(window, text="Стоп", command=stop, padx="12", pady="0")
ButtonStop.place(x=82, y=30)
ButtonStop['bg'] = "gray16"

ButtonSetting = Button(window, text='Настройки', command=setting)
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
