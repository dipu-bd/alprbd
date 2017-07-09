"""
ALPR-BD Command Line Utility.
"""
__version__ = "1.0-alpha"

from argparse import ArgumentParser

def main():
    """Main function"""
    # Create a parser
    parser = ArgumentParser(description="ALPR-BD Command Line Utility: " + __version__)

    # Version information
    parser.add_argument("-v", "--version", action="version", \
        help="Displays the current version.", \
        version='%(prog)s ' + __version__)

    # Positional argument
    parser.add_argument(dest="input_image", \
        help="Image of a car to recognize license plate number.")

    # Optional arguments
    parser.add_argument("-e", "--extract", action="store_true", \
        help="Extracts all detected plates in the current directory")
    parser.add_argument("-j", "--json", action="store_true", \
        help="Output in json format. Default=False")
    parser.add_argument("-n", dest="top_n", default=10, type=int, \
        help="Maximum number of possible plate numbers. Default=10")
    parser.add_argument("-m", "--mark", action="store_true", \
        help="Highlight plate regions in the input image with most probable plate numbers")
    
    parser.add_argument("--debug", action="store_true", \
        help="Output debug information. Default=False")

    # Process arguments and call necessary functions
    args = parser.parse_args()
    if args.version:
        print(config.version)
    print(args)
# end function

if __name__ == '__main__':
    main()
# end if
