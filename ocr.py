import cv2
import pytesseract
import re
from PIL import Image
import os
from google import genai
from dotenv import load_dotenv

load_dotenv() 

GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')

def preprocess_image(image_path):
    img = cv2.imread(image_path)

    #Resize 
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    #Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Noise removal while keeping edges
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    #Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    #Morphological operations (clean text blobs)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return processed

def clean_ocr_text(text):
    # Common OCR fixes
    replacements = {
        '0': 'o',
        '1': 'l',
        '|': 'l',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


def extract_ingredients(image_path):
    processed = preprocess_image(image_path)
    pil_img = Image.fromarray(processed)

    #OCR
    text = pytesseract.image_to_string(pil_img, config='--psm 6')

    text = clean_ocr_text(text)

    # Normalize
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)

    #Extract ONLY ingredients section
    match = re.search(
        r'(ingredients[:\-]?\s*)(.*?)(manufactured|marketed|expiry|mfg|net wt|$)',
        text,
        re.IGNORECASE
    )

    if match:
        ingredients_text = match.group(2)
    else:
        ingredients_text = text

    # Split ingredients
    ingredients = re.split(r',|;|\.', ingredients_text)

    

    cleaned = []
    for ing in ingredients:
        ing = ing.strip()

        if not ing:
            continue

        ing = re.sub(r'[^a-zA-Z0-9\s\-\(\)]', '', ing)

        cleaned.append(ing)

    ingredients=  ", ".join(cleaned)
    return gemini_post_correction(ingredients)

def gemini_post_correction(ingredients):
    """
    Takes the comma-separated string from your 'extract_ingredients' function 
    and performs chemical-aware error correction.
    """
    if not ingredients.strip():
        return "No ingredients detected."

    model = 'gemini-3.5-flash'
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are an expert INCI (International Nomenclature Cosmetic Ingredient) cleaner.
    I have a list of ingredients extracted via OCR that contains typos and noise.
    
    TASKS:
    1. Fix OCR spelling errors (e.g., 'Sodum Hyalornate' -> 'Sodium Hyaluronate').
    2. Correct character swaps (e.g., 'G1ycerin' -> 'Glycerin') but KEEP valid numbers 
       in chemical names (e.g., 'C12-15 Alkyl Benzoate', 'Vitamin B12', 'CI 77891').
    3. Remove any remaining non-ingredient text (e.g., 'Net Wt', 'Batch', 'Made in').
    4. Standardize capitalization (Title Case).
    
    INPUT LIST:
    {ingredients}
    
    CLEANED LIST (Comma-separated):
    """
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return ingredients
    

