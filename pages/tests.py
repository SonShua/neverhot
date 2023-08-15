from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from weather.models import City
from django.utils import translation


class HomePageTests(TestCase):
    def setUp(self):
        # Mock data
        City.objects.create(
            city_name="Berlin",
            lat=52.5170365,
            lon=13.3888599,
            temp=20,
            hum=10,
        )
        City.objects.create(
            city_name="Stuttgart",
            lat=34.321,
            lon=21.3888599,
            temp=30,
            hum=40,
        )

    def test_url_exists_at_correct_location_homepageview(self):
        # Expecting a redirect to en localized homepage
        response = self.client.get("/")
        self.assertRedirects(response, "/en/")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_localization_change(self):
        response = self.client.get(
            "/", headers={"accept-language": "de"}
        )  # Change language via http header
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/de/")

    def test_correct_template_used(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_content_is_in_response(self):
        response = self.client.get("/en/")
        self.assertContains(response, "Home")  # Heading
        self.assertContains(response, "Weather")  # Heading
        self.assertContains(response, "Add city?")  # Heading
        cities = City.objects.all()
        self.assertQuerysetEqual(
            response.context["city_list"], cities, ordered=False
        )  # All cities are on homepage

    def test_htmx_search_render(self):
        headers = {"HTTP_HX-Request": "true"}  # "activate" htmx
        response = self.client.get(reverse("home"), **headers)  # go to homepage
        self.assertTemplateUsed(response, "partial_results.html")
        self.assertNotContains(response, "Berlin")  # Berlin object not displayed yet
        response = self.client.get("/en/?q=ber", **headers)  # search parameter passed
        self.assertContains(response, "Berlin")  # found Berlin object
        self.assertTemplateUsed(response, "partial_results.html")

    def test_content_is_translated(self):
        """Implement test that the content is correctly translated"""
        pass


class SearchPageTests(TestCase):
    def test_url_exists_at_correct_location_homepageview(self):
        # Expecting a redirect to en localized homepage
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        response = self.client.get(reverse("search"))
        self.assertTemplateUsed(response, "search.html")

    def test_search_is_working(self):
        headers = {"HTTP_HX-Request": "true"}  # always set this if testing HTMX
        response = self.client.post(
            reverse("search"), {"city_name": "Berlin"}, follow=True, **headers
        )
        # print(vars(response.context))
        self.assertContains(response, "already in database")

    def test_search_adding_cities_to_db_success(self):
        headers = {"HTTP_HX-Request": "true"}
        response = response = self.client.post(
            reverse("search"), {"city_name": "Frankfurt"}, follow=True, **headers
        )  # should create new city objects
        city = City.objects.get(pk=1)
        self.assertContains(
            response, "alert alert-success"
        )  # Alert that something has been added to db
        self.assertContains(
            response, f"{city.city_name}, {city.country}"
        )  # Added city_name, country should be in response
        cities = City.objects.all()
        self.assertQuerysetEqual(
            response.context["city_created_list"], cities
        )  # city all in the newly created list
        response = response = self.client.post(
            reverse("search"), {"city_name": "Frankfurt"}, follow=True, **headers
        )
        self.assertQuerysetEqual(
            response.context["city_get_list"], cities
        )  # after performing search again, it is in the get list
        self.assertContains(response, "already in database")

    def test_search_adding_cities_to_db_nothing_found(self):
        headers = {"HTTP_HX-Request": "true"}
        response = response = self.client.post(
            reverse("search"),
            {"city_name": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF123"},
            follow=True,
            **headers,
        )
        self.assertContains(response, "alert alert-info")
        self.assertContains(response, "Nothing found")

    def test_search_adding_cities_to_db_fail(self):
        headers = {"HTTP_HX-Request": "true"}
        with self.assertRaises(AttributeError):
            self.client.post(
                reverse("search"),
                {"city_name": "ber"},
                follow=True,
                **headers,  # Post not possible because form is not bound because of validation check, input len too short (AttributeError)
            )
