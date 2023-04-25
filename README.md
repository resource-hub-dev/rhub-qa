# Test Automation

Welcome to the RHUB Automation Suite!


	This test suite is design to cover the most common flow occurrences in the RHUB user journey.  

## Requirements
	
- docker - as requisit
- python 3.9 > latest-stable 
- behave latest-stable
- selenoid from https://aerokube.com/selenoid/
- requests
	

## Solution design:

The initial idea is to have a strong foundation to build the e2e tests. Based on that idea the behave test framework for python was chosen. The framework brings the possibility to unify API and UI tests, since every test is written in python. 
With this in mind the actual framework enables a huge amount of possibilities when testing across technologies, using it it's possible to create a test data mass, deploy or provision the targeted application and run users journeys .

## To run the tests:

Navigate to the desired test folder, all the tests are using behave so it's to easy to start them.

You can choose run one by one (`behave test_name.feature`) or just type `behave` at the console in the features folder. This action will be understood by the system as that you want to run all the tests specified by the feature files in that folder. Another option is to setup tags in the `.feature` files as it allows that only the tests with the choosen tags will be trigged. As an example:

 ```
 behave --tags="tag"
 ```
 
Running any test method with --junit option generates a .xml file reporting all selected tests results.
  
```
behave --junit
behave test1.feature --junit
behave test1.feature test2.feature --junit
behave --tags="@tag1" --junit
``` 
 
The resulting file is in the JUnit format.
 
For more report formats follow https://behave.readthedocs.io/en/stable/.

## Developing API tests
The API tests use classes defined in the `tests/features/steps/api` directory. All the individual endpoints are represented by their respective classes which inherit from the `BaseEndpoint` class, which implements some common methods for creating request bodies and parameters, and for logging the API calls. The logging of API calls is important for the test cleanup part. You can take a look at the individial endpoint classes to get a feel for how these methods are used.

We needed to have a simple way of calling all the API endpoints in the test steps and for this reason we implemented the `API` class which stores as parameters all the other endpoint objects. Behave fixtures are used to setup the API object and also do the cleanup. These steps are implemented in the `tests/features/fixtures.py` file. You can see that we store the API object in the passed behave context object as `context.api`. From there you can easily send requests to the desired enpoint by calling the appropriate methods, e.g. `context.api.lab.region.get_list()`.

Make sure that the `RHUB_API_TOKEN` and `RHUB_API_ADDR` environment variables are set:

```
export RHUB_API_ADDR='http://localhost:8081'
export RHUB_API_TOKEN=...
```

Other important file to checkout is `tests/features/steps/api_helpers.py`, here we implemented some common methods that map the steps from the feature files onto the API calls, allow us to modify the data we send or save some parts of the response (e.g. the IDs of newly created objects) so we can use them in future calls and also there are methods for evaluating the API responses.

To further understand this we can breakdown an example test scenario:

```gherkin
1	Scenario: Create a new satellite server
2  		Given I am authenticated
3  		When I send a "get_list" request to "auth/group" endpoint
4  		And I lookup the "group" "id" from an item named "rhub-admin" in the last response
5  		And I update the "owner_group_id" item in "satellite.server.create" using the saved "group" id
6  		When I send a "create" request to "satellite/server" endpoint with body "satellite.server.create"
7  		Then I receive the following response "satellite.server.create"
```

Line 2 makes sure that the appropriate API token is used in the upcoming requests. Step 3 is implemented by the helper methods mentioned above. The `get_list` argument corresponds to a function implemented by the endpoint class and the passed in URL is parsed so that the appropriate object is used, here it is the `AuthGroupEndpoint` class found in `context.api.auth.group`. Step 4 takes the last request response and saves the `id` from a group named `rhub-admin` into the `context.saved_ids` dictionary, under the `group` key. The request data and expected responses for the API calls are defined using JSON files in the `tests/data/api/requests` and `tests/data/api/responses` directories. The steps we implemented allows us to dynamically modify the loaded data, which is what's happening in step 5. We set the `owner_group_id` attribute in the request data to the `id` we saved in the last step. Afterwards, in step 6, we send a request to create a sattelite server with the modifed request data and then requests are compared.

Some items in the responses are hard to verify, which is why each endpoint class defines a dictionary, saying what items in which responses should be ignored. For comparison we then implemented some filter methods which recursively go through the expected and recieved data dictionaries and filter out such items. Good example of this is the `LabRegionEndpoint` class defined in `tests/features/steps/api/lab_region_endpoint.py`.
___

BRs

Allan Barroso 
abarroso@redhat.com 
+55 31 99476-9506

Simon Košina skosina@redhat.com
