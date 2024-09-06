import signal
import sys
import configparser
from serial_reader import SerialReader
from tcp_forwarder import TCPForwarder


def signal_handler(sig, frame):
    print("\nExiting gracefully...")
    reader.stop()
    forwarder.stop()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)


    config = configparser.ConfigParser()
    config.read('config.ini')

    serial_port = config['Serial']['port']
    serial_baud = int(config['Serial']['baud'])
    tcp_port = int(config['TCP']['port'])

    reader = SerialReader(port=serial_port, baudrate=serial_baud)
    forwarder = TCPForwarder(port=tcp_port)
    try:
        forwarder.start()
        reader.reset()
        reader.start(forwarder)
    # except serial.SerialException as e:
    #     print(f"Error: Unable to connect to the serial port. {e}")
    #     sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
