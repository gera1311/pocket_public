import requests
import time
from datetime import datetime as dt
from sqlalchemy.orm import sessionmaker
from typing import List, Dict

from logger import logger
from models import MyTable, engine
# from bot import bot


url_getusermining = 'https://gm.pocketfi.org/mining/getUserMining'
url_claimmining = 'https://gm.pocketfi.org/mining/claimMining'
url_activatedailyboost = 'https://rubot.pocketfi.org/boost/activateDailyBoost'
url_taskexecuting = 'https://gm.pocketfi.org/mining/taskExecuting'


def get_all_users() -> List[Dict[id, str]]:
    '''Загрузка базы данных'''
    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query(MyTable).all()
    session.close()
    logger.debug(f'Получили пользователей: {users}')
    return users


def check_balance_switch(url, headers, proxies=None) -> float:
    '''Проверка баланса'''
    response = requests.get(url=url, headers=headers)
    data = response.json()
    balance = data['userMining']['gotAmount']
    logger.info(f'Баланс: {balance}')
    return balance


def check_data_response(url, headers, proxies=None) -> dict:
    '''Проверка корректности типа и структуры полученных данных'''
    response = requests.get(url=url, headers=headers, proxies=proxies)
    response = response.json()
    if isinstance(response, dict):
        logger.debug(f'Проверка структуры ответа: {type(response)}')
        try:
            response = response['userMining']
            logger.debug(f'Response JSON: {response}')
        except Exception as error:
            logger.error('Отсутствует ключ - userMining')
            print(f'Key error {error}')
        return response
    logger.error(f'Некорректный тип данных: {type(response)}')
    return False


def check_token_for_claim(response) -> float:
    '''Проверка количества токенов доступных для клейма'''
    response = response['miningAmount']
    logger.info(f'Для клейма доступно: {response} $SWITCH')
    return response


def open_daily_boost(url, headers, proxies=None):
    '''Включает ежедневный буст'''
    try:
        response = requests.post(url=url, headers=headers)
        response.json()
        logger.debug('Ежедневный буст активирован!')
    except Exception as error:
        print(f'{error}')
    return response


def time_to_deadline(response) -> tuple:
    '''Считает время дедлайна клейма'''
    unix_time = response['dttmClaimDeadline']
    unix_time = unix_time/1000
    deadline = dt.fromtimestamp(unix_time)
    remaining = deadline - dt.now()

    hours_remaining, remainder = divmod(remaining.seconds, 3600)
    minutes_remaining, seconds_remaining = divmod(remainder, 60)

    logger.debug(
        f'$SWITCH сгорят через: {hours_remaining} часа '
        f'{minutes_remaining} минут {seconds_remaining} секунд'
    )

    return hours_remaining, minutes_remaining, seconds_remaining


def claim_tokens(url, headers, proxies=None) -> bool:
    '''Клеймер'''
    response = requests.post(url, headers=headers)
    response = response.json()
    logger.info('Клейм выполнен!')
    return response


def proxy_on(proxies):
    '''Включает прокси'''
    return


def send_message(bot, message):
    '''Отправляет сообщения в телеграм'''
    chat_id = 277132375
    bot.send_message(chat_id, message)
    logger.debug('Бот отправил сообщение')


def process_user(user_id, token, proxy_data):
    '''Основная логика программы для одного пользователя'''
    logger.info(f'Пользователь с ID {user_id} начал работу')
    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'origin': 'https://pocketfi.app',
        'priority': 'u=1, i',
        'referer': 'https://pocketfi.app/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'telegramrawdata': f'{token}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    proxies = {
        'http': f'http://{proxy_data}',
        'https': f'https://{proxy_data}'
    }
    logger.info(f'Прокси подключены {proxies}')
    check_balance_switch(url_getusermining, headers=headers, proxies=proxies)
    response = check_data_response(
        url_getusermining, headers=headers, proxies=proxies)
    check_token_for_claim(response)
    time_to_deadline(response)
    open_daily_boost(url_activatedailyboost, headers=headers, proxies=proxies)
    claim_tokens(url_claimmining, headers=headers, proxies=proxies)
    check_balance_switch(url_getusermining, headers=headers, proxies=proxies)


def main():
    '''Основная логика программы для всех пользователей'''
    users = get_all_users()
    count = 1
    while True:
        for user in users:
            process_user(user.id, user.auth_data, user.proxy_ip)
            time.sleep(90)
        # message = f'Закончил {count} итерацию!'
        # send_message(bot, message)
        count += 1


if __name__ == '__main__':
    main()
