"""
DIGIT classifier
"""
import config as cfg
from utils import get_digit_data
from softmax_Nlayer import train

# Import data
def main():
    """Main function"""
    train(get_digit_data(),
          layers=[
              28 * 28,
              200,
              100,
              50,
              25,
              len(cfg.NUMERALS),
          ],
          learning_rate=0.003,
          iterations=5000,
          batch_size=100,
          base_file=cfg.DIGIT_BASES,
          weights_file=cfg.DIGIT_WEIGHTS)
# end function

if __name__ == '__main__':
    main()
# end if
