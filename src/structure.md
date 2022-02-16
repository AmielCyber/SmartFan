# Source Code Structure

## Main Method
Main function immediately sets the DEFAULT_TEMP to 80, calls get_ip_address() and checks if the user passes in a valid
parameter.

If an ip_address is found for the smart plug, the method checks to see if the user passed in a desired temperature
threshold and if so sets temp_threshold to the passed in value.  Otherwise temp_threshold is set to DEFAULT_TEMP.
Next the smart_plug and dhtDevice(temperature sensor) are initialized.

Finally, run_app is called and passed smart_plug, dhtDevice, and temp_threshold

## get_ip_address()
This function searches for the IP address of available smart plugs and returns a list of these IP addresses.

## run_app(sp, dht, tmp)
![param_Screen]()
This function continuously runs the automated fan until the user interrupts via keyboard interrupt.

The function is synced to the drivers provided in order to have proper execution.

The function checks if the current temperature is greater than the temp parameter and if the fan is currently off. 
If so, the fan will be turned on.

The function also checks if the current temperature is less than the temp parameter and if the fan is currently on.
If so, the fan will be turned off.



