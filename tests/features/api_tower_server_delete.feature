@api @tower @server @delete
@fixture.api
Feature: API - /tower/server DELETE requests

    Scenario: Delete an existing tower server
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        When I send a "delete" request to "tower/server" endpoint using the saved "server" id
        Then I receive a successful response

    Scenario: Delete an existing tower server with an invalid token
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        Given I am authenticated with an invalid token
        When I send a "delete" request to "tower/server" endpoint using the saved "server" id
        Then I receive an invalid token response

    Scenario: Delete an existing tower server with a refreshed token
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        Given I am authenticated with a refreshed token
        When I send a "delete" request to "tower/server" endpoint using the saved "server" id
        Then I receive a successful response
