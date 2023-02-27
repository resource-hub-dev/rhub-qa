import sys
import subprocess
import json
import glob
import os

from steps.api.api import API
from steps.api.base_endpoint import BaseEndpoint
from steps.cli.cli_model import ResourceHubCLI
from tempfile import TemporaryDirectory
from behave import fixture
from pathlib import Path

API_REQUESTS_PATTERN = '../data/api/requests/*.json'
API_RESPONSE_PATTERN = '../data/api/responses/*.json'


@fixture
def rhub_api(context):
    context.api_addr = os.environ["RHUB_API_ADDR"]
    context.api_token = os.environ["RHUB_API_TOKEN"]

    context.api = API(admin_token=context.api_token, api_url=context.api_addr)

    context.api.logger = BaseEndpoint.LOGGER
    context.api.request_data = {}
    context.api.response_data = {}
    context.saved_ids = {}

    request_data_paths = glob.glob(API_REQUESTS_PATTERN)
    response_data_paths = glob.glob(API_RESPONSE_PATTERN)

    for path in request_data_paths:
        with open(path) as f:
            context.api.request_data.update(json.load(f))

    for path in response_data_paths:
        with open(path) as f:
            context.api.response_data.update(json.load(f))

    yield context.api
    
    context.api.cleanup()


@fixture
def rhub_cli(context):
    try:
        temp_directory = TemporaryDirectory()
        temp_directory_path = Path(temp_directory.name)

        # create temporary python virtual environment
        subprocess.run(
            [sys.executable, '-m', 'venv', temp_directory.name],
            check=True,
        )

        # install RHub CLI on the created virtual environment
        subprocess.run(
            f"source {temp_directory_path / 'bin/activate'} ; pip install -q {ResourceHubCLI.PIP_CLONE_URL}",
            check=True,
            shell=True,
        )

        context.cli = ResourceHubCLI(temp_directory_path)
        yield context.cli

    finally:
        temp_directory.cleanup()
