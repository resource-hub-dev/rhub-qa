# TODO: log cleanups, find unverifiable items
import requests

from steps.api.base_endpoint import BaseEndpoint, log_call, IsVerifiable


class LabRegionEndpoint(BaseEndpoint):
    """
    Represents the lab/region API endpoint.
    """

    UNVERIFIABLE_ITEMS = {
        'get_list': {},
        'create': {},
        'get_usage_all': {},
        'delete': {},
        'get': {},
        'update': {},
        'remove_product': {},
        'get_products': {},
        'update_products': {},
        'get_region_usage': {}
    }

    def url(self, suffix: str = '') -> str:
        return f"{self.base_url}/lab/region{suffix}"

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['get_list'])
    def get_list(
        self,
        filter: dict | None = None,
        sort: str | None = None,
        page: int | None = None,
        limit: int | None = None
    ) -> requests.Response:
        args = self.get_function_arguments(
            locals(), skip_args=['self', '__class__'])
        params = self.create_params(args)
        response = super().get(url=self.url(), params=params)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['create'])
    def create(
        self,
        name: str,
        openstack_id: int,
        owner_group_id: str,
        tower_id: int,
        banner: str | None = None,
        description: str | None = None,
        enabled: bool | None = None,
        lifespan_length: int | None = None,
        location_id: int | None = None,
        openstack_keyname: str | None = None,
        reservation_expiration_max: int | None = None,
        reservations_enabled: bool | None = None,
        satellite_id: int | None = None,
        total_quota: dict | None = None,
        user_quota: dict | None = None,
        users_group_id: str | None = None
    ) -> requests.Response:
        args = self.get_function_arguments(locals(), skip_args=['self'])
        body = self.create_body(args)

        response = self.post(url=self.url(), json=body)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['get_usage_all'])
    def get_usage_all(self) -> requests.Response:
        url = self.url(suffix='/all/usage')
        response = super().get(url)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['delete'])
    def delete(self, id: int) -> requests.Response:
        url = self.url(suffix=f"/{id}")
        response = super().delete(url)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['get'])
    def get(self, id: int) -> requests.Response:
        url = self.url(suffix=f"/{id}")
        response = super().get(url)
        print(url)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['update'])
    def update(
        self,
        id: int,
        name: str | None = None,
        openstack_id: int | None = None,
        owner_group_id: str | None = None,
        tower_id: int | None = None,
        banner: str | None = None,
        description: str | None = None,
        enabled: bool | None = None,
        lifespan_length: int | None = None,
        location_id: int | None = None,
        openstack_keyname: str | None = None,
        reservation_expiration_max: int | None = None,
        reservations_enabled: bool | None = None,
        satellite_id: int | None = None,
        total_quota: dict | None = None,
        user_quota: dict | None = None,
        users_group_id: str | None = None
    ) -> requests.Response:
        args = self.get_function_arguments(locals(), skip_args=['self', 'id'])
        body = self.create_body(args)

        url = self.url(suffix=f"/{id}")
        response = self.patch(url, json=body)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['remove_product'])
    def remove_product(self, region_id: int, product_id: int) -> requests.Response:
        url = self.url(suffix=f"/{region_id}/products")
        body = {'id': product_id}
        response = super().delete(url, json=body)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['get_products'])
    def get_products(self, id: int, filter: dict | None = None) -> requests.Response:
        args = self.get_function_arguments(
            locals(), skip_args=['self', 'id', '__class__'])
        params = self.create_params(args)

        url = self.url(suffix=f"/{id}/products")
        response = super().get(url, params=params)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['update_products'])
    def update_products(
        self,
        region_id: int,
        product_id: int,
        enabled: bool | None = None
    ) -> requests.Response:
        args = self.get_function_arguments(
            locals(), skip_args=['self', 'region_id'])
        body = self.create_body(args)

        # remap 'product_id' to 'id'
        body['id'] = body['product_id']
        del body['product_id']

        url = self.url(suffix=f"/{region_id}/products")
        response = self.post(url, json=body)

        return response

    @log_call(BaseEndpoint.LOGGER, UNVERIFIABLE_ITEMS['get_region_usage'])
    def get_region_usage(self, id: int) -> requests.Response:
        url = self.url(suffix=f"/{id}/usage")
        response = super().get(url)

        return response
