Algorithms for the automated correction of vertical drift in eye tracking data
==============================================================================

This repository contains the code and data for a paper on vertical drift correction algorithms that is currently under review at *Behavior Research Methods*. The top-level structure of the repo is:

- `algorithms/`: Matlab/Octave, Python, and R implementations of the drift correction algorithms.

- `code/`: Python code used to analyze the algorithms (using simulated and natural datasets).

- `data/`: Various unprocessed and processed data files explained in more detail below.

- `manuscript/`: LaTeX source and postscript figures for the manuscript.

- `visuals/`: Various visualizations and illustrations, including corrections of all 48 trials by all algorithms.


Data
----

The data is organized as follows:

- `fixations/`: `sample.json` contains the fixation sequences of the 48 sample trials (after the initial cleaning steps). Each of the other JSON files corresponds to an algorithmic or human correction. These files were produced with [Eyekit](https://jwcarr.github.io/eyekit/) but should be generally interpretable.

- `manual_corrections/`: Raw manual corrections performed by the two correctors plus the gold standard correction. Each file is a reading trial, and files are named by participant ID and passage ID. Each line in these files corresponds to a fixation (duration, x-coordinate, y-coordinate, and line assignment, with 0 used to represent discarding).

- `simulations/`: Pickled Numpy arrays which store the simulated performance results. Each cell in the array stores the proportion of correct line assignments, and the arrays have a shape of (10, 50, 100) – 100 simulations of 50 gradations corrected by 10 algorithms.

- `algorithm_distances.pkl`: Pickled distance matrix which stores the median DTW distance between each pair of algorithms for use in the similarity analyses.

- `passages.json`: The text of each of the 12 passages. This file was produced with [Eyekit](https://jwcarr.github.io/eyekit/) but should be generally interpretable.


Dependencies
------------

The code in this repo was written for Python 3.8.5 with the following packages:

- cairosvg 2.4.2
- eyekit 0.2.9
- lorem 0.1.1
- matplotlib 3.3.1
- numpy 1.19.1
- scikit-learn 0.23.2
- scipy 1.5.2

The Matlab/Octave and R versions of the algorithms were tested under Matlab 9.8.0, Octave 5.2.0, and R 3.5.2.


License
-------

Except where otherwise noted, this repository is licensed under a Creative Commons Attribution 4.0 license. You are free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit, provide a link to the license, and indicate if changes were made. See LICENSE.md for full details.
