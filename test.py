import pytest
import re
from datetime import datetime, timedelta

from ru_api import get_meals_file

def test_correct_mel_document():
    url = 'https://ru.ufsc.br/ru/'
    status_code, link = get_meals_file(url)

    date_pattern = r'\d{2}\.\d{2}'
    dates = re.findall(date_pattern, link)

    data_inicio_cardapio = dates[0] + ".24"
    date_format = "%d.%m.%y"
    date_obj = datetime.strptime(data_inicio_cardapio, date_format)
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Início da semana atual (segunda-feira)
    end_of_week = start_of_week + timedelta(days=6)  # Fim da semana atual (domingo)

    correct_meal_file = False
    if start_of_week <= date_obj <= end_of_week:
        correct_meal_file = True

    assert correct_meal_file == True