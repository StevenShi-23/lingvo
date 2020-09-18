# Lint as: python3
# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""Tests for datasets."""

from lingvo import datasets
import lingvo.compat as tf
from lingvo.core import test_utils


class DatasetsTest(test_utils.TestCase):

  def testGetDatasetsFindsAllPublicMethods(self):

    class DummyDatasetHolder:

      def Train(self):
        pass

      def UnexpectedDatasetName(self):
        pass

    found_datasets = datasets.GetDatasets(DummyDatasetHolder)

    self.assertAllEqual(['Train', 'UnexpectedDatasetName'], found_datasets)

  def testGetDatasetsRaisesErrorOnInvalidDatasets(self):

    class DummyDatasetHolder:

      def Train(self):
        pass

      def BadDataset(self, any_argument):
        pass

    with self.assertRaises(datasets.DatasetFunctionError):
      datasets.GetDatasets(DummyDatasetHolder, warn_on_error=False)

  def testGetDatasetsWarnsOnError(self):

    class DummyDatasetHolder:

      def Train(self):
        pass

      def BadDataset(self, any_argument):
        pass

    with self.assertLogs() as assert_log:
      found_datasets = datasets.GetDatasets(
          DummyDatasetHolder, warn_on_error=True)
      self.assertAllEqual(['Train'], found_datasets)
    self.assertIn('WARNING:absl:Found a public function BadDataset',
                  assert_log.output[0])


if __name__ == '__main__':
  tf.test.main()
