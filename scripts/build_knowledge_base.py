import pandas as pd
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Ensure this is called before accessing environment variables
load_dotenv()

# CONSTANTS
CSV_PATH = "../data/cleaned/health_and_fitness_apps.csv"
KEY_COLUMN = "appId"  # The column to be used as the unique key for each document

# Azure Search configuration
SEARCH_SERVICE_NAME = os.getenv("SEARCH_SERVICE_NAME")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
AZURE_SEARCH_ENDPOINT = f"https://{SEARCH_SERVICE_NAME}.search.windows.net"


def prepare_documents(df):
	"""Converts a DataFrame to a list of docts formatted for Azure Search upload."""

	# Fill NaNs
	df = df.fillna("")

	# Ensure ID field is present (e.g., appId)
	if KEY_COLUMN not in df.columns:
		raise ValueError(f"DataFrame must contain {KEY_COLUMN} column.")

	# Preprocess Key column: Keys can only contain letters, digits, underscore (_), dash (-), or equal sign (=).
	# Replace invalid characters with underscore
	df[KEY_COLUMN] = df[KEY_COLUMN].str.replace(r"[^a-zA-Z0-9_=-]", "_", regex=True)
	
	
	# Cast columns if necessary
	return df.to_dict(orient="records")


def upload_to_search_index(documents):
	"""Uploads documents to Azure Cognitive Search index."""
	search_client = SearchClient(
		endpoint=AZURE_SEARCH_ENDPOINT,
		index_name=SEARCH_INDEX_NAME,
		credential=AzureKeyCredential(SEARCH_API_KEY),
	)

	result = search_client.upload_documents(documents=documents)
	succeeded = sum(1 for r in result if r.succeeded)
	failed = len(result) - succeeded

	print(f"Uploaded {succeeded} documents succeeded.")
	if failed > 0:
		print(f"Failed to upload {failed} documents.")
		for r in result:
			if not r.succeeded:
				print(f"Failed document key: {r.key}, error: {r.error_message}")



def main():
	# Load CSV
	df = pd.read_csv(CSV_PATH)

	# Prepare documents
	documents = prepare_documents(df)

	# Upload
	upload_to_search_index(documents)


if __name__ == "__main__":
	main()