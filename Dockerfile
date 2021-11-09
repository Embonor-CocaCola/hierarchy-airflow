FROM reigncl/airflow:2.2.1-python3.9-onbuild

USER airflow

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
