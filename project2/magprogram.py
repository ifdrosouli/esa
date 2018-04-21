from sense_hat import SenseHat
from datetime import datetime
import space_craft
import time

s = SenseHat()
s.set_rotation(270)

file = open("maglog.csv", "w")
file.close()

file = open("maglog.csv", "a")

#Start studying the magnetic field
s.show_message('Start studying the magnetic field')
file.write('Start studying the magnetic field\n')
print('Start studying the magnetic field\n')



#number of circles set to zero 
count_circles = 0

#number of times we found the same value on z-axis of magnetic field 
found = 0

#Get a start value of magnetic field 
file.write('Start value of a magnetic field in z-axis:\n')

raw = s.get_compass_raw()
start_mag_z = int(raw['z'])
#avoid a value of zero
while start_mag_z == 0:
    raw = s.get_compass_raw()
    start_mag_z = int(raw['z'])

#get the time that the circle starts 
start_time = time.time()
#write the start value in a file with date time stamp 
file.write(str(start_mag_z))
file.write('\t')
file.write(str(datetime.now()))
file.write('\n')

print(start_mag_z)
s.show_message('Start value of mag_z: %s' %start_mag_z,scroll_speed=0.10,text_colour=(255,255,0),back_colour=(255,0,0))
file.write('Magnetic Field\n')
file.write('X-Axis\tY-Axis\tZ-Axis\tDateTime\n')
file.close()
k=0
while True:
    #Get the values of magnetic field every 10min
    raw = s.get_compass_raw()
    mag_x = round(raw['x'],2)
    mag_y = round(raw['y'],2)
    mag_z = round(raw['z'],2)
    print(mag_x,mag_y,mag_z)
    #append them to the file with date time stamp 
    file = open("maglog.csv", "a")
    file.write(str(mag_x))
    file.write('\t')
    file.write(str(mag_y))
    file.write('\t')
    file.write(str(mag_z))
    file.write('\t')
    file.write(str(datetime.now()))
    file.write('\n')
    #show a clock that is ticking as the time passes 
    s.set_pixels(space_craft.clock_anim[k])
    k = (k + 1) % 8
    #take aproximate value of z-axis of the magnetic field 
    if start_mag_z == int(mag_z):
        #if this is not the first time you found the same value a circle was made 
        if found > 0:
            #The time now that a circle was completed 
            stop_time = time.time()
            #Time interval is the time of the last circle
            time_interval = int((stop_time - start_time) / 60)
            found = 0
            #One more circle was completed 
            count_circles = count_circles + 1
            print("You have made "+ str(count_circles)+' circles around the earth')
            s.show_message("You have made %s circles" %count_circles,scroll_speed=0.10,text_colour=(255,255,0),back_colour=(255,0,0))
            file.write('You have made '+str(count_circles)+' circles around the earth\n')
            print("Time of the last circle was: "+str(time_interval)+' min')
            s.show_message("Time of the last circle was: %s min" %time_interval,scroll_speed=0.10,text_colour=(255,255,0),back_colour=(255,0,0))
            file.write('Time of the last circle was: '+str(time_interval)+' min\n')
            #Show a space craft each time a circle completes 
            s.set_pixels(space_craft.craft)
            time.sleep(3)
        else:
            #if this is the first time you found the same value ISS is in a dimetrically opposed point 
            found = found + 1
    file.close()
    
    time.sleep(10)    

file.close()

