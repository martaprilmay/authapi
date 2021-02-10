
def validate_password(password, check_digit=False, check_alpha=False, check_symbol=False):
    """ Checks if password has letters, digits and symbols.
        Returns True if validation passes successfully and
        False if validation fails.
    """

    if not isinstance(password, str):
        return False

    for char in password:
        if char.isdigit():
            check_digit = True
        if char.isalpha():
            check_alpha = True
        if not (char.isdigit() or char.isalpha()):
            check_symbol = True

    return check_digit and check_alpha and check_symbol
