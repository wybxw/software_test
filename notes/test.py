# from selenium import webdriver
# import unittest
# class NewVisitorTest(unittest.TestCase):
#     def setUp(self):
#         self.browser = webdriver.Chrome()
#     def tearDown(self):
#         self.browser.quit()
#     def test_can_start_a_list_and_retrieve_it_later(self):
#         self.browser.get('http://localhost:8000')
#         self.assertIn('install', self.browser.title) , "Browser title was " + self.browser.title
#         self.fail('Finish the test!')
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
from django.test import TestCase
class smoketest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1+1, 3)

