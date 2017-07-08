"""
DIGIT classifier
"""
import config as cfg
from utils import get_digit_data
from softmax_1layer import train

# Import data
def main():
    """Main function"""
    train(get_digit_data(),
          input_dim=28*28,
          output_dim=len(cfg.NUMERALS),
          learning_rate=0.3,
          iterations=5000,
          batch_size=100,
          base_file=cfg.DIGIT_BASES,
          weights_file=cfg.DIGIT_WEIGHTS)
# end function

if __name__ == '__main__':
    main()
# end if
