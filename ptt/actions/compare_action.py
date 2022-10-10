import logging
import aioodbc
import pandas as pd
import numpy as np
import pathlib
from io import StringIO
from .sql_action import SQLAction

log = logging.getLogger(__name__)


class CompareAction(SQLAction):
    def __init__(self, definition) -> None:
        super().__init__(
            None if 'dsn' not in definition else definition['dsn'])

        self.compare = definition['compare']
        self.expect = definition['expect']

    async def run(self):
        compare = await self.toDataFrame(self.compare)
        expect = await self.toDataFrame(self.expect)
        
        if not compare.equals(expect):
            print(f'Result differences:\n{compare.compare(expect)}')
            # print('Compare value:', compare.to_string(index=False))
            # print('Expected value:', expect.to_string(index=False))
            raise Exception(
                'expected value is not equal to the compare value!')

    async def toDataFrame(self, data):
        [(task, target)] = data.items()
        # --------------------------------------------------------------------------------------------------
        if task == 'query':
            async with aioodbc.connect(dsn=self.get_ds(), autocommit=True) as conn:
                cur = await conn.cursor()
                await cur.execute(target)
                rows = await cur.fetchall()
                return pd.DataFrame.from_records(rows, columns=[col[0] for col in cur.description]).astype('string')
        # --------------------------------------------------------------------------------------------------
        elif task == 'table':
            async with aioodbc.connect(dsn=self.get_ds(), autocommit=True) as conn:
                cur = await conn.cursor()
                await cur.execute(f'SELECT * FROM {target}')
                rows = await cur.fetchall()
                return pd.DataFrame.from_records(rows, columns=[col[0] for col in cur.description]).astype('string')
        # --------------------------------------------------------------------------------------------------
        elif task == 'csv':
            return pd.read_csv(target, dtype=str).astype('string')
        # --------------------------------------------------------------------------------------------------
        elif task == 'data':
            return pd.read_csv(StringIO(target)).astype('string')
        # --------------------------------------------------------------------------------------------------
        elif task == 'path':
            file = pathlib.Path(target)
            if file.exists():
                data = {'': ['1']}
            else:
                data = {'': ['0']}
            return pd.DataFrame(data).astype('string')
        # --------------------------------------------------------------------------------------------------
        elif task == 'value':
            return pd.DataFrame(data=np.array([[target]]), columns=['']).astype('string')
