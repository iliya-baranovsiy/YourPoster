from datetime import datetime
from parsing.itNewsParse import it_news
from parsing.aiNewsParse import ai_news
from parsing.gamesNewsParse import games_news
from parsing.showBisNewsParse import showBis_news
from parsing.cryptoNewsParse import crypto_news
from parsing.sportNewsParse import sport_news
from parsing.scienseNewsParse import science_news
from parsing.worldNewsPars import world_news
from database.parseDB.parseOrm import clean_old_data
import time

schedule_dict_map = [
    {'time': '8', 'class': world_news, 'role': 'parse'},
    {'time': '10', 'class': sport_news, 'role': 'parse'},
    {'time': '12', 'class': showBis_news, 'role': 'parse'},
    {'time': '14', 'class': it_news, 'role': 'parse'},
    {'time': '16', 'class': world_news, 'role': 'parse'},
    {'time': '18', 'class': sport_news, 'role': 'parse'},
    {'time': '20', 'class': ai_news, 'role': 'parse'},
    {'time': '22', 'class': games_news, 'role': 'parse'},
    {'time': '0', 'class': science_news, 'role': 'parse'},
    {'time': '2', 'class': crypto_news, 'role': 'parse'},
    {'time': '3', 'class': clean_old_data, 'role': 'clear'},
    {'time': '4', 'class': it_news, 'role': 'parse'},
]


def parse_scheduler():
    while True:
        current_hour = str(datetime.now().hour)
        for task in schedule_dict_map:
            if task['time'] == current_hour and task['role'] == 'parse':
                task['class'].parse()
            elif task['time'] == current_hour and task['role'] == 'clear':
                task['class']()
        time.sleep(3600)


parse_scheduler()
