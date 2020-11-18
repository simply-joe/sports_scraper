#Import Selenium
from selenium import webdriver
import pandas as pd
from sqlalchemy import create_engine

#Writing our First Selenium Python Test
web = 'https://sports.tipico.de/en/todays-matches'
path = '/Users/joekrawiec/chromedriver'
driver = webdriver.Chrome(path)
driver.implicitly_wait(45)
driver.get(web)

#Make ChromeDriver click a button
accept = driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]')
accept.click()

#Initialize your storage
teams = []
x12 = [] #3-way
odds_events = []

#Looking for 'sports titles'
sport_title = driver.find_elements_by_class_name('SportTitle-styles-sport')

for sport in sport_title:
    # selecting only football
    if sport.text == 'Football':
        parent = sport.find_element_by_xpath('./..') #immediate parent node
        grandparent = parent.find_element_by_xpath('./..') #grandparent node = the whole 'football' section
        #Looking for single row events
        single_row_events = grandparent.find_elements_by_class_name('EventRow-styles-event-row')
        #Getting data
        for match in single_row_events:
            #'odd_events'
            odds_event = match.find_elements_by_class_name('EventOddGroup-styles-odd-groups')
            odds_events.append(odds_event)
            # Team names
            for team in match.find_elements_by_class_name('EventTeams-styles-titles'):
                teams.append(team.text)
        #Getting data: the odds
        for odds_event in odds_events:
            for n, box in enumerate(odds_event):
                rows = box.find_elements_by_xpath('.//*')
                if n == 0:
                    x12.append(rows[0].text)

driver.quit()
#Storing lists within dictionary
dict_gambling = {'Teams': teams, '1x2': x12}
#Presenting data in dataframe
df_gambling = pd.DataFrame.from_dict(dict_gambling)

engine = create_engine('')
df.to_sql('table', engine)

print(df_gambling)
