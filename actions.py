DEBUG = False

unallowed_messages = []


def check_to_bad(file_id):
    fayl = open('bad_message.txt')
    content = fayl.readlines()
    fayl.close()
    new_list = []
    for line in content:
        new_list.append(line)
    if file_id + '\n' in new_list:
        return True
    return False


def cleaner():
    fayl = open('bad_message.txt')
    content = fayl.readlines()
    fayl.close()
    new_list = []
    for line in content:
        if line not in new_list:
            new_list.append(line)
    fayl = open('bad_message.txt', 'w')
    for item in new_list:
        fayl.write(item)
    fayl.close()


def add_to_unallowed(file_id):
    unallowed_messages.append(file_id)
    fayl = open('bad_message.txt', 'a+')
    for item in unallowed_messages:
        if item + '\n' not in fayl.readlines():
            fayl.write(item + '\n')
    fayl.close()
    cleaner()
