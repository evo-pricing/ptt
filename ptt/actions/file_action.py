from glob import glob
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
        Delete file(s) from [path]:
        If [path] is a file, delete the file.
        If [path] is a directory delete all files inside the directory.
        '''
        # TODO handle exception and error
        path = self.action['delete']
        if os.path.exists(path):                        
            if os.path.isdir(path):
                for file in glob(os.path.join(path, '*.*')):
                    os.remove(file)
            if os.path.isfile(path):
                os.remove(path)
