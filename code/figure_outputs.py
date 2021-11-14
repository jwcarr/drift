import eyekit
import core

eyekit.vis.set_default_font('Helvetica Neue', 8)

passages = eyekit.io.load(core.DATA / 'passages.json')
gold_data = eyekit.io.load(core.FIXATIONS / 'gold.json')

# Adult example

gold_fixation_sequence = gold_data['trial_5']['fixations']
fig = eyekit.vis.Figure(4, 3)
for algorithm in ['sample', 'gold'] + core.algorithms:
	data = eyekit.io.load(core.FIXATIONS / f'{algorithm}.json')
	fixation_sequence = data['trial_5']['fixations']
	image = eyekit.vis.Image(1920, 1080)
	image.draw_text_block(passages['1B'], mask_text=True)
	if algorithm == 'sample':
		image.draw_fixation_sequence(fixation_sequence)
		image.set_caption('Original data')
	elif algorithm == 'gold':
		image.draw_fixation_sequence(fixation_sequence, show_discards=True)
		image.set_caption('Gold standard manual correction')
	else:
		for fxn, ref_fxn in zip(fixation_sequence, gold_fixation_sequence):
			if fxn.y != ref_fxn.y:
				fxn.add_tag('mismatch')
		image.draw_fixation_sequence(fixation_sequence,
			color=lambda fxn: 'red' if fxn.has_tag('mismatch') else 'black'
		)
		image.set_caption('%s' % algorithm, font_face='Menlo', font_size=8)
	fig.add_image(image)
fig.set_crop_margin(2)
fig.set_padding(vertical=2, horizontal=3, edge=1)
fig.set_enumeration('<a>  ', font_size=12)
fig.save(core.VISUALS / 'outputs_adult.pdf', width=174)
# fig.save(core.FIGS / 'fig08_double_column.eps', width=174)

# Child example

gold_fixation_sequence = gold_data['trial_30']['fixations']
fig = eyekit.vis.Figure(4, 3)
for algorithm in ['sample', 'gold'] + core.algorithms:
	data = eyekit.io.load(core.FIXATIONS / f'{algorithm}.json')
	fixation_sequence = data['trial_30']['fixations']
	image = eyekit.vis.Image(1920, 1080)
	image.draw_text_block(passages['4A'], mask_text=True)
	if algorithm == 'sample':
		image.draw_fixation_sequence(fixation_sequence)
		image.set_caption('Original data')
	elif algorithm == 'gold':
		image.draw_fixation_sequence(fixation_sequence, show_discards=True)
		image.set_caption('Gold standard manual correction')
	else:
		for fxn, ref_fxn in zip(fixation_sequence, gold_fixation_sequence):
			if fxn.y != ref_fxn.y:
				fxn.add_tag('mismatch')
		image.draw_fixation_sequence(fixation_sequence,
			color=lambda fxn: 'red' if fxn.has_tag('mismatch') else 'black'
		)
		image.set_caption('%s' % algorithm, font_face='Menlo', font_size=8)
	fig.add_image(image)
fig.set_crop_margin(2)
fig.set_padding(vertical=2, horizontal=3, edge=1)
fig.set_enumeration('<a>  ', font_size=12)
fig.save(core.VISUALS / 'outputs_child.pdf', width=174)
# fig.save(core.FIGS / 'fig09_double_column.eps', width=174)
