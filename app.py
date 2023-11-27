import streamlit as st
import pandas as pd
import json
import os
import requests

def fetch_data():
	url = "https://api.raincards.xyz/v1/transactions"
	headers = {
		"Accept": "application/json",
		"Api-Key": os.environ.get('API_KEY')
	}
	response = requests.get(url, headers=headers)
	return response.json()

def setup_streamlit():
	st.title('Parse card transaction data')
	return st.file_uploader('Upload JSON file', type=['json'])

def main(streamlit: st.file_uploader = None):
	if not streamlit:
		data = fetch_data()
	else:
		data = json.loads(streamlit.getvalue())

	if type(data) == dict:
		data = data["transactions"]

	collateral = []
	spend = []

	for row in data:
		if 'collateral_add' in row['type']:
			collateral.append(row)
		elif 'spend' in row['type']:
			spend.append(row)

	print(f"Collateral rows: {len(collateral)}") 
	print(f"Spend rows: {len(spend)}")

	collateral_df = pd.DataFrame(collateral)
	spend_df = pd.DataFrame(spend)

main()