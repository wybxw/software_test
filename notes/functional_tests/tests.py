from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
# import os
# import django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes.settings')
# django.setup()
MAX_WAIT = 10

from lists.models import Item,List
# class ListAndItemModelsTest(LiveServerTestCase):
#     def test_saving_and_retrieving_items(self):
#         # list_user = List()
#         # list_user.save()
#         # first_item = Item()
#         # first_item.text = 'The first list item'
#         # first_item.list = list_user
#         # first_item.save()

#         # second_item = Item()
#         # second_item.text = 'Item the second'
#         # second_item.list = list_user
#         # second_item.save()

#         # saved_list = List.objects.first()
#         # self.assertEqual(saved_list,list_user)
#         # saved_items = Item.objects.all()
#         # self.assertEqual(saved_items.count(),2)

#         # first_saved_item = saved_items[0]
#         # second_saved_item = saved_items[1]
#         # self.assertEqual(first_saved_item.text,'The first list item')
#         # self.assertEqual(first_saved_item.list,list_user)
#         # self.assertEqual(second_saved_item.text,'Item the second')
#         # self.assertEqual(second_saved_item.list,list_user)
        # pass
class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        real_server = os.environ.get('REAL_SERVER')
        if real_server:
            self.live_server_url = 'http://'+real_server
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
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    def test_can_start_a_list_and_retrieve_it_later(self):
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        # self.assertIn('To-Do', self.browser.title) , "Browser title was " + self.browser.title
        # header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        # self.assertIn('To-Do',header_text)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        # self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')
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

        # table = self.browser.find_element(By.ID,'id_list_table')
        # rows=table.find_elements(By.TAG_NAME,'tr')
        # self.assertIn('1:Buy flowers',[row.text for row in rows])
        # self.assertIn('2:Give a gift to Lisi', [row.text for row in rows])
        
        # self.check_for_row_in_list_table('1:Buy flowers')
        # self.check_for_row_in_list_table('2:Give a gift to Lisi')

        # self.fail('Finish the test!')
    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy flowers')

        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url,'/lists/.+')
        # self.wait_for_row_in_list_table('1:Buy a gift for Lisi')
        self.browser.quit()
        self.browser = webdriver.Chrome()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertNotIn('Give a gift to Lisi',page_text)

        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')

        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url,'/lists/.+')
        self.assertNotEqual(wangwu_list_url,zhangsan_list_url)

        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertIn('Buy milk',page_text)
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] /2,
            512,
            delta=10
        )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:testing')
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] /2,
            512,
            delta=10
        )
# if __name__ == '__main__':
    # unittest.main(warnings='ignore')