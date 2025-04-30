from google_play_scraper import search, app
import pandas as pd

import os
import sys

# Search for top health and fitness apps
results = search("health and fitness")

apps_data = []
for result in results:
	package_name = result['appId']
	details = app(package_name)
	

	# Remove unwanted keys from the details dictionary
	for key in list(details.keys()):
		if key in ["description"]:
			del details[key]



	apps_data.append(details)

df = pd.DataFrame(apps_data)


# make sure the directory exists
if not os.path.exists('./data/fetched'):
	os.makedirs('./data/fetched')

df.to_csv('./data/fetched/health_and_fitness_apps.csv', index=False)
print("Data saved to ./data/fetched/health_and_fitness_apps.csv")