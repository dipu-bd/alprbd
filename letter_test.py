"""
For testing the trained model
"""
import config as cfg
from test_api import run

def main():
    """Main function"""
    run(model_file=cfg.LETTER_MODEL,
        sample_folder=cfg.LETTER_SAMPLES,
        letters=cfg.LETTERS)    
# end function

if __name__ == '__main__':
    main()
# end if
