import serial

class SerialReader:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.running = False

    def start(self, forwarder):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        self.running = True
        print(f"Started reading from {self.port}")
        while self.running:
            data = self.ser.readline()
            if data:
                print(f"Received: {data.decode().strip()}")
                forwarder.send_data(data)

    def stop(self):
        self.running = False
        if self.ser:
            self.ser.close()

    def reset(self):
        print(f"Resetting serial connection on {self.port}")
        if self.ser:
            self.ser.close()
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        print(f"Serial connection reset successfully")
