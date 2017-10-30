# -*- coding: utf-8 -*-


import logging
from requests import Session

log = logging.getLogger(__name__)


class APIError(Exception):
    pass


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

    def grid_accounts(self, limit):
        """"
        Unblock a client device
        required parameter <mac>     = client MAC address
        """

        log.debug('grid_accounts() limit {limit}'.format(limit=limit))
        headers = {'Authorization': 'Bearer ' + self.token}
        params = {'limit': limit}

        res = self.session.get(self.api_url + '/grid/accounts', headers=headers, params=params)

        return res.json()['data']
