from sense_hat import SenseHat
from datetime import datetime
import animations
import time

s = SenseHat()
s.set_rotation(270)

#print welcome message
s.show_message("Best Regards from our team: Marios, Paris, Alex, John, Sophia, Kostas",scroll_speed=0.10,text_colour=(255,255,0),back_colour=(255,0,0))
s.show_message("Students of the 12th primary school of Petroupolis, Athens, Greece",scroll_speed=0.10,text_colour=(255,255,0),back_colour=(255,0,0))
s.set_pixels(animations.img1)
time.sleep(6)

#create a file to log data
file = open("log.csv", "w")
file.close()

#open log file to append data
file = open("log.csv", "a")

#start phase 1 of calibration
s.show_message('Starting Calibration, please go out for a moment')
file.write('Start Calibration\n')
print('Start Calibration\n')

#no one is on board
no_crew = True

hum=[]
k=0
#take the first 10 values in a period of 60sec
for i in range(10):
    #show an animation of ticking clock
    s.set_pixels(animations.clock_anim[k])
    k = (k + 1) % 8
    #get the humidity value and append it to a list
    h = s.get_humidity()
    h = round(h,2)
    hum.append(h)
    #write value of humidity and time stamp in the file
    file.write(str(h))
    file.write('\t')
    file.write(str(datetime.now()))
    file.write('\n')
    #the next value for humidity will be on 6 sec
    time.sleep(6)
print(hum)

s.show_message('Calibration ended')
file.write('Calibration ended\n')
print('Calibration ended\n')

#calculate the range of values from the list
range_val = max(hum)-min(hum)
range_val = round(range_val,2)

#show message with range value
s.show_message('Range value is: %s' %range_val)

#calculate the mean value of hum list
mean_val = 0.0
for i in range(10):
    mean_val = mean_val + hum[i]
mean_val = mean_val / 10
mean_val = round(mean_val,2)

#show message with mean value
s.show_message('Mean Value is: %s' %mean_val)

#write results to the file
file.write('Calibration phase results:\n')
file.write('Mean Value: '+str(mean_val)+'\n')
file.write('Range Value: '+str(range_val)+'\n')    
print('Calibration phase results:\n')
print('Mean Value: '+str(mean_val)+'\n')
print('Range Value: '+str(range_val)+'\n')

#start crew detection
file.write('Start Crew Detection:\n')
print('Start Crew Detection:\n')
#format the header for data
print('Humidity\tDateTime\n')
file.close()

while True:
    #show an animation of ticking clock refresh on every logging value
    s.set_pixels(animations.clock_anim[k])
    k = (k + 1) % 8
    #get the current value of humidity
    h = s.get_humidity()
    h = round(h,2)
    file = open("log.csv", "a")
    #write the value of humidity and date-time stamp on the file
    file.write(str(h))
    file.write('\t')
    file.write(str(datetime.now()))
    file.write('\n')
    print(str(h)+'\t'+str(datetime.now())+'\n')
    #Humidity rises 
    if (h > mean_val + range_val):
        #Humidity rises for first time and there was no astronaut before
        if no_crew:
            #found counts the number of time the humidity was greater than typical value
            found = 0
            #an astronaut maybe on the board
            no_crew = False
            file.write('Possible Crew on Deck\n')
            print('Possible Crew on Deck\n')
            s.set_pixels(animations.jai1)
            time.sleep(0.2)
            s.set_pixels(animations.jai2)
            time.sleep(0.2)
            s.set_pixels(animations.jai1)
        else:    
        #Humidity rises and there was an astronaut detection)
        #The astonaut is still on board    
            found+=1
            file.write('The Crew is still on Deck\n')
            print('The Crew is still on Deck\n')
            s.set_pixels(animations.jai1)
            time.sleep(0.2)
            s.set_pixels(animations.jai2)
            time.sleep(0.2)
            s.set_pixels(animations.jai1)
    else:
        #Humidity has fallen
        if no_crew == False:
            if (found < 2):
            #Humidity has fallen after at least 2 measures so it was a false alarm
            #No astonaut was on board    
                no_crew = True
                print('Wrong Guess. No Crew on Deck\n')                  
        #Humidity has fallen, the Crew has left the Deck
            else:
                no_crew = True
                file.write('The Crew has left. No Crew on Deck\n')
                print('The Crew has left. No Crew on Deck\n')  
    
    file.close()
    time.sleep(3)    

file.close()

