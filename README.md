# Friss Data Science assignment solution

Questions 1-6 are answered in the Python Notebook, the rest is done through the Dockerfile and the server directory.
The notebook has comments explaining my choices there. For the code there are some aspects I would like to highlight


## Choice of framework
FastAPI and Pydantic make it very easy to build an API, with an additional benefit that both are also fast in production.

## Input format
The current format is very unstructured and susceptible to breaking if new features are added.
Still it would be very simple to integrate with the current format. For a production solution I would use a proper columnar format with better data validation.
I mainly used pandas for parsing because it allowed me to re-use the code I wrote during research, but this may not be a good idea in production.
