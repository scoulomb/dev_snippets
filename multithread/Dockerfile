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

RUN mkdir /working_dir/multithread
COPY *.py /working_dir/multithread/
COPY chrono /working_dir/multithread/chrono
COPY mywikipedia /working_dir/multithread/mywikipedia
COPY parallel_map /working_dir/multithread/parallel_map

# Run unit-tests and check coverage
# For this to work COPY tests and ensure to have `__init__.py` in serialization and test
RUN pipenv run python /working_dir/multithread/client.py

