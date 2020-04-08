'''
Code for rendering fixation sequences over the relevant passage of text.
'''

from collections import defaultdict
import json
import eyekit
import tools

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
			diagram.render_passage(passages[passage_id], 28)
			diagram.render_fixations(fixation_sequence, number_fixations=True, include_discards=True)
			diagram.save(output_dir + '%s_%s.svg' % (participant_id, passage_id))

def comparison_render(passages, input_file1, input_file2, output_dir, colors, include_discards):
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
			diagram.render_passage(passages[passage_id], 28)
			diagram.render_fixation_comparison(fixation_sequence1, fixation_sequence2, color_match='green', color_mismatch='red')
			output_path = output_dir + '%s_%s.svg'%(participant_id, passage_id)
			diagram.save(output_path, crop_to_passage=True)


if __name__ == '__main__':

	passages = tools.load_passages('../data/passages/')
	
	render(passages, '../data/fixations/sample.json', '../visuals/passage_renders/sample/')