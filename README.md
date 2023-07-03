## PC4Store

SDK for work with PC4Store API

## Installation

`pip install pc4store` requires Python 3.6 or higher

## Examples

### Sync client

##### Initialize client

```python
from pc4store.clients import Pc4StoreClient

my_store_id = 'unique identifier of your store'
my_store_secret_key = 'secret'

client = Pc4StoreClient(store_id=my_store_id, store_key=my_store_secret_key)
```

##### Create order

```python
from pc4store.clients import Pc4StoreClient
from pc4store.schema import CreateOrderInput, Order, Pc4StoreError

from decimal import Decimal

my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

# initialize client
client = Pc4StoreClient(store_id=my_store_id, store_key=my_store_secret_key)

try:
    order: Order = client.create_order(CreateOrderInput(
        currency_name='USDCASH',
        currency_smart_contract='token.pcash',
        amount_to_pay=Decimal(999),     # it can also be decimal-like string, float or integer
        response_url='https://api.my-store/payment-callback/',
        expiration_time=30 * 60,  # 30 min
        merchant_order_id='12345',
        description='optional description for this order',
        success_payment_redirect_url='https://my-store/orders/12345/success',
        failed_payment_redirect_url='https://my-store/orders/12345/failed',
    ))
except Pc4StoreError as err:
    print(err)
else:
    print(order.id)     # pc4store order id
    print(order.payment_url)  # link to redirect user for payment

```



##### Get order info

```python
from pc4store.clients import Pc4StoreClient
from pc4store.schema import CreateOrderInput, Order, Pc4StoreError


my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

order_id = 'order_id_in_payment_system'

# initialize client
client = Pc4StoreClient(store_id=my_store_id, store_key=my_store_secret_key)

try:
    order: Order = client.get_order(order_id)
except Pc4StoreError as err:
    print(err)
else:
    print(order.id)     # pc4store order id
    print(order.payment_url)  # link to redirect user for payment

```

##### Create transfer
```python
from pc4store.clients import Pc4StoreClient
from pc4store.schema import CreateTransferInput, Transfer, Pc4StoreError

from decimal import Decimal

my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

# initialize client
client = Pc4StoreClient(store_id=my_store_id, store_key=my_store_secret_key)

try:
    transfer: Transfer = client.create_transfer(CreateTransferInput(
        amount=Decimal('25.5'),
        currency_name='USDCASH',
        currency_smart_contract='token.pcash',
        eos_account='reciever.pcash',
        response_url="https://api.my-store/payment-callback/",
    ))
except Pc4StoreError as err:
    print(err)
else:
    print(transfer.id)     # pc4store transfer id
    print(transfer.status)  # transfer status

```

##### Get transfer info

```python
from pc4store.clients import Pc4StoreClient
from pc4store.schema import Transfer, Pc4StoreError


my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

transfer_id = 'pc4store_transfer_id'

# initialize client
client = Pc4StoreClient(store_id=my_store_id, store_key=my_store_secret_key)

try:
    transfer: Transfer = client.get_transfer(transfer_id)
except Pc4StoreError as err:
    print(err)
else:
    print(transfer.id)     # pc4store transfer id
    print(transfer.status)  # transfer status

```

##### Verify callback request

```python
request = MultiDict()  # callback request that you receive from PC4Store API

if client.is_signature_correct(request.json(), request.headers):
    # you can trust this callback
    ...
else:
    # it could be cheating
    ...
```


### Async client

Async client has absolutely same interface.

```python
from pc4store.clients import Pc4StoreAsyncClient

my_store_id = 'unique identifier of your store'
my_store_secret_key = 'secret'

client = Pc4StoreAsyncClient(store_id=my_store_id, store_key=my_store_secret_key)
```

