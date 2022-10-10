import yaml
import os
import sys
import logging
from jinja2 import Template, Undefined
from .action import Action
from .test_case import TestCase
from ptt import settings

log = logging.getLogger(__name__)


class NullUndefined(Undefined):
    def __getattr__(self, key):
        return ''


class TestPlan():
    def __init__(self, plan_file_path) -> None:
        self.load(plan_file_path)
        log.info(f'test plan definition file [{plan_file_path}] loaded')

    def load(self, plan_file_path):
        """
        Loads the test plan from yaml file.
        """

        try:
            with open(os.path.expanduser(plan_file_path), 'r') as f:
                try:
                    txt = f.read()
                    test_plan = yaml.load(txt, Loader=yaml.FullLoader)
                    t = Template(txt, undefined=NullUndefined)
                    self.data = yaml.safe_load(t.render(test_plan | settings.data))
                    self.global_variables = self.data['variables'] if 'variables' in self.data else {}
                except yaml.YAMLError as e:
                    log.error(f'Error parsing yaml test plan definition file {e.problem_mark}: {e.problem}')
                    sys.exit(1)
        except FileNotFoundError:
            log.error(f'Error opening test plan definition file {plan_file_path}')
            sys.exit(1)

    async def setup(self):
        '''
        Runs the operations defined in the setup block of the test plan definition file
        '''

        if 'setup' in self.data:
            if self.data['setup']:
                for action in self.data['setup']:
                    await (Action(action, self.global_variables)).run()

    async def teardown(self):
        '''
        Runs the operations defined in the setup block of the teardown definition file
        '''

        if 'teardown' in self.data:
            if self.data['teardown']:
                for action in self.data['teardown']:
                    await (Action(action, self.global_variables)).run()

    async def test(self):
        '''
        Excecutes the operations defined in the TEST block of the test plan deifnition file
        '''

        errors = 0
        for tc_definition in self.data['test_cases']:
            if 'enable' in tc_definition:
                if tc_definition['enable'] == True:
                    try:
                        print('******************* Test case ' +
                              tc_definition['name'] +
                              ' ******************************')
                        await (TestCase(tc_definition, self.global_variables)).setup()
                        await (TestCase(tc_definition, self.global_variables)).test()
                        await (TestCase(tc_definition, self.global_variables)).teardown()
                    except Exception as e:
                        log.info(
                            'Test case teardown activated due to an error in setup/running phase!')
                        await (TestCase(tc_definition, self.global_variables)).teardown()
                        errors += 1
                        log.error(e)

        if errors > 0:
            log.error(f'Execution failed due to {errors} errors')
