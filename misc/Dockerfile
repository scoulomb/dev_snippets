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

RUN mkdir /working_dir/misc
COPY *.py /working_dir/misc/

# Run unit-tests and check coverage
# For this to work COPY tests and ensure to have `__init__.py` in serialization and test
RUN pipenv run python /working_dir/misc/list_not_none.py
RUN pipenv run python /working_dir/misc/another_script.py

