import secrets


# Add headers
def add_headers(res):
    res.headers["Content-Type"] = "text/html; charset=utf-8"
    res.headers["X-Frame-Options"] = "SAMEORIGIN"
    res.headers["X-XSS-Protection"] = "1; mode=block"

# Select Random
def select_random(name_list, name_dict):
    for i in range(100):
        n = secrets.randbelow(len(name_dict))
        name_dict[name_list[n]] += 1

    return name_dict

# Get max value
def get_max_value(name_list, name_dict):
    max = 0
    max_name = ""
    count = 0

    for name in name_list:
        if max == 0:
            max = name_dict[name_list[0]]
            max_name = name_list[0]
        elif max == name_dict[name]:
            count += 1
        elif max < name_dict[name]:
            max = name_dict[name]
            max_name = name
            count = 0

    return max_name, count

# Set session
def set_session(res):
    res.session["token"] = secrets.token_hex()

# Check session
def check_session(res, token):
    if token == res.session.get("token"):
        return True
    else:
        return False