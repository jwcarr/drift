import eyekit
import simulation
import globals


def run_and_visualize(passage, label, **params):
	reading_scenario = simulation.ReadingScenario(**params)
	_, fixation_sequence, _ = reading_scenario.simulate(passage)
	fixation_sequence = eyekit.FixationSequence(fixation_sequence)
	diagram = eyekit.Image(1920, 1080)
	diagram.render_text(passage, color='gray')
	diagram.render_fixations(fixation_sequence, color='black')
	diagram.crop_to_text(30)
	diagram.set_caption(label)
	return diagram


passage = eyekit.TextBlock(globals.lorem_ipsum_text, position=(360, 149), font_name='Courier New', font_size=26.667, line_height=64, adjust_bbox=-7)

noise_diagram = run_and_visualize(passage, 'Noise', noise=20.0)
slope_diagram = run_and_visualize(passage, 'Slope (downward)', noise=2.0, slope=0.1)
shift_diagram = run_and_visualize(passage, 'Shift (downward)', noise=2.0, shift=0.3)
within_diagram = run_and_visualize(passage, 'Within-line regression', noise=2.0, regression_within=0.5)
between_diagram = run_and_visualize(passage, 'Between-line regression', noise=2.0, regression_between=0.5)

figure_layout = [[noise_diagram],
                 [slope_diagram],
                 [shift_diagram],
                 [within_diagram],
                 [between_diagram]]

eyekit.image.make_figure(figure_layout, '../visuals/illustration_phenomena.pdf',
	image_width=83, v_padding=3, h_padding=3, e_padding=1)
eyekit.image.make_figure(figure_layout, '../manuscript/figs/fig04_single_column.eps',
	image_width=83, v_padding=3, h_padding=3, e_padding=1)
