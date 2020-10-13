'''
Code for calculating and visualizing how well the algorithms perform
against the gold standard manual correction.
'''

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.transforms as transforms
import numpy as np
import eyekit
import globals

plt.rcParams['svg.fonttype'] = 'none' # don't convert fonts to curves in SVGs
plt.rcParams.update({'font.size': 7})

SPECIAL_ADULT = '8'
SPECIAL_KID = '204'

def percentage_match(line_assignments1, line_assignments2):
	matches = line_assignments1 == line_assignments2
	return matches.sum() / len(matches) * 100

def line_assignments(fixations):
	line_assignments = np.zeros(len(fixations), dtype=int)
	for i, fixation in enumerate(fixations.iter_with_discards()):
		if not fixation.discarded:
			line_assignments[i] = globals.y_to_line_mapping[fixation.y]
	return line_assignments

def compare_outputs(method1, method2):
	data1 = eyekit.io.read('../data/fixations/%s.json'%method1)
	data2 = eyekit.io.read('../data/fixations/%s.json'%method2)
	results = {'adults':[], 'kids':[], 'adults_IDs':[], 'kids_IDs':[]}
	for trial_id, trial in data1.items():
		line_assignments1 = line_assignments(trial['fixations'])
		line_assignments2 = line_assignments(data2[trial_id]['fixations'])
		percentage = percentage_match(line_assignments1, line_assignments2)
		if trial['age_group'] == 'adult':
			results['adults'].append(percentage)
			results['adults_IDs'].append(trial['participant_id'])
		elif trial['age_group'] == 'child':
			results['kids'].append(percentage)
			results['kids_IDs'].append(trial['participant_id'])
	return results

def calculate_improvement(results):
	improvement_results = {}
	attach_adults = np.array(results['attach']['adults'], dtype=float)
	attach_kids = np.array(results['attach']['kids'], dtype=float)
	for algorithm in globals.true_algorithms:
		assert results[algorithm]['adults_IDs'] == results['attach']['adults_IDs']
		assert results[algorithm]['kids_IDs'] == results['attach']['kids_IDs']
		alg_adults = np.array(results[algorithm]['adults'], dtype=float)
		alg_kids = np.array(results[algorithm]['kids'], dtype=float)
		improvement_adults = list(alg_adults - attach_adults)
		improvement_kids = list(alg_kids - attach_kids)
		improvement_results[algorithm] = {'adults': improvement_adults, 'kids':improvement_kids, 'adults_IDs':results[algorithm]['adults_IDs'], 'kids_IDs':results[algorithm]['kids_IDs']}
	return improvement_results

def plot_median_lines(axis, data, x_position, y_unit):
	adult_median = np.median(data['adults'])
	kid_median = np.median(data['kids'])
	offsets = ('bottom', 'top') if adult_median > kid_median else ('top', 'bottom')
	axis.plot([x_position-0.2, x_position+0.2], [adult_median, adult_median], color='black', linewidth=2)
	axis.text(x_position+0.25, adult_median, str(round(adult_median, 1)) + y_unit, ha='left', va=offsets[0], color='black', fontsize=7)
	axis.plot([x_position-0.2, x_position-0.05], [kid_median, kid_median], color='black', linewidth=2)
	axis.plot([x_position+0.05, x_position+0.2], [kid_median, kid_median], color='black', linewidth=2)
	axis.text(x_position+0.25, kid_median, str(round(kid_median, 1)) + y_unit, ha='left', va=offsets[1], color='black', fontsize=7)

def scatter_with_specials(axis, data, x_position, color, last_special_adult_result, last_special_kid_result):
	special_adult = data['adults_IDs'].index(SPECIAL_ADULT)
	special_kid = data['kids_IDs'].index(SPECIAL_KID)
	special_adult_result = data['adults'][special_adult]
	special_kid_result = data['kids'][special_kid]
	remaining_adult_results = data['adults'][:special_adult] + data['adults'][special_adult+1:]
	remaining_kid_results = data['kids'][:special_kid] + data['kids'][special_kid+1:]
	axis.scatter(np.random.normal(x_position, 0.07, len(remaining_adult_results)), remaining_adult_results, edgecolors=color, facecolors='none', s=8, linewidths=0.5)
	axis.scatter(np.random.normal(x_position, 0.07, len(remaining_kid_results)),   remaining_kid_results,   edgecolors=color, facecolors='none', s=8, linewidths=0.5, marker='^')
	axis.scatter(x_position, special_adult_result, color=color, s=8, linewidths=0.5)
	axis.scatter(x_position, special_kid_result, color=color, s=8, linewidths=0.5, marker='^')
	if last_special_adult_result:
		axis.plot([x_position-1, x_position], [last_special_adult_result, special_adult_result], color='#BBBBBB', linestyle='--', linewidth=0.5, zorder=0)
	if last_special_kid_result:
		axis.plot([x_position-1, x_position], [last_special_kid_result, special_kid_result], color='#BBBBBB', linestyle='--', linewidth=0.5, zorder=0)
	return special_adult_result, special_kid_result

def plot_legend(axis, legend_x, legend_y):
	axis.scatter([legend_x], [legend_y], marker='o', edgecolors='black', facecolors='none', s=8, linewidths=0.5, transform=axis.transAxes)
	axis.plot([legend_x+0.01, legend_x+0.04], [legend_y, legend_y], color='black', linewidth=1.5, transform=axis.transAxes)
	axis.text(legend_x+0.05, legend_y, 'Adults', ha='left', va='center', fontsize=7, transform=axis.transAxes)
	legend_y -= 0.05
	axis.scatter([legend_x], [legend_y], marker='^', edgecolors='black', facecolors='none', s=8, linewidths=0.5, transform=axis.transAxes)
	axis.plot([legend_x+0.01, legend_x+0.02125], [legend_y, legend_y], color='black', linewidth=1.5, transform=axis.transAxes)
	axis.plot([legend_x+0.02875, legend_x+0.04], [legend_y, legend_y], color='black', linewidth=1.5, transform=axis.transAxes)
	axis.text(legend_x+0.05, legend_y, 'Children', ha='left', va='center', fontsize=7, transform=axis.transAxes)

def plot_results(results, filepath, y_label, y_limits, y_unit):
	fig, axis = plt.subplots(1, 1, figsize=(6.8, 2.5))
	if y_limits[0] < 0:
		axis.plot([-1, len(results)], [0, 0], color='black', linewidth=0.5)
	special_adult, special_kid = None, None
	x_labels = []
	for x_position, (algorithm, data) in enumerate(results.items()):
		color = globals.colors[algorithm]
		special_adult, special_kid = scatter_with_specials(axis, data, x_position, color, special_adult, special_kid)
		plot_median_lines(axis, data, x_position, y_unit)
		x_labels.append(algorithm)
	plot_legend(axis, 0.87, 0.1)
	offset = (y_limits[1] - y_limits[0]) / 20
	axis.set_ylim(y_limits[0]-offset, y_limits[1]+offset)
	axis.set_xlim(-0.5, len(x_labels)-0.3)
	axis.set_xticks(list(range(len(x_labels))))
	axis.tick_params(bottom=False)
	axis.set_xticklabels(x_labels)
	axis.set_ylabel(y_label)
	fig.tight_layout(pad=0.5, h_pad=1, w_pad=1)
	fig.savefig(filepath, format='svg')
	globals.format_svg_labels(filepath, globals.algorithms)
	if not filepath.endswith('.svg'):
		globals.convert_svg(filepath, filepath)

def plot_proportion_above(axis, accuracy_results, target_accuracy=95, show_legend=False):
	prop_adults = []
	prop_kids = []
	colors = []
	for algorithm, results in accuracy_results.items():
		prop_adult = len(np.where(np.array(results['adults']) >= target_accuracy)[0]) / len(results['adults'])
		prop_kid = len(np.where(np.array(results['kids']) >= target_accuracy)[0]) / len(results['kids'])
		prop_adults.append(prop_adult)
		prop_kids.append(prop_kid)
		colors.append(globals.colors[algorithm])
	positions = np.arange(0, 27, 3)
	axis.bar(positions, prop_adults, color=colors, width=0.9)
	axis.bar(positions+1, prop_kids, color=[pseudo_alpha(color) for color in colors], width=0.9)
	axis.set_ylabel(f'Proportion of trials at {target_accuracy}% accuracy')
	axis.set_ylim(0, 1)
	axis.set_xticks(positions+1.2)
	axis.set_xticklabels(accuracy_results.keys(), rotation=45, font='Menlo', ha='right')
	axis.tick_params(bottom=False)
	if show_legend:
		axis.legend(handles=[Patch(facecolor='#000000', label='Adults'), Patch(facecolor=pseudo_alpha('#000000', 0.3), label='Children')], frameon=False, fontsize=7)

def plot_proportions(accuracy_results, filepath):
	fig, axes = plt.subplots(1, 3, figsize=(6.8, 2.5))
	for axis, target_accuracy, show_legend, letter in zip(axes, [90, 95, 99], [False, False, True], ['A', 'B', 'C']):
		plot_proportion_above(axis, accuracy_results, target_accuracy, show_legend)
		inches_from_origin = (fig.dpi_scale_trans + transforms.ScaledTranslation(0, 1, axis.transAxes))
		axis.text(0.1, -0.1, f'({letter})', fontsize=8, fontweight='bold', ha='left', va='top', transform=inches_from_origin)
	axes[1].set_yticklabels([])
	axes[2].set_yticklabels([])
	fig.tight_layout(pad=0.5, h_pad=1, w_pad=1)
	fig.savefig(filepath, format='svg')
	globals.format_svg_labels(filepath, globals.algorithms)
	if not filepath.endswith('.svg'):
		globals.convert_svg(filepath, filepath)

def pseudo_alpha(color, opacity=0.5):
	r, g, b = tuple(bytes.fromhex(color[1:]))
	rgb = r/255, g/255, b/255
	return tuple([value * opacity - opacity + 1 for value in rgb])

if __name__ == '__main__':

	accuracy_results = {algorithm : compare_outputs('gold', algorithm) for algorithm in globals.algorithms}
	improvement_results = calculate_improvement(accuracy_results)

	plot_results(accuracy_results, '../visuals/results_accuracy.pdf', 'Accuracy of algorithmic correction (%)', (0, 100), '%')
	plot_results(accuracy_results, '../manuscript/figs/fig08_double_column.eps', 'Accuracy of algorithmic correction (%)', (0, 100), '%')

	plot_results(improvement_results, '../visuals/results_improvement.pdf', 'Percentage point improvement in accuracy', (-80, 80), 'pp')
	plot_results(improvement_results, '../manuscript/figs/fig12_double_column.eps', 'Percentage point improvement in accuracy', (-80, 80), 'pp')

	plot_proportions(accuracy_results, '../visuals/results_proportion.pdf')
	plot_proportions(accuracy_results, '../manuscript/figs/fig11_double_column.eps')
