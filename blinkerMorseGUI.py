from Tkinter import *
from ttk import *
import Tkinter as app
import ttk
import RPi.GPIO as GPIO
import time
import re

TIME_UNIT = 0.250 #s
DOT = TIME_UNIT;
DASH = 3 * TIME_UNIT;
SYMBOL_SPACE = TIME_UNIT;
LETTER_SPACE = 3 * TIME_UNIT - SYMBOL_SPACE;
WORD_SPACE = 7 * TIME_UNIT - LETTER_SPACE;

letters_code=[ 
# A to I
".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..",
# J to R 
".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.",
# S to Z
"...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.." 
]

led  = 22    # pin22

GPIO.setmode(GPIO.BOARD)    # GPIO Numbering of Pins
GPIO.setup(led, GPIO.OUT)   # Set ledPin as output
GPIO.output(led, GPIO.LOW)  # Set ledPin to LOW to turn Off the LED

## GUI Definations ###
win = app.Tk() 
win.title('Morse Code GUI')

submit_button_text = app.StringVar() 
submit_label_Entry_text = app.StringVar() 
submit_button_text.set("Submit")


### WIDGETS #####
def display_code():
  submit_button["state"] = "disabled"
  name = submit_label_Entry_text.get()
  # to lower case
  name = name.lower()
  # check for multiple words
  if name.isalpha()==0:
    print "Contains non characters so returning!!"
    submit_button["state"] = "enabled"
    return
  print "Displaying Morse for " + name + " !!"
  for i in range(len(name)):
    offset = ord(name[i]) - ord('a')
    code = letters_code[offset]
    print name[i]
    for j in range(len(code)):
      #print "{code[j]}"
      GPIO.output(led, GPIO.HIGH)
      #symboltime = DOT
      if code[j] == '-':
        symboltime = DASH
      else:
        symboltime = DOT
      time.sleep(symboltime) 
      GPIO.output(led, GPIO.LOW)
      time.sleep(SYMBOL_SPACE)
    time.sleep(LETTER_SPACE) 
  submit_button["state"] = "enabled"

def close():
    GPIO.cleanup()
    win.destroy()
 
s = ttk.Style() 
s.configure('.', background='grey') 
main_frame = ttk.Frame(win, style='main_frame.TFrame', height=100, width=50, relief='sunken') 
main_frame.pack(fill='x')

hi_label = ttk.Label(main_frame, text='Enter Your Name: ' )
hi_label.grid(row=0, column=0) 
 
user_entry = ttk.Entry(main_frame, textvariable=submit_label_Entry_text) 
user_entry.grid(row=0, column=1)

submit_button = ttk.Button( main_frame, text='Submit Button', style='submit_button.TButton', textvariable=submit_button_text, width=25, command=display_code ) 
submit_button.grid(row=2, columnspan=3, pady=5) 


win.protocol("WM_DELETE_WINDOW", close) ## exit cleanly

win.mainloop() # loop forever
