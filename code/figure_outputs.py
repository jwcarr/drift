import eyekit
import globals

passages = eyekit.io.read('../data/passages.json')
gold_data = eyekit.io.read('../data/fixations/gold.json')

# Adult example

gold_fixation_sequence = gold_data['trial_5']['fixations']
fig = eyekit.Figure(3, 3)
for algorithm in globals.algorithms:
	data = eyekit.io.read('../data/fixations/%s.json'%algorithm)
	fixation_sequence = data['trial_5']['fixations']
	image = eyekit.Image(1920, 1080)
	image.draw_text_block(passages['1B'], color='gray')
	image.draw_sequence_comparison(gold_fixation_sequence, fixation_sequence)
	image.set_caption('%s' % algorithm, font_face='Menlo', font_size=8)
	fig.add_image(image)
fig.set_lettering(font_face='Helvetica Neue bold', font_size=8)
fig.save('../visuals/outputs_adult.pdf', 174, crop_margin=2)
fig.save('../manuscript/figs/fig09_double_column.eps', 174, crop_margin=2)

# Child example

gold_fixation_sequence = gold_data['trial_30']['fixations']
fig = eyekit.Figure(3, 3)
for algorithm in globals.algorithms:
	data = eyekit.io.read('../data/fixations/%s.json'%algorithm)
	fixation_sequence = data['trial_30']['fixations']
	image = eyekit.Image(1920, 1080)
	image.draw_text_block(passages['4A'], color='gray')
	image.draw_sequence_comparison(gold_fixation_sequence, fixation_sequence)
	image.set_caption('%s' % algorithm, font_face='Menlo', font_size=8)
	fig.add_image(image)
fig.set_lettering(font_face='Helvetica Neue bold', font_size=8)
fig.save('../visuals/outputs_child.pdf', 174, crop_margin=2)
fig.save('../manuscript/figs/fig10_double_column.eps', 174, crop_margin=2)
