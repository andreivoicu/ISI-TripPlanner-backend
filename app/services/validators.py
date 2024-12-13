import re

def validate_username(username):
    if not username or len(username) < 3 or len(username) > 20:
        return "Username must be between 3 and 20 characters."
    if not re.match(r'^\w+$', username):
        return "Username must contain only alphanumeric characters and underscores."
    return True

def validate_password(password):
    if not password or len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Za-z]', password):
        return "Password must include at least one letter."
    if not re.search(r'\d', password):
        return "Password must include at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must include at least one special character."
    return True

def validate_email(email):
    if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return "Invalid email format."
    return True

def validate_name(name, field_name):
    if not name or not re.match(r'^[A-Za-z\s\-]{1,50}$', name):
        return f"{field_name} must be 1-50 characters long and contain only letters, spaces, and hyphens (-)."
    return True

def validate_user_data(data):
    required_fields = ['first_name', 'last_name', 'username', 'password', 'email']
    missing_field = next((field for field in required_fields if field not in data), None)
    if missing_field:
        return f"Missing {missing_field}"

    validations = [
        (data['first_name'], lambda value: validate_name(value, 'First name')),
        (data['last_name'], lambda value: validate_name(value, 'Last name')),
        (data['username'], validate_username),
        (data['password'], validate_password),
        (data['email'], validate_email),
    ]

    for value, validator in validations:
        result = validator(value)
        if result is not True:
            return result

    return True
