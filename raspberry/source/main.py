from container import Container
from session import Session
import config as cfg

def main():
    c = Container()
    while True:
        if(c.scanner.hasCode()):
            session = Session(c, c.scanner.readCode())
            session.run()
            session = 0

if(__name__ == "__main__"):
    main()
