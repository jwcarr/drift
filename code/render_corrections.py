'''
Code for rendering PDFs showing the orignal fixation sequences and the
manual and algorithmic corrections.
'''

import eyekit

figure_layout = [[     'sample',  'gold'       ],
                 ['attach',  'chain', 'cluster'],
                 ['compare', 'merge', 'regress'],
                 ['segment', 'split', 'warp'   ]]

passages = eyekit.io.read('../data/passages.json')
datasets = {dataset : eyekit.io.read('../data/fixations/%s.json'%dataset) for dataset in [c for r in figure_layout for c in r]}

for trial_id, trial in datasets['sample'].items():
	print(trial_id)
	sample_fixation_sequence = trial['fixations']
	gold_fixation_sequence = datasets['gold'][trial_id]['fixations']
	diagrams = []
	for row in figure_layout:
		diagrams.append([])
		for algorithm in row:
			diagram = eyekit.Image(1920, 1080)
			diagram.render_text(passages[trial['passage_id']], color='gray')
			if algorithm == 'sample':
				age = 'adult' if int(trial['participant_id']) < 100 else 'child'
				diagram.render_fixations(sample_fixation_sequence, include_discards=True)
				diagram.set_caption('Passage %s, participant %s (%s)' % (trial['passage_id'], trial['participant_id'], age))
			elif algorithm == 'gold':
				diagram.render_fixations(gold_fixation_sequence, include_discards=True)
				diagram.set_caption('Manual correction')
			else:
				data = datasets[algorithm]
				diagram.render_fixation_comparison(gold_fixation_sequence, data[trial_id]['fixations'])
				diagram.set_caption('<tspan style="font-family:Menlo">%s</tspan>' % algorithm)
			diagram.crop_to_text(50)
			diagrams[-1].append(diagram)
	filepath = '../visuals/corrections/%s_%s.pdf' % (trial['passage_id'], trial['participant_id'])
	eyekit.image.make_figure(diagrams, filepath, image_width=174, v_padding=3, h_padding=3, e_padding=10, auto_letter=False)
