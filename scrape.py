#!/usr/bin/env python3

from recipe_scrapers import scrape_me
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from textwrap import wrap
from PIL import Image
import requests
import os

# Source
url = 'https://www.jamieoliver.com/recipes/pasta-recipes/goldie-hawn-s-fettuccine-alfredo/'
scraper = scrape_me(url)

# Gathering information
title = scraper.title()
ingredients = scraper.ingredients()
instructions = scraper.instructions()

# Setting up PDF document. A4 dimensions: 210 and 297 mm
width, height = A4
margins_side: float = 2.5 * cm
margins_top: float = 2.5 * cm
margins_bottom: float = 2.0 * cm


# Title
def make_title(pdf, title_name, title_pos):
    """Generating the PDF with by calling other methods"""
    pdf.setFont('Helvetica-Bold', 20)
    pdf.drawString(margins_side, title_pos, title_name)


# Ingredients
def make_ingredients(pdf, pos_x, pos_y):
    """Generating the PDF with by calling other methods"""
    ingredients_pos_y = pos_y
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(pos_x, ingredients_pos_y, text="Ingredients:")
    pdf.setFont("Helvetica", 12)
    for ingredient in ingredients:
        ingredients_pos_y = ingredients_pos_y - (0.5 * cm)
        pdf.drawString(pos_x, ingredients_pos_y, u'    \u2022 ' + ingredient)
    return ingredients_pos_y


def make_image(pdf, img_url, pos_x, pos_y):
    """Generating the PDF with by calling other methods"""
    img_data = requests.get(img_url).content
    with open('image.jpg', 'wb') as handler:
        handler.write(img_data)
    # Resizing the image... Necessary?
    img = Image.open("image.jpg")
    img_width = 125
    scaling_percent = (img_width / float(img.size[0]))
    img_height = int((float(img.size[1]) * float(scaling_percent)))
    img = img.resize((img_width, img_height), Image.ANTIALIAS)
    img.save('image.jpg', 'JPEG')
    # Finally, draw the image
    pdf.drawImage("image.jpg", pos_x, pos_y)
    # pdf.drawImage("image.jpg", img_pos_x, img_pos_y, 5 * cm, 7.5 * cm)


# Instructions
# TODO: Fix paragraphs and spacing; add listing
def make_instructions(pdf, ingredients_y):
    """Generating the PDF with by calling other methods"""
    instructions_pos_x = margins_side
    instructions_pos_y = ingredients_y - (1.5 * cm)
    wrapped_instructions = "\n".join(wrap(instructions, 95))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(instructions_pos_x, instructions_pos_y, text="Instructions:")
    instructions_pos_y = instructions_pos_y - (0.5 * cm)
    pdf.setFont("Helvetica", 12)
    text_object = pdf.beginText()
    text_object.setTextOrigin(instructions_pos_x, instructions_pos_y)
    text_object.setFont("Times-Roman", 12)
    text_object.textLines(wrapped_instructions)
    pdf.drawText(text_object)


def generate_pdf(save_location, margins_top=(2.5 * cm), margins_bottom=(2.5 * cm), margins_side=(2.5 * cm)):
    """Generating the PDF with by calling other methods"""
    pdf = canvas.Canvas(save_location, pagesize=A4)
    title_position = height - margins_top
    ingredients_x = margins_side
    ingredients_y = title_position - (2 * cm)
    image_url = scraper.image()
    img_pos_x = width - (7 * cm)
    img_pos_y = height - (8 * cm)

    # Call other methods
    make_title(pdf, title, title_position)
    ingredients_y = make_ingredients(pdf, ingredients_x, ingredients_y)
    make_image(pdf, image_url, img_pos_x, img_pos_y)
    make_instructions(pdf, ingredients_y)

    pdf.showPage()
    pdf.save()


# Generating and saving PDF
pdf_name = title + ".pdf"
save_loc = os.path.join(os.path.expanduser("~"), "Desktop/", pdf_name)
generate_pdf(save_loc)
