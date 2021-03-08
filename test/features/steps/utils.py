import time

from behave import step


@step(u'wait for {duration:d} seconds')
def step_impl(context, duration):
    time.sleep(duration)
