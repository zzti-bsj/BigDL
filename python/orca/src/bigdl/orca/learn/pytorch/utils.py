#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Copyright 2017 The Ray Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is adapted from
# https://github.com/ray-project/ray/blob/master/python/ray/util/sgd/utils.py

import collections
from contextlib import closing, contextmanager
import logging
import numpy as np
import socket
import time
import torch.distributed as dist
import torch
from bigdl.dllib.utils.log4Error import *


logger = logging.getLogger(__name__)

BATCH_COUNT = "batch_count"
NUM_SAMPLES = "num_samples"
BATCH_SIZE = "*batch_size"


class TimerStat:
    """A running stat for conveniently logging the duration of a code block.

    Note that this class is *not* thread-safe.

    Examples:
        Time a call to 'time.sleep'.

        >>> import time
        >>> sleep_timer = TimerStat()
        >>> with sleep_timer:
        ...     time.sleep(1)
        >>> round(sleep_timer.mean)
        1
    """

    def __init__(self, window_size=10):
        self._window_size = window_size
        self._samples = []
        self._units_processed = []
        self._start_time = None
        self._total_time = 0.0
        self.count = 0

    def __enter__(self):
        invalidInputError(self._start_time is None, "concurrent updates not supported")
        self._start_time = time.time()

    def __exit__(self, type, value, tb):
        invalidInputError(self._start_time is not None, "expect start time is not none")
        time_delta = time.time() - self._start_time
        self.push(time_delta)
        self._start_time = None

    def push(self, time_delta):
        self._samples.append(time_delta)
        if len(self._samples) > self._window_size:
            self._samples.pop(0)
        self.count += 1
        self._total_time += time_delta

    def push_units_processed(self, n):
        self._units_processed.append(n)
        if len(self._units_processed) > self._window_size:
            self._units_processed.pop(0)

    @property
    def mean(self):
        return np.mean(self._samples)

    @property
    def median(self):
        return np.median(self._samples)

    @property
    def sum(self):
        return np.sum(self._samples)

    @property
    def max(self):
        return np.max(self._samples)

    @property
    def first(self):
        return self._samples[0] if self._samples else None

    @property
    def last(self):
        return self._samples[-1] if self._samples else None

    @property
    def size(self):
        return len(self._samples)

    @property
    def mean_units_processed(self):
        return float(np.mean(self._units_processed))

    @property
    def mean_throughput(self):
        time_total = sum(self._samples)
        if not time_total:
            return 0.0
        return sum(self._units_processed) / time_total

    def reset(self):
        self._samples = []
        self._units_processed = []
        self._start_time = None
        self._total_time = 0.0
        self.count = 0


@contextmanager
def _nullcontext(enter_result=None):
    """Used for mocking timer context."""
    yield enter_result


class TimerCollection:
    """A grouping of Timers."""

    def __init__(self):
        self._timers = collections.defaultdict(TimerStat)
        self._enabled = True

    def disable(self):
        self._enabled = False

    def enable(self):
        self._enabled = True

    def reset(self):
        for timer in self._timers.values():
            timer.reset()

    def record(self, key):
        if self._enabled:
            return self._timers[key]
        else:
            return _nullcontext()

    def stats(self, mean=True, last=False):
        aggregates = {}
        for k, t in self._timers.items():
            if t.count > 0:
                if mean:
                    aggregates["mean_%s_s" % k] = t.mean
                if last:
                    aggregates["last_%s_s" % k] = t.last
        return aggregates


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class AverageMeter:
    """Computes and stores the average and current value."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class AverageMeterCollection:
    """A grouping of AverageMeters."""

    def __init__(self):
        self._batch_count = 0
        self.n = 0
        self._meters = collections.defaultdict(AverageMeter)

    def update(self, metrics, n=1):
        self._batch_count += 1
        self.n += n
        for metric, value in metrics.items():
            self._meters[metric].update(value, n=n)

    def summary(self, sync_stats=False, dist_backend=None):
        """Returns a dict of average and most recent values for each metric."""
        stats = {BATCH_COUNT: self._batch_count, NUM_SAMPLES: self.n}
        for metric, meter in self._meters.items():
            if sync_stats:
                world_size = dist_backend.get_world_size()
                avg = torch.tensor(meter.avg)
                dist_backend.all_reduce(avg)
                last_val = torch.tensor(meter.val)
                dist_backend.all_reduce(last_val)
                avg = avg.item() / world_size
                last_val = last_val.item() / world_size
            else:
                avg = meter.avg
                last_val = meter.val
            stats[str(metric)] = avg
            stats["last_" + str(metric)] = last_val
        return stats


def check_for_failure(remote_values):
    """Checks remote values for any that returned and failed.

    Args:
        remote_values (list): List of object IDs representing functions
            that may fail in the middle of execution. For example, running
            a SGD training loop in multiple parallel actor calls.

    Returns:
        Bool for success in executing given remote tasks.
    """
    import ray
    from ray.exceptions import RayActorError

    unfinished = remote_values
    try:
        while len(unfinished) > 0:
            finished, unfinished = ray.wait(unfinished)
            finished = ray.get(finished)
        return True
    except RayActorError as exc:
        logger.exception(str(exc))
    return False


def override(interface_class):
    def overrider(method):
        invalidInputError(method.__name__ in dir(interface_class),
                          "method.__name__ doesn't exist in interface_class")
        return method

    return overrider


def get_filesystem(filepath):
    from fsspec.core import url_to_fs
    fs, _ = url_to_fs(str(filepath))
    return fs
