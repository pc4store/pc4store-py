from pc4store.clients import Pc4StoreClient
from pc4store.data import OrderData

my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

# initialize client
client = Pc4StoreClient(store_id=my_store_id, store_key=my_store_secret_key)

order_id = 'order_id_in_payment_system'

order: OrderData = client.get_order(order_id)

if order:
    # do some staff
    print('Actual order status: ', order.status)
else:
    print('Opps, order not found...')
