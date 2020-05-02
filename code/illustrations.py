'''
Code for producing various illustrations in the paper.
'''

import numpy as np
import matplotlib.pyplot as plt
import eyekit
from tools import unpickle
import simulation
import json

methods = ['attach', 'chain', 'cluster', 'regress', 'segment', 'warp']

y_to_line_mapping = {155:1, 219:2, 283:3, 347:4, 411:5, 475:6, 539:7, 603:8, 667:9, 731:10, 795:11, 859:12, 923:13}

cluster_colors  = ['#E85A71', '#7544D6', '#4EA1D3', '#FCBE32']

methods = [('attach', None),
           ('chain', {'x_thresh':192, 'y_thresh':32}),
           ('cluster', None),
           ('regress', {'k_bounds':(-0.1, 0.1), 'o_bounds':(-50, 50), 's_bounds':(1, 20)}),
           ('segment', {'match_theshold':99999}),
           ('warp', {'match_theshold':99999})]

def create_fixation_sequence(reading_scenario, output_file):
	fixation_sequence, true_lines = reading_scenario.generate_fixation_sequence()
	example_data = {'fixations':fixation_sequence.tolist(), 'true_lines':true_lines.tolist()}
	with open(output_file, 'w') as file:
		json.dump(example_data, file)

def load_fixation_sequence(input_file):
	with open(input_file) as file:
		example_data = json.load(file)
	return eyekit.FixationSequence(example_data['fixations']), np.array(example_data['true_lines'], dtype=int)

def run_and_visualize(passage, filename, **params):
	reading_scenario = simulation.ReadingScenario(passage, **params)
	fixation_sequence, _ = reading_scenario.generate_fixation_sequence()
	diagram = eyekit.Diagram(1920, 1080)
	diagram.render_passage(passage, 28, color='rgb(135, 135, 135)')
	diagram.render_fixations(fixation_sequence, color='black')
	diagram.save(filename, crop_to_passage=True)



def visualize_cluster(passage, fixation_sequence, output_file):
	corrected_sequence, solution = eyekit.tools.correct_vertical_drift(fixation_sequence, passage, 'cluster', copy=True, return_solution=True)
	cluster_indices, cluster_index_to_line_y = solution
	diagram = eyekit.Diagram(1920, 1080)
	diagram.render_passage(passage, 28, color='rgb(135, 135, 135)')
	for fixation, cluster_i in zip(fixation_sequence, cluster_indices):
		line_i = y_to_line_mapping[cluster_index_to_line_y[cluster_i]] - 1
		diagram.draw_arbitrary_circle(fixation.xy, 5.641895835477563, color=cluster_colors[line_i])
	diagram.save(output_file, crop_to_passage=True)

def visualize_chain(passage, fixation_sequence, output_file):
	corrected_sequence, solution = eyekit.tools.correct_vertical_drift(fixation_sequence, passage, 'chain', copy=True, return_solution=True, x_thresh=128)
	diagram = eyekit.Diagram(1920, 1080)
	diagram.render_passage(passage, 28, color='rgb(135, 135, 135)')
	for line_y, color in zip(passage.line_positions, cluster_colors):
		diagram.draw_arbitrary_line((344, line_y), (1192, line_y), color, dashed_line=True)
	prev = None
	for i, (fixation, fixation2) in enumerate(zip(fixation_sequence, corrected_sequence)):
		color = cluster_colors[y_to_line_mapping[fixation2.y]-1]
		diagram.draw_arbitrary_circle(fixation.xy, 5.641895835477563, color)
		if prev and i not in solution:
			diagram.draw_arbitrary_line(prev.xy, fixation.xy, color)
		prev = fixation
	diagram.save(output_file, crop_to_passage=True)

def visualize_attach(passage, fixation_sequence, output_file):
	corrected_sequence, solution = eyekit.tools.correct_vertical_drift(fixation_sequence, passage, 'attach', copy=True, return_solution=True)
	diagram = eyekit.Diagram(1920, 1080)
	diagram.render_passage(passage, 28, color='rgb(135, 135, 135)')
	for line_y, color in zip(passage.line_positions, cluster_colors):
		diagram.draw_arbitrary_line((344, line_y), (1192, line_y), color, dashed_line=True)
	for fixation, fixation2 in zip(fixation_sequence, corrected_sequence):
		color = cluster_colors[y_to_line_mapping[fixation2.y]-1]
		diagram.draw_arbitrary_circle(fixation.xy, 5.641895835477563, color)
		diagram.draw_arbitrary_line(fixation.xy, fixation2.xy, color)
	diagram.save(output_file, crop_to_passage=True)

def visualize_regress(passage, fixation_sequence, output_file):
	from scipy.stats import norm as _norm
	corrected_sequence, solution = eyekit.tools.correct_vertical_drift(fixation_sequence, passage, 'regress', copy=True, return_solution=True, k_bounds=methods[3][1]['k_bounds'], o_bounds=methods[3][1]['o_bounds'])
	start_points = np.array([(0, y) for y in passage.line_positions])
	(k, o, s), line_numbers = solution
	k_bounds=methods[3][1]['k_bounds']
	o_bounds=methods[3][1]['o_bounds']
	s_bounds=methods[3][1]['s_bounds']
	k = k_bounds[0] + (k_bounds[1] - k_bounds[0]) * _norm.cdf(k)
	o = o_bounds[0] + (o_bounds[1] - o_bounds[0]) * _norm.cdf(o)
	s = s_bounds[0] + (s_bounds[1] - s_bounds[0]) * _norm.cdf(s)
	start_points[:, 1] = start_points[:, 1] + o

	diagram = eyekit.Diagram(1920, 1080)
	diagram.render_passage(passage, 28, color='rgb(135, 135, 135)')
	for start_point, color in zip(start_points, cluster_colors):
		start = (344, start_point[1]+(344*k))
		end = (1192, start_point[1]+(1192*k))
		diagram.draw_arbitrary_line(start, end, color=color)
	for fixation, line_i in zip(fixation_sequence, line_numbers):
		diagram.draw_arbitrary_circle(fixation.xy, 5.641895835477563, color=cluster_colors[line_i])
		predicted_y = (fixation.x * k) + passage.line_positions[line_i] + o
		diagram.draw_arbitrary_line(fixation.xy, (fixation.x, predicted_y), color=cluster_colors[line_i])
	diagram.save(output_file, crop_to_passage=True)

def visualize_segment(passage, fixation_sequence, output_file):
	corrected_sequence, solution = eyekit.tools.correct_vertical_drift(fixation_sequence, passage, 'segment', copy=True, return_solution=True)
	diagram = eyekit.Diagram(1920, 1080)
	diagram.render_passage(passage, 28, color='rgb(135, 135, 135)')
	for i, line_change_i in enumerate(solution):
		fxn = int(line_change_i)
		diagram.draw_arbitrary_line(fixation_sequence[fxn].xy, fixation_sequence[fxn+1].xy, 'black')
	for fixation, fixation2 in zip(fixation_sequence, corrected_sequence):
		color = cluster_colors[y_to_line_mapping[fixation2.y]-1]
		diagram.draw_arbitrary_circle(fixation.xy, 5.641895835477563, color)
	diagram.save(output_file, crop_to_passage=True)

def visualize_warp(passage, fixation_sequence, output_file):
	corrected_sequence, solution = eyekit.tools.correct_vertical_drift(fixation_sequence, passage, 'warp', copy=True, return_solution=True)
	diagram = eyekit.Diagram(1920, 1080)
	diagram.render_passage(passage, 28, color='rgb(135, 135, 135)')
	for fixation, chars in zip(fixation_sequence, solution):
		for char in chars:
			char_position = passage.char_xy[char]
			color = cluster_colors[y_to_line_mapping[char_position[1]]-1]
			diagram.draw_arbitrary_circle(fixation.xy, 5.641895835477563, color)
			diagram.draw_arbitrary_line(fixation.xy, char_position, color)
	diagram.save(output_file, crop_to_passage=True)


if __name__ == '__main__':

	eyekit.set_alphabet(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

	passage = eyekit.Passage('../data/passages/lorem_ipsum_short.txt',
		                     first_character_position=(368, 155),
		                     character_spacing=16,
		                     line_spacing=64,
		                     pad_lines_with_spaces=True)

	# ALGORITHM ILLUSTRATIONS

	fixation_sequence, _ = load_fixation_sequence('../data/examples/algorithm_illustrations_simple.json')
	visualize_attach(passage, fixation_sequence, '../visuals/examples/algorithms/attach.svg')
	visualize_chain(passage, fixation_sequence, '../visuals/examples/algorithms/chain.svg')
	visualize_cluster(passage, fixation_sequence, '../visuals//examples/algorithms/cluster.svg')
	visualize_regress(passage, fixation_sequence, '../visuals/examples/algorithms/regress.svg')
	visualize_segment(passage, fixation_sequence, '../visuals/examples/algorithms/segment.svg')
	visualize_warp(passage, fixation_sequence, '../visuals/examples/algorithms/warp.svg')

	# ISOLATED PHENOMENA EXAMPLES

	run_and_visualize(passage, '../visuals/examples/phenomena/noise.svg', noise=20.0, slope=0.0, shift=0.0, regression_within=0.0, regression_between=0.0)
	run_and_visualize(passage, '../visuals/examples/phenomena/slope.svg', noise=4.0, slope=0.08, shift=0.0, regression_within=0.0, regression_between=0.0)
	run_and_visualize(passage, '../visuals/examples/phenomena/drift.svg', noise=4.0, slope=0.0, shift=0.14, regression_within=0.0, regression_between=0.0)
	run_and_visualize(passage, '../visuals/examples/phenomena/within.svg', noise=4.0, slope=0.0, shift=0.0, regression_within=0.5, regression_between=0.0)
	run_and_visualize(passage, '../visuals/examples/phenomena/between.svg', noise=4.0, slope=0.0, shift=0.0, regression_within=0.0, regression_between=0.5)
