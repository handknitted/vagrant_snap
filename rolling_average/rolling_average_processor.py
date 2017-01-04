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
import time

import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)


class RollingAverage(snap.Processor):
    """
    Calculates a rolling average of the metrics and publishes this
    """
    metrics_buffer = {}

    def process(self, metrics, config):
        for metric in metrics:
            self.rotate_buffer(metric, config)
        return self.generate_averages(config)

    def generate_averages(self, config):
        average_metrics = []
        for namespace_key, metric_list in self.metrics_buffer.iteritems():
            count = len(metric_list)
            if count > 0:
                # raise Exception("Processing metric %s" % namespace_key)
                total_value = sum([metric.data
                                   for metric in metric_list])
                average_value = total_value / count
                average_metric = self.duplicate_metric(
                    metric_list[-1], config)
                average_metric.data = str(average_value)
                average_metrics.append(average_metric)
        return average_metrics

    def duplicate_metric(self, seed_metric, config):
        now = time.time()
        duplicated_metric = snap.metric.Metric(
            namespace=[element for element in seed_metric.namespace],
            version=seed_metric.version,
            # tags=[tag for tag in seed_metric.tags], TODO - this fails with "TypeError: The 'tags' kwarg requires a dict of strings. (given: `<class 'google.protobuf.internal.containers.ScalarMap'>`)"
            config=seed_metric.config,
            timestamp=now,
            unit=seed_metric.unit,
            description=seed_metric.description
        )
        # duplicated_metric.timestamp(seed_metric.timestamp)
        duplicated_metric.namespace.add_static_element(
            config['average-suffix'])
        return duplicated_metric

    def concatenate_namespace(self, namespace):
        concat_value = ''
        for namespace_element in namespace:
            concat_value += namespace_element.value
        return concat_value

    def rotate_buffer(self, metric, config):
        namespace_key = self.concatenate_namespace(metric.namespace)
        namespaced_buffer = self.metrics_buffer.get(namespace_key, [])
        namespaced_buffer = namespaced_buffer[:4]
        namespaced_buffer.append(metric)
        self.metrics_buffer[namespace_key] = namespaced_buffer

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
                        "average-suffix",
                        snap.StringRule(default='average')
                    ),
                    (
                        "buffer-length",
                        snap.IntegerRule(default='10')
                    )
                ]
            ]
        )

if __name__ == "__main__":
    plugin_name = "rolling-average"
    plugin_version = 1
    RollingAverage(plugin_name,
             plugin_version).start_plugin()


# example = [
#     {"timestamp": "2017-01-04T09:59:09.006637096Z", "namespace": "/intel/psutil/load/load1", "data": 0.09, "unit": "",
#      "tags": {"plugin_running_on": "pukka", "sequence-id": "4031"}, "version": 0,
#      "last_advertised_time": "2017-01-04T11:06:46.124337372Z"},
#     {"timestamp": "2017-01-04T09:59:09.006637096Z", "namespace": "/intel/psutil/load/load5", "data": 0.08, "unit": "",
#      "tags": {"plugin_running_on": "pukka", "sequence-id": "4031"}, "version": 0,
#      "last_advertised_time": "2017-01-04T11:06:46.12433803Z"},
#     {"timestamp": "2017-01-04T09:59:09.006637096Z", "namespace": "/intel/psutil/load/load15", "data": 0.01, "unit": "",
#      "tags": {"plugin_running_on": "pukka", "sequence-id": "4031"}, "version": 0,
#      "last_advertised_time": "2017-01-04T11:06:46.12433849Z"},
#     {"timestamp": "2017-01-04T09:59:09.006637096Z", "namespace": "/intel/psutil/cpu/cpu-total/user", "data": 69.57,
#      "unit": "", "tags": {"plugin_running_on": "pukka", "sequence-id": "4031"}, "version": 0,
#      "last_advertised_time": "2017-01-04T11:06:46.124338965Z"},
#     {"timestamp": "2017-01-04T09:59:09.006637096Z", "namespace": "/intel/psutil/cpu/cpu-total/idle", "data": 20103.42,
#      "unit": "", "tags": {"plugin_running_on": "pukka", "sequence-id": "4031"}, "version": 0,
#      "last_advertised_time": "2017-01-04T11:06:46.124339437Z"},
#     {"timestamp": "2017-01-04T09:59:09.006637096Z", "namespace": "/intel/psutil/cpu/cpu-total/system", "data": 33.51,
#      "unit": "", "tags": {"plugin_running_on": "pukka", "sequence-id": "4031"}, "version": 0,
#      "last_advertised_time": "2017-01-04T11:06:46.124339892Z"}]
#