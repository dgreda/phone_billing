# Phone Billing Service

## Summary

A very simple phone billing system as a microservice using Python
with major package dependencies like FastAPI, SQLModel (sqlalchemy, pydantic), Alembic.

The service uses PostgreSQL in dev Docker container, and SQLite when running tests.

Service comes with a `test` container as well, where all the linters, unit and integrations tests are running.

Use cases:
* As a phone operator I want all customer calls to be charged.
* As a customer I want to be able to see my phone call history.
* As a customer I want to receive my invoice every first day of the month.

This is just a RESTful API implementation that solves the main use cases mentioned above (there's no UI to it).

The API comes with OpenAPI documentation that can be browsed under `/docs` path of the API,
so when running locally with help of the provided docker-compose.yml setup, you can visit http://localhost:8080/docs

## Installation

In order to start the application you need to have Docker installed.

First, you need to build docker images with help of docker-compose
(all the docker commands need to be called from the repository root directory):

```shell
docker-compose build
```

Next, we need to execute Alembic migrations to create initial DB structure:

```shell
docker-compose exec dev-api alembic upgrade head
```

You should then see an output similar to this, meaning that "init" migration has ran
and initialized all the tables. 

![alembic.png](docs/images/alembic.png)

You should now be able to start the service:

```shell
docker-compose up dev-api
```

And visit the OpenAPI spec to learn more about the API: http://localhost:8080/docs

## Testing

The application comes equipped with a test docker container to run the test suite
(comprised of unit and integration tests) and other linters and static code analyzers.

```shell
docker-compose run --rm test
```

Current test code coverage reaches 99% (100% of the actual domain code).

## Next Steps

Of course it's just PoC of what the actual phone billing system could be,
but it does outline a couple of principles that I strive to follow when working on software
and that I wanted to demonstrate here, including, but not limited to: Dependency Injection
(and some other SOLID principles), Design Patterns (Strategy in this case), Code Quality and Testing.

For the real-world production-ready API we would need to do much more.
Below few key points to think about:

* More extensive validation of requests
* Authorization mechanism for API e.g. OAuth
* Health check endpoints
* Prod deployment strategy (e.g. k8s), scaling/autoscaling

What's more, the complexity of such a billing service goes far beyond what has been 
implemented and demonstrated here.

For instance the actual invoice generation process would most likely be some sort of scheduled job
running on some cadence (e.g. cronjob) that would either be using API's endpoint,
or work with the service (instance) directly to iterate through users that need to invoiced,
generate invoices and deliver them to users per email for example.

Another thing to consider is whether the system is meant to be global or for local market only
(dates and timezones are always challenging to work with).
If it has to be working globally, in order to offer best and reliable experience, users should be billed
properly according to their actual timezone (well, at least the official country / number timezone),
as opposed to what the system is doing currently (working with Timezone aware timestamps,
but assuming UTC timestamps filtering for the invoice generation).


## Additional task

### Describe how you would extend the solution to be able to support different billing plans like prepaid and fixed amount per month

This is actually outlined to some extent in the codebase - I have introduced a strategy pattern
and one existing strategy currently implemented is `FlatRatePostpaidPlanStrategy`
which calculates the total charge based on a flat rate as postpaid (as requested in the task requirements).

By implementing the interface `BillingPlanStrategyInterface`,
we can add more different billing strategies without modifying the core logic of `InvoiceService`.

The billing strategy is now application-wide, but it would make sense that different users
might be on different billing plans and require different billing strategies at runtime.
