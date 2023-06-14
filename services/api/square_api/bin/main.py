from square.client import Client
from pprint import pprint

client = Client(
    access_token= 'EAAAEL6vid26E4R6BHYMubuS7aCJfZPje2CElN034Gzn3rqwWCgML_rgZlAO238k',
    environment='sandbox'
)

result = client.merchants.list_merchants()

if result.is_success():
    pprint(result.body)
elif result.is_error():
    pprint(result.errors)