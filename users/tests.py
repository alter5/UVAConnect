from django.test import TestCase

# Create your tests here.
class DummyTest(TestCase):
    def test1(self):
        a = 2
        self.assertEqual(a,2)