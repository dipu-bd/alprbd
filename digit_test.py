"""
For testing the trained model
"""
import config as cfg
from test_api import run

def main():
    """Main function"""
    run(model_file=cfg.DIGIT_MODEL,
        sample_folder=cfg.DIGIT_SAMPLES,
        letters=cfg.NUMERALS)    
# end function

if __name__ == '__main__':
    main()
# end if
