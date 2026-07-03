from sentence_transformers import SentenceTransformer
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def image_to_text(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description


def build_text(stock):
    return f"""
    Product Name: {stock['Name']}
    Product Code: {stock['Code']}
    Low Price: {stock['LowPrice']}
    High Price Price: {stock['HighPrice']}
    Product Source: {stock['Source']}
    Image Description: {stock['ImageDescription']}
"""


def embedd(text):
    try:
        return embedding_model.encode(text).tolist() # to list so qdrant can understand it
    except:
        return 0
