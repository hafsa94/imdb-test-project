# __author__ = 'hafsa'

from selenium.webdriver.common.by import By

from .page_base import AbstractBasePage


class IMDBPage(AbstractBasePage):

    _MOVIES_NAME_LOCATOR = (By.CSS_SELECTOR, '[class="titleColumn"] a')
    _MOVIES_RELEASE_YEAR_LOCATOR = (By.CSS_SELECTOR, '[class="secondaryInfo"]')
    _MOVIES_RATING_LOCATOR = (By.CSS_SELECTOR, '.imdbRating strong')

    def get_details_of_movies(self):
        name = self.get_text_of_elements(self._MOVIES_NAME_LOCATOR)
        year = self.get_text_of_elements(self._MOVIES_RELEASE_YEAR_LOCATOR)
        year = [yr.replace('(', '').replace(')', '')for yr in year]
        rating = self.get_text_of_elements(self._MOVIES_RATING_LOCATOR)
        return list(zip(name, year, rating))

    def store_result_in_database(self, db_name, table_name, table_header):
        movie_details = self.get_details_of_movies()
        return self.insert_values(db_name, table_name, table_header, movie_details)


