# Azure Document Translator

This project demonstrates how to upload, translate, and download documents using Azure Cognitive Services and Azure Blob Storage.

Your documents must be in repository called docs.
Translated doc will be in respository translated_docs.

## Requirements

- Python 3.x
- Azure subscription with Cognitive Services and Blob Storage

## Installation

Clone the repository and install the required packages:

```sh

cd DocsTranslator
pip install -r requirements.txt

```
Don't forget to define Azure translation service credentials

```
key = "<your-key>"
endpoint = "https://<your-endpoint>.cognitiveservices.azure.com/"
targetLanguage = 'en'

# Define Azure Blob Storage credentials
storage_account_name = "<your-storage-account-name>"
storage_account_key = "<your-storage-account-key>"

# SAS tokens for the containers
source_sas_token = "<your-source-sas-token>"
target_sas_token = "<your-target-sas-token>"
```

```
python translator.py