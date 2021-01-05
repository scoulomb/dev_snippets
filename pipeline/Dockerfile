FROM python:3.9

WORKDIR /working_dir

COPY pip.conf /etc/pip.conf

RUN pip install -U pip &&\
    pip install --upgrade setuptools wheel pipenv

COPY Pipfile /working_dir/
COPY Pipfile.lock /working_dir/

# Install packages, and check old ones
RUN pipenv sync --dev
# RUN pipenv check


COPY *.py /working_dir/

# Run unit-tests and check coverage
# For this to work COPY tests and ensure to have `__init__.py` in serialization and test
RUN pipenv run python /working_dir/pipeline-dojo.py

