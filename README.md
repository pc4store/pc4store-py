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
from pc4store.data import CreateOrderInput, OrderData

res = client.create_order(
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
```

##### Get order info

```python
order_id = 'order_id_in_payment_system'

order: OrderData = client.get_order(order_id)

if order:
    # do some staff
    print('Actual order status: ', order.status)
else:
    print('Opps, order not found...')
```

##### Create transfer
```python
from pc4store.data import TransferInput

if __name__ == '__main__':
    # create order
    # print(client.get_transfer('eb94786b-c0e3-43af-b5f9-218128fe3db5'))
    res = client.transfer(TransferInput(
        currency_name='USDCASH',
        currency_smart_contract='token.pcash',
        amount='100.00002',
        eos_account='myeosusername',
        response_url='https://api.my-store/transfer-callback/',
    ))

    if res.status == 'OK':
        print(res.payload.transfer)  # all data about transfer
    else:
        print(res.error)
```

##### Get order info

```python
from pc4store.data import Transfer

transfer_id = 'transfer_id_in_payment_system'
transfer: Transfer = client.get_transfer(transfer_id)

if transfer:
    # do some staff
    print('Actual transfer status: ', transfer.status, transfer.action.is_irreversible)
else:
    print('Opps, transfer not found...')
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

