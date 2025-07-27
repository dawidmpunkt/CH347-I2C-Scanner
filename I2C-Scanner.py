from ctypes import *
import time

class I2CScanner:
    ch347 = windll.LoadLibrary("./CH347DLLA64.dll")  # Adjust if needed

    def __init__(self, usb_dev=0):
        self.usb_id = usb_dev
        if I2CScanner.ch347.CH347OpenDevice(self.usb_id) != -1:
            I2CScanner.ch347.CH347CloseDevice(self.usb_id)
        else:
            raise Exception("CH347 not found")

    def check_addr(self, addr_7bit):
        addr = addr_7bit << 1  # 8-bit I2C address
        if I2CScanner.ch347.CH347OpenDevice(self.usb_id) == -1:
            return False
        write_buf = (c_byte * 1)(addr)
        read_buf = (c_byte * 1)()
        # Mode 1 = write address only, expect read (to see if it ACKs)
        result = I2CScanner.ch347.CH347StreamI2C(self.usb_id, 1, write_buf, 1, read_buf)
        I2CScanner.ch347.CH347CloseDevice(self.usb_id)
        return result == 1

    def scan(self):
        print("Scanning I²C bus...")
        found = []
        for addr in range(0x03, 0x78):  # Valid 7-bit range
            if self.check_addr(addr):
                print(f"Found device at 0x{addr:02X}")
                found.append(addr)
        if not found:
            print("No I²C devices found.")
        return found


if __name__ == "__main__":
    scanner = I2CScanner()
    devices = scanner.scan()