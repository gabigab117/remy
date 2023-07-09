from django.test import TestCase, Client
from django.urls import reverse

from ideas.models import Idea, Category
from accounts.models import Thinker


class IdeaTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Informatique")

        self.thinker = Thinker.objects.create_user(username="gabgab",
                                                   phone="0344805112",
                                                   email="gabrieltrouve5@gmail.com",
                                                   country="France",
                                                   first_name="Gabriel",
                                                   last_name="Trouvé",
                                                   password="testtesttest",
                                                   is_active=True)
        self.thinker2 = Thinker.objects.create_user(username="jeanjean",
                                                    phone="0344805112",
                                                    email="gabrieltrouve5@outlook.com",
                                                    country="France",
                                                    first_name="Gabriel",
                                                    last_name="Trouvé",
                                                    password="testtesttest",
                                                    is_active=True)
        self.thinker3 = Thinker.objects.create_user(username="gabigab117",
                                                    phone="0344805112",
                                                    email="gab@gab.com",
                                                    country="France",
                                                    first_name="Gabriel",
                                                    last_name="Trouvé",
                                                    password="12345678",
                                                    is_active=True)

        self.idea = Idea.objects.create(name="good idea", summary="test suumm", level="1",
                                        category=self.category, thinker=self.thinker,
                                        details="Bla bla bla")
        self.idea2 = Idea.objects.create(name="good idea2", summary="test suumm2", level="1",
                                         category=self.category, thinker=self.thinker,
                                         details="Bla bla bla2", paid=True, buyer=self.thinker2)

    def test_slug_created(self):
        self.assertEqual(self.idea.slug, "good-idea")

    def test_product_absolute_url(self):
        self.assertEqual(self.idea.get_absolute_url(), reverse('ideas:idea-detail',
                                                               kwargs={"slug": self.idea.slug}))

    def test_if_user_not_login_access_idea(self):
        resp = self.client.get(reverse('ideas:idea-detail',
                                       kwargs={"slug": self.idea2.slug}))
        self.assertEqual(resp.status_code, 302)

    def test_if_idea_bought_and_user_not_buyer_or_thinker(self):
        self.thinker3.is_active = True
        self.thinker3.save()
        self.client.force_login(self.thinker3)

        resp = self.client.get(self.idea2.get_absolute_url())
        print(resp)
        print(self.thinker3.is_active)
        self.assertEqual(resp.status_code, 410)

