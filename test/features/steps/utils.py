import time

from behave import given, when, then


@when(u'wait for {duration:d} seconds')
def step_impl(context, duration):
    time.sleep(duration)
