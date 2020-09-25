'''
Code for rendering PDFs showing the orignal fixation sequences and the
manual and algorithmic corrections.
'''

import eyekit

passages = eyekit.io.read('../data/passages.json')
datasets = {dataset : eyekit.io.read('../data/fixations/%s.json'%dataset) for dataset in ['sample', 'gold', 'attach', 'chain', 'cluster', 'compare', 'merge', 'regress', 'segment', 'split', 'warp']}

for trial_id, trial in datasets['sample'].items():
	print(trial_id)
	sample_fixation_sequence = trial['fixations']
	gold_fixation_sequence = datasets['gold'][trial_id]['fixations']
	fig = eyekit.Figure(4, 3)

	sample_image = eyekit.Image(1920, 1080)
	sample_image.draw_text_block(passages[trial['passage_id']], color='gray')
	sample_image.draw_fixation_sequence(sample_fixation_sequence)
	age = 'adult' if int(trial['participant_id']) < 100 else 'child'
	sample_image.set_caption('Passage %s, participant %s (%s)' % (trial['passage_id'], trial['participant_id'], age))

	gold_image = eyekit.Image(1920, 1080)
	gold_image.draw_text_block(passages[trial['passage_id']], color='gray')
	gold_image.draw_fixation_sequence(gold_fixation_sequence)
	gold_image.set_caption('Manual correction')

	fig._grid[0] = [sample_image, gold_image]

	for algorithm in ['attach', 'chain', 'cluster', 'compare', 'merge', 'regress', 'segment', 'split', 'warp']:
		data = datasets[algorithm]
		image = eyekit.Image(1920, 1080)
		image.draw_text_block(passages[trial['passage_id']], color='gray')
		image.draw_sequence_comparison(gold_fixation_sequence, data[trial_id]['fixations'])
		image.set_caption(algorithm)
		fig.add_image(image)

	filepath = '../visuals/corrections/%s_%s.pdf' % (trial['passage_id'], trial['participant_id'])

	fig.set_crop_margin(2)
	fig.set_auto_letter(False)
	fig.save(filepath, 174)
