import json
import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()
base_url = os.environ.get("AF_BASE_URL")
api_key = os.environ.get("AF_API_KEY")

print(f'Base URL: {base_url}')

def get_custom_lists():
    url = f'{base_url}/api/Exec/custom-lists/{api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        print('Custom lists fetched successfully.')

        response_json = response.json()
        print('Response:', json.dumps(response_json, indent=4))

        return response_json
    else:
        print(f'Error fetching custom lists: {response.status_code}')
        sys.exit(1)


def find_custom_list_by_name(custom_lists, name):
    for custom_list in custom_lists:
        if custom_list.get('name') == name:
            print(f'FOUND: Custom list "{name}"')
            return custom_list
    return None


def create_custom_list_item(custom_list_id, properties_payload):
    url = f'{base_url}/api/Exec/custom-list-items/{api_key}'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'customListId': custom_list_id,
        'properties': properties_payload
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        print('Item created successfully.')

        response_json = response.json()
        print('Response:', json.dumps(response_json, indent=4))

        return response_json
    else:
        print(f'Error creating custom list item: {response.status_code}')
        print('Response:', response.text)
        sys.exit(1)


def update_custom_list_item(item_id, custom_list_id, properties_payload):
    url = f'{base_url}/api/Exec/custom-list-items/{api_key}'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'id': item_id,
        'customListId': custom_list_id,
        'properties': properties_payload
    }
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code in [200, 204]:
        print('Item updated successfully.')
    else:
        print(f'Error updating custom list item: {response.status_code}')
        print('Response:', response.text)
        sys.exit(1)


def prepare_properties(custom_list_properties, title_value):
    properties_payload = []
    title_property_id = None

    for prop in custom_list_properties:
        prop_label = prop.get('label', '').lower()
        prop_type = prop.get('type', '').lower()
        prop_id = prop.get('id')

        # Initialize the property payload
        property_payload = {'id': prop_id}

        if prop_label == 'title':
            title_property_id = prop_id
            if prop_type == 'string':
                property_payload['value'] = title_value
            elif prop_type == 'int':
                property_payload['value'] = int(title_value)
            else:
                # Handle other types if necessary
                property_payload['value'] = title_value
        else:
            # For other properties, set to default or empty values based on type. Handle as you see fit.
            if prop_type == 'string':
                property_payload['value'] = ''
            elif prop_type == 'int':
                property_payload['value'] = 0
            elif prop_type == 'boolean':
                property_payload['value'] = False
            elif prop_type in ['date', 'datetime']:
                property_payload['value'] = None
            elif prop_type in ['multiSelect', 'multiCheckbox']:
                property_payload['selectedIds'] = []
            else:
                property_payload['value'] = None

        properties_payload.append(property_payload)

    if not title_property_id:
        print('Title property not found in the custom list.')
        sys.exit(1)

    return properties_payload


def main():
    # Step 1: Get all custom lists
    custom_lists = get_custom_lists()

    # Step 2: Find the custom list with name "GDPR_en_Registry"
    custom_list = find_custom_list_by_name(custom_lists, 'GDPR_en_Registry')
    if not custom_list:
        print('Custom list "GDPR_en_Registry" not found.')
        sys.exit(1)

    custom_list_id = custom_list['id']
    custom_list_properties = custom_list.get('properties', [])

    # Step 3: Prepare properties payloads for two items
    properties_payload_item1 = prepare_properties(custom_list_properties, 'Item 1')
    properties_payload_item2 = prepare_properties(custom_list_properties, 'Item 2')

    # Step 4: Create the first item
    item1_id = create_custom_list_item(custom_list_id, properties_payload_item1)
    print(f'First item created with ID: {item1_id}')

    # Step 5: Create the second item
    item2_id = create_custom_list_item(custom_list_id, properties_payload_item2)
    print(f'Second item created with ID: {item2_id}')

    # Step 6: Update the first item
    # Let's change the title from "Item 1" to "Updated Item 1"
    updated_properties_payload = prepare_properties(custom_list_properties, 'Updated Item 1')

    # Update the item using PATCH
    update_custom_list_item(item1_id, custom_list_id, updated_properties_payload)

    print('Script completed successfully.')


if __name__ == '__main__':
    main()