import sys
import os
sys.path.append(os.getcwd())

import pytest

from starlette.testclient import TestClient
from graphene.test import Client
import ujson as json
from lamia import app
from graphql.error.located_error import GraphQLLocatedError
from lamia.translation import _
from lamia.utilities import response_contains_graphql_error

def test_registration(gino_db):
    client = TestClient(app)
    
    # Test account creation
    response = client.post('/graphql', data=json.dumps({
        'query': """
            mutation testMutation {
              registerUser(userName: "test", emailAddress: "test@test.com", password: "abcde") {
                identity {
                  displayName,
                  userName
                }
              }
            }
            """
        }
    ), headers={'Accept': 'application/json', 'content-type': 'application/json'})
    response_body = json.loads(response.content)
    assert response_body['data']['registerUser']['identity']['displayName'] == 'test'
    assert response_body['data']['registerUser']['identity']['userName'] == 'test'
    
    # This should raise a graphql error due to the empty password
    response = client.post('/graphql', data=json.dumps({
        'query': """
            mutation testMutation {
              registerUser(userName: "test", emailAddress: "test@test.com", password: "") {
                identity {displayName}}}
            """
        }
    ), headers={'Accept': 'application/json', 'content-type': 'application/json'})
    assert response_contains_graphql_error(json.loads(response.content),
        'Password is too short! Should be at least five characters in length.')
    
    # This should raise a graphql error due to the duplicate name
    response = client.post('/graphql', data=json.dumps({
        'query': """
            mutation testMutation {
              registerUser(userName: "test", emailAddress: "test123@test.com", password: "abcde") {
                identity {displayName}}}
            """
        }
    ), headers={'Accept': 'application/json', 'content-type': 'application/json'})
    assert response_contains_graphql_error(json.loads(response.content),
        'This user name is already in use. User names must be unique.')

    # This should raise a graphql error due to the duplicate email
    response = client.post('/graphql', data=json.dumps({
        'query': """
            mutation testMutation {
              registerUser(userName: "test_a", emailAddress: "test@test.com", password: "abcde") {
                identity {displayName}}}
            """
        }
    ), headers={'Accept': 'application/json', 'content-type': 'application/json'})
    assert response_contains_graphql_error(json.loads(response.content),
        'This email address is already in use for another account.')

    # This should raise a graphql error due to the invalid username
    response = client.post('/graphql', data=json.dumps({
        'query': """
            mutation testMutation {
              registerUser(userName: "test@test.com", emailAddress: "test123@test.com", password: "abcde") {
                identity {displayName}}}
            """
        }
    ), headers={'Accept': 'application/json', 'content-type': 'application/json'})
    assert response_contains_graphql_error(json.loads(response.content),
        'Invalid user name. Characters allowed are a-z and _.')
    
    # This should raise a graphql error due to the invalid email syntax
    response = client.post('/graphql', data=json.dumps({
        'query': """
            mutation testMutation {
              registerUser(userName: "test_abc", emailAddress: "test_abc", password: "abcde") {
                identity {displayName}}}
            """
        }
    ), headers={'Accept': 'application/json', 'content-type': 'application/json'})
    response_body = json.loads(response.content)
    assert response_contains_graphql_error(json.loads(response.content),
        'Email address as entered is not a valid email address.')

def test_identity_query(gino_db):
    client = TestClient(app)
    
    # Test account (actually identity) querying
    response = client.post('/graphql', data=json.dumps({
        'query': """
            {
              identity(name: "test") {
                displayName,
                userName
              }
            }
            """
        }
    ), headers={'Accept': 'application/json', 'content-type': 'application/json'})
    
    response_body = json.loads(response.content)
    assert response_body['data']['identity']['displayName'] == 'test'
    assert response_body['data']['identity']['userName'] == 'test'
    
    # This should throw a graphql error because the account doesn't exist
    response = client.post('/graphql', data=json.dumps({
        'query': """{identity(name: "test123") { displayName }}"""
        }
    ), headers={'Accept': 'application/json', 'content-type': 'application/json'})
    response_body = json.loads(response.content)
    assert response_contains_graphql_error(json.loads(response.content),
        'Identity does not exist!')


