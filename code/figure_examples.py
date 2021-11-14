import eyekit
import core

eyekit.vis.set_default_font('Helvetica Neue', 8)

data = eyekit.io.load(core.FIXATIONS / 'sample.json')
passages = eyekit.io.load(core.DATA / 'passages.json')

adult_fixation_sequence = data['trial_5']['fixations']  #   8, 1B
child_fixation_sequence = data['trial_30']['fixations'] # 204, 4A

adult = eyekit.vis.Image(1920, 1080)
adult.draw_text_block(passages['1B'], mask_text=True)
adult.draw_fixation_sequence(adult_fixation_sequence)
adult.set_caption('Reading trial by an adult')

child = eyekit.vis.Image(1920, 1080)
child.draw_text_block(passages['4A'], mask_text=True)
child.draw_fixation_sequence(child_fixation_sequence)
child.set_caption('Reading trial by a child')

fig = eyekit.vis.Figure(1, 2)
fig.add_image(adult)
fig.add_image(child)
fig.set_crop_margin(3)
fig.set_padding(vertical=2, horizontal=3, edge=1)
fig.set_enumeration('<a>  ', font_size=12)
fig.save(core.VISUALS / 'illustration_examples.pdf', width=174)
# fig.save(core.FIGS / 'fig01_double_column.eps', width=174)
