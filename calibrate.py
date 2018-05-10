# Reset the existing calibration values

##NEED TO RESET VALUES OF COLOR SENSOR
COMMAND_RESET = 'reset'
Reset all of the motor parameter attributes to their default value. This will also have the effect of stopping
the motor.


# Display that the user should place the robot on “black” and wait for OK press

##DON'T KNOW HOW TO DO THIS
Prompt on screen (place on black), and wait until they click OK


# Calibrate Color Sensor in Light Mode to current value -- Minimum (Black)

cs = ColorSensor(port=3)
cs.calibrate_reflected_light_intensity_minimum(0)


# Display that the user should place the robot on "white" and wait for OK press

Prompt on screen (place on white), and wait until they click OK


# Calibrate color sensor in light mode to current value -- Maximum (white).

cs = ColorSensor(port=3)
cs.calibrate_reflected_light_intensity_maximum(100)


#EXAMPLE OF WHEN IN USE

cs = ColorSensor(port=3)
light = cs.measure_reflected_light_intensity()
threshold_value = 50
compare_result = light < threshold_value
