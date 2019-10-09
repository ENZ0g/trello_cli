import requests as re
import sys


# <<--- Enter APIkey and token --->>
AUTHOR_PARAMS = {
    'key': '',
    'token': ''
}

# <<--- Enter short boardId --->>
BOARD_ID = ''

BASE_URL = 'https://api.trello.com/1/'


def get_long_board_id():
    boards = re.get(BASE_URL +
                    'members/me/boards',
                    params=AUTHOR_PARAMS).json()

    for board in boards:
        if board['shortLink'] == BOARD_ID:
            return board['id']


def get_columns():
    return re.get(BASE_URL +
                  'boards/' +
                  BOARD_ID +
                  '/lists',
                  params=AUTHOR_PARAMS).json()


def get_cards_of_column(column_id):
    return re.get(BASE_URL +
                  'lists/' +
                  column_id +
                  '/cards',
                  params=AUTHOR_PARAMS).json()


def get_all_cards():
    columns = get_columns()

    for column in columns:
        cards = get_cards_of_column(column['id'])
        print(f"\n {len(cards)} --- {column['name']}")
        if cards:
            for card in cards:
                print(f"\t>> {card['name']}")
        else:
            print('\t>> Нет задач\n')


def create_card(column_name, task):
    columns = get_columns()

    columns_list = []
    for column in columns:
        columns_list.append(column['name'])
        if column_name == column['name']:
            query = re.post(BASE_URL +
                            'cards/',
                            data={
                                'name': task,
                                'idList': column['id'],
                                **AUTHOR_PARAMS
                            }
                            )
            if query.status_code == 200:
                print('Задача добавлена!')
                get_all_cards()
                return
            else:
                print(f'Возникла ошибка {query.status_code}. Карточка не создана!')
                return
    print('Колонки с таким именем нет! Доступные имена:')
    print(*columns_list, sep=' -- ')


def move_card(task, to_column):
    columns = get_columns()

    task_id = None
    columns_dict = {}
    cards_list = []
    count = 0

    for column in columns:
        columns_dict.update({column['name']: column['id']})

        cards = get_cards_of_column(column['id'])

        for card in cards:
            if card['name'] == task:
                count += 1
                cards_list.append([card['id'], card['dateLastActivity'], column['name']])

    if to_column not in columns_dict.keys():
        print('Колонки с таким именем нет! Доступные имена:')
        print(*columns_dict.keys(), sep=' --- ')
        return

    if count == 1:
        task_id = cards_list[0][0]
        if cards_list[0][2] == to_column:
            print('Карточка уже в этой колонке!')
            get_all_cards()
            return
    elif count > 1:
        print('С таким именем есть несколько карт:')
        n = 1
        for each in cards_list:
            print(n, '-\t', task, '- колонка >', each[2], '\t- дата последнего изменения >', each[1])
            n += 1
        card_number = int(input('Введите номер карты для перемещения ->>'))
        task_id = cards_list[card_number-1][0]
        if cards_list[card_number-1][2] == to_column:
            print('Карточка уже в этой колонке!')
            get_all_cards()
            return

    if task_id:
        if to_column in columns_dict.keys():
            query = re.put(BASE_URL +
                           'cards/' +
                           task_id +
                           '/idList',
                           data={
                               'value': columns_dict[to_column],
                               **AUTHOR_PARAMS
                           }
                           )
            if query.status_code == 200:
                print('Карточка с задачей перенесена.')
                get_all_cards()
            else:
                print(f'Возникла ошибка {query.status_code}. Карточка не перенесена!')
    else:
        print('Нет такой задачи! Все задачи:')
        get_all_cards()


def create_column(column_name):
    query = re.post(BASE_URL +
                    'lists/',
                    data={
                        'name': column_name,
                        'idBoard': get_long_board_id(),
                        'pos': 'bottom',
                        **AUTHOR_PARAMS
                    }
                    )
    if query.status_code == 200:
        print('Колонка создана успешно!')
        get_all_cards()
    else:
        print(f'Возникла ошибка {query.status_code}. Колонка не создана!')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('ENTER "python trello_cli.py help" for help')
        get_all_cards()
    else:
        if sys.argv[1].lower() == 'create':
            create_card(sys.argv[2], sys.argv[3])
        elif sys.argv[1].lower() == 'move':
            move_card(sys.argv[2], sys.argv[3])
        elif sys.argv[1].lower() == 'createlist':
            create_column(sys.argv[2])
        elif sys.argv[1].lower() == 'help':
            print(
                "\n\tNo arguments to see all cards\n\n",
                "\tCREATE column_name card_name\t--> to create the new task\n",
                "\tMOVE card_name column_name\t--> to move task to the selected column\n",
                "\tCREATELIST list_name\t\t--> to create the new list\n",
                "\n\tUse quotes for names that consist of multiple words\n"
            )

