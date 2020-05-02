'''
Code for plotting the simulation results.
'''

import numpy as np
import matplotlib.pyplot as plt
import eyekit
import tools

plt.rcParams['svg.fonttype'] = 'none' # don't convert fonts to curves in SVGs
plt.rcParams.update({'font.size': 7})

methods = ['attach',  'chain',   'cluster', 'regress', 'segment', 'warp']
colors  = ['#6B6B7F', '#E85A71', '#4EA1D3', '#FCBE32', '#17A363', '#7544D6']

factors = {'noise':('Noise distortion (dnoise)', (0, 40)),
           'slope':('Slope distortion (dslope)', (-0.1, 0.1)),
           'drift':('Drift distortion (ddrift)', (-0.2, 0.2)),
           'regression_within':('Within-line regression (rwithin)', (0, 1)),
           'regression_across':('Across-line regression (racross)', (0, 1))}

def plot_results(layout, filepath, n_rows=2, figsize=None):
	n_cols = len(layout) // n_rows
	if len(layout) % n_rows:
		n_cols += 1
	if figsize is None:
		figsize = (n_cols*4, n_rows*4)
	legend_patches = []
	fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize, squeeze=False)
	subplot_i = 0
	for factor, (r, c) in zip(layout, np.ndindex((n_rows, n_cols))):
		if factor == 'legend':
			axes[r][c].axis('off')
			axes[r][c].legend(legend_patches, methods, loc='center', frameon=False, markerscale=2)
			continue
		results = tools.unpickle('../data/algorithm_performance/%s.pkl'%factor)
		factor_label, (factor_min_val, factor_max_val) = factors[factor]
		factor_space = np.linspace(factor_min_val, factor_max_val, len(results[0]))
		for method_i, method in enumerate(methods):
			means = results[method_i, :].mean(axis=1)
			staggered_means = means - (0.01 * method_i) + (0.01 * (len(methods)-1)/2)
			line, = axes[r][c].plot(factor_space, staggered_means, color=colors[method_i], label=method, linewidth=1.2)
			if r == 0 and c == 0:
				legend_patches.append(line)
			axes[r][c].set_ylim(-0.05, 1.05)
			offset = (factor_max_val - factor_min_val) * 0.05
			axes[r][c].set_xlim(factor_min_val-offset, factor_max_val+offset)
			axes[r][c].set_xlabel(factor_label)
		axes[r][c].text(factor_min_val, 0, '(%s)'%('ABCDE'[subplot_i]), fontsize=8)
		subplot_i += 1
	for axis in axes[:, 0]:
		axis.set_ylabel('Accuracy of algorithmic correction')
	for axis in axes[:, 1:].flatten():
		axis.set_yticklabels([])
	for r, c in list(np.ndindex((n_rows, n_cols)))[len(layout):]:
		axes[r][c].axis('off')
	fig.tight_layout(pad=0.1, h_pad=0.5, w_pad=0.5)
	fig.savefig(filepath, format='svg')
	tools.format_svg_labels(filepath, methods)
	if not filepath.endswith('.svg'):
		tools.convert_svg(filepath, filepath)


if __name__ == '__main__':

	# plot_results(['noise', 'legend', 'slope', 'drift', 'regression_within', 'regression_across'], '../visuals/algorithm_performance.pdf', 3, (5.5, 7))
	plot_results(['noise', 'legend', 'slope', 'drift', 'regression_within', 'regression_across'], '../manuscript/figs/algorithm_performance.eps', 3, (6.8, 6))
