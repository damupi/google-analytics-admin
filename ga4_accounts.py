#!/usr/bin/env python3

import os, sys

# [START analyticsadmin_properties_create]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin import Property

def list_accounts():
    """"Lists the Google Analytics accounts available to the current user.

    Args:
        No args

    Returns:
        A list of dictionaries with key/value = account_id/account_name.
    """

    client = AnalyticsAdminServiceClient()
    results = client.list_accounts()

    # print("Result:")
    # print(results)
    accounts_list = []
    for account in results:
        account_id = account.name.split('/')
        accounts_list.append({account_id[1]:account.display_name})

    # print(accounts_list)
    return accounts_list

# [END analyticsadmin_accounts_list]

if __name__ == "__main__":
    # Load the Google Credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../google_credentials.json"
    list_accounts()
