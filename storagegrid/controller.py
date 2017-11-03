# -*- coding: utf-8 -*-


import logging
from requests import Session

log = logging.getLogger(__name__)


class APIError(Exception):
    pass


class Account:
    def __init__(self, id, name, capabilities, policy):
        self._id = id
        self._name = name
        self._capabilities = capabilities
        self._policy = policy

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def capabilities(self):
        return self._capabilities

    @property
    def policy(self):
        return self._policy


class Controller:
    """Interact with a Storagegrid admin node.


    """

    def __init__(self, host, username, password, version='v2', verify=True):
        """Create a Controller object.

        Arguments:
            host     -- the address of the controller host; IP or name
            username -- the username to log in with
            password -- the password to log in with
            version -- the password to log in with
            verify   -- check SSL certificate; True or False

        """

        self.host = host
        self.username = username
        self.password = password
        self.url = 'https://' + host
        self.api_url = self.url + '/api/{}'.format(version)

        log.debug('Controller for %s', self.url)

        self.session = Session()
        self.session.verify = verify

        self._login()

    def _responsecheck(self, response):
        if 'meta' in response:
            if response['meta']['rc'] != 'ok':
                raise APIError(response['meta']['msg'])
        if 'data' in response:
            return response['data']
        else:
            return None

    def _login(self):
        log.debug('login() as %s', self.username)
        json = {'username': self.username, 'password': self.password}

        login_url = self.api_url + '/authorize'
        res = self.session.post(login_url, json=json)
        self.token = res.json()['data']

    def _logout(self):
        log.debug('logout()')
        self.opener.get(self.url + 'logout')

    def get_tenants(self, limit):
        """"
        List tenants
        required parameter <limit>     = max tenants returned
        """

        log.debug('grid_accounts() limit {limit}'.format(limit=limit))
        bearer = 'Bearer {}'.format(self.token)
        headers = {'Authorization': bearer}
        params = {'limit': limit}

        res = self.session.get(self.api_url + '/grid/accounts', headers=headers, params=params)
        accounts = []
        for account in res.json()['data']:
            accountobj = Account(account.get('id', None), account.get('name', None), account.get('capabilities', None),
                                 account.get('policy', None))
            accounts.append(accountobj)

        return accounts

    def create_tenant(self, name, capabilities=['s3'], policy={"useAccountIdentitySource": True,
                                                                             "allowPlatformServices": False,
                                                                             "quotaObjectBytes": None},
                      password='passsuperSecret'):
        """"
        Create one tenant
        required parameter <name>    = name of tenant
        optionnal parameter <capabilities>    = capabilities
        optionnal parameter <policy>    = policy
        optionnal parameter <password>   = name of tenant
        """

        log.debug('create_tenant()  {name}'.format(name=name))
        bearer = 'Bearer {}'.format(self.token)
        headers = {'Authorization': bearer}
        params = {
            "name": "Widgets Unlimited",
            "capabilities": capabilities,
            "policy": policy,
            "password": password
        }

        res = self.session.post(self.api_url + '/grid/accounts', headers=headers, json=params)

        return res.status_code, res.json().get('errors', None)