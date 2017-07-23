# ALPR - Bangladesh

***Thesis**: Automated Bangla License Plate Recognition.*

This is a branch to review papers on our topic.

**Ranks**: The lower the rank is the more important the paper is to our research. Ranks can be ranged from 1 to 5.

- Papers: `10`
- Links: `3`


# Rank 1 (Must refer: `2 papers`)

## [anagnostopoulos2006license] A License Plate-Recognition Algorithm for Intelligent Transportation System Applications (2006 IEEE)

    Focus: USA license plates
    Accuracy: Total = 86.0%
        Segmentation = 96.5%
        Recognition = 89.1%

This paper provides an in-dept literature review. 

> In this paper, an algorithm implementing a novel adaptive image segmentation technique (SCWs) and connected component analysis is considered for license plate location and character segmentation. For the OCR task, a PNN with topology 108-180-36 is trained to identify alphanumeric characters, which were previously isolated from the candidate area.

## [uddin2016bangladeshi] Bangladeshi Vehicle Digital License Plate Recognition for Metropolitan Cities Using Support Vector Machine (2016 - ICAICT)

    Target: Bangladesh
    Accuracy: Overall = 91.3%
        Detection: 93.2%
        Segmentation: 98.1%
        Recognition: 99.2%

Vertical sobel operator is used to get edge image. Dilation and erosion applied aftwards to highlight plate area. Extracted plate area is converted to binary image using adaptive thresholding utilizing convolution.

For segmentation, connected component analysis is done. Then bounding box is calculated and aspect ratio is observed to choose a character. 

2D Gabor filter is used for feature extraction. City-name is kept intact. Finally an SVM with KPCA is used for character recognition.




# Rank 2 (`5 papers`)

## [abolghasemi2009edge] An edge-based color-aided method for license plate detection (2008 - Elsevier)

    Focus: Iranian license plates. 

They researched on two major areas: to enhance image contrast in plate-like regions, and a novel match filter to eliminate non-plate like regions. Their approach was referenced in many papers. 

![accuracy](img/0001.png)

## [joarder2012bangla] Bangla Automatic Number Plate Recognition System using Artificial Neural Network (2012 - ATST)

    Accuracy: Total = 75.51%
        Detection & Extraction = 92.1%
        Character Segmentation = 97.53%
        Character Recognition  = 84.16%

They provided a generalized method for the task excluding embassy and military cars. The detection was done by gaussian filter and extraction by contour analysis. Horizontal and vertical projection was used to segment characters. They kept the city-name together as a whole. To recognize a 3 layer MLP was used of dimension: `25 x 158 x 40`. 25 features are extracted manually from segmented letters.

> The classes include private vehicle and commercial vehicles. Other categories of vehicles, such as embassy cars and military cars are not addressed since they are rarely seen.

## [moustafa2015new] A New Approach for License Plate Detection and Localization: Between Reality and Applicability (2015 - IBR)

    Target: Arabian Plates
    Accuracy: 93.1

Upto detection. Uses histrogram equalization for enhancing constrast. First selects interesting rows, then columns.

## [saha2009license] License Plate Localization from Vehicle Images: An Edge Based Multi-stage Approach (2009 IJRTE)

    Accuracy: 89.2% (#FN: 8%, #FP: 2.8%)

Upto detection. Histrogram based contrast enhancement. Has detailed and algorithm description of localization process.

## [ghosh2011automatic] Automatic license plate recognition (alpr) for bangladeshi vehicles (2011 GJCST)

    Accuracy:
        Extraction = 84%
        Recognition = 80%

Used vertical Sobel operator for extraction. Skewed images were fixed. Then horizontal and vertical projection was applied. Typical bangla character recognition process with matra detection was done.

*Their description is not enough for implementation.*

> ALPR system is mostly used in Intelligent Transportation System. ALPR is important in the area of highway toll collection, traffic problems, borders and custom security, premises where high security is needed, like national assembly, V.I.P houses and so on. III.




# Rank 3 (Unpublished. `1 papers`)
## [piasautomatic] Automatic Detection of Number Plate from Images of Bangladeshi Vehicles (April-2017 ResearchGate)

    Target: Bangladeshi Plates
    Accuracy: 99%+

Used CNN to detect ROI containing the number plate. First step of training was done using CIFAR-10. Second step was for pinpoint the actual plate region from first region of interest. The CNN was designed using ReLU, 2D Convolutional Layer, Max Pooling, and Softmax at the final layer, and trained using Dropouts, and Decaying Learning Rate.

Although they claim to have a high performance system, the process is unclear.

> ANPR was invented in 1976 at the Police Scientific Development Branch in the UK and prototype systems has been in use since 1979.

## [alom2017handwritten] Handwritten Bangla Digit Recognition Using Deep Learning (May-2017 arXiv)

    Target: Bangla Digits, handwritten
    Accuracy: 98.78%

They experimented with various types of CNN. Their CNN with dropout and Gabor filters achieved 98.78% accuracy on CMATERdb 3.1.1. 

*For printed characters, I believe the accuracy can exceed 99.5%. Also the system is worth more observation to use in letter recognition*



# Rank 4 (Unusable. `2 papers`)
## [uddin2016bangladeshi] Bangla License Plate Reader for Metropolitan Cities of Bangladesh Using Template Matching

    Target: Bangladeshi Plates
    Accuracy: Not Specified

They focused on metropolitan areas only. The extraction was done by measuring the distribution of connected components. The segmentation process depends on the word: `Metro`. They claimed to have used the `matra` for recognition, but the process was not clearly described.

> According to the regulations of BRTA, the registration number of license plates in the metropolitan cities has to be written in Bangla script painted on flat steel or aluminium plate of dimensions 524mm x 112mm for a car. The plates also must follow a specific color code based on the type of the vehicle, the algorithm proposed here works independent of these color patterns.


## [mashuk2010automatic] Automatic detection of bangla characters in bangladeshi car registration plates (2010 CIMSiM)

    Target: Bangladeshi Plates
    Accuracy: Not specified

They depended on a system that takes images of the car from a certain distance and angle. Detection of plate is done empirically selecting a specific portion of the image. After converting the image to binary, segmentation was done by horizontal and vertical projection. Neural network was used for recognition.



# Rank 5 (`3 links`)

## [List_of_districts_of_Bangladesh](https://www.wikiwand.com/en/List_of_districts_of_Bangladesh#/List_of_districts)

Found names of all districts of bangladesh here.

## [Vehicle_registration_plates_of_Bangladesh](https://www.wikiwand.com/en/Vehicle_registration_plates_of_Bangladesh)

The letters permitted in the vehicle registration plate are listed here.

## [vehicle-digital-number-plate-in-bangladesh](http://www.bikebd.com/vehicle-digital-number-plate-in-bangladesh/)

An article on standard license plate extraction.

