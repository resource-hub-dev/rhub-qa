@api @tower @server @patch
@fixture.api
Feature: API - /tower/server PATCH requests

    Scenario: Update tower server information
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        When I send a "update" request to "tower/server" endpoint with body "tower.server.update" using the saved "server" id
        Then I receive the following response "tower.server.update"

    Scenario: Update tower server information with an invalid token
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        Given I am authenticated with an invalid token
        When I send a "update" request to "tower/server" endpoint with body "tower.server.update" using the saved "server" id
        Then I receive an invalid token response

    Scenario: Update tower server information with a refreshed token
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        Given I am authenticated with a refreshed token
        When I send a "update" request to "tower/server" endpoint with body "tower.server.update" using the saved "server" id
        Then I receive the following response "tower.server.update"
