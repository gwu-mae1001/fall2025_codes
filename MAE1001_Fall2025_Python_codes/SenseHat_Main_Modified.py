#Code Written for MAE1001 


#----------Import and configure SenseHat----------#
from sense_hat import SenseHat
from matplotlib import pyplot as plt
import os.path
import time
import csv

sen = SenseHat()


#Declaring Variables
timeElapsed = 0
tempList = []
pressList = []
humList = []
timeList = []

# =========== DISPLAY ONE ALPHABET ON THE LED MATRIX =========================

sen.show_letter("A", text_colour=[0,0,255])
time.sleep(2)
sen.clear()

# =========== DISPLAY A MESSAGE ON THE LED MATRIX ============================

sen.show_message("Hello MAE1001!!", text_colour=[0,0,255])

# =========== DRAW A PICTURE ON THE LED MATRIX ===============================

R = [255, 0, 0]
B = [0, 0, 255]
W = [0, 0, 0]

pixel_list = [W, W, W, W, W, W, W, W,
              W, R, R, W, W, R, R, W,
              W, R, R, W, W, R, R, W,
              W, W, W, B, B, W, W, W,
              W, R, W, B, B, W, R, W,
              W, R, W, W, W, W, R, W,
              W, W, R, R, R, R, W, W,
              W, W, W, R, R, W, W, W]

sen.set_pixels(pixel_list)
time.sleep(5)
sen.clear()


#Setting how long the Pi will collect data for taken from user input
#This while loop houses a try-except that ensures the value passed through is an int
def userInput():
    global timeLimit
    sen.clear()
    while True:
        
        try:
            timeLimit = int(input('Enter how long would you like the Pi to collect data for (in seconds) '))
        except ValueError:
            print('A valid Integer, please.')
            continue
        if type(timeLimit) == int:
            break
        else:
            print('A valid Integer, please.') 



#Function for conversion from Celsius to Fahrenheit
def ctof(c):
    result = (c*(9/5)) + 32

    return round(result, 1)


#Assign the message
def updateDisplay():
    msg = "Temp = %s F, Pressure = %s mbar, Humidity = %s" % (temp, press, hum)
    sen.show_message(msg, scroll_speed = 0.05) 


    
#Function for the creation of the subplots
# Updated plot function for bar graphs
def plot(timeIn, tempX, pressX, humX):
    
    # Initialize the graph with 3 subplots side by side
    fig, graph = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)
    
    # Create bar graphs for each measurement
    graph[0].plot(timeIn, tempX, color='red', marker='o' ,label='Temperature', linewidth=2.5,markersize=6)
    graph[1].plot(timeIn, pressX, color='blue',marker='o', label='Pressure', linewidth=2.5,markersize=6)
    graph[2].plot(timeIn, humX, color='green',marker='o', label='Humidity', linewidth=2.5,markersize=6)
    
    # Format Temperature graph
    graph[0].set_xlabel('Time (s)', fontsize=12)
    graph[0].set_ylabel('Temperature (F)', fontsize=12)
    graph[0].set_title('Temperature Over Time', fontsize=14, fontweight='bold')
    graph[0].grid(axis='y', alpha=0.3)
    
    # Format Pressure graph
    graph[1].set_xlabel('Time (s)', fontsize=12)
    graph[1].set_ylabel('Pressure (mbar)', fontsize=12)
    graph[1].set_title('Pressure Over Time', fontsize=14, fontweight='bold')
    graph[1].grid(axis='y', alpha=0.3)
    
    # Format Humidity graph
    graph[2].set_xlabel('Time (s)', fontsize=12)
    graph[2].set_ylabel('Humidity (%)', fontsize=12)
    graph[2].set_title('Humidity Over Time', fontsize=14, fontweight='bold')
    graph[2].grid(axis='y', alpha=0.3)
    
    # Message that shows this function is underway
    sen.show_message('Saving Graph', scroll_speed=0.05)
    
    # Save the figure as PNG
    output_filename = filename.replace('.csv', '_graph.png')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Graph saved as {output_filename}")
    
    # Show the graph
    time.sleep(1)
    plt.show()
    
    # Clear the display
    sen.clear()
    
    
#Function to gather environmental data
def gatherData():
    
    #Declare global variables
    global timeElapsed
    global temp
    global hum
    global press
    global start_time
    global last_second
    
    #Open csv file and prepare for writing
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Time Elapsed (s)','Temperature (F)', 'Pressure (mbar)', 'Humidity'])
     
    
        #Message on LED Display
        sen.show_message('Collecting Data', scroll_speed = 0.03)
        #Establishes the start time 
        start_time = time.time()
        #Logs the most recent second passed
        last_second = 0
    
    
        while timeElapsed < timeLimit:
            timeElapsed = time.time()- start_time
            secondsElapsed = int(timeElapsed)
            sen.clear()
            
        
            if last_second != secondsElapsed:    
                #Gather Environment Data   
                temp = sen.get_temperature()
                press = sen.get_pressure()
                hum = sen.get_humidity()
        
                #Round up the values and convert temp to F
                temp = ctof(temp)
                press = round(press, 1)
                hum = round(hum, 1)
    
                #Appending the data into arrays
                tempList.append(temp)
                pressList.append(press)
                humList.append(hum)
                timeList.append(secondsElapsed)
            
                #write data to csv file
                print(csvfile.closed)
                csvwriter.writerow([secondsElapsed, temp, press, hum])
            
                #Print data to the console
                print(tempList)
                print(pressList)
                print(humList)
                print(timeList)
                #Change the display
                sen.clear()
        
        
            last_second = secondsElapsed


def file():
    global csvfile
    global csvwriter
    global filename
    
    i = 0
    if os.path.exists('test0.csv'):
        while os.path.exists('test%s.csv' % i):
            i += 1
            filename = 'test%s.csv' % i
            print(filename)
    else:
        filename = 'test0.csv'

        
    
#|----Main Function----|

userInput()
file()
gatherData()
plot(timeList, tempList, pressList, humList)
updateDisplay()

    
