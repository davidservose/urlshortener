# Url Shortener

## Simple Setup

Execute `make run` which will:
1. Create the virtual environment (venv)
2. Install dependencies from requirements.txt
3. Run the application

## Manual Setup

1. Install python3 (python 3.10.6 specifically used for this project)
2. Create a `venv` folder: `python3 -m venv venv`
3. Activate the virtual environment: `. venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the service: `flask run`

## Testing

Run unit tests: `make test`

Manual Testing:
1. Run the application: `make run`
2. Create short urls through the `shorten` api:
   * Generated short url: `curl -X POST http://127.0.0.1:5000/v1/shorten -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}'`
   * Custom short url: `curl -X POST http://127.0.0.1:5000/v1/shorten -H "Content-Type: application/json" -d '{"url": "https://www.dell.com", "custom_short_url": "dell"}'`
3. Enter `localhost:5000/v1/<short_url>` into a web browser, and the service will redirect to the url from the shorten request

## Requirements
1. Given a URL, our service should generate a shorter and unique alias of it. This is
called a short link. This link should be short enough to be easily copied and pasted
into applications.
2. When users access a short link, our service should redirect them to the original
link.
3. The application should be written in python to match our other internal tools.

## Design

The url shortener consists of a python web application microservice which implements REST HTTP apis that interact with a database to store and retretive the shortened urls. 

## Implementation

The url shortener is implemented as a python flask web app with the following endpoints:
1. `POST: /v1/shorten` which takes two parameters: `url` and optionally `custom_short_url`, creates and returns a short url (random if not specified by custom_short_url) which maps to the original url.
2. `/v1/<short_url>` which redirects to the original url.

The data storage layer is a sqllite database accessed through sqlalchemy to demonstrate data access patterns, persistence, and modularity.

## Future Work

### Additional features (Recommended for being considered a production service)

1. Atomic database operations: The current logic has an execution gap between checking of existing of short url and creating new record for the short url. This could lead to a race condition where some other client creates the short url between the two, causing the record creation of the original request to fail and forcing the client retry their request. This would be a requirement to fix before being considered a production level service.
2. Add Namespaces for different users/organizations: This feature would allow better control over short urls and would prevent conflict different users requesting the same custom url. The updated endpoints could be `/v1/<namespace>/<short_url>` and `/v1/shorten/<namespace>`
3. Url management: Adding `update` and `delete` endpoints would be useful to change short urls to point to new urls or delete urls that are no longer used.
4. Add timestamp metadata to url records: Adding created and updated timestamps to the url record would help manage and debug the system, while also enabling other features such as creating short-lived short urls that expire after a desired time.
5. Migrate to hosted database service: Doing this would enable the app to scale beyond a single machine by enabling a consistent database across multiple clients, and significantly increase storage limits.
6. Add an API gateway in front of the service
7. Enable the service in multiple regions to ensure system uptime during outages

### Maintenance

1. Send metrics/logs to a cloud based system such as Datadog, monitor/alert on:
   * System resource utilization (memory, cpu, network)
   * Exceptions
   * Per endpoint metrics such as error rates, latency, and queries per second.
   * Downstream service metrics such as database error rates, latency, and queries per second.
2. Scaling out the service as usage grows, this could be achieved in a variety of ways:
   * Optimize the service by simplify logic, changing database queries/access patterns, update python/packages to get latest performance benefits.
   * Increasing the number of hosts/vms/containers used for the service (effective to a point, but with added cost)
   * Increase database size by adding nodes/shards as database utilization increases above a proposed limit or forecasted date.
3. Updating packages due to known security issues or deprecation of downstream apis.
