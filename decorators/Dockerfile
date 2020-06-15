FROM python:3.8

WORKDIR /working_dir

COPY pip.conf /etc/pip.conf

RUN pip install -U pip &&\
    pip install --upgrade setuptools wheel pipenv

COPY Pipfile /working_dir/
COPY Pipfile.lock /working_dir/

# Install packages, and check old ones
RUN pipenv sync --dev
# RUN pipenv check

COPY *.py ./
COPY decorators decorators

# Run unit-tests and check coverage
# For this to work COPY tests and ensure to have `__init__.py` in serialization and test
RUN pipenv run python decorators/decorator_basic.py
RUN pipenv run python decorators/decorators_with_argument.py
RUN pipenv run python decorators/observation_decorators_with_without_argument.py
RUN pipenv run python decorators/solution_decorators_with_without_argument.py
