import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NEW_RELIC_API_KEY")
account_id = os.getenv("NEW_RELIC_ACCOUNT_ID")

url = "https://api.newrelic.com/graphql"

query = """
{
  actor {
    user {
      name
    }
  }
}
"""

headers = {
    "Content-Type": "application/json",
    "API-Key": api_key
}

response = requests.post(
    url,
    headers=headers,
    json={"query": query}
)

print("HTTP Status:", response.status_code)
print("Response:")
print(response.json())
