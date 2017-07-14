"""
DIGIT classifier
"""
import config as cfg
from utils import get_city_data
from softmaxNN import train

# Import data
def main():
    """Main function"""

    row, col = cfg.CITY_DIM
    data = get_city_data()
    layers = [
        row * col,
        784,
        344,
        112,
        len(cfg.CITIES),
    ] # 3 layer network

    print('Training size =', data.train.labels.shape[0])
    print(' Testing size =', data.test.labels.shape[0])
    print()

    train(data,
          layers=layers,
          batch_size=100,
          iterations=3000,
          model_file=cfg.CITY_MODEL)
# end function

if __name__ == '__main__':
    main()
# end if

#===================================================================
# Training size = 9715
#  Testing size = 1715
#
# step   121 | accuracy =  99.94% | loss =    0.487 | LR = 0.002886
# step   242 | accuracy =  99.94% | loss =    0.354 | LR = 0.002777
# step   363 | accuracy =  99.88% | loss =    2.784 | LR = 0.002672
# step   484 | accuracy =  99.88% | loss =   12.894 | LR = 0.002571
# step   605 | accuracy =  99.94% | loss =    0.859 | LR = 0.002474
# step   726 | accuracy =  99.94% | loss =    0.896 | LR = 0.002381
# step   847 | accuracy =  99.88% | loss =    6.083 | LR = 0.002292
# step   968 | accuracy =  99.88% | loss =   81.623 | LR = 0.002206
# step  1089 | accuracy =  99.94% | loss =    0.120 | LR = 0.002123
# step  1210 | accuracy = 100.00% | loss =    0.000 | LR = 0.002044
# step  1331 | accuracy =  99.59% | loss =   38.468 | LR = 0.001968
# step  1452 | accuracy =  99.83% | loss =   13.664 | LR = 0.001894
# step  1573 | accuracy =  99.94% | loss =    1.773 | LR = 0.001824
# step  1694 | accuracy =  99.94% | loss =    0.494 | LR = 0.001757
# step  1815 | accuracy =  99.94% | loss =    4.020 | LR = 0.001692
# step  1936 | accuracy =  99.94% | loss =    2.907 | LR = 0.001629
# step  2057 | accuracy =  99.94% | loss =    1.300 | LR = 0.001569
# step  2178 | accuracy =  99.88% | loss =   18.770 | LR = 0.001512
# step  2299 | accuracy = 100.00% | loss =    0.000 | LR = 0.001456
# step  2420 | accuracy = 100.00% | loss =    0.000 | LR = 0.001403
# step  2541 | accuracy = 100.00% | loss =    0.000 | LR = 0.001352
# step  2662 | accuracy = 100.00% | loss =    0.000 | LR = 0.001303
# step  2783 | accuracy = 100.00% | loss =    0.000 | LR = 0.001256
# step  2904 | accuracy = 100.00% | loss =    0.000 | LR = 0.001210
# step  3025 | accuracy = 100.00% | loss =    0.000 | LR = 0.001167
#===================================================================
