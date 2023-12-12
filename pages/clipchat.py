import streamlit as st
from snowflake_list import annotations_list
from openai import OpenAI
import json
from macys_items import fetch_product_info
from PIL import Image
import torch
import clip
import numpy as np
import pandas as pd

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



snowflake_url = st.secrets.project_snowflake.url
# role ######################
wardrobe_list = annotations_list(snowflake_url)
role = """
you are my personal wardrobe assistant who has immense experience in the fashion industry. You know the latest trends and people appreciate you often for your fashion choices. You are also funny and give the best advice based on the event. Now, these are my wardrobe data:
Now, answer only the questions I ask and suggest only from the wardrobe.\n {wardrobe_list}
Return in the following format:\n.
"Top : (color: ,clothing type: ,pattern:), 
Bottom : (color: ,clothing type:,pattern:) 
Reason:"\n 
Please only give me responses in the specified format.No spelling error in keys. Remember, the choice should match the exact keyword from the wardrobe. Also, try to include a funny thing in the reason based on the occasion. Return the output in json only.
If any questions other than fashion are asked kindly reply in your words you are not able to. 
""".format(
    wardrobe_list="\n".join(wardrobe_list)
)
Gender = "Men"

def main():
    st.sidebar.title("Chat")
    user_input = st.sidebar.text_area("Enter text:")

    if st.sidebar.button("Submit"):
        return user_input


def interact_with_gpt(question, key, role=role):
    """
    Interacts with GPT-3.5 using the OpenAI API.

    Args:
      question: The question to ask GPT-3.5.
      role: The role to give to GPT-3.5.

    Returns:
      The response from GPT-3.5.
    """

    api_key = key
    client = OpenAI(api_key=api_key)

    # Define the parameters for the request
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": question},
    ]
    temperature = 0.3

    # Send the request to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, temperature=temperature
    )

    answer = response.choices[0].message.model_dump_json()
    # Return the response
    return answer

def disply_clip_image(search_query):
    result_image_ids = search(search_query)

    st.text(search_query)
    columns = st.columns(3)
    for j, image_id in enumerate(result_image_ids):
        image = Image.open(f'D:/Projects/ADM Project Final/Wardrobe-Stylist/Data/{image_id}.jpg')
        columns[j].image(image, caption=f"Image {j+1}")
    


if __name__ == "__main__":
    st.title("Stylist Opinion")

    # question ###################
    openai_key = openai_key_input = st.sidebar.text_input("Enter your OpenAI Key :")

    question = main()

    # handling None while display
    if question is None:
        st.write(
            """:red[Please] :orange[provide] :green[details] :blue[about] :violet[your] :gray[outfit.]"""
        )

    else:

        response = interact_with_gpt(question=question, key=openai_key)
        # Convert the response to a JSON object
        response_json = json.loads(json.loads(response)['content'])
        # Access the specific content you need
        #content = json.loads(response_json["content"])
        
        st.write("Top Wear")
        st.write(response_json['Top'])
        top_string = json.dumps(response_json['Top'])

        disply_clip_image(top_string)
        st.write("Bottom Wear")


        st.write(response_json['Bottom'])

        bottom_string = json.dumps(response_json['Bottom'])

        disply_clip_image(bottom_string)
        st.write("Reason")
        st.write(response_json['Reason'])


        # Recommendations
        st.header("Top Recommendations:")
        top_recommendations = fetch_product_info(response_json['Top']['color'],
                                                  response_json['Top']['clothing type'],
                                                  "outerwear",
                                                  response_json['Top']['pattern'],
                                                  Gender)
        if top_recommendations:
            count = 1
            for product in top_recommendations:
                st.write(f"Product {count}: [link]"+"www.macys.com"+f"{product['product_url']}")
                count = count + 1
        else:
            st.write("Error Retrieving Recommendations")


        st.header("Bottom Recommendations:")
        Bottom_recommendations = fetch_product_info(response_json['Bottom']['color'],
                                                  response_json['Bottom']['clothing type'],
                                                  response_json['Bottom']['pattern'],
                                                  Gender)
        
        if Bottom_recommendations:
            count = 1
            for product in Bottom_recommendations:
                st.write(f"Product {count}: [link]"+"www.macys.com"+f"{product['product_url']}")
                count = count + 1
        else:
            st.write("Error Retrieving Recommendations")



