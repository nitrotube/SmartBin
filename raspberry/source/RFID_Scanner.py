import serial
class RFID_Scanner:
	def __init__(self, port):
		self.UART = serial.Serial(
			port=port,
			baudrate=9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
		)
		self.CODE = ""

	def readCode(self):
		if(self.CODE == ""):
			if(self.UART.read() == b'\x02'):
				self.CODE = self.UART.read(12).decode("utf-8")
			else:
				self.CODE = ""
			self.UART.flushInput()
			return ""

		res = self.CODE
		self.CODE = ""
		return res

	def hasCode(self):
		if(self.CODE == ""):
			self.readCode()
			return False
		else:
			return True
