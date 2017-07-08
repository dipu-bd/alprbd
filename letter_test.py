"""
For testing the trained model
"""
import os
from glob import glob
import cv2
import numpy as np
import config as cfg

def read_images(folder):
    """Read all images from a directory recursively"""
    return np.sort([file for file in glob(folder + '**/*.*', recursive=True)])
# end if

def main():
    """Main function"""
    if not os.path.exists(cfg.LETTER_SAMPLES):
        return print("Samples not found")
    # end if

    W = np.load(cfg.LETTER_WEIGHTS)
    B = np.load(cfg.LETTER_BASES)
    
    files = read_images(cfg.LETTER_SAMPLES)
    for file in files:
        image = cv2.imread(file, 0)
        image = cv2.resize(image, (28, 28))
        X = np.reshape(image, (1, 784))
        Y = np.matmul(X, W) + B
        p = np.argmax(Y)
        print(file, cfg.NUMERALS[p])
    # end for
# end function

if __name__ == '__main__':
    main()
# end if
