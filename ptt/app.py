import asyncio
import logging
import os
from pathlib import Path
from ptt import g
from .test_plan import TestPlan

log = logging.getLogger(__name__)


class App():
    test_plans = []

    def __init__(self, project_root, output_path) -> None:
        # we iterate through all test plans found in project root folder
        # and instantiate the plans
        for file in Path(project_root).glob('*.yml'):
            log.info(f'Loading test plan definition file [{file}]...')
            self.test_plans.append(TestPlan(file))

        # set working directory to project_root
        g['project_root'] = project_root
        g['output_path'] = output_path
        os.chdir(project_root)

    async def main_worker(self):
        logging.info('doing qa stuff...')
        for plan in self.test_plans:
            if 'enable' in plan.data:
                if plan.data['enable'] != True:
                    planName = plan.global_variables["plan_name"]
                    log.info(f'Test plan \"{planName}\" is disabled!')
                    continue
                await plan.setup()
                await plan.test()
                print('******************* Test plan teardown ******************************')
                await plan.teardown()

    def main(self):
        '''
        Main implemented through asynchronous task.
        '''

        loop = asyncio.get_event_loop()
        try:
            print(
                'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

            # eventually we might run multiple things in parallel
            # just instantiating multiple tasks
            tasks = [
                loop.create_task(self.main_worker()),
            ]

            loop.run_until_complete(asyncio.wait(tasks))
        except (KeyboardInterrupt, SystemExit):
            # TODO better catch exceptions at termination
            # https://quantlane.com/blog/ensure-asyncio-task-exceptions-get-logged/
            pass
        finally:
            logging.info("Terminating...")
            loop.close()

        logging.info('Shutting down')
