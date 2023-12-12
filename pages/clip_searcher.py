import streamlit as st
import clip
import torch
import numpy as np
import pandas as pd
from PIL import Image

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Function to encode search query
def encode_search_query(search_query):
    with torch.no_grad():
        text_encoded = model.encode_text(clip.tokenize(search_query).to(device))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)
    return text_encoded

# Function to find best matches
def find_best_matches(text_features, image_features, image_ids, results_count=3):
    similarities = (image_features @ text_features.T).squeeze(1)
    best_image_idx = (-similarities).argsort()
    return [image_ids[i] for i in best_image_idx[:results_count]]


# Load image features and image IDs
def load_features_ids():
    features_path = r"D:/Projects/ADM Project Final/Wardrobe-Stylist/features" 
    image_ids = pd.read_csv(f"{features_path}/image_ids.csv")
    image_ids = list(image_ids['image_id'])
    image_features = np.load(f"{features_path}/features.npy")
    if device == "cpu":
        image_features = torch.from_numpy(image_features).float().to(device)
    else:
        image_features = torch.from_numpy(image_features).to(device)
    
    return image_features, image_ids


# Function for image search
def search(search_query, results_count=3):
    image_features, image_ids = load_features_ids()
    text_features = encode_search_query(search_query)
    return find_best_matches(text_features, image_features, image_ids, results_count)


# Streamlit app
st.title("Image Search using CLIP")

# Input search query
search_query = st.sidebar.text_input("Enter a search query", 'T shirt')

# Number of results to display per query
n_results_per_query = 3

if st.sidebar.button("Search"):
    result_image_ids = search(search_query, n_results_per_query)

    st.text(search_query)
    columns = st.columns(n_results_per_query)
    for j, image_id in enumerate(result_image_ids):
        image = Image.open(f'D:/Projects/ADM Project Final/Wardrobe-Stylist/Data/{image_id}.jpg')
        columns[j].image(image, caption=f"Image {j+1}")

if __name__ == "__main__":
    # Run the Streamlit app
    pass
    # st.sidebar.text("Run this script with: `streamlit run script_name.py`")
    # st.sidebar.text("Make sure to replace 'script_name.py' with the actual name of your script.")
