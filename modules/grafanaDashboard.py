import json
import requests

STATUS_FILE = "/var/lib/hymera/status"
TEMPLATE_FILE = "/var/lib/hymera/template.json"
KEY_FILE = "/var/lib/hymera/secret"

class grafanaApi():

	@staticmethod
	def createDashboard():
		with open(TEMPLATE_FILE) as j:
			dashboard = json.load(j)

		with open(STATUS_FILE) as f:
			name = f.read()

		with open(KEY_FILE) as f:
			AUTH_KEY = f.read()

		dashboard["title"] = name
		dashboard["panels"][0]["title"] = name
		dashboard["panels"][0]["measurement"] = name
		dashboard["panels"][0]["targets"][0]["measurement"] = name
		dashboard["id"] = None
		dashboard["uid"] = None
		dashboard["isHome"] = True
		payload = {"dashboard": dashboard, "folderId": 15}
		headers = {"Accept": "application/json",
				"Content-Type": "application/json",
				"Authorization" : "Bearer {0}".format(AUTH_KEY)}

		p = requests.post("http://localhost:80/api/dashboards/db", headers=headers, json=payload)
		return True

if __name__ == "__main__":
	grafanaApi.createDashboard()
