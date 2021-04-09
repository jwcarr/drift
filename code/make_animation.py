from PIL import Image
import imageio
import eyekit
import core

def make_image(seq, number):
	img = eyekit.vis.Image(1920, 1080)
	img.draw_text_block(txt)
	img.draw_fixation_sequence(seq, color='DarkSlateGray')
	img.save(core.VISUALS / 'animation_frames' / f'{number}.png', crop_margin=40)

def make_frames():
	make_image(orig_seq, 0)
	for i, (of, nf) in enumerate(zip(orig_seq, corr_seq), 1):
		of.y = nf.y
		make_image(orig_seq, i)

def make_animation():
	images = []
	for i in range(136):
		print(i)
		im = Image.open(str(core.VISUALS / 'animation_frames' / f'{i}.png'))
		im = im.resize((800, 450))
		if i == 0:
			for _ in range(60):
				images.append(im)
		elif i == 135:
			for _ in range(60):
				images.append(im)
		else:
			images.append(im)
	imageio.mimsave(str(core.VISUALS / 'animation.gif'), images, fps=30, loop=0, palettesize=8, subrectangles=True)


data = eyekit.io.read(core.FIXATIONS / 'sample.json')
txt = eyekit.io.read(core.DATA / 'passages.json')['1B']

orig_seq = data['trial_5']['fixations']
corr_seq = orig_seq.copy()

eyekit.tools.snap_to_lines(corr_seq, txt)

# make_frames()
make_animation()
