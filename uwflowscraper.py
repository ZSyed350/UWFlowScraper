import requests
import re
import pandas as pd

COURSES_PATH = 'courses' + '.txt'
OUTPUT_PATH = 'listA' + '.xlsx'

URL = "https://uwflow.com/graphql"

QUERY = """
query {
  course {
	id
	code
	name
	description
	antireqs
	prereqs
	rating {
	  liked
	  easy
	  useful
	}
  }
}
"""

HEADERS = {
	"Content-Type": "application/json",
	"User-Agent": "Mozilla/5.0"
}

PATTERN = r":\s*(.*?)\]"
PATTERN2 = r'^([A-Za-z]{2,4}\d{2,3}[A-Za-z]?)'

def extract_course_codes(file_path):
    course_codes = []
    with open(file_path, 'r') as file:
        for line in file:
            # Strip leading/trailing whitespace
            line = line.strip()
            if not line:
                continue  # skip empty lines

            # Match course codes using regex: e.g., "STV100", "MSE442"
            match = re.match(PATTERN2, line)
            if match:
                course_codes.append(match.group(1))

    return course_codes

def get_terms_offered(description):
	offerings = {'F': 'N/A', 'W': 'N/A', 'S': 'N/A'}
	if description:
		match = re.search(PATTERN, description)
		if match:
			result = match.group(1)
			for key in offerings:
				offerings[key] = key in result
	return offerings

if __name__ == "__main__":
	response = requests.post(URL, json={"query": QUERY}, headers=HEADERS)
	data = response.json()

	courses = extract_course_codes(COURSES_PATH)
	course_data = []
	for course in data["data"]["course"]:
		if course["code"].upper() not in [c.upper() for c in courses]:
			continue
		terms = get_terms_offered(course["description"])
		row = {
			"Code": course["code"].upper(),
			"Name": course["name"],
			"Antireqs": course["antireqs"],
			"Prereqs": course["prereqs"],
			"Liked": course["rating"]["liked"] if course["rating"] else 'N/A',
			"Easy": course["rating"]["easy"] if course["rating"] else 'N/A',
			"Useful": course["rating"]["useful"] if course["rating"] else 'N/A',
			"Offered F": terms["F"],
			"Offered W": terms["W"],
			"Offered S": terms["S"]
		}
		
		course_data.append(row)

	df = pd.DataFrame(course_data)

	# Save to Excel
	df.to_excel(OUTPUT_PATH, index=False)
	print("Data written to ", OUTPUT_PATH)