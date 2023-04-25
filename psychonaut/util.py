import pytest
import os
import json


@pytest.fixture
def load_test_fixture(request):
    def _load_file(filename, as_json=False, fixtures_dir=True):
        test_module_path = os.path.dirname(request.fspath)
        file_relative_path = filename
        if fixtures_dir:
            file_relative_path = os.path.join("fixtures", filename)
        file_absolute_path = os.path.join(test_module_path, file_relative_path)
        with open(file_absolute_path, "r") as file:
            res = file.read()
            if as_json:
                res = json.loads(res)
        return res
    return _load_file