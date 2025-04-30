from google_play_scraper import search, app
import pandas as pd

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

df.to_csv('health_and_fitness_apps.csv', index=False)
print("Data saved to health_and_fitness_apps.csv")