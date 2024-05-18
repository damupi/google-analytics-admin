#!/usr/bin/env python3

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

import os, sys

from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin import ConversionEvent

# [START analyticsadmin_properties_web_data_streams_create]

def create_conversion_event(property_id, event_name ="generate_lead", counting_method="ONCE_PER_EVENT"):
    """Creates a conversion event for the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    conversion_event = client.create_conversion_event(
        parent=f"properties/{property_id}",
        conversion_event=ConversionEvent(event_name=event_name, counting_method=counting_method),
    )

    # print("Conversion Result:")
    print(f"Conversion event {conversion_event.event_name} created at {conversion_event.create_time}")

    return

# [END analyticsadmin_properties_conversion_events_create]

if __name__ == "__main__":
    # Load the Google Credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../google_credentials.json"
    # properties = ["314443512"]
    # for property_id in properties:
    #     print(f"####### Start of {property_id} #######")
    #     create_conversion_event(property_id, 'generate_lead')
    #     create_conversion_event(property_id, 'generate_lead_goal', 'ONCE_PER_SESSION')
    #     print(f"####### End of {property_id} #######")