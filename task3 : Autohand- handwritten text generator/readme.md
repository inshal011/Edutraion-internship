#  AUTO HAND - Your Handwriting as an AI-Generated Font

**Auto Hand** is a Gradio-powered web application that takes typed text input and transforms it into handwritten text — in either built-in styles or **your own handwriting** (via `.ttf` font files). The output is rendered on realistic paper textures and downloadable as both `.png` and `.pdf`.

---

## 🚀 Features

- 🖊️ Choose from 4 built-in handwriting fonts
- ✍️ Upload your own `.ttf` handwriting font
- 📄 Choose between A4 or notebook-style paper backgrounds
- 🎨 Customize ink color and font size
- 📸 Realistic blur + semi-transparent ink effect
- 📥 Download output as PNG and PDF

---

## 🧪 RNN-Based Handwriting Experiments (Colab)

Alongside the app, we explored **Recurrent Neural Networks (RNNs)** to understand how sequential models like LSTMs/GRUs learn and replicate handwriting-style patterns. This experimentation is documented in the notebook:

📍 `experiments/handwriting_rnn_experiment.ipynb`

### Highlights:
- Tokenization of character sequences
- RNN architecture and training loop
- Sequence generation and loss evaluation
- Discussion on why `.ttf` font generation is more efficient for the app

---

---

## 🖼️ How to Upload Your Handwriting Font

To generate `.ttf` from your handwriting:

1. Visit [https://www.calligraphr.com](https://www.calligraphr.com)
2. Download the handwriting template
3. Fill it using a pen
4. Scan/upload it to generate a `.ttf` file
5. Upload the `.ttf` in the app and type to see your handwriting in action!

---

## 💻 Try the App Online

👉 Hosted on Hugging Face Spaces: [**🔗 Launch App**][(https://huggingface.co/spaces/inshaladil/AutoHand)]

---

## 🛠️ Tech Stack

- Python
- Gradio
- Pillow (PIL)
- Google Colab (for RNN experimentation)
- Hugging Face Spaces (for app hosting)

---

## 📦 Installation (For Local Setup)

```bash
cd app/
pip install -r requirements.txt
python app.py

### created by : inshal bint-i-adil


