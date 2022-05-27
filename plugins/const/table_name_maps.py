original_table_name_to_new_name_map = {
    'answers': 'answer',
    'BranchOffices': 'branch_office',
    'ChiefsPlants': 'chief_plant',
    'Customers': 'customer',
    'Plants': 'plant',
    'questions': 'question',
    'SupervisorsPlants': 'supervisor_plant',
    'surveys': 'survey',
    'Vendors': 'vendor',
    'VendorsCustomers': 'vendor_customer',
    'VendorsPlants': 'vendor_plant',
    'VendorTypes': 'vendor_type',
    'Dictionary': 'dictionary',
    'SuccessPhotoProduct': 'success_photo_product',
    'missing_hierarchy': 'missing_hierarchy',
}

table_name_to_columns = {
    'survey': {
        'raw': ['source_id', 'paused', 'name'],
    },
}
