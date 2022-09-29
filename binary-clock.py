"""scripte """
from sense_hat import SenseHat
from datetime import datetime
import time
import signal
import sys
import re

sense = SenseHat()

sense.show_message("programmet starter")


def signal_term_handler(signal, frame):
    """håndter når program slutter at vise en besked"""
    sense.show_message("Programmet slutter")
    sys.exit(0)

sense = SenseHat()

#colors
hour_color = (0, 255, 0)
minute_color = (0, 0, 255)
second_color = (255, 0, 0)
timeformat12_color = (255,255,255)
timeformat24_color = (252, 3, 235)
pm_color = (252, 165, 3)
am_color = (252, 252, 3)
off_color = (0, 0, 0)

#ur format
timeformat12 = False
directionhorizontal = True

stop = False
start = True

sense.clear()

def display_binary(value, row, color):
    """laver value om til binary og siger hvor det skal være samt hvad farve den her"""
    global directionhorizontal
    if directionhorizontal:
        binary_str = "{0:8b}".format(value)
        for x in range(0, 8):
            if binary_str[x] == '1':
                sense.set_pixel(x, row, color)
            else:
                sense.set_pixel(x, row, off_color)
    else:
        arr = [int(a) for a in str(value)]
        if len(arr)>1:
            binary_str = "{0:4b}".format(arr[1])
            for y in range(0,4):
                if binary_str[y] == '1':
                    sense.set_pixel(row+1, y, color)
                else:
                    sense.set_pixel(row+1, y, off_color)
        binary_str = "{0:4b}".format(arr[0])
        for x in range(0, 4):
            if binary_str[x] == '1':
                sense.set_pixel(row, x, color)
            else:
                sense.set_pixel(row, x, off_color)

    
def pushed_up(event):
    """I denne event handler sætte ur til at være i 12 timer format """
    global timeformat12
    if event.action == "released":
        sense.clear()
        timeformat12 = True
        sense.set_pixel(0, 0, timeformat12_color)

def pushed_down(event):
    """I denne event handler sætte ur til at være i 24 timer format """
    global timeformat12
    if event.action == "released":
        sense.clear()
        timeformat12 = False
        sense.set_pixel(0, 0, timeformat24_color)

def pushed_left(event):
    """I denne event handler sætte ur til at være i vandret format """
    global directionhorizontal
    if event.action == "released":
        sense.clear()
        directionhorizontal = False

def pushed_right(event):
    """I denne event handler sætte ur til at være i lodret format """
    global directionhorizontal
    if event.action == "released":
        sense.clear()
        directionhorizontal = True

def pushed_middle(event):
    global stop
    if event.action == "released":
        sense.clear()
        stop = True
        

def startup():
    """Har se vi om der er give noget parametre igemmen kommando line og sætte uret op til hvad bruger vil har"""
    global start
    global timeformat12
    global directionhorizontal
    #slice argv list for vi vil ikke har fat i filens navn da vi ikke skal bruge den til noget
    argvlist = sys.argv[1::]
    for i in argvlist:
        #if (bool(re.search('12',i))):
        if i == "12":
            timeformat12 = True
        elif i.lower() == "v" or i.lower() == "vertical":
            directionhorizontal = False
    start = False
#hårdter når program slutter 
signal.signal(signal.SIGTERM, signal_term_handler)
signal.signal(signal.SIGINT, signal_term_handler)

#Har sætter vi op til at håndter mini-joysticket
sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_right = pushed_right
sense.stick.direction_left = pushed_left
sense.stick.direction_middle = pushed_middle

def main():
    """Har køre hele program ind for while loop"""
    global start
    global stop
    global timeformat12
    while True:
        if start:
            startup()
        if stop:
            sense.show_message("Programmet slutter")
            sys.exit(0)
        #tid = datetime(year=1999,month=5,day=4,hour=19,minute=30,second=55,microsecond=0)
        tid = datetime.now()
        if timeformat12 == True:
            # har ser vi om det er am eller pm og sætte den color som passer med tidspukket 
            AM_or_PM = tid.strftime("%I:%M:%S:%P")
            AM_or_PM = AM_or_PM.split(":")[3]
            if AM_or_PM == "pm":
                sense.set_pixel(0,7,pm_color)
            else:
                sense.set_pixel(0,7,am_color)

            #lave tid om til 12 timer format
            tid = tid.strftime("%I:%M:%S")
            tid = datetime.strptime(tid, "%H:%M:%S")

        display_binary(tid.hour, 2, hour_color)
        display_binary(tid.minute, 4, minute_color)
        display_binary(tid.second, 6, second_color)

        time.sleep(1)


if __name__ == "__main__":
    main()
