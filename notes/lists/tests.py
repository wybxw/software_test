
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item,List

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={
            'item_text': 'A new list item'
        })

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={
            'item_text': 'A new list item'
        })
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')
class HomePageTest(TestCase):
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func,home_page)
    def test_uses_home_template(self):
        #v1
        # request =HttpRequest()
        # response = home_page(request)
        # html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>',html)
        # self.assertTrue(html.endswith('</html>'))
        #v2
        response=self.client.get('/')
        self.assertTemplateUsed(response,'home.html')
    # def test_can_save_a_POST_request(self):
    #     response = self.client.post('/',data={
    #         'item_text':'A new list item'})

    #     self.assertEqual(Item.objects.count(),1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text,'A new list item')

    #     # self.assertIn('A new list item',response.content.decode())
    #     # self.assertTemplateUsed(response,'home.html')
        
    #     # self.assertEqual(response.status_code,302)
    #     # self.assertEqual(response['location'],'/')
    #     # self.assertEqual(List.objects.count(),1)
    #     # new_list = List.objects.first()
    #     # self.assertEqual(new_list.item_text,'A new list item')
    
    # def test_redirects_after_POST(self):
    #     response = self.client.post('/',data={
    #         'item_text':'A new list item'})
    #     self.assertEqual(response.status_code,302)
    #     self.assertEqual(response['location'],'/lists/the-new-page/')

    # def test_only_saves_items_when_necessary(self):
    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(),0)

    # def test_displays_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')

    #     response = self.client.get('/')

    #     self.assertIn('itemey 1',response.content.decode())
    #     self.assertIn('itemey 2',response.content.decode())
class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-new-page/')
        self.assertTemplateUsed(response,'list.html')
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1',list=other_list)
        Item.objects.create(text='other list item 2',list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response,'itemey 1')
        self.assertContains(response,'itemey 2')
        self.assertNotContains(response,'other list item 1')
        self.assertNotContains(response,'other list item 2')
    def test_use_list_template(self):
        response = self.client.get('/lists/the-new-page/')
        self.assertTemplateUsed(response,'list.html')