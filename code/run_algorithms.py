'''
Code for running the algorithms over the sample data
'''

from collections import defaultdict
import json
import eyekit
import tools

methods = [('attach', {}),
           ('chain', {'x_thresh':192, 'y_thresh':32}),
           ('cluster', {}),
           ('regress', {'k_bounds':(-0.1, 0.1), 'o_bounds':(-50, 50), 's_bounds':(1, 20)}),
           ('segment', {'match_threshold':9999}),
           ('warp', {'match_threshold':9999})]

def run_algorithm(sample_data, passages, output_dir, method, **params):
	print(method.upper())
	output_data = defaultdict(dict)
	for passage_id, participant_data in sample_data.items():
		print(passage_id)
		for participant_id, fixations in participant_data.items():
			print('-', participant_id)
			fixation_sequence = eyekit.FixationSequence(fixations)
			eyekit.tools.correct_vertical_drift(fixation_sequence, passages[passage_id], method, **params)
			output_data[passage_id][participant_id] = fixation_sequence.tolist()
	with open(output_dir + '%s.json' % method, 'w') as file:
		json.dump(output_data, file)


if __name__ == '__main__':

	sample_file = '../data/fixations/sample.json'
	with open(sample_file) as file:
		sample_data = json.load(file)

	passages = tools.load_passages('../data/passages/')

	for method, params in methods:
		run_algorithm(sample_data, passages, '../data/fixations/', method, **params)