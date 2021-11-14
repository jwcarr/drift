'''
Code for running the algorithms over the sample data
'''

import eyekit
import algorithms
import core

def run_algorithm(sample_data, passages, output_dir, method):
	print(method.upper())
	output_data = {}
	for trial_id, trial in sample_data.items():
		print('-', trial_id)
		new_trial = {'participant_id':trial['participant_id'], 'age_group':trial['age_group'], 'passage_id':trial['passage_id'], 'fixations':[]}
		fixation_XY = [fixation.xy for fixation in trial['fixations']]
		correction = algorithms.correct_drift(method, fixation_XY, passages[trial['passage_id']])
		for fixation, (_, y) in zip(trial['fixations'], correction):
			new_trial['fixations'].append((fixation.x, int(y), fixation.start, fixation.end, fixation.discarded))
		new_trial['fixations'] = eyekit.FixationSequence(new_trial['fixations'])
		output_data[trial_id] = new_trial
	eyekit.io.save(output_data, output_dir / f'{method}.json', compress=True)


if __name__ == '__main__':

	sample_data = eyekit.io.load(core.FIXATIONS / 'sample.json')
	passages = eyekit.io.load(core.DATA / 'passages.json')

	for method in core.algorithms:
		run_algorithm(sample_data, passages, core.FIXATIONS, method)
