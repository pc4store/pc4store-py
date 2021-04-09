from multidict import MultiDict

from pc4store.clients import Pc4StoreAsyncClient

my_store_id = 'e40e58c5-2dd2-4c3b-994f-5af9c7ea255b'
my_store_secret_key = 'b8c4d4c6-579a-41aa-b887-d390242ce339'

# initialize client
client = Pc4StoreAsyncClient(store_id=my_store_id,
                             store_key=my_store_secret_key)

request = MultiDict()  # callback request that you receive from PC4Store API

if client.is_signature_correct(request.json(), request.headers):
    # you can trust this callback
    ...
else:
    # it could be cheating
    ...
