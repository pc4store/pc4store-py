import asyncio
from decimal import Decimal

from pc4store.clients import Pc4StoreAsyncClient
from pc4store.schema import CreateOrderInput, Order, Pc4StoreError, enums

my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

# initialize client
client = Pc4StoreAsyncClient(store_id=my_store_id, store_key=my_store_secret_key)


async def main():
    try:
        order: Order = await client.create_order(CreateOrderInput(
            currency_name='USDCASH',
            currency_smart_contract='token.pcash',
            amount_to_pay=Decimal(100),     # it can also be decimal-like string, float or integer
            response_url='https://api.my-store/payment-callback/',
            allowed_methods=[enums.PaymentMethod.WORLD_PAY, enums.PaymentMethod.RUS_PAY]    # allow only fiat payments
        ))
    except Pc4StoreError as err:
        print(err)
    else:
        print(order.id)     # pc4store order id
        print(order.payment_url)  # link to redirect user for payment

asyncio.run(main())