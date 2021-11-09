import contextlib
import csv
import logging
import sqlalchemy

from airflow.hooks.dbapi import DbApiHook

from typing import (
    List,
    Generator,
)
from sqlalchemy.orm import sessionmaker


class BaseHook(DbApiHook):
    def __init__(self, *args, **kwargs):
        super(BaseHook, self).__init__(*args, **kwargs)

    def get_sqlalchemy_sessionmaker(self):
        engine = self.get_sqlalchemy_engine()
        return sessionmaker(bind=engine)

    @contextlib.contextmanager
    def session_scope(self):
        session = self.get_sqlalchemy_sessionmaker()()
        try:
            yield session
            session.commit()
        except Exception as e:
            logging.exception(f'exception occured during session {str(session).strip()}: {str(e)}')
            session.rollback()
            raise
        finally:
            session.close()

    def query(
        self,
        sql: str,
        parameters: List[str] = None,
        include_headers: bool = True,
    ) -> Generator:
        if parameters is None:
            parameters = []

        if len(parameters) > 0:
            sql = sql % tuple(parameters)

        sql_text = sqlalchemy.text(sql)
        with self.session_scope() as session:
            results = session.execute(sql_text)

            if include_headers:
                yield results.keys()
            for row in results:
                yield row

    def export(
        self,
        sql: str,
        filepath: str,
        parameters: List[str] = None,
        include_headers: bool = True,
        **kwargs,
    ) -> str:
        if parameters is None:
            parameters = []

        with open(filepath, 'w') as fp:
            writer = csv.writer(fp)
            for result in self.query(
                sql,
                parameters=parameters,
                include_headers=include_headers,
                **kwargs,
            ):
                writer.writerow(result)
        return filepath
