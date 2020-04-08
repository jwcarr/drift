Algorithms for the automated correction of eye tracking calibration error in multiline reading experiments
==========================================================================================================

The top-level structure of the repo is:

- `code/`: All Python code used for the model and analysis

- `data/`: Raw data files 

- `manuscript/`: LaTeX source and EPS figures for the manuscript

- `visuals/`: Various visualizations


Data
----

The data is organized into four directories:

- `algorithm_performance/`: Pickled numpy arrays which store the simulated performance results.

- `fixations/`: The original fixation sequences for the 48 sample trials are stored in sample.json. Each of the other 9 JSON files corresponds to an algorithmic or human correction.

- `manual_corrections/`: Manual corrections performed by the two correctors plus the gold standard correction. Each file is a reading trial, and files are nammed by participant ID and passage ID. Each line in these files corresponds to a fixation (duration, x-coordinate, y-coordinate, and line assignment (0 is used to represent discard)).

- `passages/`: The text of each of the 12 passages.


License
-------

Except where otherwise noted, this repository is licensed under a Creative Commons Attribution 4.0 license. You are free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit, provide a link to the license, and indicate if changes were made. See LICENSE.md for full details.
