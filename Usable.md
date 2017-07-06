## Bangla Automatic Number Plate Recognition System using Artificial Neural Network (2012 - ATST)

    Accuracy: Total = 75.51%
        Detection & Extraction = 92.1%
        Character Segmentation = 97.53%
        Character Recognition  = 84.16%
    Warning: Not publised formally.

They provided a generalized method for the task excluding embassy and military cars. The detection was done by gaussian filter and extraction by contour analysis. Horizontal and vertical projection was used to segment characters. They kept the city-name together as a whole. To recognize a 3 layer MLP was used of dimension: `25 x 158 x 40`. 25 features are extracted manually from segmented letters.

> The classes include private vehicle and commercial vehicles. Other categories of vehicles, such as embassy cars and military cars are not addressed since they are rarely seen.

