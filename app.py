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

setup_streamlit() # will add more functionality when applicable

streamlit = st.file_uploader('Upload JSON file', type=['json'])

if not streamlit:
	data = fetch_data()
else:
	data = json.loads(streamlit.getvalue())

if type(data) == dict:
	data = data["transactions"]

collateral = []
spend = []

for row in data: # 1 row = 1 transaction
	row["amount"] = row["amount"] / 100
	del row["currency"]
	if row['type'] == 'collateral_add':
		del row["chain"]
		del row["transactionHash"]
		del row["walletAddress"]
		del row["type"]
		collateral.append(row)
	elif row['type'] == 'spend':
		del row["type"]
		spend.append(row)
	else:
		print(f"Unknown type: {row['type']}")

print(f"Collateral rows: {len(collateral)}") 
print(f"Spend rows: {len(spend)}")

collateral_df = pd.DataFrame(collateral)
spend_df = pd.DataFrame(spend)

st.write("Collateral Adds")
st.dataframe(collateral_df)

st.write("Spends")
st.dataframe(spend_df)