import platform
import pytest

def test_custodial_import(monkeypatch):
    monkeypatch.setattr(platform, 'system', lambda: 'Not Darwin')
    with pytest.raises(NotImplementedError):
        import custodial
