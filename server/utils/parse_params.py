import argparse


def parse_parameters(default_config):
    parser = argparse.ArgumentParser(description='SR server', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s', '--server', type=int, help='Index of this server config in config file list')
    parser.add_argument('-c', '--config', type=str, metavar='PATH',
                        help='Path to configuration file', default=default_config)
    parser.add_argument('-d', '--debug', action='store_true', help='run in debug mode', default=False)
    return parser.parse_args()
