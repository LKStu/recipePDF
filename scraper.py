#!/usr/bin/env python3

from recipe_scrapers import scrape_me
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from textwrap import wrap
from PIL import Image
import requests

# Source
url = 'https://www.jamieoliver.com/recipes/pasta-recipes/goldie-hawn-s-fettuccine-alfredo/'
scraper = scrape_me(url)

# Gathering information
title = scraper.title()
ingredients = scraper.ingredients()
instructions = scraper.instructions()

# Setting up PDF document. A4 dimensions: 210 and 297 mm
pdf = canvas.Canvas('recipe.pdf', pagesize=A4)
width, height = A4
margins_side: float = 2.5 * cm
margins_top: float = 2.5 * cm
margins_bottom: float = 2.0 * cm

# Title
pdf.setFont('Helvetica-Bold', 20)
title_pos = height - margins_top
pdf.drawString(margins_side, title_pos, title)

# Ingredients
ingredients_x = margins_side
ingredients_y = title_pos - (2 * cm)
pdf.setFont("Helvetica-Bold", 12)
pdf.drawString(ingredients_x, ingredients_y, text="Ingredients:")
pdf.setFont("Helvetica", 12)
for ingredient in ingredients:
    ingredients_y = ingredients_y - (0.5 * cm)
    pdf.drawString(ingredients_x, ingredients_y, u'    \u2022 ' + ingredient)

# Getting the image
image_url = scraper.image()
img_data = requests.get(image_url).content
with open('image.jpg', 'wb') as handler:
    handler.write(img_data)
# Resizing the image
img = Image.open("image.jpg")
img_width = 125
scaling_percent = (img_width / float(img.size[0]))
img_height = int((float(img.size[1]) * float(scaling_percent)))
img = img.resize((img_width, img_height), Image.ANTIALIAS)
img.save('image.jpg', 'JPEG')
# Positioning image
img_pos_x = width - (7 * cm)
img_pos_y = height - (8 * cm)
pdf.drawImage("image.jpg", img_pos_x, img_pos_y)
# pdf.drawImage("image.jpg", img_pos_x, img_pos_y, 5 * cm, 7.5 * cm)

# Instructions
# TODO: Fix paragraphs and spacing; add listing
wrapped_instructions = "\n".join(wrap(instructions, 95))
instructions_pos_x = margins_side
instructions_pos_y = ingredients_y - (1.5 * cm)
pdf.setFont("Helvetica-Bold", 12)
pdf.drawString(instructions_pos_x, instructions_pos_y, text="Instructions:")
instructions_pos_y = instructions_pos_y - (0.5 * cm)
pdf.setFont("Helvetica", 12)
textObject = pdf.beginText()
textObject.setTextOrigin(instructions_pos_x, instructions_pos_y)
textObject.setFont("Times-Roman", 12)
textObject.textLines(wrapped_instructions)
pdf.drawText(textObject)

# Generating and saving PDF
pdf.showPage()
pdf.save()
