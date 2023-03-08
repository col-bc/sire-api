from google.cloud import storage
from google.oauth2 import service_account
import os


SERVICE_KEY_URL = f'{os.path.join(os.getcwd(), "gcp-service-key.json")}'
credentials = service_account.Credentials.from_service_account_file(SERVICE_KEY_URL)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(
        source_file_name
    )

    return blob._get_download_url(client=storage_client)


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    try:
        blob.delete()
        print(f"Blob {blob_name} deleted.")
    except Exception as e:
        print(f"Error deleting blob: {e}")
        return False
    
    return True
