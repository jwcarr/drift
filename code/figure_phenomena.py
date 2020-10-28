import numpy as np
import eyekit
import simulation
import core

eyekit.vis.set_default_font('Helvetica Neue', 8)

def run_and_visualize(passage, label, **params):
	reading_scenario = simulation.ReadingScenario(**params)
	_, fixations, _ = reading_scenario.simulate(passage)
	fixations = np.column_stack([fixations, np.full(len(fixations), 100, dtype=int)])
	fixation_sequence = eyekit.FixationSequence(fixations)
	diagram = eyekit.vis.Image(1920, 1080)
	diagram.draw_text_block(passage, color='gray')
	diagram.draw_fixation_sequence(fixation_sequence, color='black')
	diagram.set_caption(label)
	return diagram

lorem_ipsum_text = ['Lorem ipsum dolor sit amet, consectetur',
                    'adipiscing elit, sed do eiusmod tempor',
                    'incididunt ut labore.']

passage = eyekit.TextBlock(lorem_ipsum_text, position=(360, 161), font_face='Courier New', font_size=26.667, line_height=64)

fig = eyekit.vis.Figure(5, 1)
fig.add_image(run_and_visualize(passage, 'Noise', noise=20.0))
fig.add_image(run_and_visualize(passage, 'Slope (downward)', noise=2.0, slope=0.1))
fig.add_image(run_and_visualize(passage, 'Shift (downward)', noise=2.0, shift=0.25))
fig.add_image(run_and_visualize(passage, 'Within-line regression', noise=2.0, regression_within=0.5))
fig.add_image(run_and_visualize(passage, 'Between-line regression', noise=2.0, regression_between=0.5))
fig.set_crop_margin(5)
fig.save(core.VISUALS / 'illustration_phenomena.pdf', 83)
# fig.save(core.FIGS / 'fig03_single_column.eps', 83)
