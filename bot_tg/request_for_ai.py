def get_message_for_ai(allies_list: list, enemy_list: list, update: bool = False):
    message = f"Подбери ТОЛЬКО НАЗВАНИЕ пяти наиболее подходящих героев для моей команды в Dota 2, " \
            f"если за меня играют {allies_list}, а против меня {enemy_list}"
    if update:
        message = "Не включай героев, которые уже указаны в составах или в предыдущих ответах."
    return message

def parse_enter_message(message: str) -> list:
    allies = ','.join(list(message.split('/')[0].split(','))).strip()
    enemy =','.join(list(message.split('/')[1].split(','))).strip()
    return [allies, enemy]
