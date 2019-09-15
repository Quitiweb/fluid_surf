from django.test import TestCase

class TestBlog:
    def test_one(self):
        x = "my blog test"
        assert 'blog' in x
