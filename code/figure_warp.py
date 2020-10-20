import numpy as np
import eyekit
import algorithms
import globals

data = eyekit.io.read('../data/fixations/sample.json')
passages = eyekit.io.read('../data/passages.json')

original_sequence = data['trial_5']['fixations']

for fixation in original_sequence:
	fixation.duration = 100

fixation_XY = original_sequence.XYarray()
word_XY = np.array(passages['1B'].word_centers, dtype=int)

expected_sequence = eyekit.FixationSequence(np.column_stack([word_XY, np.full(len(word_XY), 100, dtype=int)]))

diagram = eyekit.vis.Image(1920, 1080)
diagram.draw_text_block(passages['1B'], color='gray')
diagram.draw_fixation_sequence(expected_sequence, color=globals.illustration_colors[1])
diagram.draw_fixation_sequence(original_sequence, color=globals.illustration_colors[2])

_, warping_path = algorithms.dynamic_time_warping(fixation_XY, word_XY)

for fixation, mapped_words in zip(original_sequence, warping_path):
	for word_i in mapped_words:
		word_x, word_y = word_XY[word_i]
		diagram.draw_line(fixation.xy, (word_x, word_y), 'black', stroke_width=0.5, dashed=True)

fig = eyekit.vis.Figure()
fig.add_image(diagram)
fig.set_lettering(False)
fig.set_crop_margin(3)
fig.save('../visuals/illustration_warp.pdf', 83)
fig.save('../manuscript/figs/fig02_single_column.eps', 83)
