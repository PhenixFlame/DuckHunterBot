from events import Event, EVENTS
import pytest


class TestMessage:
    def __init__(self, text):
        self.content = text


async def Event_on_empty(event: Event):
    return await event.events(TestMessage(''))


@pytest.mark.asyncio
@pytest.mark.parametrize('event', EVENTS.keys())
async def test_Event_on_empty(event):
    event = Event(event)
    assert not await Event_on_empty(event)


@pytest.mark.parametrize('event', EVENTS.keys())
def test_Event_yaml_tests(event):
    errors = []
    tests = EVENTS[event]['tests']
    event = Event(event)
    for expected, samples in tests.items():
        if isinstance(samples, str):
            samples = [samples]
        for test_text in samples:
            message = TestMessage(test_text)
            value = event._checker(message)
            if not expected == value:
                if hasattr(event._checker, 'pattern'):
                    print(f'{event.name} \n'
                          f'\ttest_text: {test_text}\n'
                          f'\texpected: {expected}\n'
                          f'\tchecker : [{event._checker.pattern}]'
                          )
                else:
                    print(f'{event.name} \n'
                          f'\ttest_text: {test_text}\n'
                          f'\texpected: {expected}\n'
                          )

                errors.append(test_text)
                # errors.append((expected, value))
    assert not errors

