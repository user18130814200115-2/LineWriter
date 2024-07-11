#!/usr/bin/python3

import readchar
from readchar import key
import datetime
from threading import Thread
import sys


#################################################################

import i2c_lcd

lcd = i2c_lcd.lcd()

lcd.lcd_display_string("Opening New File", 1) 

def display(string):
    offset = int(str(len(string)/15)[0]) # This beaks when we have a line with over 150 characters
    
    if offset > 0:
        offset-= 1

    formatted = string[offset*15:]

    formatted_top = formatted[:16] + ' ' * ( 16 - len(formatted[:16]))
    formatted_bottom = formatted[16:] + ' ' * ( 16 - len(formatted[16:])) 

    lcd.lcd_display_string(formatted_top, 1) 
    lcd.lcd_display_string(formatted_bottom, 2) 

#################################################################

working_string = ''
file_name = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S.txt")
file_data = []
exit_indicator = False

def main():
	global working_string
	global exit_indicator

	Thread(target=update_display).start()

	while not exit_indicator:
		k = readchar.readkey()

		if (k == key.BACKSPACE):
			working_string = working_string[:-1]
		elif (k == key.ENTER):
			string_to_stack(working_string)
			working_string = ''
		else:	
			working_string += k
		

def string_to_stack(string):
	global exit_indicator
	
	if string == "EXIT":
		exit_indicator=True
	else:
		with open(file_name, 'a') as file:
			file.write(string + '\n')
		file.close()

def update_display():
	global working_string
	global exit_indicator
    
	while not exit_indicator:
		display(working_string)

if __name__ == "__main__":
	main()
