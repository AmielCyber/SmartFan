# Automated Fan

## Quick Summary
A program that turns any normal fan into a smart fan which automatically turns on/off based on the 
temperature of the current environment. 

## Pictures

## Set Up
### Hardware Requirements
![HardwarePicture](/images/hardware.png)

* Raspberry Pi 
* DHT11/DHT22 Temperature Sensor
    * Note, you must have the DHT output pin in PIN 4 in the Raspberry Pi board

![raspberrypiWithTemp](/images/raspbSetup.png)
* TP-Link Smart Plug that is compatible with [python-kasa](https://github.com/python-kasa/python-kasa#supported-devices)
    * If you use a TP-Link Smart Plug that is not in the link above, you may have some features missing

![smart_plug](/images/smartPlug.png)

### Dependencies
* DHT11/DHT22 Temperature Sensor [driver](https://github.com/adafruit/Adafruit_CircuitPython_DHT)
    * `pip3 install adafruit-circuitpython-dht`
* Kasa Smart TP-Link HS100 [driver](https://github.com/python-kasa/python-kasa#supported-devices) 
    * `pip install python-kasa --pre`

### Running the Program
To run the program we need to run the following bash script located in the src directory:
```bash
#!/bin/bash

# Script to run the smart fan python script
# Will take an argument $1 and pass it to the python script
SF_PATH = '~/Documents/SmartFan/smart_fan.py'
python3 $SF_PATH "$1"
```
To run this script in the terminal we enter the following command:
* `./smart_fan.sh <args>` where \<args> is the temperature in Fahrenheit where the fan will turn on.
If there is no parameter passed, then the default temperature threshold will be set to 80 degrees Fahrenheit.

You could replace `~/Documents/SmartFan/smart_fan.py` to a directory where the python script is located.

#### Note
You must change the executable permission to run the script in your Raspberry Pi. To do this we enter the following
command in the terminal:
* `chmod 755 smart_fan.sh`

#### Run Script Without Explicit Path 
1. Make a bin directory in your home directory 
    * `mkdir bin`
2. Copy the shell script in the bin directory 
    * `cp ~/Documents/SmartFan/src/smart_fan.sh ~/bin/`
3. [Optional] Remove `.sh` to run script as `smart_fan` like the ssh example below
    * `mv ~/bin/smart_fan.sh ~/bin/smart_fan`

#### SSH Raspberry Pi Example
Instead of having to directly connect to your Raspberry Pi, you could remote connect and run the script with
your personal computer. Just make sure you look up what is the address of your Raspberry Pi.

![sshExampleScreenShot](/images/sshExample.png)


For more Raspberry Pi Remote access click [here](https://www.raspberrypi.com/documentation/computers/remote-access.html)

### Ending the Program
To stop the program we simply need to use a keyboard interrupt which is `ctrl + c`

### Driver Sources
TP Link  Smart WiFI Plug drivers
* https://github.com/python-kasa/python-kasa

Adafruit DHT22 Temperature and Humidity drivers
* https://github.com/adafruit/Adafruit_CircuitPython_DHT

## Project Overview
This section is a more technical overview of what the program is capable of and describes the design and implementation steps 
that occurred for this project.

### Summary 
We created a program automatically turns on and off a typical fan based on the temperature.  
The fan is connected to a WiFi enabled plug which is controlled by a Raspberry Pi.  
The Raspberry Pi has a temperature sensor connected to the board and will automatically turn on the fan when a certain 
temperature is reached.  When the temperature drops below a certain temperature, the fan is turned off by the 
Raspberry Pi.  The temperature limit that turns on the fan is entered by the user.

### Design
![Communication Design](/images/inputOutput.png)

Above is a high level overview of our design of the automatic fan.  
The Raspberry Pi is what connects all of our components together and allows them to work with each other.
The temperature sensor we used connects directly to the Raspberry Pi and allows for easy access to temperature data we 
need. Next, we needed our Raspberry Pi to be able to turn the fan on and off.  
To accomplish this, we used a WiFi enabled plug to connect the fan to an outlet.  
The Raspberry Pi is able to communicate with the plug via WiFi as long as they are on the same network.  
We decided to use ssh via terminal in order to send and receive data from the Raspberry Pi and this terminal window 
acted as our display.

### Implementation
In the process of implementing our Automated Smart Fan, we needed to accomplish several tasks:
* Set up the Raspberry Pi 
* Install the necessary drivers
    * Install temperature sensor(DHT22) drivers 
    * Install SmartPlug(Kasa Smart TP-Link HS100) drivers
* Implement Python code to control our device
    * The Python script job is to:
        * store a set temperature from the user
        * display the current temperature every 5 seconds
        * turn on the fan if the current temperature exceeds the set temperature

### Testing
Testing for our project occurred throughout our implementation process.
The first initial test was to see if the Raspberry Pi was set up properly.
After installing the driver for the DHT22 temperature sensor, a simple test was performed to see if 
the temperature was being read properly and if the sensor was correctly attached to the raspberry pi.
Another test was done to see if we could control the WiFi plug from the Raspberry Pi after installing the driver for 
the TP-link HS100 WiFi smart plug. This was to ensure that both the WiFi plug and Raspberry Pi were connected to the same network. After these tests succeeded, it was time to test the Python script to ensure it was working as intended.

### Distributions of Tasks
* [Amiel](): Design, Implementation, and README
* [Jeremy](): Design and README/Documentation
* Kenny: Testing
