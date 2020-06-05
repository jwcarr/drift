'''
Code for calculating and visualizing how well the algorithms perform
against the gold standard manual correction.
'''

import matplotlib.pyplot as plt
import numpy as np
import json
import tools
import defaults

plt.rcParams['svg.fonttype'] = 'none' # don't convert fonts to curves in SVGs
plt.rcParams.update({'font.size': 7})


def percentage_match(line_assignments1, line_assignments2):
	matches = line_assignments1 == line_assignments2
	return matches.sum() / len(matches) * 100

def line_assignments(fixations):
	line_assignments = np.zeros(len(fixations), dtype=int)
	for i, fixation in enumerate(fixations):
		if fixation[3] == False:
			line_assignments[i] = defaults.y_to_line_mapping[fixation[1]]
	return line_assignments

def compare_outputs(method1, method2):
	with open('../data/fixations/%s.json'%method1) as file:
		data1 = json.load(file)
	with open('../data/fixations/%s.json'%method2) as file:
		data2 = json.load(file)
	results = {'adults':[], 'kids':[], 'adults_IDs':[], 'kids_IDs':[]}
	IDs = []
	for passage_id, participant_data in data1.items():
		for participant_id, fixations in participant_data.items():
			line_assignments1 = line_assignments(fixations)
			line_assignments2 = line_assignments(data2[passage_id][participant_id])
			percentage = percentage_match(line_assignments1, line_assignments2)
			if int(participant_id) > 100:
				results['kids'].append(percentage)
				results['kids_IDs'].append(participant_id)
			else:
				results['adults'].append(percentage)
				results['adults_IDs'].append(participant_id)
			IDs.append(participant_id)
	return results, IDs

def calculate_improvement(results):
	improvement_results = {}
	attach_adults = np.array(results['attach']['adults'], dtype=float)
	attach_kids = np.array(results['attach']['kids'], dtype=float)
	for algorithm in defaults.true_algorithms:
		assert results[algorithm]['adults_IDs'] == results['attach']['adults_IDs']
		assert results[algorithm]['kids_IDs'] == results['attach']['kids_IDs']
		alg_adults = np.array(results[algorithm]['adults'], dtype=float)
		alg_kids = np.array(results[algorithm]['kids'], dtype=float)
		improvement_adults = list(alg_adults - attach_adults)
		improvement_kids = list(alg_kids - attach_kids)
		improvement_results[algorithm] = {'adults': improvement_adults, 'kids':improvement_kids, 'adults_IDs':results[algorithm]['adults_IDs'], 'kids_IDs':results[algorithm]['kids_IDs']}
	return improvement_results

def plot_accuracy(results, filepath):
	fig, axis = plt.subplots(1, 1, figsize=(6.8, 2.5))
	last_special_adult_result, last_special_kid_result = None, None
	for algorithm, data in results.items():
		i = defaults.algorithms.index(algorithm)

		special_adult = data['adults_IDs'].index('8')
		special_kid = data['kids_IDs'].index('204')
		special_adult_result = data['adults'][special_adult]
		special_kid_result = data['kids'][special_kid]
		remaining_adult_results = data['adults'][:special_adult] + data['adults'][special_adult+1:]
		remaining_kid_results = data['kids'][:special_kid] + data['kids'][special_kid+1:]

		axis.scatter(np.random.normal(i, 0.075, len(remaining_adult_results)), remaining_adult_results, edgecolors=defaults.colors[algorithm], facecolors='none', s=8, linewidths=0.5)
		axis.scatter(np.random.normal(i, 0.075, len(remaining_kid_results)),   remaining_kid_results,   edgecolors=defaults.colors[algorithm], facecolors='none', s=8, linewidths=0.5, marker='^')
		axis.scatter(i, special_adult_result, color=defaults.colors[algorithm], s=8)
		axis.scatter(i, special_kid_result, color=defaults.colors[algorithm], s=8, marker='^')

		if last_special_adult_result:
			axis.plot([i-1, i], [last_special_adult_result, special_adult_result], color='#BBBBBB', linestyle='--', linewidth=0.5, zorder=0)
		if last_special_kid_result:
			axis.plot([i-1, i], [last_special_kid_result, special_kid_result], color='#BBBBBB', linestyle='--', linewidth=0.5, zorder=0)

		median = np.median(data['adults'] + data['kids'])
		axis.plot([i-0.185, i+0.185], [median, median], color='black', linewidth=2)
		axis.text(i+0.25, median, str(round(median, 1)) + '%', ha='left', va='center', color='black', fontsize=7)

		last_special_adult_result, last_special_kid_result = special_adult_result, special_kid_result

	axis.set_ylabel('Accuracy of algorithmic correction (%)')
	axis.set_ylim(-5, 105)
	axis.set_xlim(-0.5, i+0.7)
	axis.set_xticks(list(range(len(results))))
	axis.tick_params(bottom=False)
	axis.set_xticklabels(defaults.algorithms)
	fig.tight_layout(pad=0.1, h_pad=0.5, w_pad=0.5)
	fig.savefig(filepath, format='svg')
	tools.format_svg_labels(filepath, defaults.algorithms)
	if not filepath.endswith('.svg'):
		tools.convert_svg(filepath, filepath)

def plot_accuracy_improvement(results, filepath):
	fig, axis = plt.subplots(1, 1, figsize=(6.8, 2.5))
	axis.plot([-1, len(results)+1], [0, 0], color='black', linewidth=1, zorder=0)
	last_special_adult_result, last_special_kid_result = None, None
	for algorithm, data in results.items():
		i = defaults.algorithms.index(algorithm)

		special_adult = data['adults_IDs'].index('8')
		special_kid = data['kids_IDs'].index('204')
		special_adult_result = data['adults'][special_adult]
		special_kid_result = data['kids'][special_kid]
		remaining_adult_results = data['adults'][:special_adult] + data['adults'][special_adult+1:]
		remaining_kid_results = data['kids'][:special_kid] + data['kids'][special_kid+1:]

		axis.scatter(np.random.normal(i, 0.075, len(remaining_adult_results)), remaining_adult_results, edgecolors=defaults.colors[algorithm], facecolors='none', s=8, linewidths=0.5)
		axis.scatter(np.random.normal(i, 0.075, len(remaining_kid_results)),   remaining_kid_results,   edgecolors=defaults.colors[algorithm], facecolors='none', s=8, linewidths=0.5, marker='^')
		axis.scatter(i, special_adult_result, color=defaults.colors[algorithm], s=8, linewidths=0.5)
		axis.scatter(i, special_kid_result, color=defaults.colors[algorithm], s=8, linewidths=0.5, marker='^')

		if last_special_adult_result:
			axis.plot([i-1, i], [last_special_adult_result, special_adult_result], color='gray', linestyle='--', linewidth=0.5, zorder=0)
		if last_special_kid_result:
			axis.plot([i-1, i], [last_special_kid_result, special_kid_result], color='gray', linestyle='--', linewidth=0.5, zorder=0)

		median = np.median(data['adults'] + data['kids'])
		axis.plot([i-0.185, i+0.185], [median, median], color='black', linewidth=2)
		axis.text(i+0.25, median, str(round(median, 1)) + 'pp', ha='left', va='bottom', color='black', fontsize=7)

		last_special_adult_result, last_special_kid_result = special_adult_result, special_kid_result

	axis.set_ylabel('Percentage point improvement in accuracy')
	axis.set_ylim(-88, 88)
	axis.set_xlim(0.5, i+0.7)
	axis.set_xticks(list(range(1, len(results)+1)))
	axis.tick_params(bottom=False)
	axis.set_xticklabels(defaults.true_algorithms)
	fig.tight_layout(pad=0.1, h_pad=0.5, w_pad=0.5)
	fig.savefig(filepath, format='svg')
	tools.format_svg_labels(filepath, defaults.algorithms)
	if not filepath.endswith('.svg'):
		tools.convert_svg(filepath, filepath)


if __name__ == '__main__':

	results = {}
	for algorithm in defaults.algorithms:
		alg_results, IDs = compare_outputs('gold', algorithm)
		results[algorithm] = alg_results

	plot_accuracy(results, '../visuals/results_accuracy.pdf')
	plot_accuracy(results, '../manuscript/figs/results_accuracy.eps')

	improvement_results = calculate_improvement(results)

	plot_accuracy_improvement(improvement_results, '../visuals/results_improvement.pdf')
	plot_accuracy_improvement(improvement_results, '../manuscript/figs/results_improvement.eps')
