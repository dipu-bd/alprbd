"""
DIGIT classifier
"""
import config as cfg
from utils import get_digit_data
from softmax_Nlayer import train

# Import data
def main():
    """Main function"""

    row, col = cfg.IMAGE_DIM
    data = get_digit_data()
    layers = [
        row * col,
        512,
        256,
        128,
        64,
        len(cfg.NUMERALS),
    ]

    print('Training size =', data.train.labels.shape[0])
    print(' Testing size =', data.test.labels.shape[0])
    print()

    train(data,
          layers=layers,
          batch_size=100,
          iterations=3000,
          learning_rate=0.001,
          model_file=cfg.DIGIT_MODEL)
# end function

if __name__ == '__main__':
    main()
# end if
