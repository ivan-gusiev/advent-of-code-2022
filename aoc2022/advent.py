import os

day = 0

def set_day_from_filename(filename: str):
    global day
    """
    Sets the current day

    :param str filename: always put __file__ there
    """
    modulename = os.path.basename(filename).replace(".py", "")
    day = int(modulename.replace("day", ""))

def day_from_filename(filename: str):
    """
    Gets the day number from filename

    :param str filename: always put __file__ there
    """
    modulename = os.path.basename(filename).replace(".txt", "")
    result = int(modulename.replace("day", ""))
    return result

def current_day() -> int:
    global day
    return day