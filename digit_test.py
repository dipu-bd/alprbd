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
    return np.sort([file for file in glob(folder + '/**/*.bmp', recursive=True)])
# end if

def main():
    """Main function"""
    if not os.path.exists('sample'):
        return print("Samples not found")
    # end if

    W = np.load('output/weight.npy')
    B = np.load('output/base.npy')
    
    files = read_images('sample')
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

