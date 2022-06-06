import struct
import u3

class LJTickDAC:
    """Updates DACA and DACB on a LJTick-DAC connected to a U3, U6 or UE9."""
    EEPROM_ADDRESS = 0x50
    DAC_ADDRESS = 0x12

    def __init__(self, device, dioPin, failsafe):
        """device: The object to an opened U3, U6 or UE9.
        dioPin: The digital I/O line that the LJTick-DAC's DIOA is connected to.
        """
        self.device = device

        # The pin numbers for the I2C command-response
        self.sclPin = dioPin
        self.sdaPin = self.sclPin + 1

        self.getCalConstants()
        self.failsafe = failsafe

    def toDouble(self, buff):
        """Converts the 8 byte array into a floating point number.
        buff: An array with 8 bytes.
        """
        right, left = struct.unpack("<Ii", struct.pack("B" * 8, *buff[0:8]))
        return float(left) + float(right)/(2**32)

    def getCalConstants(self):
        """Loads or reloads the calibration constants for the LJTick-DAC.
        See datasheet for more info.
        """
        data = self.device.i2c(LJTickDAC.EEPROM_ADDRESS, [64],
                               NumI2CBytesToReceive=36, SDAPinNum=self.sdaPin,
                               SCLPinNum=self.sclPin)
        response = data['I2CBytes']
        self.slopeA = self.toDouble(response[0:8])
        self.offsetA = self.toDouble(response[8:16])
        self.slopeB = self.toDouble(response[16:24])
        self.offsetB = self.toDouble(response[24:32])

        if 255 in response:
            msg = "LJTick-DAC calibration constants seem off. Check that the " \
                  "LJTick-DAC is connected properly."
            raise Exception(msg)

    def update(self, dacA, dacB):
        """Updates the voltages on the LJTick-DAC.
        dacA: The DACA voltage to set.
        dacB: The DACB voltage to set.
        """
        
        # Prevent from going over failsafe value
        if (dacA > self.failsafe/100) or (dacB > self.failsafe/100):
            raise Exception('Shock value exceeded failsafe, check what is going on')
        
        binaryA = int(dacA*self.slopeA + self.offsetA)
        self.device.i2c(LJTickDAC.DAC_ADDRESS,
                        [48, binaryA // 256, binaryA % 256],
                        SDAPinNum=self.sdaPin, SCLPinNum=self.sclPin)
        binaryB = int(dacB*self.slopeB + self.offsetB)
        self.device.i2c(LJTickDAC.DAC_ADDRESS,
                        [49, binaryB // 256, binaryB % 256],
                        SDAPinNum=self.sdaPin, SCLPinNum=self.sclPin)
