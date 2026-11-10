from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(CONTADOR_INTERVALO=0)
class ContadorTest(TestCase):
    def test_contador_sincrono(self):
        resposta = self.client.get(reverse("contador_sync"))

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["modo"], "sincrono")
        self.assertEqual(len(resposta.json()["contadores"]), 3)

    def test_contador_assincrono(self):
        resposta = self.client.get(reverse("contador_async"))

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["modo"], "assincrono")
        self.assertEqual(len(resposta.json()["contadores"]), 3)