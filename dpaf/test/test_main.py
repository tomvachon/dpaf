import unittest

import os
import sys
import time
import os.path as op
from functools import partial
from kivy.clock import Clock


main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)

from main import OpCli

class TestMain(unittest.TestCase):
    
    # sleep function that catches ``dt`` from Clock
    def pause(*args):
        time.sleep(0.000001)

    # main test function
    def run_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)

        # Do something

        # Comment out if you are editing the test, it'll leave the
        # Window opened.
        app.stop()
    
    def test_example(self):
        app = OpCli()
        p = partial(self.run_test, app)
        Clock.schedule_once(p, 0.000001)
        app.run()