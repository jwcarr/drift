Algorithms for the automated correction of vertical drift in eye tracking data
==============================================================================

This repository contains the code and data for a paper on vertical drift correction algorithms that is currently under review at *Behavior Research Methods*.

If you simply want to correct some eyetracking data, you may first want to look into the Python package [Eyekit](https://jwcarr.github.io/eyekit/) or the R package [popEye](https://github.com/sascha2schroeder/popEye). These packages provide more general, higher-level tools for managing, cleaning, and analyzing eyetracking data with a particular emphasis on reading behavior. This includes the ability to correct vertical drift issues with many of the algorithms reported in the paper.

Alternatively, if you are looking to do something a bit more advanced (e.g. you want to integrate one or more of the algorithms into your own analysis code), then take a look in the `algorithms/` directory. There you will find Matlab, Python, and R functions that you can use as a starting point. You will probably need to do some work to restructure these functions into something that makes sense for your specific project.

If you want to replicate the analyses reported in the paper or build on our work, read on...


Structure of this repository
----------------------------

- `algorithms/`: Matlab/Octave, Python, and R implementations of the drift correction algorithms.

- `code/`: Python code used to analyze the algorithms (using simulated and natural datasets).

- `data/`: Various unprocessed and processed data files:

	- `fixations/`: `sample.json` contains the fixation sequences of the 48 sample trials (after the initial cleaning steps). Each of the other JSON files corresponds to an algorithmic or human correction. These files were produced with [Eyekit](https://jwcarr.github.io/eyekit/) but should be generally interpretable.

	- `manual_corrections/`: Raw manual corrections performed by the two correctors plus the gold standard correction. Each file is a reading trial, and files are named by participant ID and passage ID. Each line in these files corresponds to a fixation (duration, x-coordinate, y-coordinate, and line assignment, with 0 used to represent discarding).

	- `simulations/`: Pickled Numpy arrays which store the simulated performance results. Each cell in the array stores the proportion of correct line assignments, and the arrays have a shape of (10, 50, 100) – 100 simulations of 50 gradations corrected by 10 algorithms.

	- `algorithm_distances.pkl`: Pickled distance matrix which stores the median DTW distance between each pair of algorithms for use in the similarity analyses.

	- `passages.json`: The text of each of the 12 passages. This file was produced with [Eyekit](https://jwcarr.github.io/eyekit/) but should be generally interpretable.

- `manuscript/`: LaTeX source and postscript figures for the manuscript.

- `supplement/`: Supplementary Item 1 (pseudocode) and Supplementary Item 2 (corrections of all 48 trials by all algorithms).

- `visuals/`: Various visualizations and illustrations.


Replication of the analyses
---------------------------

If you have any problems replicating our analyses, please [raise an issue](https://github.com/jwcarr/drift/issues) and we will try to help. First, clone or download the repository and `cd` into the top-level directory:

```shell
$ cd path/to/drift/
```

You will probably want to create and activate a new Python virtual environment, for example:

```shell
$ python3 -m venv .venv/
$ source .venv/bin/activate
```

Install the required Python packages:

```shell
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


### Results on simulated data

To reproduce our simulation results:

```shell
$ python code/simulation_results.py
```

This will use the precomputed results stored in `data/simulations/` and will output:

```
visuals/results_simulations.pdf
visuals/results_invariance.pdf
```

If you want to recreate the simulation results from scratch, then you can simulate each of the five factors like this:

```shell
$ python code/simulation.py noise data/simulations/ --n_gradations 50 --n_sims 100
$ python code/simulation.py slope data/simulations/ --n_gradations 50 --n_sims 100
$ python code/simulation.py shift data/simulations/ --n_gradations 50 --n_sims 100
$ python code/simulation.py regression_within data/simulations/ --n_gradations 50 --n_sims 100
$ python code/simulation.py regression_between data/simulations/ --n_gradations 50 --n_sims 100
```

This will take several hours to run, so you may want to run each factor in parallel and/or decrease the number of gradations in the parameter space or the number of simulations performed per gradation. For more details on the simulations, explore the code itself.


### Results on natural data

To reproduce our benchmarking results on the natural dataset:

```shell
$ python code/accuracy.py
```

This will use the manual corrections and precomputed algorithmic corrections from `data/fixations/` to produce:

```
visuals/results_accuracy.pdf
visuals/results_improvement.pdf
visuals/results_proportion.pdf
```

If you want to recreate the algorithmic corrections:

```shell
$ python code/run_algorithms.py
```

This will take a little while to run (note also that some algorithms, such as `cluster`, are nondeterministic and will not produce the same output on every run, so you might get slightly different results). If you want to recreate the manual corrections, or investigate these further, check `code/manual_corrections.py` and/or the raw correction files under `data/manual_corrections/`.


### Similarity analyses

To reproduce the algorithm similarity analyses (hierarchical clustering and MDS):

```shell
$ python code/similarity_analysis.py
```

This will use the precomputed distance matrix stored in `data/algorithm_distances.pkl` and will output:

```
visuals/results_similarity.pdf
```

To reproduce the distance matrix, uncomment the relevant line in `code/similarity_analysis.py` – this will take a little while to run. 


Building a new algorithm
------------------------

If you are building an entirely new algorithm, please also try to create a separate, minimalist implementation that conforms to the same API used here. This will greatly aid future development and benchmarking efforts. Alternatively, it may be worth discussing how the current framework could be extended to support new directions – feel free to [raise an issue](https://github.com/jwcarr/drift/issues) if you have ideas about this.

To conform to our API, an algorithm should take two inputs and maybe some optional parameters. The first input should be an array of size *n* × 2, which gives the *xy*-values of the *n* fixations, and the second should be an array of length *m*, which gives the *y*-value of each line of text (however, the second input might also be something a little different if necessary – see e.g. the `compare` and `warp` algorithms). These two inputs reflect the two objects that we are ultimately trying to bring into alignment – the fixations and the text. The output should have the same structure as the fixation input – an array of size *n* × 2, which gives the *xy*-values of the *n* fixations – except that each *y*-value will have been adjusted to the *y*-value of the relevant line of text. Thus, the general call signature of a new algorithm will look like this:

```python
def algorithm(fixation_XY, line_Y, param1=1.0, param2=True):
	...
	return fixation_XY # y-values have been modified
```

We have generally tried to name the algorithms using a short verb that is descriptive of how the algorithm acts on the fixations. Although we wouldn't want to curtail your creativity, it would be nice if you could follow this pattern 😉


Contributing
------------

If you find any bugs in the algorithms, errors in our analyses, or mistakes in our interpretation of prior works, please do report these through the [GitHub issues page](https://github.com/jwcarr/drift/issues). In addition, please free free to contribute to the discussion on this topic more generally. The best way to make progress on the issues of drift correction and line assignment is to get everyone talking and working within a unified framework.


Citing this work
----------------

If you wish to cite this work, please cite the following preprint:

Carr, J. W., Pescuma, V. N., Furlan, M., Ktori, M., & Crepaldi, D. (under review). Algorithms for the automated correction of vertical drift in eye tracking data. https://doi.org/10.31219/osf.io/jg3nc

```bibtex
@article{Carr:algorithms,
	author = {Carr, Jon W and Pescuma, Valentina N and Furlan, Michele and Ktori, Maria and Crepaldi, Davide},
	title = {Algorithms for the Automated Correction of Vertical Drift in Eye Tracking Data},
	journal = {},
	year = {},
	volume = {},
	number = {},
	pages = {},
	doi = {10.31219/osf.io/jg3nc}
}
```


License
-------

Except where otherwise noted, this repository is licensed under a Creative Commons Attribution 4.0 license. You are free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit, provide a link to the license, and indicate if changes were made. See LICENSE.md for full details.
