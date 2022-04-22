from selenium.webdriver.firefox.service import Service as f_service
from selenium.webdriver.chrome.service import Service as c_service
from selenium.webdriver.edge.service import Service as e_service


FIREFOX = 0
CHROME = 1
EDGE = 2


def check_exe_path(browser, executable_path):
    if executable_path is None:
        service = get_service(browser)
    else:
        service = get_service(browser, executable_path)

    return service


def check_binary_location(option, binary_location):
    if binary_location is None:
        return option
    else:
        option.binary_location = binary_location
        return option


def get_service(browser, executable_path=None):
    if executable_path is None:
        if browser == FIREFOX:
            return f_service()
        elif browser == CHROME:
            return c_service()
        elif browser == EDGE:
            return e_service()
    else:
        if browser == FIREFOX:
            return f_service(executable_path=executable_path)
        elif browser == CHROME:
            return c_service(executable_path=executable_path)
        elif browser == EDGE:
            return e_service(executable_path=executable_path)
