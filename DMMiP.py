import configparser

from Shipyard import Shipyard

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    port = config['MAIN']['port']
    host = config['MAIN']['host']
    to_compute = config.getboolean('MAIN', 'compute')

    shipyard = Shipyard(host, port)
    if to_compute:
        shipyard.compute_entry()
    shipyard.start()

