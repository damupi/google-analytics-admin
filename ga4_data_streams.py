#!/usr/bin/env python

# Copyright 2021 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Analytics Admin API sample application which creates a data stream
for the Google Analytics 4 property.
See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.dataStreams/create
for more information.
"""
import os, sys

# [START analyticsadmin_properties_data_streams_create]
from google.analytics.admin import AnalyticsAdminServiceClient, Property
from google.analytics.admin import DataStream

def create_data_stream(pid, property_name):
    """Creates a data stream for the Google Analytics 4 property.

    Args:
      pid: Google Analytics property Id.
      path: GTM Container's API relative path.
      fingerprint: The fingerprint of the GTM Variable as computed at storage time. 
        Its values is modified after update.
      variable: variable object to be updated

    Returns:
      The created workspace.
    """

    client = AnalyticsAdminServiceClient()
    data_stream = DataStream(
        display_name=property_name + " - GA4",
        web_stream_data=DataStream.WebStreamData(default_uri="https://www."+ property_name),
    )
    data_stream.type_ = "WEB_DATA_STREAM"
    result = client.create_data_stream(
        parent=f"properties/{pid}", data_stream=data_stream,
    )
    stream_id = result.name.split("/")[-1]
    print(f"Data Stream Created:")
    print(f"Stream Id: {stream_id}")
    print(f"Display Name: {result.display_name}")
    print(f"{result.web_stream_data}")

    return
  # [END analyticsadmin_properties_data_streams_create]

def list_data_streams(property_id):
    """Lists data streams for the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    results = client.list_data_streams(parent=f"properties/{property_id}")

    # print("Result:")
    for data_stream in results:
        # print(data_stream)
        data_stream_id = data_stream.name.split('/')
        print(f"{data_stream_id[3]};{data_stream.web_stream_data.measurement_id};{data_stream.display_name}")
    return
# [END analyticsadmin_properties_data_streams_list]

if __name__ == "__main__":
    # Load the Google Credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../google_credentials.json"
