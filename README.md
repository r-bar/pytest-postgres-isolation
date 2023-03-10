# Parallel isolated database testing POC

Test running pytest with multiple workers while maintaining database isolation
for each test. Database isolation is acheived by:
  1. Creating a template database (if it does not already exist)
  2. Running migrations on the template database
  3. Creating a new database with a randomly generated name from the template
     for each test.
  4. Running pytest tests with multiple parallel workers via pytest-xdist
  5. Deleting the generated database after each test


## Running the tests

```shell
docker-compose run --rm test
```
