#!/usr/bin/env python

from operator import index
import os, sys

# [START analyticsadmin_properties_create]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin import Property
from google.analytics.admin import ListPropertiesRequest
from ga4_accounts import list_accounts


def list_properties(account_id):
    """
    Lists Google Analytics 4 properties under the specified parent account
    that are available to the current user.
    Args:
        account_id(str): The Google Analytics account ID.

    Returns:
        A list of dictionaries --> [{property_id:property_name},{property_id:property_name}]    
    """
    client = AnalyticsAdminServiceClient()
    results = client.list_properties(
        ListPropertiesRequest(filter=f"parent:accounts/{account_id}", show_deleted=True)
    )
    # print(results)

    properties_list = []
    for property in results:
        # print(property)
        property_id = property.name.split('/')
        # print(property.name, property.display_name)
        # properties_list.append(property_id[1])
        properties_list.append({property_id[1]:property.display_name})
    # print(properties_list)
    return properties_list

# [END analyticsadmin_properties_list]

# [start analyticsadmin_properties_list]
def get_property_name(property_id):
    """
    Retrieves the Google Analytics 4 Display Name details.
    Args:
        property_id(str): The Google Analytics Property ID.
    Return:
        display_name: The Google Analytics Property Display Name 
    """    
    client = AnalyticsAdminServiceClient()
    result = client.get_property(name=f"properties/{property_id}")

    return result.display_name


def create_property(account_id, property_name, property_type='PROPERTY_TYPE_UNSPECIFIED', currency_code ='EUR', time_zone ='Europe/Dublin', service_level='GOOGLE_ANALYTICS_360'):
    """This function creates a Google Analytics 4 (GA4) property. 
    And calls the next function to create a GA4 Web Data Stream

    Args:
    account_id: GA Account Id. first argument of the file.
    property_name: Name of the GA4 property. 2nd argument of the file.
    currency code: Currency of the property. 3rd argument of the file. Default = EUR
    time_zone: Time Zone. 4th argument of the file. Default Europe/Dublin.

    Attributes:
        property_type (google.analytics.admin_v1alpha.types.PropertyType):
            Immutable. The property type for this Property resource.
            When creating a property, if the type is
            "PROPERTY_TYPE_UNSPECIFIED", then "ORDINARY_PROPERTY" will
            be implied.
        property_name (str):
            Required. Human-readable display name for
            this property.
            The max allowed display name length is 100
            UTF-16 code units.
        time_zone (str):
            Required. Reporting Time Zone, used as the day boundary for
            reports, regardless of where the data originates. If the
            time zone honors DST, Analytics will automatically adjust
            for the changes.

            NOTE: Changing the time zone only affects data going
            forward, and is not applied retroactively.

            Format: https://www.iana.org/time-zones Example:
            "America/Los_Angeles".
        currency_code (str):
            The currency type used in reports involving monetary values.

            Format: https://en.wikipedia.org/wiki/ISO_4217 Examples:
            "USD", "EUR", "JPY".
        service_level (google.analytics.admin_v1alpha.types.ServiceLevel):
            Output only. The Google Analytics service
            level that applies to this property.
     


    Returns:
        Returns a tuple with the property Id and the property Name.
        (property_id, property_.display_name)
    """  

    # Get the authentication service object
    client = AnalyticsAdminServiceClient()
    property_ = client.create_property(
        property=Property(
            parent=f"accounts/{account_id}",
            property_type=property_type,
            currency_code=currency_code,
            display_name= property_name + " - GA4",
            industry_category="ARTS_AND_ENTERTAINMENT",
            time_zone=time_zone,
        )
    )

    property_id = property_.name.split('/')
    property_id = property_id[1]
    
    print("Property created")
    print("Property ID: ", property_id)
    print("Property Name: ", property_.display_name)

    property_response = (property_id, property_.display_name)

    return property_response

# [END analyticsadmin_properties_create]

# function to create a subproperty
def create_subproperty(parent_property_id, subproperty_name, time_zone="Europe/Dublin", currency_code="EUR"):
    """This function creates a Google Analytics 4 (GA4) subproperty. 
    And calls the next function to create a GA4 Web Data Stream

    Args:
    parent_property_id: GA Property Id. 
    subproperty_name: Name of the GA4 subproperty. 

    Returns:
        Returns a tuple with the subproperty Id and the subproperty Name.
        (subproperty_id, subproperty_.display_name)
    """  

    # Get the authentication service object
    client = AnalyticsAdminServiceClient()
    subproperty_ = client.create_subproperty({
        "parent":f"properties/{parent_property_id}",
        "subproperty":Property(
            display_name= subproperty_name,
            property_type="PROPERTY_TYPE_SUBPROPERTY",
            time_zone=time_zone,
            currency_code= currency_code,
            industry_category="ARTS_AND_ENTERTAINMENT",
        )
    })

    # subproperty_id = subproperty_.parent.split('/')
    # subproperty_id = subproperty_id[1]
    # subproperty_name = subproperty_.subproperty.display_name
    
    print("Subproperty created")
    print(subproperty_)

    response = subproperty_.subproperty
    print(f"Subproperty ID: {response.name}")
    print(f"Subproperty Name: {response.display_name}")
    print(f"Time Zone: {response.time_zone}")
    print(f"Currency Code: {response.currency_code}")

    return response

if __name__ == "__main__":
    # Load the Google Credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/davidpino/Documents/github/google_credentials_360.json"
