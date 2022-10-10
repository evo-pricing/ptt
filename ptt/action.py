import logging
import os
from .actions import SQLQueryAction, IspacAction, LoadAction, CompareAction, FileAction

log = logging.getLogger(__name__)


class Action():
    def __init__(self, definition, global_variables=None) -> None:
        self.action = definition
        self.global_variables = global_variables if global_variables is not None else {}

    async def run(self):
        '''
        Executes the given action
        '''
        # match the RUN action which executes a script file given its path
        if 'run' in self.action:
            file_path = self.action['run']
            _, file_ext = os.path.splitext(file_path)

            # run block is expected to have local variables defined too
            # defined local variables replaces global ones
            variables = self.get_all_variables(
                self.action['variables'] if 'variables' in self.action else {})

            # execute a SQL script file
            if file_ext == '.sql':
                await SQLQueryAction(self.action).run(file_path, variables)
            # execute an SSIS package from and an ISPAC file
            elif file_ext == '.ispac':
                await IspacAction(self.action).run()
            else:
                Exception(
                    f'Action not yet implemented, check test definition file syntax [{self.action}]')

        # match the LOAD action which reads a csv file and fills a SQL table
        elif 'load' in self.action:
            await LoadAction(self.action).run()

        # match the COMPARE action which retrieves data from a SQL table and compares it
        # with a local cav file
        elif 'compare' in self.action:
            await CompareAction(self.action).run()

        # match the COPY action which prepares the package's feed (csv,xml,...)
        elif 'copy' in self.action:
            await FileAction(self.action).copy()

        # match the DELETE action which prepares the cleaning package's feed (csv,xml,...)
        elif 'delete' in self.action:
            await FileAction(self.action).delete()

        else:
            raise Exception(
                f'Action not yet implemented, check test definition file syntax [{self.action}]')

    def get_all_variables(self, other_variables):
        '''
        Merge variables dicts defined on YAML test plan file.
        It always return a dictionary object
        '''

        return self.global_variables | other_variables
