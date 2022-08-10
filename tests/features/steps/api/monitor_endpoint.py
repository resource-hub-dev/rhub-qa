import requests

from api.base_endpoint import BaseEndpoint
from api.monitor_bm_endpoint import MonitorBMEndpoint
from api.monitor_lab_endpoints import MonitorLabEndpoint
from api.monitor_vm_endpoint import MonitorVMEndpoint


class MonitorEndpoint(BaseEndpoint):
    """
    Represents the /monitor API endpoint.
    """

    UNVERIFIABLE_ITEMS = {}

    def __init__(self, session: requests.Session):
        super().__init__(session)

        self.bm = MonitorBMEndpoint(self.session)
        self.lab = MonitorLabEndpoint(self.session)
        self.vm = MonitorVMEndpoint(self.session)

    def url(self, suffix: str = '') -> str:
        return f"{self.base_url}/monitor{suffix}"
