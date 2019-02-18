import sys
import os
sys.path.append(os.getcwd())

import pytest

from lamia.activitypub.webfinger import normalize

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

def test_port_identifier_normalization_without_port():
    expected_base_url = "https://lamia.social"
    assert normalize('acct:lamia@lamia.social:8000') == ('lamia@lamia.social', expected_base_url,)
    assert normalize('https://lamia.social:8000/users/lamia') == ('lamia.social/users/lamia', expected_base_url,)
    assert normalize('https://lamia.social:8000/@lamia') == ('lamia.social/@lamia', expected_base_url,)
    assert normalize('lamia@lamia.social:8000') == ('lamia@lamia.social', expected_base_url,)
    assert normalize('acct:lamia.social:8000/lamia') == ('lamia.social/lamia', expected_base_url,)
    
def test_port_identifier_normalization():
    expected_base_url = "https://lamia.social:8000"
    assert normalize('acct:lamia@lamia.social:8000', True) == ('lamia@lamia.social:8000', expected_base_url,)
    assert normalize('https://lamia.social:8000/users/lamia', True) == ('lamia.social:8000/users/lamia', expected_base_url,)
    assert normalize('https://lamia.social:8000/@lamia', True) == ('lamia.social:8000/@lamia', expected_base_url,)
    assert normalize('lamia@lamia.social:8000', True) == ('lamia@lamia.social:8000', expected_base_url,)
    assert normalize('acct:lamia.social:8000/lamia', True) == ('lamia.social:8000/lamia', expected_base_url,)