import selenium
from selenium import webdriver
import pandas as pd
import os

##Setting up selenium package parameters
driver = webdriver.Chrome('/Users/mattdolan/Downloads/chromedriver')
driver.get('https://sports.tipico.de/en/all/football/england/premier-league')

#creating empty lists for scraped information
teams = []
x12 = [] #3-way
odds_events = []                                                                                     

#making sure we only collect upcoming matches as opposed to in play
upcoming_matches_box = driver.find_element_by_xpath('//div[contains(@testid, "Program_SELECTION")]')

#football_teams = ['Manchester City', 'Chelsea', 'Liverpool']

#looking for upcoming matches
box = driver.find_element_by_xpath('//div[contains(@testid, "Program_SELECTION")]') #update 3
#Looking for 'sports titles' so we can pull elements in from below function
sport_title = box.find_elements_by_class_name('SportTitle-styles-sport')

#function to pull information from upcoming matches
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


#quitting selenium so we can transform scraped data into data frame                
driver.quit()

#Storing lists within dictionary
dict_gambling = {'Teams': teams, '1x2': x12}

#Presenting data in dataframe
df_gambling = pd.DataFrame.from_dict(dict_gambling)

#print output of scraped data
print(df_gambling)
                    







