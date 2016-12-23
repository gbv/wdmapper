"""existence of this file avoids the need to declare PYTHONPATH=."""

import pytest
import sys
import io


@pytest.fixture
def stdin():
    return lambda s: MockStdin(s)


class MockStdin:
    def __init__(self, data):
        self.data = data
        self.stdin = sys.stdin

    def __enter__(self):
        if sys.version_info[0] == 3:
            # Python 3: sys.stdin is unicode
            sys.stdin = io.StringIO(self.data)
        else:
            # Python 2: sys.stdin is bytes (UTF-8)
            sys.stdin = io.BytesIO(self.data.encode('utf-8'))

    def __exit__(self, type, value, traceback):
        sys.stdin = self.stdin
