FROM reigncl/airflow:2.3.1-python3.9-onbuild

USER airflow
RUN mkdir -p data
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
