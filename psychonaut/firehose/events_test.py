from multiformats import CID
from .events import IndexRecord


def test_index_record():
    r = IndexRecord(
        type="index_record",
        action="Create",
        uri="at://foo/bar",
        cid=CID.decode("zdpuArKcqh4Bfc5ufSWKTSS1jFRYJ47gpuxCEVXeWdMEjDpAM"),
        timestamp="2021-01-01T00:00:00Z",
    )
