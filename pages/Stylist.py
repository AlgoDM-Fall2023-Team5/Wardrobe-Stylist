import streamlit as st
from openai import OpenAI
import json
from PIL import Image
from io import BytesIO
import boto3
from snowflake_list import annotations_list
from macys_items import fetch_product_info
import requests


url_clip="http://3.133.150.2/image-search"

url_product="http://3.133.150.2/get_product_info"
# Collect AWS secrets
try:
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
except Exception as e:
    st.error(f"Error collecting AWS secrets: {str(e)}")



# role ######################
try:
    snowflake_url = st.secrets.project_snowflake.url
    wardrobe_list = annotations_list(snowflake_url)
except Exception as e:
    st.error(f"Error fetching wardrobe list: {str(e)}")

role = """
you are my personal wardrobe assistant who has immense experience in the fashion industry. You know the latest trends and people appreciate you often for your fashion choices. You are also funny and give the best advice based on the event. Now, these are my wardrobe data:
Now, answer only the questions I ask and suggest only from the wardrobe.\n {wardrobe_list}
Return in the following format:\n.
"Top : (color: ,clothing type: ,pattern:), 
Bottom : (color: ,clothing type:,pattern:) 
Reason:"\n 
Please only give me responses in the specified format. No spelling error in keys. Remember, the choice should match the exact keyword from the wardrobe. Also, try to include a funny thing in the reason based on the occasion. Return the output in json only.
If any questions other than fashion are asked kindly reply in your words you are not able to. 
""".format(
    wardrobe_list="\n".join(wardrobe_list)
)
Gender = "Men"

# Function to display images from S3

def display_images_from_s3(image_ids):
    columns = st.columns(2)
    for j, image_id in enumerate(image_ids):
        image_data = s3_client.get_object(Bucket=bucket_name, Key=f"Wardrobe/{image_id}.jpg")['Body'].read()
        image = Image.open(BytesIO(image_data))
        columns[j].image(image, caption=f"Image {j+1}")


def main():
    st.sidebar.title("Chat")
    user_input = st.sidebar.text_area("Enter text to Transform Your Event Look!:")

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

    try:
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

    except Exception as e:
        st.error(f"Error interacting with GPT-3.5: {str(e)}")
        return None

if __name__ == "__main__":
    st.title("Stylist Opinion")

    try:
        # question ###################
        openai_key = st.sidebar.text_input("Enter your OpenAI Key :")

        question = main()

        # handling None while display
        if question is None:
            st.write(
                """:red[Please] :orange[provide] :green[details] :blue[about] :violet[your] :gray[outfit.]"""
            )

        else:
            response = interact_with_gpt(question=question, key=openai_key)
            if response is not None:
                response_json = json.loads(json.loads(response)['content'])

                st.write("Top Wear")
                top_string = json.dumps(response_json['Top'])
                # display_images_from_s3(search(top_string))
                response = requests.post( url_clip, json={"query": top_string})
                response.raise_for_status()  
                result = response.json()
                # Display the images returned by the FastAPI endpoint
                display_images_from_s3(result['image_ids'])



                st.write("Bottom Wear")
                bottom_string = json.dumps(response_json['Bottom'])
                response2 = requests.post(url_clip, json={"query": bottom_string})
                response2.raise_for_status()  
                result2 = response2.json()
                # Display the images returned by the FastAPI endpoint
                display_images_from_s3(result2['image_ids'])


                st.write("Reason")
                st.write(response_json['Reason'])

                # Recommendations
                st.header("Top Recommendations:")
                url_top = [response_json['Top']['color'],
                                                            response_json['Top']['clothing type'],
                                                            response_json['Top']['pattern'],
                                                            Gender]
                

                try:
                    response = requests.post(url_product, json={"urls": url_top})
                    response.raise_for_status()  # Raise an exception for 4xx and 5xx errors
                    Top_recommendations = response.json()
                    count = 1
                    for product in Top_recommendations["products"]:
                        st.write(f"Product {count}: [link]" + "www.macys.com" + f"{product['product_url']}")
                        count = count + 1
                        # product["image_url"]

                
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching products: {e}")

                st.header("Bottom Recommendations:")
                # Bottom_recommendations = fetch_product_info(response_json['Bottom']['color'],
                #                                             response_json['Bottom']['clothing type'],
                #                                             response_json['Bottom']['pattern'],
                #                                             Gender)

                # Bottom_recommendations = None

                url_bottom = [response_json['Bottom']['color'],
                                                            response_json['Bottom']['clothing type'],
                                                            response_json['Bottom']['pattern'],
                                                            Gender]
                

                try:
                    response = requests.post(url_product, json={"urls": url_bottom})
                    response.raise_for_status()  # Raise an exception for 4xx and 5xx errors
                    Bottom_recommendations = response.json()
                    count = 1
                    for product in Bottom_recommendations["products"]:
                        st.write(f"Product {count}: [link]" + "www.macys.com" + f"{product['product_url']}")
                        count = count + 1
                        # product["image_url"]

                
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching products: {e}")


                    


    except Exception as e:
        st.error(f"Please Enter Valid Input or Try Again.An unexpected error occurred: {str(e)}")
        
