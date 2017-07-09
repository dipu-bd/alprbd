"""
ALPR-BD Command Line Utility.
"""
import json
from argparse import ArgumentParser

def get_config():
    """Returns the configuration file"""
    config_file = open('./app.config.json')
    config = json.loads(config_file.read())
    config_file.close()
    return config
# end fucntion

def main():
    """Main function"""
    # Load cofiguration
    config = get_config()

    parser = ArgumentParser(description=config['name'] + " Version: " + config['version'])
    # Optional arguments
    parser.add_argument("-v", "--version", action="store_true", \
        help="Displays the current version.")
    parser.add_argument("-j", "--json", action="store_true", \
        help="Output in json format. Default=False")
    parser.add_argument("-n", "--maxN", dest="number", default=10, type=int, \
        help="Maximum number of possible plate numbers. Default=10")
    parser.add_argument("--mark", dest="output_file", \
        help="Highlight plate regions in the input image with most probable plate numbers")
    parser.add_argument("--extract", action="store_true", \
        help="Extracts all detected plates in current directory")
    parser.add_argument("--debug", \
        help="Output debug information. Default=False")

    # Positional argument
    parser.add_argument("-i", "--input", dest="input_image", \
        help="Image of a car to recognize license plate number.")

    # Developer mode
    subparsers = parser.add_subparsers(title='Developer',
                                       description='Addition tool support',
                                       help='developer mode')
    dev_parser = subparsers.add_parser('dev')
    dev_parser.add_argument('-t', action="count", help="just a test")

    # Process arguments and call necessary functions
    args = parser.parse_args()
    if args.version:
        print(config.version)
    print(args)
# end function

if __name__ == '__main__':
    main()
# end if
