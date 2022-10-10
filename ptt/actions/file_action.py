import logging
import os
import shutil


log = logging.getLogger(__name__)


class FileAction():
    def __init__(self, action) -> None:
        self.action = action

    async def copy(self):
        '''
        Copy file from [source] to [destination]
        '''
        # TODO handle exception and error
        shutil.copy(self.action['copy'], self.action['destination'])

    async def delete(self):
        '''
        Delete file from [path]
        '''
        # TODO handle exception and error
        if os.path.exists(self.action['delete']):
            os.remove(self.action['delete'])
