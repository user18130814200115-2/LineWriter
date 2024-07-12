#!/usr/bin/python3

import readchar
from readchar import key
import datetime
from threading import Thread
import sys

#################################################################
# Display Manager
# This section can easily be replaced for different displays
#################################################################

# Initialize the display
import i2c_lcd
lcd = i2c_lcd.lcd()
lcd.lcd_display_string("Opening New File", 1) 

def display(string):
	# Since the display is 16 characters long,
	# we will want to display the current string in blocks of 16 characters.
	# Here we calculate which block we are on.
    offset = int(len(string)/15))
    if offset > 0:
        offset -= 1

	# We then extract the last two blocks from the working string
    formatted = string[offset*15:]

	# And format them into two lines (with spaces making up the remainder)
    formatted_top = formatted[:16] + ' ' * ( 16 - len(formatted[:16]))
    formatted_bottom = formatted[16:] + ' ' * ( 16 - len(formatted[16:])) 

	# These lines are then written to the display
    lcd.lcd_display_string(formatted_top, 1) 
    lcd.lcd_display_string(formatted_bottom, 2) 

#################################################################
# Text Manager
#################################################################

# Set the file name to the current date and time
file_name = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S.txt")
working_string = ''
file_data = []
exit_indicator = False

def main():
	global working_string
	global exit_indicator

	# Start updating the display on a separate thread
	Thread(target=update_display).start()

	while not exit_indicator:
		# Wait for a key to be pressed and save its value into memory
		k = readchar.readkey()

		# If we press backspace, remove the last character of the string
		if (k == key.BACKSPACE):
			working_string = working_string[:-1]
		# If we press enter, send the current string off for processing
		elif (k == key.ENTER):
			string_to_stack(working_string)
			working_string = ''
		# IF it is any other key, append it to the working string
		else:	
			working_string += k
		

# String processing
def string_to_stack(string):
	global exit_indicator
	
	# IF we type 'EXIT' on a blank line, quit the program.
	# This is done with a variable so that both threads quit gracefully
	if string == "EXIT":
		exit_indicator=True
	# If the string is anything else, just append it to the file
	else:
		with open(file_name, 'a') as file:
			file.write(string + '\n')
		file.close()

def update_display():
	global working_string
	global exit_indicator
    
	# This is the loop which updates the display
	while not exit_indicator:
		display(working_string)

if __name__ == "__main__":
	main()
