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

def trim_image(img_file):
    """
    Trims the image
    """
    # open
    img = cv2.imread(img_file, 0)
    rows, cols = img.shape
    # find area
    nzx, nzy = np.nonzero(img)
    x1 = max(0, np.min(nzx))
    x2 = min(rows, np.max(nzx) + 2)
    y1 = max(0, np.min(nzy))
    y2 = min(cols, np.max(nzy) + 2)
    # crop
    cropped = img[x1:x2, y1:y2]
    # resize
    resized = cv2.resize(cropped, cfg.IMAGE_DIM)    
    # save
    cv2.imwrite(img_file, resized)
# end function

def main():
    """Main function"""
    if not os.path.exists(cfg.LETTER_SAMPLES):
        return print("Samples not found")
    # end if

    W = np.load(cfg.LETTER_WEIGHTS)
    B = np.load(cfg.LETTER_BASES)
    
    files = read_images(cfg.LETTER_SAMPLES)
    for file in files:
        #trim_image(file)
        image = cv2.imread(file, 0)        
        image = cv2.resize(image, (28, 28))
        X = np.reshape(image, (1, 784))
        Y = np.matmul(X, W) + B
        p = np.argmax(Y)
        print(file, cfg.LETTERS[p])
    # end for
# end function

if __name__ == '__main__':
    main()
# end if
