'''
Code for running the algorithms over the sample data
'''

import numpy as np
import eyekit
import algorithms
import globals

def run_algorithm(sample_data, passages, output_dir, method):
	print(method.upper())
	output_data = {}
	for trial_id, trial in sample_data.items():
		print('-', trial_id)
		new_trial = {'participant_id':trial['participant_id'], 'age_group':trial['age_group'], 'passage_id':trial['passage_id'], 'fixations':[]}
		fixation_XY = trial['fixations'].XYarray(include_discards=True)
		correction = algorithms.correct_drift(method, fixation_XY, passages[trial['passage_id']])
		for fixation, (_, y) in zip(trial['fixations'], correction):
			new_trial['fixations'].append((fixation.x, int(y), fixation.duration, fixation.discarded))
		output_data[trial_id] = new_trial
	eyekit.io.write(output_data, output_dir + '%s.json' % method)


if __name__ == '__main__':

	sample_data = eyekit.io.read('../data/fixations/sample.json')
	passages = eyekit.io.load_texts('../data/passages.json')

	for method in globals.algorithms:
		run_algorithm(sample_data, passages, '../data/fixations/', method)
