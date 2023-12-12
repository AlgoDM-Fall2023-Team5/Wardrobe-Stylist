import streamlit as st
import boto3
import botocore.exceptions

# Collect AWS secrets
bucket_name = st.secrets.aws_credentials.bucket_name
service_name = st.secrets.aws_credentials.service_name
aws_access_key_id = st.secrets.aws_credentials.aws_access_key_id
aws_secret_access_key = st.secrets.aws_credentials.aws_secret_access_key
region_name = st.secrets.aws_credentials.region_name

# S3 client setup
s3_client = boto3.client(
    service_name="s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Streamlit app
st.title("Upload Images to S3")

# Image upload
uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Folder name input
folder_name = st.text_input("Enter a folder name (optional)")

# Function to upload multiple images to S3
def upload_multiple_to_s3(files, folder_name=None):
    try:
        for file in files:
            if folder_name:
                object_key = f"{folder_name}/{file.name}"
            else:
                object_key = file.name

            s3_client.upload_fileobj(file, bucket_name, object_key)
        
        st.success("Upload successful!")
    except botocore.exceptions.NoCredentialsError:
        st.error("AWS credentials not available.")
    except Exception as e:
        st.error(f"Error uploading files to S3: {e}")

# Upload button
if uploaded_files:
    for file in uploaded_files:
        st.image(file, caption=f"Uploaded Image: {file.name}", use_column_width=True)

    if st.button("Upload to S3"):
        upload_multiple_to_s3(uploaded_files, folder_name)
