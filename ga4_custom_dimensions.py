#!/usr/bin/env python
import os, sys
from urllib import response

from google.analytics.admin import AnalyticsAdminServiceClient
from googleapiclient.errors import HttpError
from google.analytics import admin
from oauth2client.client import AccessTokenRefreshError


def create_custom_dimension(property_id, parameter_name, scope = "EVENT"):
    # Get the authentication service object
    client = AnalyticsAdminServiceClient()
    parent=f"properties/{property_id}"

    # Initialize request argument(s)
    custom_dimension = admin.CustomDimension()
    custom_dimension.parameter_name = parameter_name
    custom_dimension.display_name = parameter_name
    custom_dimension.scope = scope

    response = client.create_custom_dimension(parent=parent, custom_dimension=custom_dimension)

    # Handle the response
    # print(response)
    if response.scope == 1:
        scope_value = "EVENT"
    elif response.scope == 2:
        scope_value = "USER"
    elif response.scope == 3:
        scope_value = "ITEM"
    else:
        scope_value = "DIMENSION_SCOPE_UNSPECIFIED"

    # print(f"Custom dimension {response.parameter_name} created. Scope: {scope_value}")
    print(f"Custom dimension '{response.parameter_name}' created. Pid: {property_id}. Scope: {scope_value}")

    return

if __name__ == "__main__":
    # Load the Google Credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../google_credentials.json"
    # properties = ["123456789"]

    # for property_id in properties:
    #     print(f"########## Start of {property_id} ##########")
    #     create_custom_dimension(property_id, "type", "EVENT")
    #     create_custom_dimension(property_id, "category", "EVENT")
    #     create_custom_dimension(property_id, "value", "EVENT")
    #     create_custom_dimension(property_id, "logged", "USER")
    #     create_custom_dimension(property_id, "color", "ITEM")
    #     print(f"########## End of {property_id} ##########")