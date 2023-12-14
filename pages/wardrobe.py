import boto3
import streamlit as st
import botocore.exceptions

#include [aws_credentials] in streamlit secrets######################

# Credentials
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

# Function to display wardrobe images
def display_wardrobe(all_image_ids):
    
    if all_image_ids == None:
        return None
    # Define the number of columns
    num_columns = 3

    # Create columns for displaying images
    columns = st.columns(num_columns)

    # Iterate through all images and display them in columns
    for i, image_id in enumerate(all_image_ids):
        img = s3_client.get_object(Bucket=bucket_name, Key=image_id)
        image_bytes = img['Body'].read()

        # Determine the column to display the image in
        current_column = columns[i % num_columns]

        # Display the image in the current column
        current_column.image(image_bytes, caption=f'Image: {image_id}', use_column_width=True)

folder_name = "Wardrobe"
# Function to list images in the specified folder
def list_images_in_folder(folder_name):
    try:
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)['Contents']
        image_urls = [f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{obj['Key']}" for obj in objects]
        return image_urls
    except botocore.exceptions.NoCredentialsError:
        st.error("AWS credentials not available.")
        return []
    except Exception as e:
        st.error(f"Error listing images in folder: {e}")
        return []


def clear_screen():
    st.image([])

# Streamlit app
def main():
    # Title
    st.title("My Wardrobe")

    col1,col2,col3 = st.columns(3)
    
    with col1:
        # Select box to trigger wardrobe display
        selected_option = st.selectbox("Select an option", ["Show My Wardrobe","Add Image into Wardrobe"])
    

    # List all objects in the specified folder
    folder_path = 'Wardrobe/'
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

    # Extract object keys from the response
    all_image_ids = [obj['Key'] for obj in response.get('Contents', [])]

    
    # Check if the select box option is chosen
    if selected_option == "Show My Wardrobe":
        with col2:
            st.write("")
            st.write("")
            fetch_button = st.button("fetch")

        # Display the wardrobe images
        if fetch_button:
            display_wardrobe(all_image_ids)
        else:
            display_wardrobe(None)
    else:
        st.header("Add your Images!")
        uploaded_file = st.file_uploader("Choose an image file to add", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            if st.button("Add Image"):
                try:
                    object_key = f"{folder_name}/{uploaded_file.name}"
                    s3_client.upload_fileobj(uploaded_file, bucket_name, object_key)
                    st.success(f"Image {uploaded_file.name} added successfully!")
                except botocore.exceptions.NoCredentialsError:
                    st.error("AWS credentials not available.")
                except Exception as e:
                    st.error(f"Error adding image: {e}")


    

# Run the Streamlit app
if __name__ == "__main__":
    main()
