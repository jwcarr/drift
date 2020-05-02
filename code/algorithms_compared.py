'''
Code for comparing the algorithmic outputs in an MDS and hierarchical
clustering analysis.
'''

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from scipy.spatial import distance
from scipy.cluster import hierarchy
import json
import tools

plt.rcParams['svg.fonttype'] = 'none' # don't convert fonts to curves in SVGs
plt.rcParams.update({'font.size': 7})

y_to_line_mapping = {155:1, 219:2, 283:3, 347:4, 411:5, 475:6, 539:7, 603:8, 667:9, 731:10, 795:11, 859:12, 923:13}

methods = ['attach',  'chain',   'cluster', 'regress', 'segment', 'warp',    'gold']
colors  = ['#6B6B7F', '#E85A71', '#4EA1D3', '#FCBE32', '#17A363', '#7544D6', '#B0944B']

def prop_mismatch(line_assignments1, line_assignments2):
	matches = line_assignments1 == line_assignments2
	return matches.sum() / len(matches)

def line_assignments(fixations):
	line_assignments = np.zeros(len(fixations), dtype=int)
	for i, fixation in enumerate(fixations):
		if fixation[3] == False:
			line_assignments[i] = y_to_line_mapping[fixation[1]]
	return line_assignments

def compare_outputs(method1, method2):
	with open('../data/fixations/%s.json'%method1) as file:
		data1 = json.load(file)
	with open('../data/fixations/%s.json'%method2) as file:
		data2 = json.load(file)
	results = []
	for passage_id, participant_data in data1.items():
		for participant_id, fixations in participant_data.items():
			line_assignments1 = line_assignments(fixations)
			line_assignments2 = line_assignments(data2[passage_id][participant_id])
			prop = prop_mismatch(line_assignments1, line_assignments2)
			dist = 1 - prop
			results.append(dist)
	return np.median(results)

def min_max_normalize(positions):
	for i in range(positions.shape[1]):
		positions[:, i] = (positions[:, i] - positions[:, i].min()) / (positions[:, i].max() - positions[:, i].min())
	return positions

def compute_distance_matrix(methods):
	distances = []
	for i in range(len(methods)):
		for j in range(i+1, len(methods)):
			d = compare_outputs(methods[i], methods[j])
			distances.append(d)
	return distance.squareform(distances, 'tomatrix')

def plot_tree(node, axis, x=0, y=0, min_x=0, max_x=0, min_y=0):
	min_x = min(x-1, min_x)
	max_x = max(x+1, max_x)
	min_y = min(y-1, min_y)
	double_leaved = False
	axis.scatter([x], [y], c='black')
	left = node.get_left()
	right = node.get_right()
	if left.is_leaf():
		axis.scatter([x-1], [y-1], c=colors[left.get_id()])
		axis.annotate(methods[left.get_id()], (x-1, y-1.2), va='top', ha='center', fontsize=7)
	else:
		double_leaved, min_x, max_x, min_y = plot_tree(left, axis, x-1, y-1, min_x, max_x, min_y)
	if double_leaved and not right.is_leaf():
		axis.plot([x-1, x, x+1, x+1], [y-1, y, y-1, y-2], c='black', zorder=0)
		y -= 1
	else:
		axis.plot([x-1, x, x+1], [y-1, y, y-1], c='black', zorder=0)
	if right.is_leaf():
		axis.scatter([x+1], [y-1], c=colors[right.get_id()])
		axis.annotate(methods[right.get_id()], (x+1, y-1.2), va='top', ha='center', fontsize=7)
	else:
		_, min_x, max_x, min_y = plot_tree(right, axis, x+1, y-1, min_x, max_x, min_y)
	return left.is_leaf() and right.is_leaf(), min_x, max_x, min_y

def plot_analyses(filepath):

	fig, axes = plt.subplots(1, 2, figsize=(5.5, 2.5))

	algorithm_distances = compute_distance_matrix(methods[:-1])

	linkage = hierarchy.linkage(distance.squareform(algorithm_distances, 'tovector'))
	tree = hierarchy.to_tree(linkage)
	_, min_x, max_x, min_y = plot_tree(tree, axes[0])
	axes[0].set_xlim(min_x-0.75, max_x+0.75)
	axes[0].set_ylim(min_y-0.75, 0.25)
	axes[0].set_xticks([])
	axes[0].set_yticks([])

	algorithm_distances = compute_distance_matrix(methods)
	solution = MDS(dissimilarity='precomputed', n_components=2, n_init=25, max_iter=2000, random_state=100)
	positions = solution.fit_transform(algorithm_distances)
	positions = min_max_normalize(positions)
	mn, mx = positions[:, 0].min(), positions[:, 0].max()
	offset = (mx - mn) * 0.1
	furthest_method_to_right = methods[np.argmax(positions[:, 0])]
	axes[1].scatter(positions[:, 0], positions[:, 1], color=colors)
	for label, position in zip(methods, positions):
		if label == furthest_method_to_right:
			axes[1].text(position[0]-offset/2, position[1], label, va='center', ha='right')
		else:
			axes[1].text(position[0]+offset/2, position[1], label, va='center', ha='left')
	axes[1].set_xlim(mn-offset, mx+offset)
	mn, mx = positions[:, 1].min(), positions[:, 1].max()
	offset = (mx - mn) * 0.1
	axes[1].set_ylim(mn-offset, mx+offset)
	axes[1].set_xticks([])
	axes[1].set_yticks([])

	arrow_offset = 0.05
	arrow_length = 0.4
	axes[1].arrow(0, arrow_offset, 0, arrow_length, width=0.01, color='black')
	axes[1].text(arrow_offset, arrow_offset+arrow_length/2, 'position–order', ha='center', va='center', rotation=90)
	axes[1].arrow(arrow_offset, 0, arrow_length, 0, width=0.01, color='black')
	axes[1].text(arrow_offset+arrow_length/2, arrow_offset, 'global–local', ha='center', va='center')

	fig.tight_layout(pad=0.1, h_pad=0.5, w_pad=0.5)
	fig.savefig(filepath, format='svg')
	tools.format_svg_labels(filepath, monospace=['attach', 'chain', 'cluster', 'regress', 'segment', 'warp'], arbitrary_replacements={'gold':'Gold standard'})
	if not filepath.endswith('.svg'):
		tools.convert_svg(filepath, filepath)

if __name__ == '__main__':

	# plot_analyses('../visuals/analysis.pdf')
	plot_analyses('../manuscript/figs/analysis.eps')
