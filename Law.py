from bs4 import BeautifulSoup
import requests 
from pandas import DataFrame



how_many_ids = 10
col_names = {}
for i in range(1,how_many_ids):
	try:
		url = r'https://www.law.com/law-firm-profile/?id={}'.format(i)
		response = requests.get(url).text
		soup = BeautifulSoup(response, 'html.parser')
		name = soup.find('h1' ,{'class':'page-title left'}).text
		description = soup.find('p' ,{'class':'description'}).text
		rankings = soup.find_all('div',  {'class':'rankings'})
		children = soup.find('ul' ,{'class':'overview'}).findChildren('li' , recursive=False)
		for rank in rankings:
			survey_name = rank.find('p', {'class':'survey-name'}).text.replace(' ', '-')
			years = [x.text for x in rank.find_all('p' ,{'class':'date'})]
			positions   = [r.text.replace('#','') for r in rank.find_all('p', {'class':'rank'})]
			for year , pos  in zip(years , positions):
				if not(f"{survey_name}_yr-{year}") in col_names:
					col_names[f"{survey_name}_yr-{year}"] = []
				col_names[f"{survey_name}_yr-{year}"].append(pos)	

		for child in children:
			row , description = child.findChildren('div',{'class':'col-md-6'}, recursive=False)
			if not(row.text) in col_names:
				col_names[row.text] = []
			col_names[row.text].append(description.text)
	except:
		continue



df = DataFrame.from_dict(col_names)
df.to_excel('LawFirm.xlsx', header=True)