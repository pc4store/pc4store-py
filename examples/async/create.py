from pc4store.clients import Pc4StoreAsyncClient
from pc4store.data import CreateOrderInput, OrderData

my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

# initialize client
client = Pc4StoreAsyncClient(store_id=my_store_id,
                             store_key=my_store_secret_key)

# create order
res = await client.create_order(
    CreateOrderInput(
        currency_name='USDCASH',
        currency_smart_contract='token.pcash',
        amount_to_pay='99.99999',
        response_url='https://api.my-store/payment-callback/',
        expiration_time=30 * 60,  # 30 min
        merchant_order_id='12345',
        description='optional description for this order',
        success_payment_redirect_url='https://my-store/orders/12345/success',
        failed_payment_redirect_url='https://my-store/orders/12345/failed',
    )
)

if res.status == 'OK':
    order: OrderData = res.payload.order  # all data about order
    payment_link = order.payment_url  # link to redirect user for payment
    order_id = order.id  # unique order id in payment system
else:
    print(res.error)
