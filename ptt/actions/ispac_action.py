import asyncio
import logging
from ptt import settings, g
from pathlib import Path
import time

log = logging.getLogger(__name__)


class IspacAction():
    def __init__(self, action) -> None:
        self.action = action
        self.test_name = action['test_name']
        self.plan_name = action['plan_name']
        self.file_path = action['run']
        self.output_path = g['output_path']

        if 'expect' in action:
            self.rule = 'expect'
            self.include = True
            self.term = action['expect']
        elif 'notexpect' in action:
            self.rule = 'notexpect'
            self.include = False
            self.term = action['notexpect']
        else:
            self.rule = None
            self.term = None

    async def run(self):
        '''
        Runs an Ispac SSIS package file
        '''

        program = settings.get('tools.dtexec')
        # we populate the command line
        arguments = [
            '/Project', self.file_path,
            '/Package', self.action['package'],
            '/Reporting', 'E'
        ]

        for parameter in self.action['parameters']:
            arguments += ['/Set', parameter]

        proc = await asyncio.create_subprocess_exec(
            program,
            *arguments,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        stdout = stdout.decode() if stdout else None
        stderr = stderr.decode() if stderr else None

        if stdout:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            Path(self.output_path).mkdir(parents=True, exist_ok=True)
            with open(f"{self.output_path}{self.plan_name}_{self.test_name}_log_{timestamp}.txt", "w") as f:
                f.write(f'[stdout]\n{stdout}')

        if stderr:
            log.error(f'[stderr]\n{stderr}')

        if self.term:
            result = (self.term in stdout)
            if not result is self.include:
                raise Exception(
                    f'[{self.rule}] to see [{self.term}] in the ispac log.')

        # if proc.returncode == 0:
        #     log.info('The package executed successfully.')
        # elif proc.returncode == 1:
        #     log.info('The package failed.')
        # elif proc.returncode == 2:
        #     log.info('The package executed successfully.')
        # elif proc.returncode == 3:
        #     log.info('The package was canceled by the user.')
        # elif proc.returncode == 4:
        #     log.info('The package could not be found.')
        # elif proc.returncode == 5:
        #     log.info('The package could not be loaded.')
        # elif proc.returncode == 6:
        #     log.info(
        #         'The utility encountered a syntactic/semantic errors in the command line.')

        # if proc.returncode != self.expect_return_code:
        #     raise Exception(
        #         f'Ispac package return code mismatch [{proc.returncode} != {self.expect_return_code}].')
