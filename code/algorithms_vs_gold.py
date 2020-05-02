'''
Code for calculating and visualizing how well the algorithms perform
against the gold standard manual correction.
'''

import matplotlib.pyplot as plt
import numpy as np
import json
import tools

plt.rcParams['svg.fonttype'] = 'none' # don't convert fonts to curves in SVGs
plt.rcParams.update({'font.size': 7})

algorithms = ['attach', 'chain', 'cluster', 'regress', 'segment', 'warp']
colors  = ['#6B6B7F', '#E85A71', '#4EA1D3', '#FCBE32', '#17A363', '#7544D6', '#6172D4']

y_to_line_mapping = {155:1, 219:2, 283:3, 347:4, 411:5, 475:6, 539:7, 603:8, 667:9, 731:10, 795:11, 859:12, 923:13}

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
	results = {'adults':[], 'kids':[]}
	IDs = []
	for passage_id, participant_data in data1.items():
		for participant_id, fixations in participant_data.items():
			line_assignments1 = line_assignments(fixations)
			line_assignments2 = line_assignments(data2[passage_id][participant_id])
			prop = prop_mismatch(line_assignments1, line_assignments2)
			if int(participant_id) > 100:
				results['kids'].append(prop)
			else:
				results['adults'].append(prop)
			IDs.append(participant_id)
	return results, IDs

def plot_accuracy(results, filepath):
	fig, axis = plt.subplots(1, 1, figsize=(6.8, 2.5))
	for algorithm, data in results.items():
		i = algorithms.index(algorithm)
		axis.scatter(np.random.normal(i, 0.075, len(data['adults'])), data['adults'], color=colors[i], s=6)
		axis.scatter(np.random.normal(i, 0.075, len(data['kids'])), data['kids'], color=colors[i], s=6, marker='^')
		median_a = np.median(data['adults'])
		median_k = np.median(data['kids'])
		axis.plot([i-0.185, i+0.185], [median_a, median_a], color='black', linewidth=2)
		axis.plot([i-0.2, i+0.2], [median_k, median_k], color='black', linewidth=2, linestyle=':')
		axis.text(i+0.25, median_a, str(round(median_a*100, 1)) + '%', ha='left', va='bottom', color='black', fontsize=7)
		axis.text(i+0.25, median_k, str(round(median_k*100, 1)) + '%', ha='left', va='top', color='black', fontsize=7)
	axis.set_ylabel('Accuracy of algorithmic correction')
	axis.set_ylim(-0.05, 1.05)
	axis.set_xlim(-0.5, i+0.7)
	axis.set_xticks(list(range(len(results))))
	axis.tick_params(bottom=False)
	axis.set_xticklabels(algorithms)
	fig.tight_layout(pad=0.1, h_pad=0.5, w_pad=0.5)
	fig.savefig(filepath, format='svg')
	tools.format_svg_labels(filepath, algorithms)
	if not filepath.endswith('.svg'):
		tools.convert_svg(filepath, filepath)


if __name__ == '__main__':

	results = {}
	for algorithm in algorithms:
		alg_results, IDs = compare_outputs('gold', algorithm)
		results[algorithm] = alg_results

	# plot_accuracy(results, '../visuals/algorithms_vs_gold.pdf')
	plot_accuracy(results, '../manuscript/figs/algorithms_vs_gold.eps')
