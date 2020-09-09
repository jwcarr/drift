import eyekit
import algorithms
import globals

data = eyekit.io.read('../data/fixations/sample.json')
passages = eyekit.io.load_texts('../data/passages.json')

for fixation in data['trial_5']['fixations']:
	fixation.duration = 100
corrected_fixation_sequence, solution = algorithms.correct_drift('warp', data['trial_5']['fixations'].XYarray(), passages['1B'], return_solution=True)
corrected_fixation_sequence = eyekit.FixationSequence(corrected_fixation_sequence)
word_XY = passages['1B'].word_centers

diagram = eyekit.Image(1920, 1080)
diagram.render_text(passages['1B'], color='gray')
diagram.render_fixations(eyekit.FixationSequence(word_XY), include_discards=True, color=globals.illustration_colors[1])
diagram.render_fixations(data['trial_5']['fixations'], include_discards=True, color=globals.illustration_colors[2])
for fixation, mapped_words in zip(data['trial_5']['fixations'], solution):
	for word_i in mapped_words:
		word_x, word_y = word_XY[word_i]
		diagram.draw_line(fixation.xy, (word_x, word_y), 'black', dashed=True)
diagram.crop_to_text(50)

figure_layout = [[diagram]]
eyekit.image.combine_images(figure_layout, '../visuals/illustration_warp_.pdf',
	image_width=83, v_padding=3, h_padding=3, e_padding=1, auto_letter=False)
eyekit.image.combine_images(figure_layout, '../manuscript/figs/fig03_single_column_.eps',
	image_width=83, v_padding=3, h_padding=3, e_padding=1, auto_letter=False)
