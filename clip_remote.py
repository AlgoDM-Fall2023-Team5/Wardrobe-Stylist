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
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import time


app = FastAPI()

class ProductInfo(BaseModel):
    image_url: str
    product_url: str

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model= clip.load("ViT-B/32", device=device)[0]


# Collect AWS secrets
bucket_name = "team5adm"
service_name = 's3'
aws_access_key_id = 'AKIAQ4WOK7VQVKP4WJVB'
aws_secret_access_key = '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'
region_name = 'us-east-2'

# S3 client setup
s3_client = boto3.client(
    service_name=service_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)



# role ######################
snowflake_url = "snowflake://shirish:Northeastern123@PXTNTMC-FTB58373/CLOTHING_TAGS/PUBLIC?warehouse=COMPUTE_WH&role=ACCOUNTADMIN"
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

def fetch_product_info(keywords):
    print(keywords)
    base_url = "https://www.macys.com/shop/search?keyword=" + "+".join(keywords)

    headers = {
        # 'authority': 'www.macys.com',
        # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }

    # Send a request to get the product information
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product containers
        product_containers = soup.find_all('div', class_='productThumbnail')

        # Create a list to store product information
        products = []

        for container in product_containers:
            # Extract image URL
            img_element = container.find('img', class_='thumbnailImage')
            image_url = img_element['src'] if img_element and 'src' in img_element.attrs else None

            # Extract product URL
            product_url_element = container.find('a', class_='productDescLink')
            product_url = product_url_element['href'] if product_url_element else None

            if image_url and product_url:
                products.append({
                    'image_url': image_url,
                    'product_url': product_url
                })

        time.sleep(2)

        return products

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

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



@app.post("/image-search")
def image_search(query: dict):
    try:
        print(query)
        results = search(str(query))
        return {"image_ids": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_product_info")
async def get_product_info(data: dict):
    # keywords = data.values()
    result = fetch_product_info(list(data))

    if result:
       return {"products": result}


    return JSONResponse(content={"message": "Failed to fetch data"}, status_code=500)





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)