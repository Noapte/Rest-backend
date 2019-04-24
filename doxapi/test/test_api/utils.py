# pylint: disable=too-many-arguments,locally-disabled

import json


class ApiClient:

    BASE_URL = "/api"

    def __init__(self, client):
        self.client = client
        self.headers = {}

    def delete(self, url, headers=None):
        return self._execute_request("delete", url, headers)

    def get(self, url, headers=None):
        return self._execute_request("get", url, headers)

    def patch(self, url, data, headers=None):
        return self._execute_request("patch", url, headers, data)

    def post(self, url, data, headers=None):
        return self._execute_request("post", url, headers, data)

    def put(self, url, data, headers=None):
        return self._execute_request("put", url, headers, data)

    def _execute_request(self, method, url, headers=None, data=None):
        headers = headers or self.headers
        return getattr(self.client, method)(
            self.BASE_URL + url,
            data=json.dumps(data),
            headers=headers,
            content_type="application/json",
        )


class ApiAuthClient(ApiClient):
    def __init__(self, client, **credentials):
        super(ApiAuthClient, self).__init__(client)
        response = self.post("/auth", credentials)
        self.headers = {"Authorization": response.json["access_token"]}
