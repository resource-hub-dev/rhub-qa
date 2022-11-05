@api @tower @server @get
@fixture.api
Feature: API - /tower/server GET requests

    Scenario: Retreive a list of tower servers
        Given I am authenticated
        When I send a "get_list" request to "tower/server" endpoint
        Then I receive a list of items with the following structure "tower.server.get_list"

    Scenario: Retreive a list of tower servers with an invalid token
        Given I am authenticated with an invalid token
        When I send a "get_list" request to "tower/server" endpoint
        Then I receive an invalid token response

    Scenario: Retreive a list of tower servers with a refreshed token
        Given I am authenticated with a refreshed token
        When I send a "get_list" request to "tower/server" endpoint
        Then I receive a list of items with the following structure "tower.server.get_list"

    Scenario: Retreive tower server details
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        When I send a "get" request to "tower/server" endpoint using the saved "server" id
        Then I receive the following response "tower.server.get"

    Scenario: Retreive tower server details with an invalid token
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        Given I am authenticated with an invalid token
        When I send a "get" request to "tower/server" endpoint using the saved "server" id
        Then I receive an invalid token response

    Scenario: Retreive tower server details with a refreshed token
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        When I save the received "server" id
        Given I am authenticated with a refreshed token
        When I send a "get" request to "tower/server" endpoint using the saved "server" id
        Then I receive the following response "tower.server.get"
