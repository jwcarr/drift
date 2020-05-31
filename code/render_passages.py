'''
Code for rendering fixation sequences over the relevant passage of text.
'''

from collections import defaultdict
import json
import eyekit
import tools
import defaults

def render(passages, input_file, output_dir):
	print('RENDERING: %s' % input_file)
	with open(input_file) as file:
		input_data = json.load(file)
	for passage_id, participant_data in input_data.items():
		print(passage_id)
		for participant_id, fixations in participant_data.items():
			print('-', participant_id)
			fixation_sequence = eyekit.FixationSequence(fixations)
			diagram = eyekit.Diagram(1920, 1080)
			diagram.render_passage(passages[passage_id], 28, color='gray')
			diagram.render_fixations(fixation_sequence, include_discards=True)
			diagram.crop_to_passage()
			diagram.save(output_dir + '%s_%s.pdf' % (participant_id, passage_id))

def comparison_render(passages, input_file1, input_file2, output_dir):
	print('RENDERING: %s against %s' % (input_file1, input_file2))
	with open(input_file1) as file:
		input_data1 = json.load(file)
	with open(input_file2) as file:
		input_data2 = json.load(file)
	for passage_id, participant_data in input_data1.items():
		print(passage_id)
		for participant_id, fixations in participant_data.items():
			print('-', participant_id)
			fixation_sequence1 = eyekit.FixationSequence(fixations)
			fixation_sequence2 = eyekit.FixationSequence(input_data2[passage_id][participant_id])
			diagram = eyekit.Diagram(1920, 1080)
			diagram.render_passage(passages[passage_id], 28, color='gray')
			diagram.render_fixation_comparison(fixation_sequence1, fixation_sequence2, color_match='black', color_mismatch='red')
			diagram.crop_to_passage()
			output_path = output_dir + '%s_%s.pdf'%(participant_id, passage_id)
			diagram.save(output_path)


if __name__ == '__main__':

	passages = tools.load_passages('../data/passages/')
	
	# Render the original data
	render(passages, '../data/fixations/sample.json', '../visuals/passage_renders/sample/')

	# Render the gold standard corrections
	render(passages, '../data/fixations/gold.json', '../visuals/passage_renders/gold/')

	# Render the algorithmic corrections
	for algorithm in defaults.algorithms:
		comparison_render(passages, '../data/fixations/gold.json', '../data/fixations/%s.json'%algorithm, '../visuals/passage_renders/%s/'%algorithm)
