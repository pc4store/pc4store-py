import asyncio

from pc4store.clients import Pc4StoreAsyncClient
from pc4store.schema import Order, Pc4StoreError

my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

# initialize client
client = Pc4StoreAsyncClient(store_id=my_store_id, store_key=my_store_secret_key)

order_id = '831a6509-445a-4558-9812-7bbe2ade96b4'

async def main():
    try:
        order: Order = await client.get_order(order_id)
    except Pc4StoreError as err:
        print(err)
    else:
        print(order.id)     # pc4store order id
        print(order.payment_url)  # link to redirect user for payment

asyncio.run(main())