@api @tower @server @post
@fixture.api
Feature: API - /tower/server POST requests

    Scenario: Create a new tower
        Given I am authenticated
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        Then I receive the following response "tower.server.create"

    Scenario: Create a new tower with an invalid token
        Given I am authenticated with an invalid token
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        Then I receive an invalid token response

    Scenario: Create a new tower with a refreshed token
        Given I am authenticated with a refreshed token
        When I send a "create" request to "tower/server" endpoint with body "tower.server.create"
        Then I receive the following response "tower.server.create"
