# monobank-api - The Monobank API wrapper for Python

![GitHub-issues](https://img.shields.io/github/issues/edicasoft/monobank-api)

Python client for Monobank open API (https://api.monobank.ua/docs/)

* [Installation](#Installation)
* [Usage](#usage)
    * [Without authorization](#Without-authorization)
    * [Personal token](#Personal-token)
    * [Authorization request](#Authorization-request)
* [License](#license)

## Installation

```bash
pip install monobank-api
```

or add to to your requirements.txt `monobank-api==0.1.1` and run

```bash
pip install -r requirements.txt
```

## Usage

### Without authorization

Monobank open API allows making certain requests without any authorization.

```python
from monobank_api import BaseAPI

mono = BaseAPI()
currencies = mono.get_currency()
```

### Personal token

Request and activate your token at https://api.monobank.ua

```python
from monobank_api import PersonalAPI

PERSONAL_TOKEN = "copy token here"
```

### Authorization request

The corporate API documentation (https://api.monobank.ua/docs/corporate.html)

To use this authorization method, you'll need to generate a key and contact Monobank team.

#### Generate private key 
```shell script
openssl ecparam -genkey -name secp256k1 -out private_key.key
```
***NOTE***: Do not share this key with anyone.

#### Generate public key
```shell script
openssl ec -in private_key.key -pubout > public_key.pub
```

For more information check the [Monobank API documentation](https://api.monobank.ua/docs/corporate.html).

#### Usage example

```python
from monobank_api import CorporateAPI

# the url has to be used by the user to confirm authorization
mono = CorporateAPI.request_auth("./private_key.pem")

if mono.check_auth():
    user_info = mono.get_client_info()
```

## License

The MIT License (MIT). Please see [License](LICENSE) for more information.