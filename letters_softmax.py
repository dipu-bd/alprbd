"""
LETTER classifier
"""
import config as cfg
from utils import get_letter_data
from softmax_1layer import train

# Import data
def main():
    """Main function"""
    train(get_letter_data(),
          input_dim=28*28,
          output_dim=len(cfg.LETTERS),
          learning_rate=0.2,
          iterations=10000,
          batch_size=100,
          base_file=cfg.LETTER_BASES,
          weights_file=cfg.LETTER_WEIGHTS)
# end function

if __name__ == '__main__':
    main()
# end if
