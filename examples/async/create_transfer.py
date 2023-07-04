import asyncio
from decimal import Decimal

from pc4store.clients import Pc4StoreAsyncClient
from pc4store.schema import CreateTransferInput, Transfer, Pc4StoreError

my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

# initialize client
client = Pc4StoreAsyncClient(store_id=my_store_id, store_key=my_store_secret_key)


async def main():
    try:
        transfer: Transfer = await client.create_transfer(CreateTransferInput(
            amount=Decimal('25.5'),
            currency_name='USDCASH',
            currency_smart_contract='token.pcash',
            eos_account='reciever.pcash',
            response_url="https://api.my-store/payment-callback/",
        ))
    except Pc4StoreError as err:
        print(err)
    else:
        print(transfer.id)  # pc4store transfer id
        print(transfer.status)  # transfer status

asyncio.run(main())