#import

import MySQLdb
import RPi.GPIO as GPIO
import time
 
#Define Pulse Input pin
pulseIn = 2
pulseOut = 4

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

db = MySQLdb.connect(host="localhost", user="root", passwd="password123", db="meter")
cur = db.cursor()


def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  GPIO.setup(pulseIn, GPIO.IN) #pulseIn as input
  GPIO.setup(pulseOut, GPIO.OUT) 
  GPIO.output(pulseOut,GPIO.HIGH)
  time.sleep(1)
  # Initialise display
  lcd_init()
  count = 0
  lcd_string("Smart Energy Meter", LCD_LINE_1)
  lcd_string("Calculating", LCD_LINE_2)
  db = MySQLdb.connect(host="localhost", user="root", passwd="password123", db="meter")
  cur = db.cursor()
  cur.execute("SELECT balance_amount,energy_remaining FROM meter.user_info")

# loop to iterate
  for row in cur.fetchall() :
       #data from rows
       amount = str(row[0])
       energy = str(row[1])

       #print it
       lcd_string("Balance =" +str(amount), LCD_LINE_1)
       lcd_string("Energy =" +str(energy), LCD_LINE_2)
       print "BALANCE AMOUNT ="+amount
       print "Energy Remaining ="+energy

       #db.commit()

  update_database = """UPDATE meter.user_info SET balance_amount = %d, energy_remaining = %d WHERE user_id = 1;""",(amount,energy)

  while True:
 
       # Send some test
       check_amount = int(amount)
       
       if ((GPIO.input(pulseIn) == True) and (check_amount > 0)):
        	
		GPIO.output(pulseOut,GPIO.HIGH)
		count = count + 1
                print count%3
                
		time.sleep(0.054)
                if (count%3==0):
                  
                    temp_amount = int(amount)
                    temp_energy = int(energy)
                    temp_amount = temp_amount - 1
                    temp_energy = temp_energy - 1
                    amount = str(temp_amount)
                    energy = str(temp_energy)
                    lcd_string("Balance =" + str(amount), LCD_LINE_1)
	            lcd_string("Energy =" + str(energy),LCD_LINE_2)
                    cur.execute("UPDATE meter.user_info SET balance_amount = balance_amount+1, energy_remaining = energy_remaining+1 WHERE user_id = 1;")
                    db.commit()
		   
		    if(temp_amount==0):
			GPIO.output(pulseOut,GPIO.LOW)
	            #time.sleep(0.054)

       elif ((GPIO.input(pulseIn) == False) and (check_amount > 0)):
		    GPIO.output(pulseOut,GPIO.HIGH)
		    time.sleep(0.001)

       elif ((GPIO.input(pulseIn) == True) and (check_amount == 0)):
		    print "ZERO BALANCE"
		    GPIO.output(pulseOut,GPIO.LOW)
		    time.sleep(0.001)
		    db.close()
		    time.sleep(0.001)
		    cur.execute("SELECT balance_amount,energy_remaining from meter.user_info where user_id=1;")
		    time.sleep(0.001)
		    # loop to iterate
  		    for row in cur.fetchall() :
       			#data from rows
       			new_amount = str(row[0])
       			new_energy = str(row[1])
		    check_amount = int(new_amount)
		    time.sleep(0.054)
 
       elif ((GPIO.input(pulseIn) == False) and (check_amount == 0)) :
		    print "Checking Balance"
	   	    db = MySQLdb.connect(host="localhost", user="root", passwd="password123", db="meter")
		    cur = db.cursor()		  
		    cur.execute("SELECT balance_amount,energy_remaining FROM meter.user_info;")
		    time.sleep(0.001);
		    # loop to iterate
		    for row in cur.fetchall() :
       			#data from rows
       			nw_amount = str(row[0])
       			nw_energy = str(row[1])
		    db.close()
       		    #print it
       		    lcd_string("Balance =" +str(amount), LCD_LINE_1)
       		    lcd_string("Energy =" +str(energy), LCD_LINE_2)
                    print "BALANCE AMOUNT ="+nw_amount
       		    print "Energy Remaining ="+nw_energy
                    check_amount = int(nw_amount)
		    print nw_amount
		    print nw_energy
		    if(check_amount == 0) :
			GPIO.output(pulseOut,GPIO.LOW)
			print "Please recharge"
		    else :
			GPIO.output(pulseOut,GPIO.HIGH)
			time.sleep(0.054)
                    time.sleep(0.054)	
       else : 
	#	    GPIO.output(pulseOut,GPIO.LOW)
#		    print "ZERO"
		    cur.execute("SELECT balance_amount,energy_remaining FROM meter.user_info;")

		    # loop to iterate
	            for row in cur.fetchall() :
                    #data from rows
                    	amount = str(row[0])
                        energy = str(row[1])

                    #print it
       		    lcd_string("Balance =" +str(amount), LCD_LINE_1)
       		    lcd_string("Energy =" +str(energy), LCD_LINE_2)
       		   # print "BALANCE AMOUNT ="+amount
       		   # print "Energy Remaining ="+energy
		    check_amount = int(amount)
		    if(check_amount == 0) :
                                GPIO.output(pulseOut,GPIO.LOW)
                                print "Please recharge"
                    else :
                                GPIO.output(pulseOut,GPIO.HIGH)
		    time.sleep(0.001)


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
    # close the cursor
    cur.close()

    # close the connection
    db.close ()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    GPIO.output(pulseOut,GPIO.LOW)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
