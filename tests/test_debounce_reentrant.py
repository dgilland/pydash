"""Callbacks may start a fresh debounce burst without blocking or losing state."""

import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap

import pytest

import pydash


@pytest.mark.parametrize("first_path", ["timer", "max_wait"])
def test_callback_can_start_another_burst(first_path):
    # Run in a subprocess so a lock regression fails with a bounded timeout.
    script = textwrap.dedent("""
        import json
        import sys
        from unittest.mock import patch
        import pydash

        clock = [0]
        timers = []
        calls = []

        class Timer:
            def __init__(self, interval, function, args):
                self.due = clock[0] + round(interval * 1000)
                self.function, self.args = function, args
                self.cancelled = False
                timers.append(self)
            def start(self):
                pass
            def cancel(self):
                self.cancelled = True

        def advance(now):
            clock[0] = now
            for timer in list(timers):
                if not timer.cancelled and timer.due <= now:
                    timer.cancelled = True
                    timer.function(*timer.args)

        def callback(value):
            calls.append([clock[0], value])
            if len(calls) == 1:
                debounced('reentrant')
            return value

        with (
            patch('pydash.functions.threading.Timer', Timer),
            patch('pydash.now', lambda: clock[0]),
        ):
            debounced = pydash.debounce(callback, 10, max_wait=25)
            debounced('first')
            if sys.argv[1] == 'timer':
                advance(10)
                start = 10
            else:
                clock[0] = 25
                debounced('first')
                start = 25
            clock[0] = start + 10
            debounced('middle')
            clock[0] = start + 18
            debounced('latest')
            advance(start + 25)
            assert calls == [[start, 'first'], [start + 25, 'latest']], calls
            print(json.dumps(calls))
    """)
    env = dict(os.environ, PYTHONPATH=str(Path(pydash.__file__).resolve().parent.parent))
    result = subprocess.run(
        [sys.executable, "-c", script, first_path],
        capture_output=True,
        text=True,
        timeout=3,
        env=env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert len(json.loads(result.stdout)) == 2
