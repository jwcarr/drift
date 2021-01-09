import numpy as np
import eyekit
import algorithms
import core

data = eyekit.io.read(core.FIXATIONS / 'sample.json')
passages = eyekit.io.read(core.DATA / 'passages.json')

original_sequence = data['trial_5']['fixations']

fixation_XY = np.array([fixation.xy for fixation in original_sequence], dtype=int)
word_XY = np.array(passages['1B'].word_centers(), dtype=int)

start_times = np.array([i*100 for i in range(len(word_XY))], dtype=int)
expected_sequence = eyekit.FixationSequence(np.column_stack([word_XY, start_times, start_times+100]))

diagram = eyekit.vis.Image(1920, 1080)
diagram.draw_text_block(passages['1B'], color='gray')
diagram.draw_fixation_sequence(expected_sequence, color='#E32823', fixation_radius=6)
diagram.draw_fixation_sequence(original_sequence, color='#205E84', fixation_radius=6)

_, warping_path = algorithms.dynamic_time_warping(fixation_XY, word_XY)

for fixation, mapped_words in zip(original_sequence, warping_path):
	for word_i in mapped_words:
		word_x, word_y = word_XY[word_i]
		diagram.draw_line(fixation.xy, (word_x, word_y), 'black', stroke_width=0.5, dashed=True)

fig = eyekit.vis.Figure()
fig.add_image(diagram)
fig.set_lettering(False)
fig.set_crop_margin(3)
fig.save(core.VISUALS / 'illustration_warp.pdf', 83)
# fig.save(core.FIGS / 'fig02_single_column.eps', 83)
