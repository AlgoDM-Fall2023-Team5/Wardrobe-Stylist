import streamlit as st
import boto3
import botocore.exceptions
from io import BytesIO

# Collect AWS secrets
bucket_name = st.secrets.aws_credentials.bucket_name
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
st.title("S3 Image Viewer and Editor")

# Folder name input
# folder_name = st.text_input("Enter a folder name")
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

# Display images in the specified folder
# image_urls = list_images_in_folder(folder_name)
# if image_urls:
#     for image_url in image_urls:
#         st.image(image_url, caption=image_url, use_column_width=True)

# Option to delete an image
# image_to_delete = st.text_input("Enter the name of the image to delete (e.g., image.jpg)")
# if st.button("Delete Image"):
#     try:
#         s3_client.delete_object(Bucket=bucket_name, Key=f"{folder_name}/{image_to_delete}")
#         st.success(f"Image {image_to_delete} deleted successfully!")
#     except botocore.exceptions.NoCredentialsError:
#         st.error("AWS credentials not available.")
#     except Exception as e:
#         st.error(f"Error deleting image: {e}")

# Option to add an image
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
