'''
Creates visualizations of the sample trials and empty correction files into
which the two correctors can record their fixation-by-fixation corrections.

And code for validating the manual corrections and converting them into JSON
files for analysis. Validation includes:

- All correction files are present
- Lines in the correction file are present and correctly ordered
- Correction file is correctly formatted (e.g. tab separated numbers)
- Correct number of line assignments (e.g. passage with 10 lines should have
  assignments from 1 to 10 and maybe 0s)
'''

import eyekit
import core

def create_empty_correction_file(correction_path, fixation_sequence, participant_id, passage_id):
	participant_id = participant_id.zfill(3)
	correction_file_path = str(correction_path / f'{participant_id}_{passage_id}')
	with open(correction_file_path, 'w') as file:
		for fixation in fixation_sequence:
			file.write('%s\t%s\t%s\t\n' % (str(round(fixation.duration)).zfill(4), str(round(fixation.x)).zfill(4), str(round(fixation.y)).zfill(4)))

def create_visualization(correction_path, fixation_sequence, passage, participant_id, passage_id):
	participant_id = participant_id.zfill(3)
	image_file_path = str(correction_path / f'{participant_id}_{passage_id}.pdf')
	fig = eyekit.vis.Image(1920, 1080)
	fig.draw_text_block(passage)
	fig.draw_fixation_sequence(fixation_sequence, number_fixations=True)
	fig.save(image_file_path)

def check_correction(correction_path, participant_data, passages):
	for trial_id, trial in participant_data.items():
		participant_id = trial["participant_id"].zfill(3)
		passage_id = trial['passage_id']
		correction_file_path = str(correction_path / f'{participant_id}_{passage_id}')
		line_numbers = []
		with open(correction_file_path) as file:
			for i, (line, fixation) in enumerate(zip(file, trial['fixations']), 1):
				try:
					d, x, y, l = line.split('\t')
					d, x, y, l = int(d), int(x), int(y), int(l)
					assert x == fixation.x
					assert y == fixation.y
					assert d == fixation.duration
				except:
					print('Error on line %i in %s' % (i, correction_file_path))
					quit()
				line_numbers.append(l)
		line_numbers = sorted(list(set(line_numbers)))
		try:
			assert (len(line_numbers) == max(line_numbers) and 0 not in line_numbers) or (len(line_numbers) == max(line_numbers)+1)
		except AssertionError:
			print('Warning: %s only contains line numbers %s' % (correction_file_path, str(line_numbers)))
		try:
			assert max(line_numbers) == passages[trial['passage_id']].n_rows
		except AssertionError:
			print('Warning: %s doesn\'t match number of lines in passage' % correction_file_path)

def make_corrected_file(correction_path, participant_data, passages, corrected_file_path):
	new_dataset = {}
	for trial_id, trial in participant_data.items():
		new_trial = {'participant_id':trial['participant_id'], 'age_group':trial['age_group'], 'passage_id':trial['passage_id'], 'fixations':[]}
		participant_id = trial["participant_id"].zfill(3)
		passage_id = trial['passage_id']
		correction_file_path = str(correction_path / f'{participant_id}_{passage_id}')
		with open(correction_file_path) as file:
			for line, fixation in zip(file, trial['fixations']):
				l = int(line.split('\t')[3])
				if l == 0:
					new_trial['fixations'].append((fixation.x, fixation.y, fixation.start, fixation.end, True))
				else:
					new_y = passages[trial['passage_id']].midlines[l-1]
					new_trial['fixations'].append((fixation.x, int(new_y), fixation.start, fixation.end, False))
		new_trial['fixations'] = eyekit.FixationSequence(new_trial['fixations'])
		new_dataset[trial_id] = new_trial
	eyekit.io.save(new_dataset, corrected_file_path, compress=True)

def compare_two_corrections(correction1_file_path, correction2_file_path):
	correction1 = eyekit.io.load(correction1_file_path)
	correction2 = eyekit.io.load(correction2_file_path)
	for trial_id, trial in correction1.items():
		print('Trial %s, Participant %s, passage %s'%(trial_id, trial['participant_id'], trial['passage_id']))
		for i, fixation1 in enumerate(trial['fixations']):
			fixation2 = correction2[trial_id]['fixations'][i]
			if fixation1.discarded:
				line_assignment1 = 0
			else:
				line_assignment1 = core.y_to_line_mapping[fixation1.y]
			if fixation2.discarded:
				line_assignment2 = 0
			else:
				line_assignment2 = core.y_to_line_mapping[fixation2.y]
			if line_assignment1 != line_assignment2:
				if line_assignment1 == 0 or line_assignment2 == 0:
					print(' - Fixation %i: Corrector 1 says %i, Corrector 2 says %i (difference in discarding)'%((i+1), line_assignment1, line_assignment2))
				else:
					print(' - Fixation %i: Corrector 1 says %i, Corrector 2 says %i (difference in line assignment)'%((i+1), line_assignment1, line_assignment2))


if __name__ == '__main__':

	participant_data = eyekit.io.load(core.FIXATIONS / 'sample.json')
	passages = eyekit.io.load(core.DATA / 'passages.json')

	# Step 0: Initialize the empty correction files and plots of the original data
	# for corrector_id in ['JC', 'VP']:
	# 	correction_path = core.MANUAL_CORRECTIONS / corrector_id
	# 	correction_path.mkdir()
	# 	for trial_id, trial in participant_data.items():
	# 		create_empty_correction_file(correction_path, trial['fixations'], trial['participant_id'], trial['passage_id'])
	# 		create_visualization(correction_path, trial['fixations'], passages[trial['passage_id']], trial['participant_id'], trial['passage_id'])

	# Step 1: Check validity of JC's correction and make JSON file
	check_correction(core.MANUAL_CORRECTIONS / 'JC', participant_data, passages)
	make_corrected_file(core.MANUAL_CORRECTIONS / 'JC', participant_data, passages, core.FIXATIONS / 'JC.json')

	# Step 2: Check validity of VP's correction and make JSON file
	check_correction(core.MANUAL_CORRECTIONS / 'VP', participant_data, passages)
	make_corrected_file(core.MANUAL_CORRECTIONS / 'VP', participant_data, passages, core.FIXATIONS / 'VP.json')

	# Step 3: Compare JC and VP's corrections and highlight any differences
	compare_two_corrections(core.FIXATIONS / 'JC.json', core.FIXATIONS / 'VP.json')

	# Step 4: Create the gold standard JSON file from a merger of the two corrections (manual merger should be created first)
	check_correction(core.MANUAL_CORRECTIONS / 'gold', participant_data, passages)
	make_corrected_file(core.MANUAL_CORRECTIONS / 'gold', participant_data, passages, core.FIXATIONS / 'gold.json')
