from types import SimpleNamespace

from django.test import TestCase

from tanda_backend.merchant.models import Merchant, Provider
from tanda_backend.orders.models import DeliveryType, Order, PaymentType
from tanda_backend.orders.services import create_orders
from tanda_backend.products.models import Product, ProductVariant
from tanda_backend.users.models import User


class CreateOrdersTestCase(TestCase):
    def setUp(self) -> None:
        self.provider = Provider.objects.create(name="Provider")
        self.user = User.objects.create(username="user", sso_id="1")

    def _create_variant(self, merchant: Merchant, stock_id: str) -> ProductVariant:
        product = Product.objects.create(
            title=f"Product {stock_id}",
            slug=f"product-{stock_id}",
            images=["img"],
            stock_id=f"prod-{stock_id}",
            merchant=merchant,
            provider=self.provider,
        )
        return ProductVariant.objects.create(
            product=product,
            stock_id=stock_id,
            available_quantity=10,
            selling_price=5,
        )

    def test_multiple_orders_created_for_different_merchants(self) -> None:
        merchant1 = Merchant.objects.create(name="M1", provider=self.provider)
        merchant2 = Merchant.objects.create(name="M2", provider=self.provider)

        v1 = self._create_variant(merchant1, "v1")
        v2 = self._create_variant(merchant2, "v2")

        variants = [
            SimpleNamespace(variant_id=v1.id, quantity=1),
            SimpleNamespace(variant_id=v2.id, quantity=2),
        ]

        orders = create_orders(
            user=self.user,
            full_name="John Doe",
            phone_number="123", 
            payment_type=PaymentType.CASH,
            city="City",
            address="Address",
            delivery_type=DeliveryType.SELF_DELIVERY,
            comments="",
            variants=variants,
        )

        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(len(orders), 2)
        self.assertSetEqual({o.merchant_id for o in orders}, {merchant1.id, merchant2.id})
