import nose.tools
import nose.plugins.multiprocess
import os

from test_base import BaseTest
from page_class.imdb_page import IMDBPage


class TestIMDBPage(BaseTest):

    db_name = "imdb.db"
    table_name = "imdb_table"
    table_header = ['Name', 'ReleaseYear', 'Rating']

    @classmethod
    def setUpClass(self):
        super(TestIMDBPage, self).setUpClass()
        self.imdb_page = IMDBPage(self._browser)
        self.imdb_page.go_to_page()
        self.imdb_page.maximize()

    def test_01_check_table_is_created(self):
        nose.tools.assert_true(self.imdb_page.create_table(
            self.db_name,
            self.table_name,
            self.table_header
        ))

    def test_02_check_data_is_inserted_in_the_table(self):
        nose.tools.assert_true(self.imdb_page.store_result_in_database(
            self.db_name,
            self.table_name,
            self.table_header
        ))

    def test_03_check_table_data_is_displayed(self):
        nose.tools.assert_true(self.imdb_page.fetch_value(
            self.db_name,
            self.table_name,
            self.table_header
        ))

    @classmethod
    def tearDownClass(self):
        super(TestIMDBPage, self).tearDownClass()
        os.remove(os.path.join(os.getcwd(), self.db_name))
