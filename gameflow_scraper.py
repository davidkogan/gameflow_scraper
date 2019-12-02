from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
from collections import OrderedDict
from selenium.common.exceptions import TimeoutException

csv_file = open('game_data.csv', 'w')
writer = csv.writer(csv_file, dialect = 'excel')
writer.writerow(['gameid', 'date', 'awayteam', 'hometeam', 'final_away_score', 'final_home_score', 'line', 'gameflow'])

driver = webdriver.Chrome(ChromeDriverManager().install())

import itertools

dates = [[str(2013 + i) for i in range(6)], ['01', '02', '03', '04', '05', '10', '11', '12'], 
         ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', 
          '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']]
dates = list(itertools.product(*dates))
dates = list(map(lambda x: ''.join(x), dates))
for x in dates:
    if(x[4:] == '0229' or x[4:] == '0230' or x[4:] == '0431' or x[4:] == '1131'):
        dates.remove(x)

urls = ['http://www.espn.com/nba/scoreboard/_/date/' + date for date in dates]

gameid = 1
for url in urls:
    try:
        driver.get(url)
    except TimeoutException:
        continue
    gamelinks = [x.get_attribute('href') for x in driver.find_elements_by_class_name('mobileScoreboardLink')]
    date = url[42:]
    for link in gamelinks:
        game_dict = OrderedDict()
        game_dict['gameid'] = gameid
        game_dict['date'] = date 
        driver.get(link) 
        try:
            game_dict['awayteam'] = driver.find_elements_by_class_name('abbrev')[0].get_attribute('title')
        except:
            game_dict['awayteam'] = 'Null'
        try:
            game_dict['hometeam'] = driver.find_elements_by_class_name('abbrev')[1].get_attribute('title')
        except:
            game_dict['hometeam'] = 'Null'
        try:
            game_dict['final_away_score'] = driver.find_elements_by_class_name('score-container')[0].text
        except:
            game_dict['final_away_score'] = 'Null'
        try:
            game_dict['final_home_score'] = driver.find_elements_by_class_name('score-container')[1].text
        except:
            game_dict['final_home_score'] = 'Null'
        try:
            game_dict['line'] = driver.find_elements_by_class_name('odds-details')[0].text
        except:
            game_dict['line'] = 'Null'
        try:
            game_dict['gameflow'] = driver.find_element_by_id('gameFlow-graph').get_attribute('data-plays')
        except:
            game_dict['gameflow'] = 'Null'
        writer.writerow(game_dict.values())
        gameid += 1
driver.close()