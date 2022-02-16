"""
This simple python script will take an argument from the command line
and set the temperature threshold when the fan will turn on if
the temperature goes above this threshold. The script can be
ended by doing a keyboard interrupt. Doing this will shut down
all sensors and gracefully exit.

"""
import time             # To pause the process if we cannot get a reading from the temp HW
import board            # To read the temperature connected to the raspberry pi board
import adafruit_dht     # To use the temperature hardware's API
import asyncio          # Use asyncronous operations with our hardware
from kasa import Discover, SmartPlug    # Use the smpart plug's API
import sys              # To read the user's arguments passed


def get_ip_address():
    """
    Calls the Discover object in the Kasa library to get all the IP addresses of TP link products found in the network
    :return: a list of strings that contain the IP addresses found
    """
    ip_address = []                             # Creates a list of ip addresses from all tp link devices
    devices = asyncio.run(Discover.discover())  # Calls discover to get all the devices found in this network

    for addr, dev in devices.items():
        # Add each tp link ip address to our list
        ip_address.append(addr)

    return ip_address


async def exit_program(close_msg, smart_plug, dht_device):
    """
    Gracefully closes the smart_fan python script.
    :param close_msg:       The closing message to display to the user
    :param smart_plug:      The smart_plug device that controls our fan
    :param dht_device:      DHT device that reads the enviornment's temperature and humidity
    """
    print('\n', close_msg)
    print('Turning off temperature sensor...')
    dht_device.exit()                   # Turns off the temperature sensor.
    print('Turning off fan...')
    await smart_plug.turn_off()         # Turns off the fan.
    print('Now exiting program...')


async def run_app(smart_plug, dht_device, temp):
    """
    Runs the automated fan until it is interrupted by the user.
    :param smart_plug:      A smart plug object
    :param dht_device:      A DHT22 object (the temperature sensor)
    :param temp:            The user's desired temperature when to have the fan on
    """
    SLEEP_TIME = 5.0        # Wait time until we check the temperature again
    await smart_plug.update()       # must be call to wait till the device is ready
    model_name = smart_plug.model   # Get the smart plug's model name
    print('Using {}'.format(model_name))
    print('Using temperature threshold: {} F'.format(temp))
    cont = True
    while cont:
        # Run until the user interrupts to end
        # Try to catch any errors
        try:
            # Update the status info on the smart plug
            await smart_plug.update()

            # Get readings from DHT
            temperature_c = dht_device.temperature          # Get temperature reading in Celsius
            temperature_f = temperature_c * (9 / 5) + 32    # Convert Celsius reading to Fahrenheit
            humidity = dht_device.humidity                  # Get humidity percentage reading

            # Print DHT readings
            print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))

            # Turn fan on/off based on the readings.
            if temperature_f > temp and not smart_plug.is_on:
                # If temperature is higher than temp threshold and smart plug is off, then turn on
                await smart_plug.turn_on()
            elif temperature_f < temp and smart_plug.is_on:
                # If temperature is lower than temp threshold and smart plug is on, then turn off
                await smart_plug.turn_off()

            # Update the status info on the smart plug and print its status.
            await smart_plug.update()
            print(model_name, 'status: ', 'ON' if smart_plug.is_on else 'OFF')

        # Catch any errors or interruptions
        except RuntimeError as error:
            # If a DHT error is found then we just wait and run the program again
            print(error.args[0])        # Print the type of error
            try:
                time.sleep(SLEEP_TIME)  # Hold to see if the error is resolved
                continue                # Continue execution
            except KeyboardInterrupt:
                # If the user ended the program during resolving dht reading
                MSG = 'User ended session.'
                await exit_program(MSG, smart_plug, dht_device)
                cont = False
        except KeyboardInterrupt:
            # If the user ended the program
            MSG = 'User ended session.'
            await exit_program(MSG, smart_plug, dht_device)
            cont = False
        except Exception as error:
            # An error that is not from our devices
            MSG = 'Error Occurred, now closing program.'
            await exit_program(MSG, smart_plug, dht_device)
            raise error
        try:
            time.sleep(SLEEP_TIME)  # Hold SLEEP_TIME for next reading
            continue                # Continue execution
        except KeyboardInterrupt:
            # If the user ended the program during SLEEP_TIME
            MSG = 'User ended session.'
            await exit_program(MSG, smart_plug, dht_device)
            cont = False
    await smart_plug.turn_off()


if __name__ == '__main__':
    DEFAULT_TEMP = 80                                           # Default temperature threshold
    ip_address = get_ip_address()                               # Get smart WiFi plug ip address to send commands
    valid_arg = len(sys.argv) > 1 and sys.argv[1].isnumeric()   # Boolean to check if argument is valid

    if ip_address and sys.argv:
        # Get the passed argument temperature threshold from the command line argument
        if valid_arg:
            # If user passed a valid argument
            temp_threshold = int(sys.argv[1])
        else:
            temp_threshold = DEFAULT_TEMP

        # Create smart plug instance with the first ip_address found
        smart_plug = SmartPlug(ip_address[0])
        # Initialize the temperature reader device with the argument passed as D4 for the pin number used in rasp Pi
        dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        # Start running the application
        asyncio.run(run_app(smart_plug, dht_device, temp_threshold))

    else:
        # If there were no tp link devices found
        print('No tp link device found!')
        print('Now exiting...')
    # Print friendly exit
    print('Program closed successfully')
