'''
Code for performing the fixation sequence simulations.
'''

import numpy as np
import eyekit
from tools import pickle

methods = [('attach', {}),
           ('chain', {'x_thresh':192, 'y_thresh':32}),
           ('cluster', {}),
           ('regress', {'k_bounds':(-0.1, 0.1), 'o_bounds':(-50, 50), 's_bounds':(1, 20)}),
           ('segment', {'match_threshold':9999}),
           ('warp', {'match_threshold':9999})]

factors = {'noise':(0, 40), 'slope':(-0.1, 0.1), 'drift':(-0.2, 0.2), 'regression_within':(0, 1), 'regression_across':(0, 1)}

class ReadingScenario:

	def __init__(self, passage, noise=0, slope=0, drift=0, regression_within=0, regression_across=0):
		self.passage = passage
		self.noise = noise
		self.slope = slope
		self.drift = drift
		self.regression_within = regression_within
		self.regression_across = regression_across
		self.x_margin, self.y_margin = self.passage.first_character_position
		self.max_line_width = self.passage.character_spacing * self.passage.n_cols

	def _generate_line_sequence(self, line_i, partial_reading=False, inherited_line_y_for_drift=None):
		if partial_reading:
			start_point = np.random.randint(0, self.max_line_width//2) + self.x_margin
			end_point = np.random.randint(self.max_line_width//2, self.max_line_width) + self.x_margin
		else:
			start_point = self.x_margin
			end_point = self.max_line_width + self.x_margin
		line_X = []
		for word_i, word in enumerate(self.passage.iter_words(line_n=line_i)):
			x_word_center = word[0].x + ((word[-1].x - word[0].x) / 2)
			if x_word_center < start_point or x_word_center > end_point:
				continue
			x_value = int(np.random.triangular(word[0].x, x_word_center, word[-1].x+1))
			line_X.append(x_value)
			if word_i > 0 and np.random.random() < self.regression_within:
				x_regression = int(np.random.triangular(self.x_margin, word[0].x, word[0].x))
				line_X.append(x_regression)
		line_X = np.array(line_X, dtype=int) - self.x_margin
		line_y = self.passage.line_positions[line_i] - self.y_margin
		line_Y = np.random.normal(line_y, self.noise, len(line_X))
		line_Y += line_X * self.slope
		if inherited_line_y_for_drift:
			line_Y += (inherited_line_y_for_drift-self.y_margin) * self.drift
		else:
			line_Y += line_y * self.drift
		line_Y = np.array(list(map(round, line_Y)), dtype=int)
		return line_X+self.x_margin, line_Y+self.y_margin, [line_i]*len(line_X)

	def generate_fixation_sequence(self):
		'''
		Given a passage, generate a fixation sequence with certain noise,
		slope, and drift characteristics. Returns both the fixation sequence
		and the "correct" lines numbers for each fixation.
		'''
		X, Y, I = [], [], []
		for line_i, line_y in enumerate(self.passage.line_positions):
			line_X, line_Y, line_I = self._generate_line_sequence(line_i)
			X.extend(line_X)
			Y.extend(line_Y)
			I.extend(line_I)
			if line_i > 0 and np.random.random() < self.regression_across:
				rand_prev_line = int(np.random.triangular(0, line_i, line_i))
				rand_insert_point = np.random.randint(1, len(line_X)-1)
				regression = self._generate_line_sequence(rand_prev_line, partial_reading=True, inherited_line_y_for_drift=line_y)
				for rx, ry, ri in zip(*regression):
					X.insert(-rand_insert_point, rx)
					Y.insert(-rand_insert_point, ry)
					I.insert(-rand_insert_point, ri)
		fixation_sequence = eyekit.FixationSequence([(x, y, 100) for x, y in zip(X, Y)])
		return fixation_sequence, np.array(I, dtype=int)


def simulate_factor(passage, factor, n_gradations, n_sims):
	line_positions = list(passage.line_positions)
	results = np.zeros((len(methods), n_gradations, n_sims), dtype=float)
	factor_min, factor_max = factors[factor]
	for gradation_i, factor_value in enumerate(np.linspace(factor_min, factor_max, n_gradations)):
		reading_scenario = ReadingScenario(passage, **{factor:factor_value})
		for method_i, (method, params) in enumerate(methods):
			for sim_i in range(n_sims):
				fixation_sequence, true_line_numbers = reading_scenario.generate_fixation_sequence()
				eyekit.tools.correct_vertical_drift(fixation_sequence, passage, method, **params)
				pred_line_numbers = np.array([line_positions.index(fixation.y) for fixation in fixation_sequence], dtype=int)
				matches = true_line_numbers == pred_line_numbers
				results[method_i][gradation_i][sim_i] = matches.sum() / len(matches)
	return results


if __name__ == '__main__':

	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('factor', action='store', type=str, help='factor to simulate')
	parser.add_argument('output_dir', action='store', type=str, help='directory to write results to')
	parser.add_argument('--n_gradations', action='store', type=int, default=30, help='number of gradations in factor')
	parser.add_argument('--n_sims', action='store', type=int, default=100, help='number of simulations per method/gradation')
	args = parser.parse_args()

	passage = eyekit.Passage('../data/passages/lorem_ipsum.txt',
		                     first_character_position=(368, 155),
		                     character_spacing=16,
		                     line_spacing=64)
	results = simulate_factor(passage, args.factor, args.n_gradations, args.n_sims)
	pickle(results, '%s/%s.pkl' % (args.output_dir, args.factor))
