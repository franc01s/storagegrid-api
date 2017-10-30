storagegrid-api
=========

---

A pure python library to work with Netapp Storagegrid 

Install
-------

    sudo pip install -U storagegrid

API Example
-----------

```python
from storagegrid.controller import Controller

c = Controller(host='host', username='user', password='passw0rd', verify=False)
accounts = c.grid_accounts(100)
for account in accounts:
    print('id: {id} name: {name}'.format(id=account['id'], name=account['name']))
```

API
---

### `class Controller`

Interact with a Netapp Storagegrid admin node.


### `__init__(self, host, username, password, version, verify)`

Create a Controller object.

 - `host`		-- the address of the controller host; IP or name
 - `username`	-- the username to log in with
 - `password`	-- the password to log in with
 -  `version`	-- the api version
 -  `verify`	-- check SSL certificate

### `grid_accounts(self, limit)`

Accounts list.

 - `limit` -- limit the number accounts returned.



# TO DO


License
-------

MIT

