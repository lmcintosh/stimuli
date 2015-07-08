# stimuli
Visual stimuli for evoking responses from vertebrate retina experiments.

## psychtoolbox visual stimulus generation

A set of routines for generating visual stimuli for retinal experiments using psychtoolbox.

### Usage

1. Write down a `config.json` file and place it in the logs directory
2. Run `runme`. This will parse the experiments in `config.json`, run them, and save info back into the logs directory
3. After the experiment, run the `replay` script to generate a `stimulus.h5` file that contains the pixel values and timestamps for all of the stimuli used in the experiment.

