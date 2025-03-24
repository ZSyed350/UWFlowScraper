import requests

url = "https://uwflow.com/graphql"

query = """
query {
  course {
    id
    code
    name
    description
  }
}
"""

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

response = requests.post(url, json={"query": query}, headers=headers)
data = response.json()

# Example: print just MTE380 course info
for course in data["data"]["course"]:
    if course["code"].lower() == "mte380":
        print(f"Code: {course['code']}")
        print(f"Name: {course['name']}")
        print(f"Description: {course['description']}")
