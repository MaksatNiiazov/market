from django.test import SimpleTestCase, override_settings
from unittest.mock import Mock, patch, mock_open, ANY
from rest_framework.test import APIRequestFactory

from tanda_backend.payment.views import CreatePaymentView

from tanda_backend.payment.services import (
    create_finik_qr_payment,
    create_finik_card_payment,
)


TEST_SETTINGS = {
    "FINIK_PAYMENT_URL": "https://finik.test/payment",
    "FINIK_TEST_PAYMENT_URL": "https://beta.test/payment",
    "FINIK_ACCOUNT_ID": "acc",
    "FINIK_MCC_CODE": "1234",
    "FINIK_CARD_REDIRECT_BASE": "https://redirect/",
    "FINIK_API_KEY": "api-key",
    "FINIK_PRIVATE_KEY_PATH": "dummy.pem",
}


class CreateFinikQRPaymentTests(SimpleTestCase):
    @override_settings(**TEST_SETTINGS)
    @patch("tanda_backend.payment.services.open", new_callable=mock_open, read_data=b"KEY")
    @patch("tanda_backend.payment.services.Signer")
    @patch("tanda_backend.payment.services.requests.post")
    def test_returns_item_id_from_response(self, mock_post, mock_signer_cls, mock_file):
        mock_signer = mock_signer_cls.return_value
        mock_signer.sign.return_value = "sig"

        response_mock = Mock()
        response_mock.headers = {"Content-Type": "application/json"}
        response_mock.json.return_value = {"id": "finik123", "redirectUrl": "http://pay"}
        response_mock.text = "{}"
        response_mock.raise_for_status.return_value = None
        mock_post.return_value = response_mock

        result = create_finik_qr_payment("order1", 100, "Test")

        self.assertEqual(result["item_id"], "finik123")
        self.assertEqual(result["qr_url"], "http://pay")


class CreateFinikCardPaymentTests(SimpleTestCase):
    @override_settings(**TEST_SETTINGS)
    @patch("tanda_backend.payment.services.open", new_callable=mock_open, read_data=b"KEY")
    @patch("tanda_backend.payment.services.Signer")
    @patch("tanda_backend.payment.services.requests.post")
    def test_returns_item_id_from_response(self, mock_post, mock_signer_cls, mock_file):
        mock_signer = mock_signer_cls.return_value
        mock_signer.sign.return_value = "sig"

        response_mock = Mock()
        response_mock.headers = {"Content-Type": "application/json"}
        response_mock.json.return_value = {"id": "card123", "redirectUrl": "http://card"}
        response_mock.text = "{}"
        response_mock.raise_for_status.return_value = None
        mock_post.return_value = response_mock

        result = create_finik_card_payment("order2", 200, "Card")

        self.assertEqual(result["item_id"], "card123")
        self.assertEqual(result["qr_url"], "http://card")


class CreatePaymentViewTests(SimpleTestCase):
    @override_settings(**TEST_SETTINGS)
    @patch("tanda_backend.payment.views.create_finik_qr_payment")
    @patch("tanda_backend.payment.views.Payment")
    def test_payment_saved_with_finik_id(self, mock_payment_cls, mock_create):
        mock_create.return_value = {"item_id": "finik456", "qr_url": "http://pay", "qr_image": ""}

        payment_instance = Mock()
        mock_payment_cls.objects.filter.return_value.exists.return_value = False
        mock_payment_cls.objects.create.return_value = payment_instance

        factory = APIRequestFactory()
        view = CreatePaymentView.as_view()
        request = factory.post("/", {"order_id": "1", "amount": "10"})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(payment_instance.finik_item_id, "finik456")
        self.assertEqual(response.data["finik_item_id"], "finik456")

    @override_settings(**TEST_SETTINGS)
    @patch("tanda_backend.payment.views.create_finik_card_payment")
    @patch("tanda_backend.payment.views.Payment")
    def test_card_payment_saved_with_finik_id(self, mock_payment_cls, mock_create):
        mock_create.return_value = {"item_id": "card789", "qr_url": "http://card", "qr_image": ""}

        payment_instance = Mock()
        mock_payment_cls.objects.filter.return_value.exists.return_value = False
        mock_payment_cls.objects.create.return_value = payment_instance

        factory = APIRequestFactory()
        view = CreatePaymentView.as_view()
        request = factory.post("/", {"order_id": "2", "amount": "20", "method": "card"})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(payment_instance.finik_item_id, "card789")
        self.assertEqual(response.data["finik_item_id"], "card789")


class FinikModeSelectionTests(SimpleTestCase):
    @override_settings(**TEST_SETTINGS, FINIK_TEST=False)
    @patch("tanda_backend.payment.services.open", new_callable=mock_open, read_data=b"KEY")
    @patch("tanda_backend.payment.services.Signer")
    @patch("tanda_backend.payment.services.requests.post")
    def test_production_url_used(self, mock_post, mock_signer_cls, mock_file):
        mock_signer_cls.return_value.sign.return_value = "sig"

        response_mock = Mock()
        response_mock.headers = {"Content-Type": "application/json"}
        response_mock.json.return_value = {"id": "x", "redirectUrl": "http://p"}
        response_mock.text = "{}"
        response_mock.raise_for_status.return_value = None
        mock_post.return_value = response_mock

        create_finik_qr_payment("o1", 10, "test")

        mock_post.assert_called_once_with(
            TEST_SETTINGS["FINIK_PAYMENT_URL"],
            data=ANY,
            headers=ANY,
        )

    @override_settings(**TEST_SETTINGS, FINIK_TEST=True)
    @patch("tanda_backend.payment.services.open", new_callable=mock_open, read_data=b"KEY")
    @patch("tanda_backend.payment.services.Signer")
    @patch("tanda_backend.payment.services.requests.post")
    def test_beta_url_used(self, mock_post, mock_signer_cls, mock_file):
        mock_signer_cls.return_value.sign.return_value = "sig"

        response_mock = Mock()
        response_mock.headers = {"Content-Type": "application/json"}
        response_mock.json.return_value = {"id": "x", "redirectUrl": "http://p"}
        response_mock.text = "{}"
        response_mock.raise_for_status.return_value = None
        mock_post.return_value = response_mock

        create_finik_qr_payment("o1", 10, "test")

        mock_post.assert_called_once_with(
            TEST_SETTINGS["FINIK_TEST_PAYMENT_URL"],
            data=ANY,
            headers=ANY,
        )
