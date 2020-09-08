import pickle as _pickle
import re
import eyekit

def pickle(obj, file_path):
	with open(file_path, mode='wb') as file:
		_pickle.dump(obj, file)

def unpickle(file_path):
	with open(file_path, mode='rb') as file:
		return _pickle.load(file)

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
	for check in re.finditer('<text.*?✔</text>', svg):
		if check:
			svg = svg.replace(check.group(0), check.group(0).replace('Helvetica Neue', 'Menlo'))
	for word in monospace:
		for matched_line in re.finditer('<text.*?%s</text>'%word, svg):
			if matched_line:
				svg = svg.replace(matched_line.group(0), matched_line.group(0).replace('Helvetica Neue', 'Menlo'))
	for find, replace in arbitrary_replacements.items():
		svg = svg.replace(find, replace)
	with open(svg_file_path, mode='w', encoding='utf-8') as file:
		file.write(svg)
