from decimal import Decimal

from pc4store.clients import Pc4StoreClient
from pc4store.schema import CreateOrderInput, Order, Pc4StoreError

my_store_id = "e40e58c5-2dd2-4c3b-994f-5af9c7ea255b"
my_store_secret_key = "b8c4d4c6-579a-41aa-b887-d390242ce339"

# initialize client
client = Pc4StoreClient(store_id=my_store_id, store_key=my_store_secret_key)

try:
    order: Order = client.create_order(
        CreateOrderInput(
            currency_name="USDCASH",
            currency_smart_contract="token.pcash",
            amount_to_pay=Decimal(
                999
            ),  # it can also be decimal-like string, float or integer
            response_url="https://api.my-store/payment-callback/",
            expiration_time=30 * 60,  # 30 min
            merchant_order_id="12345",
            description="optional description for this order",
            success_payment_redirect_url="https://my-store/orders/12345/success",
            failed_payment_redirect_url="https://my-store/orders/12345/failed",
        )
    )
except Pc4StoreError as err:
    print(err)
else:
    print(order.id)  # pc4store order id
    print(order.payment_url)  # link to redirect user for payment
