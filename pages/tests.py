from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from weather.models import City
from django.utils import translation


class HomePageTests(TestCase):
    def test_url_exists_at_correct_location_homepageview(self):
        # Expecting a redirect to en localized homepage
        response = self.client.get("/")
        self.assertRedirects(response, "/en/")

    def test_localization_change(self):
        # HTML accept header
        response = self.client.get("/", headers={"accept-language": "de"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/de/")

    def test_correct_template_used(self):
        response = self.client.get("/en/")
        self.assertTemplateUsed(response, "home.html")

    def test_content_is_in_response(self):
        response = self.client.get("/en/")
        self.assertContains(response, "Home")
        self.assertContains(response, "Weather")
        self.assertContains(response, "Add city?")
        print(response)

    def test_htmx_search_render(self):
        City.objects.create(
            city_name="Berlin",
            lat=52.5170365,
            lon=13.3888599,
            temp=20,
            hum=10,
        )
        # Trigger HTMX
        headers = {"HTTP_HX-Request": "true"}

        # City object should not be on page
        response = self.client.get("/en/", **headers)
        self.assertNotContains(response, "Berlin")
        self.assertTemplateUsed(response, "partial_results.html")

        # Search is performed, City should now show
        response = self.client.get("/en/?q=ber", **headers)
        self.assertContains(response, "Berlin")
        self.assertTemplateUsed(response, "partial_results.html")

    def test_content_is_translated(self):
        """Implement test that the content is correctly translated"""
        pass


class CityTests(TestCase):
    # need to create Berlin object, otherwise weather can't be displayed
    def setUp(self):
        City.objects.create(
            city_name="Berlin",
            lat=52.5170365,
            lon=13.3888599,
            temp=20,
            hum=10,
        )

    def test_search_bar(self):
        pass

    def test_url_exists_at_correct_location_weatherview(self):
        # response = self.client.get("/en/?q=berlin")
        # response = self.client.get("weather/")
        # self.assertEqual(response.status_code, 404)
        # The temp set before for Berlin object
        # self.assertContains(response, "20")
        # The hum set before for Berlin object
        # self.assertContains(response, "10")
        pass
