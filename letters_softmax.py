"""
LETTER classifier
"""
import config as cfg
from utils import get_letter_data
from softmax_Nlayer import train

# Import data
def main():
    """Main function"""
    
    row, col = cfg.IMAGE_DIM
    data = get_letter_data()
    layers = [
        row * col,
        512,
        256,
        128,
        64,
        len(cfg.LETTERS),
    ]

    print('Training size =', data.train.labels.shape[0])
    print(' Testing size =', data.test.labels.shape[0])
    print()

    train(data,
          layers=layers,
          batch_size=100,
          iterations=10000,
          learning_rate=0.001,
          model_file=cfg.LETTER_MODEL)
# end function

if __name__ == '__main__':
    main()
# end if
