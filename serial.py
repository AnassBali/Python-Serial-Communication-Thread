import threading
import time
import serial

# https://superfastpython.com/thread-event-object-in-python/

def ProcessInputQueue(inputQueue, readCounter):
    print(f"Processed input queue: {inputQueue}, Read counter: {readCounter}")

class MyThread(threading.Thread):
    def __init__(self, ThreadID, ThreadName, PortName, Event):
        threading.Thread.__init__(self)
        self.threadID = ThreadID
        self.name = ThreadName
        self.readCounter = 0
        self.bAlive = True
        self.ser = None
        self.portName = PortName
        self.portBaudrate = 9600
        self.portParity = serial.PARITY_NONE
        self.portStopBits = serial.STOPBITS_ONE
        self.portTimeout = 0.1
        self.portRtsCts = False
        self.inputQueue = ''
        self.outputQueue = ''
        self.event = Event
        self.event.clear()

    def run(self):
        print(f"Starting Thread: {self.name}")
        try:
            self.ser = serial.Serial(port=self.portName,
                                     baudrate=self.portBaudrate,
                                     parity=self.portParity,
                                     stopbits=self.portStopBits,
                                     timeout=self.portTimeout,
                                     rtscts=self.portRtsCts)
            while self.bAlive:
                char_c = self.ser.read(1)
                if char_c != b'':
                    self.inputQueue += char_c.decode('utf-8')  # Decode bytes to string
                    self.readCounter += 1
                    if char_c == b'\n':
                        ProcessInputQueue(self.inputQueue, self.readCounter)
                        self.inputQueue = ''  # Clear input queue after processing

        except ValueError as e:
            print(f"ValueError: {e}")
        except serial.SerialException as se:
            print(f"SerialException: {se}")

        print(f"Exiting {self.name}")

    def stopping(self):
        if self.ser:
            self.ser.cancel_read()
            self.ser.close()  # Close the serial port 
        self.bAlive = False
