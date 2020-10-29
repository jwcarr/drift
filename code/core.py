from os.path import splitext
from pathlib import Path
import re
import cairosvg

# Paths to common directories
ROOT = Path(__file__).parent.parent
DATA = ROOT / 'data'
FIGS = ROOT / 'manuscript' / 'figs'
FIXATIONS = DATA / 'fixations'
MANUAL_CORRECTIONS = DATA / 'manual_corrections'
SIMULATIONS = DATA / 'simulations'
SUPPLEMENT = ROOT / 'supplement'
VISUALS = ROOT / 'visuals'

# For mapping y-values to the equivalent line of text
y_to_line_mapping = {155:1, 219:2, 283:3, 347:4, 411:5, 475:6, 539:7, 603:8, 667:9, 731:10, 795:11, 859:12, 923:13}

# Color used to represent each algorithm
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

# Main set of ten algorithms
algorithms = ['attach', 'chain', 'cluster', 'compare', 'merge', 'regress', 'segment', 'split', 'stretch', 'warp']

# Algorithms without attach
true_algorithms = ['chain', 'cluster', 'compare', 'merge', 'regress', 'segment', 'split', 'stretch', 'warp']

# Algorithms without compare
good_algorithms = ['attach', 'chain', 'cluster', 'merge', 'regress', 'segment', 'split', 'stretch', 'warp']

# Simulation factors and their parameter spaces
factors = {'noise':('Noise distortion', (0, 40)),
           'slope':('Slope distortion', (-0.1, 0.1)),
           'shift':('Shift distortion', (-0.2, 0.2)),
           'regression_within':('Probability of within-line regression', (0, 1)),
           'regression_between':('Probability of between-line regression', (0, 1))}


def format_svg_labels(svg_file_path, monospace=[], arbitrary_replacements={}):
	'''
	Applies some nicer formatting to an Matplotlib plots, including setting the
	font to Helvetica and using a monospaced font for algorithm names. The
	following must be set at the top of the script:
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
	Convert an SVG file into PDF, EPS, or PNG. This function is essentially a
	wrapper around CairoSVG.
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
