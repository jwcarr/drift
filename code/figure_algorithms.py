import numpy as np
import eyekit
import algorithms
import globals

def visualize_attach(passage, fixation_sequence):
	corrected_sequence, solution = algorithms.correct_drift('attach', fixation_sequence.XYarray(), passage, return_solution=True)
	corrected_sequence = eyekit.FixationSequence(corrected_sequence)
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	for fixation, fixation2 in zip(fixation_sequence, corrected_sequence):
		color = globals.illustration_colors[globals.y_to_line_mapping[fixation2.y]-1]
		diagram.draw_circle(*fixation.xy, 5.641895835477563, color=None, fill_color=color)
		diagram.draw_line(fixation.xy, fixation2.xy, color=color, stroke_width=2)
	diagram.set_caption('attach', font_face='Menlo', font_size=8)
	return diagram

def visualize_chain(passage, fixation_sequence):
	corrected_sequence, solution = algorithms.correct_drift('chain', fixation_sequence.XYarray(), passage, return_solution=True, x_thresh=100)
	corrected_sequence = eyekit.FixationSequence(corrected_sequence)
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	prev = None
	for i, (fixation, fixation2) in enumerate(zip(fixation_sequence, corrected_sequence)):
		color = globals.illustration_colors[globals.y_to_line_mapping[fixation2.y]-1]
		diagram.draw_circle(*fixation.xy, 5.641895835477563, color=None, fill_color=color)
		if prev and i not in solution:
			diagram.draw_line(prev.xy, fixation.xy, color, stroke_width=2)
		prev = fixation
	diagram.set_caption('chain', font_face='Menlo', font_size=8)
	return diagram

def visualize_cluster(passage, fixation_sequence):
	corrected_sequence, solution = algorithms.correct_drift('cluster', fixation_sequence.XYarray(), passage, return_solution=True)
	corrected_sequence = eyekit.FixationSequence(corrected_sequence)
	clusters, ordered_cluster_indices = solution
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	for fixation, cluster_i in zip(fixation_sequence, clusters):
		line_i = ordered_cluster_indices.index(cluster_i)
		diagram.draw_circle(*fixation.xy, 5.641895835477563, color=None, fill_color=globals.illustration_colors[line_i])
	for line_i, cluster_i in enumerate(ordered_cluster_indices):
		fixations_in_cluster = np.where(clusters == cluster_i)[0]
		y_values = [fixation_sequence[int(f)].y for f in fixations_in_cluster]
		mn, mx = min(y_values), max(y_values)
		diagram.draw_rectangle(344, mn, 656, mx-mn, color=globals.illustration_colors[line_i], dashed=True)
	diagram.set_caption('cluster', font_face='Menlo', font_size=8)
	return diagram

def visualize_compare(passage, fixation_sequence):
	_, solution = algorithms.correct_drift('compare', fixation_sequence.XYarray(), passage, return_solution=True, x_thresh=300)
	word_XY = passage.word_centers
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	gaze_line = solution[0][0]
	text_lines = solution[0][1]
	warp_paths = solution[0][2]
	line_costs = solution[0][3]
	for color_i, (text_line, warp_path) in enumerate(zip(text_lines, warp_paths)):
		for fixation, mapped_words in zip(gaze_line, warp_path):
			for word_i in mapped_words:
				word_x, word_y = text_line[word_i]
				# diagram.draw_circle(word_x, word_y, 5.641895835477563, color=None, fill_color='gray')
				diagram.draw_line(tuple(fixation), (word_x, fixation[1]), color=globals.illustration_colors[color_i], stroke_width=2)
		for fixation in gaze_line:
			diagram.draw_circle(*tuple(fixation), 5.641895835477563, color=None, fill_color='black')
		diagram.draw_annotation(950, text_line[0][1], str(int(line_costs[color_i])), color=globals.illustration_colors[color_i], font_size=30, font_face='Helvetica Neue bold')
		gaze_line[:, 1] += 64
	diagram.set_caption('compare', font_face='Menlo', font_size=8)
	return diagram

def visualize_merge(passage, fixation_sequence):
	corrected_sequence, solution = algorithms.correct_drift('merge', fixation_sequence.XYarray(), passage, return_solution=True)
	corrected_sequence = eyekit.FixationSequence(corrected_sequence)
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	for line_i, sequence in solution.items():
		color = globals.illustration_colors[line_i]
		diagram.draw_circle(*fixation_sequence[sequence[0]].xy, 5.641895835477563, color=None, fill_color=color)
		for i in range(1, len(sequence)):
			diagram.draw_line(fixation_sequence[sequence[i-1]].xy, fixation_sequence[sequence[i]].xy, color, stroke_width=2)
			diagram.draw_circle(*fixation_sequence[sequence[i]].xy, 5.641895835477563, color=None, fill_color=color)
		fixation_XY = fixation_sequence.XYarray()[sequence]
		k, intercept = np.polyfit(fixation_XY[:, 0], fixation_XY[:, 1], 1)
		start = (344, intercept+(344*k))
		end = (1000, intercept+(1000*k))
		diagram.draw_line(start, end, color=color, dashed=True, stroke_width=2)
	diagram.set_caption('merge', font_face='Menlo', font_size=8)
	return diagram

def visualize_regress(passage, fixation_sequence):
	corrected_sequence, solution = algorithms.correct_drift('regress', fixation_sequence.XYarray(), passage, return_solution=True)
	corrected_sequence = eyekit.FixationSequence(corrected_sequence)
	start_points = np.array([(0, y) for y in passage.line_positions])
	(k, o, s), line_numbers = solution
	start_points[:, 1] = start_points[:, 1] + o
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	for start_point, color in zip(start_points, globals.illustration_colors):
		start = (344, start_point[1]+(344*k))
		end = (1000, start_point[1]+(1000*k))
		diagram.draw_line(start, end, color=color, dashed=True, stroke_width=2)
	for fixation, line_i in zip(fixation_sequence, line_numbers):
		diagram.draw_circle(*fixation.xy, 5.641895835477563, color=None, fill_color=globals.illustration_colors[line_i])
		predicted_y = (fixation.x * k) + passage.line_positions[line_i] + o
		diagram.draw_line(fixation.xy, (fixation.x, predicted_y), color=globals.illustration_colors[line_i], stroke_width=2)
	diagram.set_caption('regress', font_face='Menlo', font_size=8)
	return diagram

def visualize_segment(passage, fixation_sequence):
	corrected_sequence, solution = algorithms.correct_drift('segment', fixation_sequence.XYarray(), passage, return_solution=True)
	corrected_sequence = eyekit.FixationSequence(corrected_sequence)
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	for i, line_change_i in enumerate(solution):
		fxn = int(line_change_i)
		diagram.draw_line(fixation_sequence[fxn].xy, fixation_sequence[fxn+1].xy, 'black', stroke_width=2)
	for fixation, fixation2 in zip(fixation_sequence, corrected_sequence):
		color = globals.illustration_colors[globals.y_to_line_mapping[fixation2.y]-1]
		diagram.draw_circle(*fixation.xy, 5.641895835477563, color=None, fill_color=color)
	diagram.set_caption('segment', font_face='Menlo', font_size=8)
	return diagram

def visualize_split(passage, fixation_sequence):
	corrected_sequence, solution = algorithms.correct_drift('split', fixation_sequence.XYarray(), passage, return_solution=True)
	corrected_sequence = eyekit.FixationSequence(corrected_sequence)
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	for i, line_change_i in enumerate(solution[:-1]):
		fxn = int(line_change_i) - 1
		diagram.draw_line(fixation_sequence[fxn].xy, fixation_sequence[fxn+1].xy, 'black', stroke_width=2)
	for fixation, fixation2 in zip(fixation_sequence, corrected_sequence):
		color = globals.illustration_colors[globals.y_to_line_mapping[fixation2.y]-1]
		diagram.draw_circle(*fixation.xy, 5.641895835477563, color=None, fill_color=color)
	diagram.set_caption('split', font_face='Menlo', font_size=8)
	return diagram

def visualize_warp(passage, fixation_sequence):
	_, solution = algorithms.correct_drift('warp', fixation_sequence.XYarray(), passage, return_solution=True)
	word_XY = np.array(passage.word_centers, dtype=int)
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	# for word in passage.word_centers:
		# diagram.draw_circle(*word, 5.641895835477563, color=None, fill_color='gray')
	for fixation, mapped_words in zip(fixation_sequence, solution):
		for word_i in mapped_words:
			word_x, word_y = word_XY[word_i]
			color = globals.illustration_colors[globals.y_to_line_mapping[word_y]-1]
			diagram.draw_circle(*fixation.xy, 5.641895835477563, color=None, fill_color=color)
			diagram.draw_line(fixation.xy, (word_x, word_y), color, stroke_width=2)
	diagram.set_caption('warp', font_face='Menlo', font_size=8)
	return diagram


passage = eyekit.TextBlock(globals.lorem_ipsum_text, position=(360, 161), font_face='Courier New', font_size=26.667, line_height=64)
fixation_sequence = eyekit.FixationSequence(globals.lorem_ipsum_XY)

fig = eyekit.vis.Figure(3, 3)

fig.add_image(visualize_attach(passage, fixation_sequence))
fig.add_image(visualize_chain(passage, fixation_sequence))
fig.add_image(visualize_cluster(passage, fixation_sequence))
fig.add_image(visualize_compare(passage, fixation_sequence))
fig.add_image(visualize_merge(passage, fixation_sequence))
fig.add_image(visualize_regress(passage, fixation_sequence))
fig.add_image(visualize_segment(passage, fixation_sequence))
fig.add_image(visualize_split(passage, fixation_sequence))
fig.add_image(visualize_warp(passage, fixation_sequence))
fig.set_lettering(font_face='Helvetica Neue bold', font_size=8)
fig.set_crop_margin(2)
fig.save('../visuals/illustration_algorithms.pdf', 174)
fig.save('../manuscript/figs/fig02_double_column.eps', 174)
