'''
Code for rendering PDFs showing the orignal fixation sequences and the
manual and algorithmic corrections.
'''

import eyekit
import globals

eyekit.vis.set_default_font('Helvetica Neue', 8)

passages = eyekit.io.read('../data/passages.json')
datasets = {dataset : eyekit.io.read('../data/fixations/%s.json'%dataset) for dataset in ['sample', 'gold']+globals.algorithms}

booklet = eyekit.vis.Booklet()

for trial_id, trial in datasets['sample'].items():
	print(trial_id)
	sample_fixation_sequence = trial['fixations']
	gold_fixation_sequence = datasets['gold'][trial_id]['fixations']

	fig = eyekit.vis.Figure(4, 3)

	sample_image = eyekit.vis.Image(1920, 1080)
	sample_image.draw_text_block(passages[trial['passage_id']], color='gray')
	sample_image.draw_fixation_sequence(sample_fixation_sequence)
	sample_image.set_caption(f'Participant {trial["participant_id"]}, passage {trial["passage_id"]} ({trial["age_group"]})')
	fig.add_image(sample_image)

	gold_image = eyekit.vis.Image(1920, 1080)
	gold_image.draw_text_block(passages[trial['passage_id']], color='gray')
	gold_image.draw_fixation_sequence(gold_fixation_sequence, show_discards=True)
	gold_image.set_caption('Gold standard manual correction')
	fig.add_image(gold_image)

	for algorithm in globals.algorithms:
		data = datasets[algorithm]
		image = eyekit.vis.Image(1920, 1080)
		image.draw_text_block(passages[trial['passage_id']], color='gray')
		image.draw_sequence_comparison(gold_fixation_sequence, data[trial_id]['fixations'])
		image.set_caption(algorithm, font_face='Menlo')
		fig.add_image(image)

	fig.set_crop_margin(2)
	fig.set_lettering(False)
	fig.set_padding(5, 5, 10)

	booklet.add_figure(fig)

booklet.save('../visuals/corrections.pdf', height=227)
