import time

from behave import when


@when(u'wait for {duration:d} seconds')
def step_impl(context, duration):
    time.sleep(duration)
