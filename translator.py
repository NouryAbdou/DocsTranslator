# Import libraries
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# Define Azure translation service credentials
key = "<your-key>"
endpoint = "<your-end-key"
targetLanguage = 'en'

# Define Azure Blob Storage credentials
storage_account_name = "<your-azure-strorage-accountname"
storage_account_key = "<your-storage-accountkey"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net/", credential=storage_account_key)

# Create container clients
source_container_name = "source"
target_container_name = "target"

# SAS tokens for the containers
source_sas_token = "<your-source-sas-token"
target_sas_token = "<your-target-sas-token"

sourceUri = f"https://{storage_account_name}.blob.core.windows.net/{source_container_name}?{source_sas_token}"
targetUri = f"https://{storage_account_name}.blob.core.windows.net/{target_container_name}?{target_sas_token}"

source_container_client = blob_service_client.get_container_client(source_container_name)
target_container_client = blob_service_client.get_container_client(target_container_name)


# Upload local files to the source container
local_source_dir = "docs"
for filename in os.listdir(local_source_dir):
    file_path = os.path.join(local_source_dir, filename)
    if os.path.isfile(file_path):
        blob_client = source_container_client.get_blob_client(filename)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)


# DOCUMENT TRANSLATION SECTION
# Initialize DocumentTranslationClient
client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

# Begin translation operation
poller = client.begin_translation(sourceUri, targetUri, targetLanguage)
result = poller.result()

# Print translation results
print('Status: {}'.format(poller.status()))
print('Created on: {}'.format(poller.details.created_on))
print('Last updated on: {}'.format(poller.details.last_updated_on))
print('Total number of translations on documents: {}'.format(poller.details.documents_total_count))
print('\nOf total documents...')
print('{} failed'.format(poller.details.documents_failed_count))
print('{} succeeded'.format(poller.details.documents_succeeded_count))

for document in result:
    print('Document ID: {}'.format(document.id))
    print('Document status: {}'.format(document.status))
    if document.status == 'Succeeded':
        print('Source document location: {}'.format(document.source_document_url))
        print('Translated document location: {}'.format(document.translated_document_url))
        print('Translated to language: {}\n'.format(document.translated_to))
    else:
        print('Error Code: {}, Message: {}\n'.format(document.error.code, document.error.message))

# DOWNLOAD TRANSLATED FILES SECTION

local_target_dir = "translated_docs"
os.makedirs(local_target_dir, exist_ok=True)

blobs_list = target_container_client.list_blobs()
for blob in blobs_list:
    blob_client = target_container_client.get_blob_client(blob.name)
    download_file_path = os.path.join(local_target_dir, blob.name)
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

print("All translated files have been downloaded to:", local_target_dir)

# Function to delete all blobs in a container
def delete_all_blobs(container_client):
    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        blob_client = container_client.get_blob_client(blob.name)
        blob_client.delete_blob()
        print(f"Deleted blob: {blob.name}")

# Delete blobs from source and target containers
delete_all_blobs(source_container_client)
delete_all_blobs(target_container_client)

print("All blobs have been deleted from both containers.")