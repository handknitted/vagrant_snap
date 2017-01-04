#!/usr/bin/env python

# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2016 Intel Corporation
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

import logging
import threading

import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)


class SequenceGenerator(object):

    lock = threading.Lock()
    sequence_id = 0

    @staticmethod
    def get_sequence_id():
        try:
            SequenceGenerator.lock.acquire()
            SequenceGenerator.sequence_id += 1
            returnable_sequence_id = SequenceGenerator.sequence_id
            return returnable_sequence_id
        finally:
            SequenceGenerator.lock.release()


class Sequence(snap.Processor):
    """Tag
    Adds the tag 'sequence_num' to metrics.  The value is provided by a static
    counter.
    """

    def process(self, metrics, config):
        metric_sequence_id = SequenceGenerator.get_sequence_id()
        LOG.debug("Tagging sequence id %s" % metric_sequence_id)
        for metric in metrics:
            metric.tags["sequence-id"] = str(metric_sequence_id)
        return metrics

    def get_config_policy(self):
        """Get's the config policy
        The config policy for this plugin defines a string configuration item
        `instance-id` with the default value of `xyz-abc-qwerty`.
        """
        return snap.ConfigPolicy(
            [
                None,
                [
                    (
                        "sequence-id",
                        snap.StringRule(default='Unset')
                    )
                ]
            ]
        )

if __name__ == "__main__":
    plugin_name = "sequence-py"
    plugin_version = 1
    Sequence(plugin_name,
             plugin_version).start_plugin()
