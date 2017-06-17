import os
import numpy as np
import config as cfg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

if not os.path.exists('output'):
  os.mkdir('output')

mat = np.zeros(cfg.size, dtype=np.uint8)
img = Image.fromarray(mat)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("fonts/solaimanlipi.ttf", 20)
draw.text((5, 2), "A", 255, font=font)
img.save('output/0001.jpg')
