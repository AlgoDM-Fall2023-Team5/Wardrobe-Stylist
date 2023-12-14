import streamlit as st
from PIL import Image
import torch
import clip
import numpy as np
import pandas as pd
from io import BytesIO
import boto3
from snowflake_list import annotations_list
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from pydantic import BaseModel
import uvicorn
import io

app = FastAPI()


# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model= clip.load("ViT-B/32", device=device)[0]


# Collect AWS secrets
bucket_name = st.secrets.aws_credentials.bucket_name
service_name = st.secrets.aws_credentials.service_name
aws_access_key_id = st.secrets.aws_credentials.aws_access_key_id
aws_secret_access_key = st.secrets.aws_credentials.aws_secret_access_key
region_name = st.secrets.aws_credentials.region_name

# S3 client setup
s3_client = boto3.client(
    service_name=service_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)



# role ######################
snowflake_url = st.secrets.project_snowflake.url
wardrobe_list = annotations_list(snowflake_url)





# Load image features and image IDs from S3

def load_features_ids():
    features_path_s3 = "features"

    # Load the image IDs from S3
    image_ids_data = s3_client.get_object(Bucket=bucket_name, Key=features_path_s3 + 'image_ids.csv')['Body'].read()
    image_ids = pd.read_csv(BytesIO(image_ids_data))
    image_ids = list(image_ids['image_id'])

    # Load the features vectors from S3
    features_data = s3_client.get_object(Bucket=bucket_name, Key=features_path_s3 + 'features.npy')['Body'].read()
    image_features = np.load(BytesIO(features_data))

    if device == "cpu":
        image_features = torch.from_numpy(image_features).float().to(device)
    else:
        image_features = torch.from_numpy(image_features).to(device)

    return image_features, image_ids


# Function to encode search query

def encode_search_query(search_query):
    with torch.no_grad():
        text_encoded = model.encode_text(clip.tokenize(search_query).to(device))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)
    return text_encoded

# Function to find best matches
def find_best_matches(text_features, image_features, image_ids, results_count=2):
    similarities = (image_features @ text_features.T).squeeze(1)
    best_image_idx = (-similarities).argsort()
    return [image_ids[i] for i in best_image_idx[:results_count]]

# Function for image search

def search(search_query, results_count=2):
    image_features, image_ids = load_features_ids()
    text_features = encode_search_query(search_query)
    return find_best_matches(text_features, image_features, image_ids, results_count)


# Function to display images from S3
# def display_images_from_s3(image_ids):
#     columns = st.columns(3)
#     for j, image_id in enumerate(image_ids):
#         image_data = s3_client.get_object(Bucket=bucket_name, Key=f"Wardrobe/{image_id}.jpg")['Body'].read()
#         image = Image.open(BytesIO(image_data))
#         columns[j].image(image, caption=f"Image {j+1}")


@app.post("/image-search")
def image_search(query: dict):
    try:
        print(query)
        results = search(str(query))
        return {"image_ids": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
