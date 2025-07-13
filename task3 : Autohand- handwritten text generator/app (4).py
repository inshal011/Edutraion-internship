<# app.py

import gradio as gr
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
import textwrap
import os
import tempfile

FONT_OPTIONS = {
    "Patrick Hand": "PatrickHand-Regular.ttf",
    "Journal": "JOURNAL.ttf",
    "Homemade Apple": "HomemadeApple-Regular.ttf",
    "Julia": "Julia_Handwritten.ttf"
}

PAPER_OPTIONS = {
    "notebook": "notebook.jpg",
    "a4": "A4page.jpg"
}

def generate_handwriting(text, font_choice, uploaded_font, font_mode, page_type, font_size, ink_color):
    try:
        bg_path = PAPER_OPTIONS.get(page_type)
        if not os.path.exists(bg_path):
            return None, None, f"Background image not found at {bg_path}"
        background = Image.open(bg_path).convert("RGB")
        width, height = background.size

        if font_mode == "Use built-in font":
            font_path = FONT_OPTIONS.get(font_choice)
        elif uploaded_font is not None:
            font_path = uploaded_font.name
        else:
            return None, None, "No font selected or uploaded."

        if not os.path.exists(font_path):
            return None, None, f"Font file not found at {font_path}"

        font = ImageFont.truetype(font_path, size=font_size)

        margin = 100
        max_width = width - 2 * margin
        draw = ImageDraw.Draw(background)
        lines = textwrap.wrap(text, width=50)
        y_text = margin

        text_layer = Image.new("RGBA", background.size, (255, 255, 255, 0))
        draw_layer = ImageDraw.Draw(text_layer)

        r, g, b = ImageColor.getrgb(ink_color)
        ink_with_alpha = (r, g, b, 160)

        for line in lines:
            draw_layer.text((margin, y_text), line, font=font, fill=ink_with_alpha)
            y_text += font_size + 15

        blurred_layer = text_layer.filter(ImageFilter.GaussianBlur(radius=0.6))
        final_image = Image.alpha_composite(background.convert("RGBA"), blurred_layer).convert("RGB")

        image_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        final_image.save(image_file.name)

        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        final_image.save(pdf_file.name, "PDF", resolution=100.0)

        return image_file.name, pdf_file.name, None

    except Exception as e:
        return None, None, f"Error: {str(e)}"

with gr.Blocks() as demo:
    gr.HTML("<h1 style='text-align: center;'>AUTO HAND - Handwritten Text Generator</h1>")

    with gr.Accordion("ℹ️ How to Upload Your Handwriting (.ttf)", open=False):
        gr.Markdown("""
### Convert Your Own Handwriting to a Font File (.TTF)

You can make this app use your own handwriting! Just follow these steps:

1. Visit [www.calligraphr.com](https://www.calligraphr.com)
2. Sign up (free plan is fine)
3. Download the handwriting template.
4. Fill it using your own handwriting and a **blue/black pen**.
5. Scan or take a clear photo and upload it back to Calligraphr.
6. Download the generated `.ttf` file.
7. Upload that `.ttf` here in the app to convert any text into **your handwriting!**
""")

    text = gr.Textbox(label="Enter your text", lines=4)
    font_mode = gr.Radio(["Use built-in font", "Upload your own handwriting (.ttf)"], label="Font Mode")
    font_choice = gr.Dropdown(choices=list(FONT_OPTIONS.keys()), label="Choose a built-in font", visible=True)
    uploaded_font = gr.File(label="Upload your .ttf file", file_types=[".ttf"], visible=False)

    def toggle_fonts(choice):
        return {
            font_choice: gr.update(visible=(choice == "Use built-in font")),
            uploaded_font: gr.update(visible=(choice == "Upload your own handwriting (.ttf)"))
        }

    font_mode.change(fn=toggle_fonts, inputs=font_mode, outputs=[font_choice, uploaded_font])

    page_type = gr.Radio(["notebook", "a4"], label="Page Type")
    font_size = gr.Slider(20, 110, value=48, label="Font Size")
    ink_color = gr.ColorPicker(label="Ink Color", value="#000000")

    output_image = gr.Image(label="Preview", type="filepath")
    download_png = gr.File(label="Download PNG", visible=True)
    download_pdf = gr.File(label="Download PDF", visible=True)
    error_box = gr.Textbox(label="Error Message", lines=2, visible=True)

    def generate_and_return_file(*args):
        image_path, pdf_path, error = generate_handwriting(*args)
        if image_path:
            return image_path, image_path, pdf_path, ""
        else:
            return None, None, None, error

    gr.Button("Generate").click(
        fn=generate_and_return_file,
        inputs=[text, font_choice, uploaded_font, font_mode, page_type, font_size, ink_color],
        outputs=[output_image, download_png, download_pdf, error_box]
    )

demo.launch()
>