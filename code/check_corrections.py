'''
Code for validating the manual corrections and converting them into
JSON files for analysis. Validation includes:

- All correction files are present
- Lines in the correction file are present and correctly ordered
- Correction file is correctly formatted (e.g. tab separated numbers)
- Correct number of line assignments (e.g. passage with 10 lines
  should have assignments from 1 to 10 and maybe 0s)
'''

import eyekit
import globals

def check_correction(correction_path, participant_data, passages):
	for trial_id, trial in participant_data.items():
		file_path = correction_path + '%s_%s' % (trial['participant_id'].zfill(3), trial['passage_id'])
		line_numbers = []
		with open(file_path) as file:
			for i, (line, fixation) in enumerate(zip(file, trial['fixations']), 1):
				try:
					d, x, y, l = line.split('\t')
					d, x, y, l = int(d), int(x), int(y), int(l)
					assert x == fixation.x
					assert y == fixation.y
					assert d == fixation.duration
				except:
					print('Error on line %i in %s' % (i, file_path))
					quit()
				line_numbers.append(l)
		line_numbers = sorted(list(set(line_numbers)))
		try:
			assert (len(line_numbers) == max(line_numbers) and 0 not in line_numbers) or (len(line_numbers) == max(line_numbers)+1)
		except AssertionError:
			print('Warning: %s only contains line numbers %s' % (file_path, str(line_numbers)))
		try:
			assert max(line_numbers) == passages[trial['passage_id']].n_rows
		except AssertionError:
			print('Warning: %s doesn\'t match number of lines in passage' % file_path)

def make_corrected_file(correction_path, participant_data, passages, corrected_file_path):
	new_dataset = {}
	for trial_id, trial in participant_data.items():
		new_trial = {'participant_id':trial['participant_id'], 'age_group':trial['age_group'], 'passage_id':trial['passage_id'], 'fixations':[]}
		file_path = correction_path + '%s_%s' % (trial['participant_id'].zfill(3), trial['passage_id'])
		with open(file_path) as file:
			for line, fixation in zip(file, trial['fixations'].iter_with_discards()):
				l = int(line.split('\t')[3])
				if l == 0:
					new_trial['fixations'].append((fixation.x, fixation.y, fixation.duration, True))
				else:
					new_y = passages[trial['passage_id']].line_positions[l-1]
					new_trial['fixations'].append((fixation.x, int(new_y), fixation.duration, False))
		new_dataset[trial_id] = new_trial
	eyekit.io.write(new_dataset, corrected_file_path)

def compare_two_corrections(correction1_file_path, correction2_file_path):
	correction1 = eyekit.io.read(correction1_file_path)
	correction2 = eyekit.io.read(correction2_file_path)
	for trial_id, trial in correction1.items():
		print('Trial %s, Participant %s, passage %s'%(trial_id, trial['participant_id'], trial['passage_id']))
		for i, fixation1 in enumerate(trial['fixations'].iter_with_discards()):
			fixation2 = correction2[trial_id]['fixations'][i]
			if fixation1.discarded:
				line_assignment1 = 0
			else:
				line_assignment1 = globals.y_to_line_mapping[fixation1.y]
			if fixation2.discarded:
				line_assignment2 = 0
			else:
				line_assignment2 = globals.y_to_line_mapping[fixation2.y]
			if line_assignment1 != line_assignment2:
				if line_assignment1 == 0 or line_assignment2 == 0:
					print(' - Fixation %i: JC says %i, VP says %i (difference in discarding)'%((i+1), line_assignment1, line_assignment2))
				else:
					print(' - Fixation %i: JC says %i, VP says %i (difference in line assignment)'%((i+1), line_assignment1, line_assignment2))


if __name__ == '__main__':

	passages = eyekit.io.load_texts('../data/passages.json')
	participant_data = eyekit.io.read('../data/fixations/sample.json')

	# Step 1: Check validity of JC's correction and make JSON file
	correction_path = '../data/manual_corrections/JC/'
	corrected_file_path = '../data/fixations/JC.json'
	check_correction(correction_path, participant_data, passages)
	make_corrected_file(correction_path, participant_data, passages, corrected_file_path)

	# Step 2: Check validity of VP's correction and make JSON file
	correction_path = '../data/manual_corrections/VP/'
	corrected_file_path = '../data/fixations/VP.json'
	check_correction(correction_path, participant_data, passages)
	make_corrected_file(correction_path, participant_data, passages, corrected_file_path)

	# Step 3: Compare JC and VP's corrections and highlight any differences
	compare_two_corrections('../data/fixations/JC.json', '../data/fixations/VP.json')

	# Step 4: Create the gold standard JSON file from a merger of the two corrections
	correction_path = '../data/manual_corrections/gold/'
	corrected_file_path = '../data/fixations/gold.json'
	check_correction(correction_path, participant_data, passages)
	make_corrected_file(correction_path, participant_data, passages, corrected_file_path)
