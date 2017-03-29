# ALPR - Bangladesh

***Thesis**: Automated Bangla License Plate Recognition.*

This repository contains the implementation for the above thesis.


## Setup 
- Install `anaconda3`
- Install `opencv3`: `conda install -c menpo opencv3` 
- Clone this repository: `git clone git@github.com:dipu-bd/ALPR-Bangladesh.git`


## Usage 
- Create a directory called `stages` inside the current folder.
- Save input images inside `stages/stage.0` folder.
- Input image file-names should follow the format: `<name>.<extension>`
- Run `python .` to execute all stages simultaneously.
- Run `python . <stage_number>` to execute a single stage.
Replace the `<stage_number>` here with an integer starting from `1`.
The `stages` folder must have folder named `stage.<X>` for stage `X`.


## Development Notes

### Editor choice
- I prefer **PyCharm** *Community Edition*.

### Definitions
- `main.py`: Main starting script.
- `stage`: **Stage** here means states of the processing.
`stage.0` identifies original image list.
 After applying first step the `stage.1` is found, and so on.
- `alpr.py`: It connects all functions with stage numbers.

### Stage Artifacts
- **Stage Artifacts** are the output files generated after executing each stages.
- The output images should be stored inside `stage.<stage_number>` folder.
- The format of these image file: `<name>.<extension>`. 
- Here `<name>` refers to the name of original image.

### Creating A Stage:
- create a python file inside `modules` folder. 
- Import it inside `alpr.py`.
- Insert the name of the function in `STAGE_FUNC` variable.

