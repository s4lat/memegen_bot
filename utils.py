from PIL import Image, ImageDraw, ImageFont
import cfg, textwrap, random, io

def generate_image(img, txt):
	im = Image.open(img["PATH"]).convert('RGBA')

	txt = textwrap.wrap(txt, 25, 
		break_long_words=True, break_on_hyphens=False)

	im_fraction = 0.50
	fontsize = 1

	longest_line = max(txt, key=len)

	fnt = ImageFont.truetype(cfg.FONT, fontsize)
	while (fnt.getsize(longest_line)[0] < im_fraction*im.size[0] 
		and fontsize < 32):
		# iterate until the text size is just larger than the criteria
		fontsize += 1
		fnt = ImageFont.truetype(cfg.FONT, fontsize)

	max_width = fnt.getsize(longest_line)[0]+30
	buttons = []
	for l in txt:
		text_size = fnt.getsize(l)

		button_size = (max_width, text_size[1]+20)
		button_im = Image.new('RGBA', button_size)

		d = ImageDraw.Draw(button_im)
		w, h = text_size
		x, y = (max_width-w)/2, 0
		d.text((x-1, y-1), l, font=fnt, fill='black')
		d.text((x+1, y-1), l, font=fnt, fill='black')
		d.text((x-1, y+1), l, font=fnt, fill='black')
		d.text((x+1, y+1), l, font=fnt, fill='black')
		d.text((x, y),
			l, font=fnt, fill=(255, 255, 255, 255))

		buttons.append(button_im)

	button_width = max_width+10
	button_height = 0
	buttons_height = []
	for b in buttons:
		buttons_height.append(button_height)
		button_height += b.height

	button_im = Image.new("RGBA", (button_width, button_height+40))
	for i, b in enumerate(buttons):
		button_im.paste(b, (0, buttons_height[i]))

	pos = random.choice(img["POS"])
	im.paste(button_im, (int(im.width*pos[0]), int(im.height*pos[1])), 
		button_im)

	b = io.BytesIO()
	im.save(b, "PNG")
	b.seek(0)
	return b

# msg = "Где в слове некст написано следующая суббота?"
# b = generate_image(cfg.IMAGES['1'], msg)

# with open('result.png', 'wb') as f:
# 	f.write(b.read())
