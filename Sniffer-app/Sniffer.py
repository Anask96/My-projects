import threading
import time
import serial
import serial.tools.list_ports
from decode_data import decode_message
from shared import DataStorage, stop_event, pause_event
from GUI import create_app

#use this event connect and disconnect to serial port  

def process_data():
    while True:
        # Retrieve data from the queue
        data = DataStorage.data_queue.get()
        if data is None:
            break
        decode_message(data)
        DataStorage.data_queue.task_done()  #

def find_specific_serial_port(description_prefix, description_prefix2):
    # Get a list of available serial ports
    ports = serial.tools.list_ports.comports()
    
    # Iterate over the list of ports and find the one with the matching description
    for port in ports:
        if port.description.startswith(description_prefix):
            return port.device
        elif port.description.startswith(description_prefix2):
            return port.device
        return None

def read_from_serial(port='COM4', baudrate=115200, timeout=1):
    ser = None
    try:
        while True:
            if not pause_event.is_set():
                # Open the serial port if it's not open
                if ser is None or not ser.is_open:
                    ser = serial.Serial(port, baudrate, timeout=timeout)
                    print(f"Opened {ser.name} at {baudrate} baud rate")
                
                if ser.in_waiting > 0:
                    # Read a line from the serial port
                    line = ser.readline()
                    line_decoded = line.decode('latin1').rstrip()
                    DataStorage.data_queue.put(line_decoded)
                    print(f"Received: {line_decoded}")
            else:
                # Close the serial port if it's open
                if ser is not None and ser.is_open:
                    ser.close()
                    print(f"Closed {ser.name}")
                    ser = None
            
            # Add a small delay to prevent CPU overload
            time.sleep(0.1)
    
    except serial.SerialException as e:
        pass
    except Exception as e:
        pass
    finally:
        if ser is not None and ser.is_open:
            ser.close()
            print(f"Closed {ser.name}")

def create_threads():
    threads = []
    for _ in range(2):
        thread = threading.Thread(target=process_data)
        thread.daemon = True
        thread.start()
        threads.append(thread)


    while True:
        com_port = find_specific_serial_port("Silicon Labs CP210x USB to UART Bridge", "Prolific USB-to-Serial Comm Port")
        if com_port != None:
            read_from_serial(com_port)

if __name__ == "__main__":
    serial_thread = threading.Thread(target=create_threads)
    serial_thread.daemon = True
    serial_thread.start()
    create_app()
