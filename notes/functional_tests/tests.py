from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
# import os
# import django
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes.settings')
# django.setup()
MAX_WAIT = 10

from lists.models import Item
class ItemModelTest(LiveServerTestCase):
    def test_saving_and_retrieving_items(self):
        # first_item = Item()
        # first_item.text = 'The first list item'
        # first_item.save()

        # second_item = Item()
        # second_item.text = 'Item the second'
        # second_item.save()
        
        # saved_items = Item.objects.all()
        # self.assertEqual(saved_items.count(),2)

        # first_saved_item = saved_items[0]
        # second_saved_item = saved_items[1]
        # self.assertEqual(first_saved_item.text,'The first list item')
        # self.assertEqual(second_saved_item.text,'Item the second')
        pass
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    def tearDown(self):
        self.browser.quit()
    def wait_for_row_in_list_table(self,row_text):
        #v1
        # table = self.browser.find_element(By.ID,'id_list_table')
        # rows=table.find_elements(By.TAG_NAME,'tr')
        # self.assertIn(row_text,[row.text for row in rows])
        #v2
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID,'id_list_table')
                rows=table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                break
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    def test_can_start_a_list_and_retrieve_it_later(self):
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title) , "Browser title was " + self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_text)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy flowers')
        # time.sleep(1)

        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        
        self.wait_for_row_in_list_table('1:Buy flowers')
        self.wait_for_row_in_list_table('2:Give a gift to Lisi')

        table = self.browser.find_element(By.ID,'id_list_table')
        rows=table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1:Buy flowers',[row.text for row in rows])
        self.assertIn('2:Give a gift to Lisi', [row.text for row in rows])
        
        # self.check_for_row_in_list_table('1:Buy flowers')
        # self.check_for_row_in_list_table('2:Give a gift to Lisi')

        self.fail('Finish the test!')
# if __name__ == '__main__':
    # unittest.main(warnings='ignore')