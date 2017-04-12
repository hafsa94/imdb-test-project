from random import randint
import time
import sqlite3
from prettytable import PrettyTable

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AbstractBasePage(object):

    PATH = '/'

    _timeout = 30
    MAIN_URL = 'http://www.imdb.com/chart/top'

    def __init__(self, *args):
        """ Initializer method for Page base """
        self._base_url = self.MAIN_URL
        # Waring!
        #   Variable 'selenium' is not an object of Selenium class
        #   It is a Selenium Webdriver Object!

        self.selenium = args[0]

    def click_on_element(
            self,
            locator,
            index=None):
        """ Clicks one of elements of specified index
            :param locator: CSS Selector/ XPATH of element
            :param index: Index of element to be clicked
            :return: True/False
        """
        click_result = False
        try:
            WebDriverWait(self.selenium, self._timeout).until(
                EC.presence_of_element_located(locator))
            WebDriverWait(self.selenium, self._timeout).until(
                EC.element_to_be_clickable(locator))

            button_link = self.selenium.find_elements(*locator)

            if index is None:
                if len(button_link) > 1:
                    index = randint(0, len(button_link) - 1)
                else:
                    index = 0

            time.sleep(3)
            button_link[index].click()
            click_result = True

        finally:
            # return True
            return click_result

    def enter_field_input(
            self,
            input_locator,
            values="No Input"):
        """ Sends text to an input element
            :param input_locator: CSS Selector/ XPATH of element
            :param values: Values to be passed in an element
            :return: True/False
        """
        fill_result = False
        try:
            WebDriverWait(self.selenium, self._timeout).until(
                EC.presence_of_element_located(input_locator))
            WebDriverWait(self.selenium, self._timeout).until(
                EC.visibility_of_element_located(input_locator))

            name_field = self.selenium.find_element(*input_locator)
            time.sleep(3)

            name_field.send_keys(Keys.CONTROL + 'a')
            name_field.send_keys(Keys.BACKSPACE)
            name_field.send_keys(str(values))

            fill_result = True

        finally:
            return fill_result

    def get_text_of_elements(self, locator):
        """ Returns list of text of element/s
            :param locator: CSS Selector/ XPATH of element
            :return: List of elements text
        """
        WebDriverWait(self.selenium, self._timeout).until(
            EC.presence_of_element_located(locator))
        WebDriverWait(self.selenium, self._timeout).until(
            EC.visibility_of_element_located(locator))
        time.sleep(0.5)
        element = self.selenium.find_elements(*locator)
        if element is not None:
            element_texts = [elem.text for elem in element]
            return element_texts

    def check_for_new_url(
            self,
            expected_url_string):
        """ Check if the current page url is expected url
            :param expected_url_string: Expected url string
            :return: True/False
        """
        check_result = False
        time.sleep(3)
        current_page_url = str(self.selenium.current_url)
        if expected_url_string in current_page_url:
            check_result = True
        return check_result

    def go_to_page(self):
        url = self._base_url + self.PATH
        self.selenium.get(url)

    def refresh(self):
        self.selenium.refresh()

    def maximize(self):
        self.selenium.maximize_window()

    def scroll_into_view(self, locator, index=0, scroll_val=100):
        """ Scroll to one of elements of specified index
            :param locator: CSS Selector/ XPATH of element
            :param index: Index of element to be clicked
            :param scroll_val: Vertical scroll value
        """
        WebDriverWait(self.selenium, self._timeout).until(
            EC.presence_of_element_located(locator))
        WebDriverWait(self.selenium, self._timeout).until(
            EC.visibility_of_element_located(locator))
        elems = self.selenium.find_elements(*locator)
        self.selenium.execute_script("return arguments[0].scrollIntoView();", elems[index])
        self.selenium.execute_script("window.scrollBy(0, -" + str(scroll_val) + ");")

    """
    Functions to create, insert, fetch SQLite Table
    """

    @staticmethod
    def insert_values(db_name, table_name, table_header, values):
        """ Insert values into the table
            :param db_name: Database name
            :param table_name: Table name
            :param table_header: Table columns name
            :param values: Table columns values
            :return: True/False
        """
        result = False
        try:
            connection_obj = sqlite3.connect(db_name)
            cursor_obj = connection_obj.cursor()
            cursor_obj.executemany("INSERT INTO %s %s VALUES (NULL,?,?,?)" %
                                   (table_name, tuple(['rowid']+table_header)), values)
            connection_obj.commit()
            connection_obj.close()
            result = True
        except Exception as e:
            print("Python says:", str(e))
            result = False
        finally:
            return result

    @staticmethod
    def fetch_value(db_name, table_name, table_header):
        """ Fetch a value from table
            :param db_name: Database name
            :param table_name: Table name
            :param table_header: Table columns name
            :return: True/False
        """
        result = False
        try:
            connection_obj = sqlite3.connect(db_name)
            cursor_obj = connection_obj.cursor()
            sql = "SELECT %s FROM %s;" % (','.join(['rowid']+table_header), table_name)
            cursor_obj.execute(sql)
            details = cursor_obj.fetchall()
            table = PrettyTable(['No.']+table_header)
            for elem in details:
                table.add_row(elem)
            print()
            print(table)
            result = True
        except Exception as e:
            print("Python says:", str(e))
            result = False
        finally:
            return result

    @staticmethod
    def create_table(db_name, table_name, table_header):
        """Create a table
            :param db_name: Database name
            :param table_name: Table name
            :param table_header: Table columns name
            :return: True/False"""
        result = False
        try:
            connection_obj = sqlite3.connect(db_name)
            cursor_obj = connection_obj.cursor()
            cursor_obj.execute("CREATE TABLE %s %s" % (table_name, tuple(table_header)))
            connection_obj.commit()
            connection_obj.close()
            print("-Created Table %s" % table_name)
            result = True
        except Exception as e:
            print("Python says:", str(e))
            result = False
        finally:
            return result
