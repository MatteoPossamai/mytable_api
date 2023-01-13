def valid_password(password: str) -> list:
    """
    Description: checks if a given password is valid
    """
    if not password:
        return [False, 'Password is required']
    elif len(password) < 8:
        return [False, 'Password too short']
    elif len(password) > 16:
        return [False, 'Password too long']
    elif password.isalpha():
        return [False, 'Password must contain at least one number']
    elif password.isdigit():
        return [False, 'Password must contain at least one letter']
    return [True, 'Password is valid']

def valid_username(username: str) -> list:
    """
    Check if a given username is valid
    """
    if not username:
        return [False, 'Username not provided']
    elif len(username) < 3:
        return [False, 'Username too short']
    elif len(username) > 20:
        return [False, 'Username too long']
    else:
        return [True, '']