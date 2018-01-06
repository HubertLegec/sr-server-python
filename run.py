from server.app import start
from server.utils import parse_parameters

if __name__ == '__main__':
    parameters = parse_parameters('config.json')
    start(parameters)
