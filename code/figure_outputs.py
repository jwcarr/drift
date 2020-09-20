import eyekit

figure_layout = [['attach',  'chain', 'cluster'],
                 ['compare', 'merge', 'regress'],
                 ['segment', 'split', 'warp'   ]]

passages = eyekit.io.read('../data/passages.json')
gold_data = eyekit.io.read('../data/fixations/gold.json')

# Adult example

gold_fixation_sequence = gold_data['trial_5']['fixations']
diagrams = []
for i, row in enumerate(figure_layout):
	diagrams.append([])
	for j, algorithm in enumerate(row):
		data = eyekit.io.read('../data/fixations/%s.json'%algorithm)
		fixation_sequence = data['trial_5']['fixations']
		diagram = eyekit.Image(1920, 1080)
		diagram.render_text(passages['1B'], color='gray')
		diagram.render_fixation_comparison(gold_fixation_sequence, fixation_sequence)
		diagram.crop_to_text(50)
		diagram.set_caption('<tspan style="font-family:Menlo">%s</tspan>' % algorithm)
		diagrams[-1].append(diagram)
eyekit.image.make_figure(diagrams, '../visuals/outputs_adult.pdf',
	image_width=174, v_padding=3, h_padding=3, e_padding=1)
eyekit.image.make_figure(diagrams, '../manuscript/figs/fig09_double_column.eps',
	image_width=174, v_padding=3, h_padding=3, e_padding=1)

# Child example

gold_fixation_sequence = gold_data['trial_30']['fixations']
diagrams = []
for i, row in enumerate(figure_layout):
	diagrams.append([])
	for j, algorithm in enumerate(row):
		data = eyekit.io.read('../data/fixations/%s.json'%algorithm)
		fixation_sequence = data['trial_30']['fixations']
		diagram = eyekit.Image(1920, 1080)
		diagram.render_text(passages['4A'], color='gray')
		diagram.render_fixation_comparison(gold_fixation_sequence, fixation_sequence)
		diagram.crop_to_text(50)
		diagram.set_caption('<tspan style="font-family:Menlo">%s</tspan>' % algorithm)
		diagrams[-1].append(diagram)
eyekit.image.make_figure(diagrams, '../visuals/outputs_child.pdf',
	image_width=174, v_padding=3, h_padding=3, e_padding=1)
eyekit.image.make_figure(diagrams, '../manuscript/figs/fig10_double_column.eps',
	image_width=174, v_padding=3, h_padding=3, e_padding=1)
