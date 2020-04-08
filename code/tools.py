from subprocess import call, STDOUT, DEVNULL
from os import listdir, path
import pickle as _pickle
import re
import json
import eyekit

INKSCAPE_PATH = '/usr/local/bin/inkscape'

def pickle(obj, file_path):
	with open(file_path, mode='wb') as file:
		_pickle.dump(obj, file)

def unpickle(file_path):
	with open(file_path, mode='rb') as file:
		return _pickle.load(file)

def load_passages(passages_dir):
	passages = {}
	for passage_file in listdir(passages_dir):
		if not passage_file.endswith('.txt'):
			continue
		passage_id, _ = passage_file.split('.')
		passage_path = path.join(passages_dir, passage_file)
		passages[passage_id] = eyekit.Passage(passage_path,
			first_character_position=(368, 155),
			character_spacing=16,
			line_spacing=64,
			pad_lines_with_spaces=True)
	return passages

def load_data(data_file):
	with open(data_file) as file:
		data = json.load(file)
	return data

def convert_svg(svg_file_path, out_file_path, png_width=1000):
	filename, extension = path.splitext(out_file_path)
	if extension == '.pdf':
		call([INKSCAPE_PATH, svg_file_path, '-A', out_file_path, '--export-text-to-path'], stdout=DEVNULL, stderr=STDOUT)
	elif extension == '.eps':
		call([INKSCAPE_PATH, svg_file_path, '-E', out_file_path, '--export-text-to-path'], stdout=DEVNULL, stderr=STDOUT)
	elif extension == '.png':
		call([INKSCAPE_PATH, svg_file_path, '-e', out_file_path, '--export-width=%i'%png_width], stdout=DEVNULL, stderr=STDOUT)
	else:
		raise ValueError('Cannot save to this format. Use either .pdf, .eps, or .png')

def format_svg_labels(svg_file_path, monospace=[], arbitrary_replacements={}):
	'''
	Applies some nicer formatting to an SVG plot, including setting
	the font to Helvetica and adding italics. Requires you to set
	this at the top of the script:
	plt.rcParams['svg.fonttype'] = 'none'
	'''
	with open(svg_file_path, mode='r', encoding='utf-8') as file:
		svg = file.read()
	svg = re.sub(r'font-family:.*?;', 'font-family:Helvetica Neue;', svg)
	svg = svg.replace('dnoise', '<tspan style="font-style: italic;">d</tspan><tspan baseline-shift="sub" style="font-size: 4pt">noise</tspan>')
	svg = svg.replace('dslope', '<tspan style="font-style: italic;">d</tspan><tspan baseline-shift="sub" style="font-size: 4pt">slope</tspan>')
	svg = svg.replace('ddrift', '<tspan style="font-style: italic;">d</tspan><tspan baseline-shift="sub" style="font-size: 4pt">drift</tspan>')
	svg = svg.replace('rwithin', '<tspan style="font-style: italic;">r</tspan><tspan baseline-shift="sub" style="font-size: 4pt">within</tspan>')
	svg = svg.replace('racross', '<tspan style="font-style: italic;">r</tspan><tspan baseline-shift="sub" style="font-size: 4pt">across</tspan>')
	for word in monospace:
		for matched_line in re.finditer('<text.*?%s</text>'%word, svg):
			if matched_line:
				svg = svg.replace(matched_line.group(0), matched_line.group(0).replace('Helvetica Neue', 'Menlo'))
	for find, replace in arbitrary_replacements.items():
		svg = svg.replace(find, replace)
	with open(svg_file_path, mode='w', encoding='utf-8') as file:
		file.write(svg)
