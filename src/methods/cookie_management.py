from flask import session


def get_current_basket_cookie():
    return session.get("waiter_current_basket", None)


def get_is_logged_in_cookie():
    is_logged = session.get("waiter_is_logged_in", None)

    if is_logged is None:
        return False
    if not is_logged:
        return False
    return True


def set_is_logged_in_cookie(is_logged_in):
    session["waiter_is_logged_in"] = True if is_logged_in else False


def get_current_user_id_cookie():
    return session.get("waiter_current_user_id", None)


def set_current_user_id_cookie(user_id):
    session["waiter_current_user_id"] = user_id


def get_is_cook_cookie():
    is_cook = session.get("waiter_is_cook", None)
    if is_cook is None:
        return False
    if not is_cook:
        return False
    return True


def set_is_cook_cookie(is_cook):
    session["waiter_is_cook"] = is_cook