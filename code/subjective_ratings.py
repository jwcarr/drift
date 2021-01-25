'''

Create randomly ordered images of all 480 corrections and give each correction
a random ID so that the raters can rate each correction blind to algorithm.
Produces two text files: one for recording the ratings and one for mapping the
IDs back to the trial/algorithm.

'''

import eyekit
import core
import random

passages = eyekit.io.read(core.DATA / 'passages.json')
datasets = {dataset : eyekit.io.read(core.FIXATIONS / f'{dataset}.json') for dataset in ['sample', 'gold']+core.algorithms}

def generate_rating_set(rater_id):

	random_ids = [str(i).zfill(3) for i in range(1, 481)]
	random.shuffle(random_ids)
	id_trial_mapping = []

	for trial_id, trial in datasets['sample'].items():

		orig_fixation_sequence = trial['fixations']
		gold_fixation_sequence = datasets['gold'][trial_id]['fixations']

		original_image = eyekit.vis.Image(1920, 1080)
		original_image.draw_text_block(passages[trial['passage_id']], color='gray')
		original_image.draw_fixation_sequence(orig_fixation_sequence)

		for algorithm in core.algorithms:

			random_id = random_ids.pop()
			id_trial_mapping.append(f'{random_id}\t{trial_id}\t{algorithm}')

			correction_image = eyekit.vis.Image(1920, 1080)
			correction_image.draw_text_block(passages[trial['passage_id']], color='gray')
			correction_image.draw_sequence_comparison(gold_fixation_sequence, datasets[algorithm][trial_id]['fixations'])

			fig = eyekit.vis.Figure(1, 2)
			fig.add_image(original_image)
			fig.add_image(correction_image)
			fig.set_crop_margin(2)
			fig.set_lettering(False)
			fig.set_padding(5, 5, 10)
			fig.save(core.VISUALS / 'rating_images' / rater_id / f'{random_id}.pdf')

	id_trial_mapping.sort()

	with open(core.RATINGS / f'{rater_id}_map', 'w') as file:
		file.write('\n'.join(id_trial_mapping))

	with open(core.RATINGS / f'{rater_id}_ratings', 'w') as file:
		file.write('\n'.join([str(i).zfill(3) + '\t' for i in range(1, 481)]))
		

if __name__ == '__main__':

	# Generate a rating set for JC and VP
	generate_rating_set('JC')
	generate_rating_set('VP')
