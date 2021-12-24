import csv
import json
import pathlib
import os
import pandas as pd
from pandas.io.json import json_normalize
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, EntitiesOptions

inFile = "ReadURL.csv"

with open(inFile, 'r') as read_obj:
	csv_reader=csv.reader(read_obj)
	header = next(csv_reader)
	if header != None:
		for col in csv_reader:
			inURL= col[0]
			already_downloaded=col[1]
			if already_downloaded=="Yes":
				pass
			else:      
				authenticator = IAMAuthenticator('G2CkuNwMzqPHtByDgOMTmMIVjJeF1GzT-RCMHvGslddR')
				natural_language_understanding = NaturalLanguageUnderstandingV1(
					version='2020-08-01',
					authenticator=authenticator
				)

				natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/79d13f1f-8a18-4625-8d46-79bc17cdfd20')


				#natural_language_understanding.set_service_url('{url}')

				response = natural_language_understanding.analyze(
					url=inURL,
					#url="https://www.erim.eur.nl/people/stefan-stremersch/",
					features=Features(entities=EntitiesOptions(sentiment=False)),clean=False).get_result()
				data = json_normalize(response['entities'])
				a = data.iloc[(data.groupby(["type"])['relevance'].idxmax())][['type','text']]
				Company = a[(a['type']=="Company")]['text'].to_string(index=False)
				Email = a[(a['type']=="EmailAddress")]['text'].to_string(index=False)
				Location = a[(a['type']=="Location")]['text'].to_string(index=False)
				Person = a[(a['type']=="Person")]['text'].to_string(index=False)
				TopPublication = a[(a['type']=="PrintMedia")]['text'].to_string(index=False)
				Person

				file_exists = os.path.isfile('names.csv')
				with open('names.csv', 'a') as csvfile:
					fieldnames = ['Person', 'Email', 'Company', 'Location']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					if not file_exists:
						writer.writeheader()
					writer.writerow({'Person': Person, 'Email': Email, 'Company':Company, 'Location': Location})