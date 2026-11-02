from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import BloodType, BloodRequest, Message, UserVisit


class LifeDropTests(TestCase):
    def setUp(self):
        self.o_pos = BloodType.objects.create(name="O+", slug="o-pos")
        self.requester = User.objects.create_user("req", password="pw12345pw")
        self.donor = User.objects.create_user("donor", password="pw12345pw")
        self.req = BloodRequest.objects.create(
            requester=self.requester, blood_type=self.o_pos, patient="Test patient",
            hospital="City Hospital", city="Windsor", units=2, urgency="urgent")

    def test_guest_can_browse_home(self):
        r = self.client.get(reverse("home"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Test patient")

    def test_search_filters_by_city(self):
        self.assertContains(self.client.get(reverse("home"), {"city": "Windsor"}), "Test patient")
        self.assertNotContains(self.client.get(reverse("home"), {"city": "Toronto"}), "Test patient")

    def test_missing_request_returns_404(self):
        self.assertEqual(self.client.get(reverse("request_detail", args=[9999])).status_code, 404)

    def test_guest_cannot_post(self):
        r = self.client.get(reverse("post_request"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login/", r.url)

    def test_member_can_post_request(self):
        self.client.login(username="req", password="pw12345pw")
        self.client.post(reverse("post_request"), {
            "patient": "New patient", "blood_type": self.o_pos.id, "hospital": "ER",
            "city": "Windsor", "units": 1, "urgency": "normal", "status": "open", "notes": ""})
        self.assertEqual(BloodRequest.objects.filter(patient="New patient").count(), 1)

    def test_offer_to_donate_creates_message(self):
        self.client.login(username="donor", password="pw12345pw")
        self.client.post(reverse("offer_to_donate", args=[self.req.id]))
        self.assertEqual(Message.objects.filter(receiver=self.requester).count(), 1)

    def test_empty_message_rejected(self):
        self.client.login(username="donor", password="pw12345pw")
        self.client.post(reverse("send_message", args=[self.req.id]), {"body": "   "})
        self.assertEqual(Message.objects.filter(body__contains="   ").count(), 0)

    def test_visit_is_tracked(self):
        self.client.login(username="donor", password="pw12345pw")
        self.client.get(reverse("home"))
        self.assertEqual(UserVisit.objects.filter(user=self.donor).count(), 1)
