# Cosmetic Ingredient Recognition and Product Recommendation

A Digital Image Processing and Machine Learning project that extracts cosmetic ingredients from product label images, evaluates ingredient safety using an external dataset, and recommends suitable skincare products.

## Features

- Image preprocessing using OpenCV
- Automatic document/label detection using contour detection
- Perspective correction for tilted product images
- Adaptive thresholding and morphological operations for OCR enhancement
- Ingredient extraction using Tesseract OCR
- OCR text cleaning and ingredient normalization
- Safety analysis using an external cosmetic ingredient dataset
- Product recommendation using a machine learning model
- Simple Flask-based web interface

---

## Project Pipeline

```
Input Cosmetic Label Image
        │
        ▼
Image Preprocessing
(OpenCV)
• Resize
• Grayscale Conversion
• Noise Removal
• Contour Detection
• Perspective Transformation
• Adaptive Thresholding
• Morphological Operations
        │
        ▼
Enhanced Image
        │
        ▼
Tesseract OCR
        │
        ▼
Extracted Text
        │
        ▼
Text Cleaning
• OCR Correction
• Regex Parsing
• Manufacturer Information Removal
• Ingredient Normalization
        │
        ▼
Ingredient List
        │
        ▼
Safety Analysis
(External Ingredient Dataset)
        │
        ▼
Product Recommendation
(scikit-learn)
```

---

## Technologies Used

- Python
- OpenCV
- Tesseract OCR
- Pillow
- scikit-image
- scikit-learn
- Flask
- Pandas
- NumPy

---

## Digital Image Processing Techniques

The project applies several image processing techniques before OCR:

- Grayscale conversion
- Gaussian/Bilateral filtering
- Canny edge detection
- Contour detection
- Perspective transformation
- Adaptive thresholding
- Morphological operations

These significantly improve OCR accuracy on cosmetic labels.

---

## OCR

The enhanced image is passed to **Tesseract OCR** to convert printed ingredient labels into machine-readable text.

OCR output is then processed using:

- Regular expressions
- Text normalization
- OCR error correction
- Ingredient parsing

---

## Ingredient Safety Analysis

Each extracted ingredient is matched against an external cosmetic ingredient safety dataset.

The system determines:

- Safe ingredients
- Potential irritants
- Ingredient functions
- Safety ratings

---

## Product Recommendation

Based on the extracted ingredients and safety analysis, a machine learning model recommends suitable skincare products.

---

## Project Structure

```
.
├── app.py                  # Flask application
├── model.py                # Recommendation model
├── ingredient_extractor.py # OCR and image processing
├── dataset/
│   ├── ingredients.csv
│   └── products.csv
├── static/
├── templates/
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Tesseract OCR

### macOS

```bash
brew install tesseract
```

### Ubuntu

```bash
sudo apt install tesseract-ocr
```

### Windows

Download and install Tesseract OCR and add it to your system PATH.

---

## Run

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## Future Improvements

- EasyOCR integration
- Ingredient spell correction using fuzzy matching
- Deep learning-based text detection
- Mobile application support
- Automatic INCI ingredient validation
- Explainable recommendation system

---

## Authors

Developed as part of a Digital Image Processing project.
