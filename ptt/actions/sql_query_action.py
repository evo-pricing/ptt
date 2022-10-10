import aioodbc
import logging
from jinja2 import Template, Undefined
from .sql_action import SQLAction

log = logging.getLogger(__name__)


class NullUndefined(Undefined):
    def __getattr__(self, key):
        return ''


class SQLQueryAction(SQLAction):

    def __init__(self, definition) -> None:
        super().__init__(
            None if 'dsn' not in definition else definition['dsn'])

    async def run(self, file_path, variables):
        '''
        Runs a SQL query file 
        '''
        with open(file_path, encoding='utf-8') as f:
            # substitute variables on SQL file using Jinja
            t = Template(f.read(), undefined=NullUndefined)
            statements = t.render(variables).split('GO')
            async with aioodbc.connect(dsn=self.get_ds(), autocommit=True) as conn:
                cur = await conn.cursor()
                for i, statement in enumerate(statements):
                    sql_query = statement.strip()  # we trim the statement string
                    if sql_query == '':
                        continue

                    # run the SQL query if not empty
                    await cur.execute(sql_query)
                    await cur.execute('SELECT @@ROWCOUNT')
                    row_count = (await cur.fetchall())[0][0]
                    log.info(
                        f'[{file_path}] statement {i} affected {row_count} rows')
