#!/usr/bin/env python3

import os, sys

from google.analytics.admin import AnalyticsAdminServiceClient
from ga4_accounts import list_accounts
from ga4_properties import create_property
from ga4_data_streams import create_data_stream
from ga4_custom_dimensions import create_custom_dimension
from ga4_conversions import create_conversion_event


if __name__ == "__main__":
    # Load the Google Credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../google_credentials.json"
    # Get the GA Account Ids and GA Account Names in case the user does not write the id
    accounts = list_accounts()
    account_ids = []
    for account in accounts:
        for key in account.keys():
            account_ids.append(key)
 
    # Print the GA Account Id and its name in case is not declared
    if len(sys.argv) == 1:
        for item in accounts:
            for key, value in item.items():
                print(f'{value} --> {key}')
        print('The first argument must be a GA Account Id. (ex. 314443512)')
        raise Exception('GA Account Id missed. (ex. python3 ga4_create_website.py 314443512)')
    # Check if the GA Account Id given is correct 
    # (the service account has permissions and is well written)
    if sys.argv[1] in account_ids:
        ga_account_id = sys.argv[1]
    else:
        raise Exception('The GA Account Id doesn\'t exits \n\
            or the service account credentials has no permissions \n\
            to write on that GA Account')

    ga_account_id = int(ga_account_id)    
    
    # Check if GA Property Name is declared
    if len(sys.argv) == 2:
        raise Exception('Specify at least a second argument with a GA Property Name. (ex. python3 ga4_create_website.py 314443512 my-domain.com)')
    # Check if GA Property Name is string
    if isinstance(sys.argv[2], str) == False:
        raise Exception('Specify at least a second argument with a GA Property Name. (ex. python3 ga4_create_website.py 314443512 my-domain.com)')
    property_name = sys.argv[2]
    
    # In case no property type is written in the prompt will take PROPERTY_TYPE_ORDINARY as default
    if len(sys.argv) > 3:
        property_type = sys.argv[4]
    else:
        property_type = "PROPERTY_TYPE_UNSPECIFIED"

    # In case no no Currency is written in the prompt will take EUR as default
    if len(sys.argv) > 4:
        currency_code = sys.argv[5]
    else:
        currency_code = "EUR"

    # In case no no Time Zone is written in the prompt will take Europe/Dublin as default
    if len(sys.argv) > 5:
        time_zone = sys.argv[6]
    else:
        time_zone = "Europe/Dublin"


    # create_property("127830174", "BonusFinder Mexico"
    
    # Create property that returns a list: (property_id, property_name)
    property_response = create_property(ga_account_id, property_name, property_type, currency_code, time_zone)
    print("----------------")
    property_id = property_response[0]

    # Create a Web DataStream
    ds_response = create_data_stream(property_id, property_name)
    print("----------------")

    # Create conversions
    create_conversion_event(property_id, 'generate_lead')
    create_conversion_event(property_id, 'generate_lead_goal', 'ONCE_PER_SESSION')
    print("----------------")
    
    # Create custom dimension
    create_custom_dimension(property_id, "category", "EVENT")
    create_custom_dimension(property_id, "type", "EVENT")
    create_custom_dimension(property_id, "value", "EVENT")
    create_custom_dimension(property_id, "logged", "USER")
    create_custom_dimension(property_id, "color", "ITEM")

    # "session_id" is reserved
    # create_custom_dimension(property_id, "session_id", "USER") 
    print("----------------")

        
