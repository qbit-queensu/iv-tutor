# Python code to receive messages over serial port from Arduino

import serial

# Define the serial port and baud rate
ser = serial.Serial('COM8', 9600) # Change COM3 to your Arduino's serial port

# Define variables
insertion = False

while True:
    # Read a line from serial port
    msg = ser.readline()
    # Print the received message
    print("Message from Arduino:", msg.decode().strip())
    # Parse Message
    split_string = msg.decode().strip().split(":")
    if (split_string[0] == "Needle is is not in vein!"):
        insertion = False
    if (split_string[0] == "Successful Needle Insertion"):
        insertion = True

    # Print variable update
    # print("Python insertion = %b", insertion)

