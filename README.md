# Social Network Project

# Mainatiners

- [Krasheninnikov Mikhail Dmitrievich](t.me/technothecow), 2210

# Codestyle

## Import order

First block should be completely of imports from python standard library and third-party libraries. Second block should be imports from libraries of the system. Third block should be of imports from the current project (except models/protobufs). Fourth block should be of imports from the current project (models/protobufs).

# Codegen

## How to generate code

To generate code you need to run the following command in the root of the project:
```bash
python -m make-gen
```

# Launch

All services should start with the following command:
```bash
cd <service> && python -m src.main
```