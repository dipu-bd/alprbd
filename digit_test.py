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


#      1.jpg = ১ (100.00% sure)
#    1_1.jpg = ১ (100.00% sure)
#      2.jpg = ২ (100.00% sure)
#      3.jpg = ৩ (100.00% sure)
#      4.jpg = ৪ (100.00% sure)
#      5.jpg = ৫ (100.00% sure)
#      6.jpg = ৬ (100.00% sure)
#      7.jpg = ৭ (100.00% sure)
#      8.jpg = ৮ (100.00% sure)
#    8_2.jpg = ৮ (100.00% sure)
#      9.jpg = ৯ (100.00% sure)
