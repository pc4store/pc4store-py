import asyncio

from pc4store.clients import Pc4StoreAsyncClient
from pc4store.schema import Transfer, Pc4StoreError

my_store_id = "e40e58c5-2dd2-4c3b-994f-5af9c7ea255b"
my_store_secret_key = "b8c4d4c6-579a-41aa-b887-d390242ce339"

# initialize client
client = Pc4StoreAsyncClient(store_id=my_store_id, store_key=my_store_secret_key)

transfer_id = "bccc2c48-c147-42de-a1e4-e2a567bcf3be"


async def main():
    try:
        transfer: Transfer = await client.get_transfer(transfer_id)
    except Pc4StoreError as err:
        print(err)
    else:
        print(transfer.id)  # pc4store transfer id
        print(transfer.status)  # transfer status


asyncio.run(main())
