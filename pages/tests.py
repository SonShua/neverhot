from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from weather.models import City


class HomePageTests(SimpleTestCase):
    def test_url_exists_at_correct_location_homepageview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Home")


class WeatherPageTests(TestCase):
    # need to create Berlin object, otherwise weather can't be displayed
    def setUp(self):
        City.objects.create(
            city_name="Berlin",
            lat=52.5170365,
            lon=13.3888599,
            temp=20,
            hum=10,
        )

    def test_url_exists_at_correct_location_weatherview(self):
        response = self.client.get("/weather/")
        self.assertEqual(response.status_code, 200)
        # The temp set before for Berlin object
        self.assertContains(response, "20")
        # The hum set before for Berlin object
        self.assertContains(response, "10")
