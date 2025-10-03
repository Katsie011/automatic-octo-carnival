from PCANBasic import *
import select, time

class CANReader:
    def __init__(self, channel=PCAN_USBBUS1, baudrate=PCAN_BAUD_250K):
        self.pcan = PCANBasic()
        self.channel = channel
        self.baudrate = baudrate
        result = self.pcan.Initialize(channel, baudrate)
        if result != PCAN_ERROR_OK:
            raise RuntimeError(f"CAN init failed: {self.pcan.GetErrorText(result)}")

    def read_message(self):
        result = self.pcan.Read(self.channel)
        if result[0] == PCAN_ERROR_OK:
            msg = result[1]
            return msg.ID, msg.DATA[:msg.LEN]
        elif result[0] == PCAN_ERROR_QRCVEMPTY:
            time.sleep(0.001)
            return None
        else:
            return None

    def close(self):
        self.pcan.Uninitialize(self.channel)
