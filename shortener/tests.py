from django.test import TestCase
from shortener.models import Link
from appchance.settings import SHORTENED_LINK_LENGTH
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LinkModelTests(TestCase):
    def setUp(self) -> None:
        self.link = Link()
        self.link.link = 'https://www.google.com/'
        self.link.user_ip = '222.222.22.22'
        self.link.user_agent = 'asd'

    def test_create_link_object_with_corect_data(self):
        self.link.full_clean()
        self.link.save()
        self.assertEqual(
            SHORTENED_LINK_LENGTH,
            len(self.link.shortened_link)
        )

    def test_cannot_create_several_objects_for_the_same_link(self):
        Link.objects.create(link='https://www.google.com/', user_ip='222.222.22.22')
        self.assertRaises(IntegrityError, Link.objects.create, link='https://www.google.com/', user_ip='111.111.22.22')

    def test_cannot_create_link_object_with_bad_user_ip(self):
        self.link.user_ip = '222.2222222'
        self.assertRaises(ValidationError, self.link.full_clean)

    def test_cannot_create_link_object_with_bad_url_address(self):
        self.link.link = 'google.com/'
        self.assertRaises(ValidationError, self.link.full_clean)


class ShortenerRedirectViewTests(TestCase):
    def test_redirect_to_the_page_by_the_shortened_link(self):
        url = 'https://google.com'
        link = Link.objects.create(link=url, user_ip='222.222.22.22')
        response = self.client.get(reverse('shortener:redirect', args=(link.shortened_link,)))
        self.assertEqual(response.status_code, status.HTTP_308_PERMANENT_REDIRECT)
        self.assertEqual(response.url, url)

    def test_try_redirect_to_the_page_by_not_existing_shortened_link(self):
        response = self.client.get(reverse('shortener:redirect', args=('aaa',)))
        self.assertEqual(response.status_code, 404)


class ShortenerAddViewTests(APITestCase):
    def test_add_new_shortened_link(self):
        link = 'https://google.com/'
        response = self.client.post('/', {'link': link}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(Link.objects.get().link, link)

    def test_try_add_a_shortened_link_for_an_existing_link(self):
        link = 'https://google.com/'
        Link.objects.create(link=link).save()
        response = self.client.post('/', {'link': link}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(response.data['link'], link)

    def test_cannot_add_new_shortened_link_with_bad_url_format(self):
        link = 'google.com/'
        response = self.client.post('/', {'link': link}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Link.objects.count(), 0)


class ShortenerShowViewTests(APITestCase):
    def setUp(self) -> None:
        Link.objects.create(link='https://google.com/', user_ip='172.18.0.1', user_agent='HTTPie/3.1.0').save()
        Link.objects.create(link='https://github.com/', user_ip='172.18.0.1', user_agent='HTTPie/3.1.0').save()

    def test_show_all_shortened_link_info(self):
        response = self.client.get('/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('https://google.com/', response.data[0]['link'])
        self.assertEqual('172.18.0.1', response.data[0]['user_ip'])
        self.assertEqual('HTTPie/3.1.0', response.data[0]['user_agent'])
        self.assertEqual('https://github.com/', response.data[1]['link'])

    def test_show_one_shortened_link_info(self):
        link = Link.objects.all()[0]
        response = self.client.get('/' + link.shortened_link + '/info', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(link.link, response.data['link'])
        self.assertEqual('172.18.0.1', response.data['user_ip'])
        self.assertEqual('HTTPie/3.1.0', response.data['user_agent'])

    def test_try_show_not_existing_shortened_link_info(self):
        response = self.client.get('/aaaa/info', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
