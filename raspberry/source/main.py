from Container import Container
from Session import Session


def main():

	c = Container()
	while True:
		if(c.scaner.hasCode()):
			session = Session(c, c.scaner.readCode())
			session.run()
			session = 0

	GPIO.cleanup()

if(__name__=="__main__"):
	main()
