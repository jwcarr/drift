import eyekit

data = eyekit.io.read('../data/fixations/sample.json')
passages = eyekit.io.read('../data/passages.json')

adult_fixation_sequence = data['trial_5']['fixations']  #   8, 1B
child_fixation_sequence = data['trial_30']['fixations'] # 204, 4A

adult = eyekit.Image(1920, 1080)
adult.render_text(passages['1B'], color='gray')
adult.render_fixations(adult_fixation_sequence, include_discards=True)
adult.crop_to_text(50)
adult.set_caption('Reading trial by an adult')

child = eyekit.Image(1920, 1080)
child.render_text(passages['4A'], color='gray')
child.render_fixations(child_fixation_sequence, include_discards=True)
child.crop_to_text(50)
child.set_caption('Reading trial by a child')

figure_layout = [[adult, child]]
eyekit.image.make_figure(figure_layout, '../visuals/illustration_examples.pdf',
	image_width=174, v_padding=3, h_padding=3, e_padding=1)
eyekit.image.make_figure(figure_layout, '../manuscript/figs/fig01_double_column.eps',
	image_width=174, v_padding=3, h_padding=3, e_padding=1)
