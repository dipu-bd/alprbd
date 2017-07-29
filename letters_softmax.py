"""
LETTER classifier
"""
import config as cfg
from utils import get_letter_data
from convolutional import train

# Import data
def main():
    """Main function"""

    data = get_letter_data(reshape=True)
    print('Training size =', data.train.labels.shape[0])
    print(' Testing size =', data.test.labels.shape[0])
    print()

    train(data,
          num_classes=len(cfg.LETTERS),
          batch_size=100,
          iterations=2000,
          model_file=cfg.LETTER_MODEL)
# end function

if __name__ == '__main__':
    main()
# end if


#===================================================================
# Training size = 35947
#  Testing size = 6344
#
# step   401 | accuracy =  66.58% | loss =  112.895 | LR = 0.002886
# step   802 | accuracy =  85.78% | loss =   33.943 | LR = 0.002777
# step  1203 | accuracy =  97.57% | loss =   12.081 | LR = 0.002672
# step  1604 | accuracy =  98.53% | loss =    6.688 | LR = 0.002571
# step  2005 | accuracy =  98.85% | loss =    4.734 | LR = 0.002474
# step  2406 | accuracy =  99.29% | loss =    2.691 | LR = 0.002381
# step  2807 | accuracy =  99.20% | loss =    4.210 | LR = 0.002292
# step  3208 | accuracy =  99.51% | loss =    1.749 | LR = 0.002206
# step  3609 | accuracy =  99.45% | loss =    2.136 | LR = 0.002123
# step  4010 | accuracy =  99.59% | loss =    1.868 | LR = 0.002044
# step  4411 | accuracy =  99.56% | loss =    2.021 | LR = 0.001968
# step  4812 | accuracy =  99.04% | loss =    4.484 | LR = 0.001894
# step  5213 | accuracy =  99.50% | loss =    1.961 | LR = 0.001824
# step  5614 | accuracy =  99.61% | loss =    1.903 | LR = 0.001757
# step  6015 | accuracy =  99.73% | loss =    1.060 | LR = 0.001692
# step  6416 | accuracy =  99.64% | loss =    1.564 | LR = 0.001629
# step  6817 | accuracy =  99.73% | loss =    1.385 | LR = 0.001569
# step  7218 | accuracy =  99.59% | loss =    1.550 | LR = 0.001512
# step  7619 | accuracy =  99.68% | loss =    1.481 | LR = 0.001456
# step  8020 | accuracy =  99.70% | loss =    1.211 | LR = 0.001403
# step  8421 | accuracy =  99.75% | loss =    0.975 | LR = 0.001352
# step  8822 | accuracy =  99.80% | loss =    0.945 | LR = 0.001303
# step  9223 | accuracy =  99.75% | loss =    1.183 | LR = 0.001256
# step  9624 | accuracy =  99.67% | loss =    1.298 | LR = 0.001210
# step 10025 | accuracy =  99.87% | loss =    0.504 | LR = 0.001167
#===================================================================
