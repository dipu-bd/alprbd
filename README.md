# ALPR - Bangladesh

***Thesis**: Automated Bangla License Plate Recognition.*

This repository has the API for Automated Bangla License Plate Dectection.

## Development plan

### End-User's Api

    USAGE:
        alprbd [options] <image_file_name>
    
    OPTIONS:
      -h, --help
        Display this message.

      --version
        Displays current version information.

      --log <directory>
        Directory to output log data.
        Must provide if --debug is set.
      
      --debug
        Output debug information. Default=Off
        Must provide a log file to save output.

      -j, --json
        Output in JSON format. Default=Off
      
      -n <number>, --top-n <number>
        Maximum number of possible plate numbers.
        Default=10
    
      --mark <file_name>
        Highlight plate regions with most probable plate number.
      
      --extract <directory>
        Crop all plates and store them in given directory.

      --dev
        To use developer options.
        For details see: alprbd --dev -h
    
    ALPR-BD COMMAND LINE UTILITY


### Developer's API

    USAGE:
        alprbd --dev [dev-options]

    DEVLOPER OPTIONS:
      -h, --help
        Displays this message.

      --dataset <directory>
        Generates dataset to train neural-network.
        <directory> : to save the output.
    
      --train <dataset_dir> [<model_dir>]
        Trains the neural network.
        <dataset_dir> : directory containing dataset.
        <model_dir> : to save the final model.
      
      --use-model <model_dir>
        Setup the given model to use for recognition.
        <model_dir> : directory containing the model.
      
      --test <image_file>
        Tests the current model using the image_file.
