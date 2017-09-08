# -*- coding: utf-8 -*-
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


#     ch.jpg = চ (99.85% sure)
#   ch_1.jpg = চ (100.00% sure)
#   ch_2.jpg = চ (99.99% sure)
#   ch_3.jpg = চ (99.60% sure)
#     ga.jpg = গ (100.00% sure)
#   ga_1.jpg = গ (100.00% sure)
#   ga_2.jpg = গ (100.00% sure)
#   ga_3.jpg = গ (100.00% sure)
#     ka.jpg = ক (100.00% sure)
#   ka_1.jpg = ক (99.99% sure)
#    kha.jpg = খ (100.00% sure)
