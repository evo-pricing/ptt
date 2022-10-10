import logging
import os
import aioodbc
import pandas as pd
from .sql_action import SQLAction

log = logging.getLogger(__name__)


class LoadAction(SQLAction):
    def __init__(self, definition) -> None:
        super().__init__(
            None if 'dsn' not in definition else definition['dsn'])

        self.action = definition

        self.file_path = definition['load']
        file_name, self.file_ext = os.path.splitext(self.file_path)

        # if the destination_table field is not defined the value is
        # extracted from the file name assigning the default schema dbo
        # this requires the DB to be specified at DSN
        if 'destination_table' in definition:
            self.destination_table = definition['destination_table']
        else:
            self.destination_table = f'[dbo].[{file_name}]'

    async def run(self):
        if self.file_ext == '.csv':
            data = pd.read_csv(self.file_path, index_col=None,keep_default_na=False)
        else:
            raise Exception(f'Type of file not supported [{self.file_ext}]')

        # we assemble the INSERT query as pandas does not support asyncio yet
        columns = ''
        values = ''
        for column in data.columns:
            columns += f'{column},'
            values += '?,'

        insert_query = f'INSERT INTO {self.destination_table} ({columns.rstrip(",")}) VALUES ({values.rstrip(",")})'
        # log.info(f'Executing LOAD query {insert_query}...')
        async with aioodbc.connect(dsn=self.get_ds(), autocommit=True) as conn:
            cur = await conn.cursor()

            # executes a DELETE if specified in the definition
            if 'append' in self.action and self.action['append'] == False:
                await cur.execute(f'DELETE FROM {self.destination_table}')

            await cur.executemany(insert_query, data.values.tolist())
            log.info(
                f'[{self.file_path}] added {data.shape[0]} rows to table {self.destination_table}')
