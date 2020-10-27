from os.path import splitext
from pathlib import Path
import re
import cairosvg

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

def convert_svg(svg_file_path, out_file_path):
	'''
	Convert an SVG file into PDF, EPS, or PNG. This function is
	essentially a wrapper around CairoSVG.
	'''
	_, extension = splitext(out_file_path)
	if extension == '.pdf':
		cairosvg.svg2pdf(url=svg_file_path, write_to=out_file_path)
	elif extension == '.eps':
		cairosvg.svg2ps(url=svg_file_path, write_to=out_file_path)
	elif extension == '.png':
		cairosvg.svg2png(url=svg_file_path, write_to=out_file_path)
	else:
		raise ValueError('Cannot save to this format. Use either .pdf, .eps, or .png')


# PATHS TO COMMON DIRECTORIES
ROOT = Path(__file__).parent.parent
DATA = ROOT / 'data'
FIXATIONS = DATA / 'fixations'
MANUAL_CORRECTIONS = DATA / 'manual_corrections'
SIMULATIONS = DATA / 'simulations'
VISUALS = ROOT / 'visuals'


y_to_line_mapping = {155:1, 219:2, 283:3, 347:4, 411:5, 475:6, 539:7, 603:8, 667:9, 731:10, 795:11, 859:12, 923:13}

colors = {'attach':'#81818D',
          'chain':'#D64E7A',
          'cluster':'#45ADEC',
          'compare':'#F3711A',
          'merge':'#205E84',
          'regress':'#009142',
          'segment':'#FCAF32',
          'split':'#E32823',
          'stretch':'#525200',
          'warp':'#6742B0',
          'gold':'#B0944B',
          'JC':'black',
          'VP':'black'
}

algorithms = ['attach', 'chain', 'cluster', 'compare', 'merge', 'regress', 'segment', 'split', 'stretch', 'warp']

true_algorithms = ['chain', 'cluster', 'compare', 'merge', 'regress', 'segment', 'split', 'stretch', 'warp']

good_algorithms = ['attach', 'chain', 'cluster', 'merge', 'regress', 'segment', 'split', 'stretch', 'warp']

factors = {'noise':('Noise distortion', (0, 40)),
           'slope':('Slope distortion', (-0.1, 0.1)),
           'shift':('Shift distortion', (-0.2, 0.2)),
           'regression_within':('Probability of within-line regression', (0, 1)),
           'regression_between':('Probability of between-line regression', (0, 1))}

lorem_ipsum_text = ['Lorem ipsum dolor sit amet, consectetur',
                    'adipiscing elit, sed do eiusmod tempor',
                    'incididunt ut labore.']

lorem_ipsum_XY = [[395, 150, 100], [479, 152, 100], [619, 166, 100], [670, 188, 100], [726, 157, 100], [899, 145, 100],
                  [401, 221, 100], [499, 230, 100], [594, 228, 100], [655, 229, 100], [806, 231, 100], [896, 216, 100],
                  [379, 270, 100], [472, 273, 100], [553, 289, 100], [645, 296, 100]]

illustration_colors  = ['#000000', '#E32823', '#205E84']