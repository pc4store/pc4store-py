from pc4store.clients import Pc4StoreClient
from pc4store.schema import FiatMethod, Pc4StoreError

my_store_id = "e40e58c5-2dd2-4c3b-994f-5af9c7ea255b"
my_store_secret_key = "b8c4d4c6-579a-41aa-b887-d390242ce339"

# initialize client
client = Pc4StoreClient(store_id=my_store_id, store_key=my_store_secret_key)

try:
    methods: list[FiatMethod] = client.get_fiat_methods()
except Pc4StoreError as err:
    print(err)
else:
    print(methods)
