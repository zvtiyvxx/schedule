from config import USER_GROUPS_FILE

def load_user_group(user_id):
    try:
        with open(USER_GROUPS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                stored_user_id, group, _ = line.strip().split(':', 2)
                if int(stored_user_id) == user_id:
                    return group
    except FileNotFoundError:
        pass

    return None


def save_user_group(user_id, group):
    user_groups = {}
    try:
        with open(USER_GROUPS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                stored_user_id, stored_group, stored_notifications = line.strip().split(':', 2)
                user_groups[int(stored_user_id)] = (stored_group, stored_notifications)
    except FileNotFoundError:
        pass

    notifications = user_groups.get(user_id, (None, "off"))[1]
    user_groups[user_id] = (group, notifications)

    with open(USER_GROUPS_FILE, 'w', encoding='utf-8') as f:
        for stored_user_id, (stored_group, stored_notifications) in user_groups.items():
            f.write(f"{stored_user_id}:{stored_group}:{stored_notifications}\n")


def load_notifications_state(user_id):
    try:
        with open(USER_GROUPS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                stored_user_id, _, notifications = line.strip().split(':')
                if int(stored_user_id) == user_id:
                    return notifications
    except FileNotFoundError:
        pass

    return "off"


def save_notifications_state(user_id, state):
    user_groups = {}
    try:
        with open(USER_GROUPS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                stored_user_id, stored_group, stored_notifications = line.strip().split(':')
                user_groups[int(stored_user_id)] = (stored_group, stored_notifications)
    except FileNotFoundError:
        pass

    group = user_groups.get(user_id, (None, "off"))[0]
    user_groups[user_id] = (group, state)

    with open(USER_GROUPS_FILE, 'w', encoding='utf-8') as f:
        for stored_user_id, (stored_group, stored_notifications) in user_groups.items():
            f.write(f"{stored_user_id}:{stored_group}:{stored_notifications}\n")

def load_user_groups():
    user_groups = {}
    try:
        with open(USER_GROUPS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                stored_user_id, stored_group, stored_notifications = line.strip().split(':')
                user_groups[int(stored_user_id)] = stored_group
    except FileNotFoundError:
        pass
    return user_groups
