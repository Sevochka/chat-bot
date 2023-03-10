import json
from random import randint

import weather
from datetime import datetime

with open('data/goods.json', encoding='utf-8') as file:
    data = json.load(file)
    GOODS = data["goods"]


def get_random_good():
    return GOODS[randint(0, len(GOODS) - 1)]


def get_time():
    now = datetime.now()
    return {"time": now.strftime("%H:%M:%S")}


def get_shared():
    return get_random_good()


# object with functions
data_by_intent = {
    'weather': weather.get_weather,
    'time': get_time
}


def intent_in_data(intent):
    return intent in data_by_intent


def add_additional_data_to_answer_by_intent(answer, intent):
    if intent_in_data(intent):
        data = data_by_intent[intent]()
        return answer.format(**data)
    else:
        data = get_shared()
        return answer.format(**data)
