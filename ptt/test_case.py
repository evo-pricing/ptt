import logging
from .action import Action

log = logging.getLogger(__name__)


class TestCase():
    def __init__(self, definition, global_variables) -> None:
        self.name = definition['name']
        self.description = definition['description']
        self.actions = definition['actions']
        self.global_variables = global_variables
        self.tc_setup = None if 'setup' not in definition else definition['setup']
        self.tc_teardown = None if 'teardown' not in definition else definition['teardown']

    async def test(self):
        # TODO manage return codes and output on screen

        log.info(f'{self.name} running...')
        try:
            for i, action in enumerate(self.actions):
                log.info(
                    f'{self.name} {next(iter(self.actions[i])).upper()} action {i+1}/{len(self.actions)}')
                action['test_name'] = self.name
                action['plan_name'] = self.global_variables['plan_name']
                await (Action(action)).run()
        except Exception as e:
            raise Exception(
                f'{self.name} test failed; inner exception is: [{e}]. Extra info: {self.actions[i].get("compare")}')

        log.info(f'{self.name} test completed')

    async def setup(self):
        if self.tc_setup:
            for action in self.tc_setup:
                await (Action(action, self.global_variables)).run()
            log.info(f'{self.name} setup completed')

    async def teardown(self):
        if self.tc_teardown:
            for action in self.tc_teardown:
                await (Action(action, self.global_variables)).run()
            log.info(f'{self.name} teardown completed')
