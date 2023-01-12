def valid_password(password: str) -> list:
    if not password:
        return [False, "Password is required"]
    if len(password) < 8:
        return [False, "Password too short"]
    if len(password) > 16:
        return [False, "Password too long"]
    if password.isalpha():
        return [False, "Password must contain at least one number"]
    if password.isdigit():
        return [False, "Password must contain at least one letter"]
    return [True, "Password is valid"]