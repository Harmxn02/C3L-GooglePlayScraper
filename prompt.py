from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

from bs4 import BeautifulSoup

# Ensure this is called before accessing environment variables
load_dotenv()

# Azure Search configuration
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")

# Azure OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_API_VERSION = "2024-12-01-preview"

# Initialise OpenAI client

endpoint = "https://harma-mab1hz0w-swedencentral.cognitiveservices.azure.com/"

openai_client = AzureOpenAI(
    api_version=OPENAI_API_VERSION,
    azure_endpoint=OPENAI_ENDPOINT,
	api_key=OPENAI_API_KEY,
)

# Initialise Search client
search_client = SearchClient(
	endpoint=SEARCH_ENDPOINT,
	index_name=SEARCH_INDEX_NAME,
	credential=AzureKeyCredential(SEARCH_API_KEY),
)


def query_search(query):
	# Query the Azure AI Search index
	results = search_client.search(query, query_type=QueryType.SIMPLE)
	documents = [doc for doc in results]
	print(f"Found {len(documents)} documents in the index.")
	return documents


def extract_content(doc):
	"""Extract relevant content from a document, focusing on specific fields."""
	title = doc.get("title", "")
	description = BeautifulSoup(doc.get("descriptionHTML", ""), "html.parser").get_text()
	summary = doc.get("summary", "")
	url = doc.get("url", "")
	score = doc.get("score", "")
	price = doc.get("price", "")

	# Combine title, summary, and cleaned description into context
	content = f"""
		Title: {title}
		\nSummary: {summary}
		\nDescription: {description[:200]}
		\nURL: {url}\n
		\nScore: {score}
		\nPrice: {price}
		"""
	return content


def generate_response(prompt, documents):
	# Combine documents content into a prompt for the LLM
	context = "\n".join([extract_content(doc) for doc in documents])
	prompt_with_context = f"""
	Use the following context to answer the question.
	Answer the question as concisely as possible, do not add too much information.
	If you mention the name of an app, also provide the name and app url as a link in markdown format, e.g. [app name](app url).
	If make a list, use bullet points.
	Only use the information in the context to answer the question.
	\n\nContext:\n\n{context}\n
	
	
	\nQuestion: {prompt}
	\nAnswer:
	"""

	# Get the response from the LLM
	response = openai_client.completions.create(
		model=OPENAI_DEPLOYMENT_NAME,
		prompt=prompt_with_context,
		max_tokens=200,
		temperature=0.7,
	)

	return response.choices[0].text.strip()


def main(query):
	# Perform the search
	documents = query_search(query)

	if documents:
		response = generate_response(query, documents)
		print(f"Response: {response}")
	else:
		print("No relevant documents founds in the index.")


if __name__ == "__main__":
	query = input("Prompt: ")
	main(query)