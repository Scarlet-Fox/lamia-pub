import pytest
# Import lamia either from pythonpath or a relative parent dir
try:
    import lamia
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.getcwd())
    
from lamia.utilities.webfinger import normalize

def test_identifier_normalization():
    expected_base_url = "https://lamia.social"
    assert normalize('acct:lamia@lamia.social') == ('lamia@lamia.social', expected_base_url,)
    assert normalize('https://lamia.social/users/lamia') == ('lamia.social/users/lamia', expected_base_url,)
    assert normalize('https://lamia.social/@lamia') == ('lamia.social/@lamia', expected_base_url,)
    assert normalize('lamia@lamia.social') == ('lamia@lamia.social', expected_base_url,)
    assert normalize('acct:lamia.social/lamia') == ('lamia.social/lamia', expected_base_url,)

def test_http_identifier_normalization():
    expected_base_url = "https://lamia.social"
    assert normalize('http://lamia.social/users/lamia') == ('lamia.social/users/lamia', expected_base_url,)
    assert normalize('http://lamia.social/@lamia') == ('lamia.social/@lamia', expected_base_url,)
    
def test_port_identifier_normalization():
    expected_base_url = "https://lamia.social"
    assert normalize('acct:lamia@lamia.social:8000') == ('lamia@lamia.social', expected_base_url,)
    assert normalize('https://lamia.social:8000/users/lamia') == ('lamia.social/users/lamia', expected_base_url,)
    assert normalize('https://lamia.social:8000/@lamia') == ('lamia.social/@lamia', expected_base_url,)
    assert normalize('lamia@lamia.social:8000') == ('lamia@lamia.social', expected_base_url,)
    assert normalize('acct:lamia.social:8000/lamia') == ('lamia.social/lamia', expected_base_url,)