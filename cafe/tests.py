import re

from django.core.management import call_command
from django.test import TestCase


class SiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_cafe", verbosity=0)

    URLS = ["/", "/about", "/blog", "/blog/best-chai-in-mumbai",
            "/blog/how-to-make-kadak-masala-chai", "/blog/best-snacks-with-chai"]

    def html(self, url):
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200, url)
        return r.content.decode()

    def test_one_h1_and_heading_order(self):
        for url in self.URLS:
            h = self.html(url)
            self.assertEqual(len(re.findall(r"<h1[ >]", h)), 1, url)
            levels = [int(x) for x in re.findall(r"<h([1-6])[ >]", h)]
            for prev, cur in zip(levels, levels[1:]):
                self.assertLessEqual(cur, prev + 1, f"{url}: h{prev} -> h{cur}")

    def test_unique_title_and_description(self):
        titles, descs = set(), set()
        for url in self.URLS:
            h = self.html(url)
            titles.add(re.search(r"<title>(.*?)</title>", h).group(1))
            descs.add(re.search(r'name="description" content="(.*?)"', h).group(1))
        self.assertEqual(len(titles), len(self.URLS))
        self.assertEqual(len(descs), len(self.URLS))

    def test_all_images_have_alt(self):
        for url in self.URLS:
            for tag in re.findall(r"<img[^>]*>", self.html(url)):
                self.assertRegex(tag, r'alt="[^"]+"', f"{url}: {tag}")

    def test_home_has_local_business_schema(self):
        h = self.html("/")
        self.assertIn("application/ld+json", h)
        self.assertIn("CafeOrCoffeeShop", h)

    def test_sitemap_and_robots(self):
        s = self.client.get("/sitemap.xml").content.decode()
        for path in ["/about", "/blog", "/blog/best-chai-in-mumbai"]:
            self.assertIn(path + "</loc>", s)
        r = self.client.get("/robots.txt")
        self.assertIn("Sitemap: http://testserver/sitemap.xml", r.content.decode())

    def test_404(self):
        r = self.client.get("/blog/does-not-exist")
        self.assertEqual(r.status_code, 404)
        self.assertIn("noindex", r.content.decode())
