# TODO: log cleanups, find unverifiable items
import requests

from steps.api.base_endpoint import BaseEndpoint, log_call, IsVerifiable


class TowerServerEndpoint(BaseEndpoint):
    """
    Represents the tower/server API endpoint.
    """

    UNVERIFIABLE_ITEMS = {
        'get_list': {'id': IsVerifiable.NO, '_href': IsVerifiable.NO},
        'create': {'id': IsVerifiable.NO, '_href': IsVerifiable.NO},
        'delete': {},
        'get': {'id': IsVerifiable.NO, '_href': IsVerifiable.NO},
        'update': {'id': IsVerifiable.NO, '_href': IsVerifiable.NO}
    }

    def url(self, suffix: str = '') -> str:
        return f"{self.base_url}/tower/server{suffix}"

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['get_list'])
    def get_list(
        self,
        filter: dict = None,
        sort: str = None,
        page: int = None,
        limit: int = None
    ) -> requests.Response:
        args = self.get_function_arguments(
            locals(), skip_args=['self', '__class__'])
        params = self.create_params(args)
        response = super().get(self.url(), params=params)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['create'])
    def create(
        self,
        credentials: str,
        name: str,
        url: str,
        description: str = None,
        enabled: bool = None,
        verify_ssl: bool = None,
    ) -> requests.Response:
        args = self.get_function_arguments(locals(), skip_args=['self'])
        body = self.create_body(args)
        response = self.post(self.url(), json=body)

        try:
            response.raise_for_status()
            id = response.json()['id']
            BaseEndpoint.LOGGER.log_cleanup(self.delete, id=id)
        except requests.HTTPError:
            pass

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['delete'])
    def delete(self, id: int) -> requests.Response:
        response = super().delete(self.url(suffix=f"/{id}"))

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['get'])
    def get(self, id: int) -> requests.Response:
        response = super().get(self.url(suffix=f"/{id}"))

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['update'])
    def update(
        self,
        id: int,
        credentials: str = None,
        name: str = None,
        url: str = None,
        description: str = None,
        enabled: bool = None,
        verify_ssl: bool = None,
    ) -> requests.Response:
        args = self.get_function_arguments(locals(), skip_args=['self', 'id'])
        body = self.create_body(args)
        cleanup_args = self.get_values_before_update(self.get, id, args)

        response = self.patch(self.url(f"/{id}"), json=body)

        try:
            response.raise_for_status()
            BaseEndpoint.LOGGER.log_cleanup(self.update, id=id, **cleanup_args)
        except requests.HTTPError:
            pass

        return response
