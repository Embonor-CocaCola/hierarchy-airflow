import simplejson as json

from base.utils.pandas import null_safe


def product_row_to_db_record(row, **kwargs):
    return (
        row['ProductId'],
        json.dumps({
            'ban': null_safe(row['Ban']),
            'sku': null_safe(row['SKU']),
            'upc': null_safe(row['UPC']),
            'name': null_safe(row['ProductName']),
            'short_name': null_safe(row['ShortName']),
            'client_code': null_safe(row['ClientCode']),
            'manufacturer': null_safe(row['Manufacturer']),
            'brand_name': null_safe(row['BrandName']),
            'sub_brand_name': null_safe(row['SubBrandName']),
            'product_uid': null_safe(row['ProductUID']),
            'product_distribution_identifier': null_safe(row['ProductDistributionIdentifier']),
            'label_name': null_safe(row['LabelName']),
            'country_code': null_safe(row['CountryCode']),
            'cc_id': null_safe(row['CCId']),
            'pim_id': null_safe(row['PIMId']),
            'bar_code': null_safe(row['Barcode']),
            'article_code': null_safe(row['ArticleCode']),
            'third_party_product': null_safe(row['ThirdPartyProduct']),
            'thumbnail_url': null_safe(row['ThumbnailUrl']),
        }),
        json.dumps({
            'packaging_type': null_safe(row['PackagingType']),
            'package_type': null_safe(row['PackageType']),
            'measurement_unit': null_safe(row['MeasurementUnit']),
            'selling_pack_type': null_safe(row['SellingPackType']),
            'selling_pack_size': null_safe(row['SellingPackSize']),
            'normalize_packaging_size': null_safe(row['NormalizePackagingSize']),
            'selling_pack_front_facings': null_safe(row['SellingPackFrontFacings']),
            'selling_pack_side_facings': null_safe(row['SellingPackSideFacings']),
            'package_size': null_safe(row['PackageSize']),
            'sales_unit': null_safe(row['SalesUnit']),
        }),
        json.dumps({
            'category': null_safe(row['ProductCategory']),
            'category_code': null_safe(row['ProductCategoryCode']),
            'beverage_type': null_safe(row['BeverageType']),
            'flavour_name': null_safe(row['FlavourName']),
            'local_category_name': null_safe(row['LocalProductCategoryName']),
            'local_sub_category_name': null_safe(row['ProductLocalSubCategoryName']),
            'local_sub_category_code': null_safe(row['ProductLocalSubCategoryCode']),
            'group': null_safe(row['ProductGroup']),
            'price': null_safe(row['Price']),
            'currency_name': null_safe(row['CurrencyName']),
            'type': null_safe(row['Type']),
            'sweetener_type': null_safe(row['SweetnerType']),
            'serving_type': null_safe(row['ServingType']),
        }),
        json.dumps({
            'is_foreign': null_safe(row['IsForeign']),
            'is_unknown': null_safe(row['IsUnknown']),
            'is_trained': null_safe(row['IsTrained']),
            'is_flagged': null_safe(row['IsFlagged']),
            'is_competitor': null_safe(row['IsCompetitor']),
            're_sku_code': null_safe(row['RESkuCode']),
            'is_active': null_safe(row['IsActive']),
            'sku_last_seen': null_safe(row['SKULastSeen']),
            're_id': null_safe(row['REId']),
        }),
        null_safe(row['CreatedByUserId']),
        null_safe(row['CreatedOn']),
        null_safe(row['ModifiedByUserId']),
        null_safe(row['ModifiedOn']),
        null_safe(row['SKU']) and int(row['SKU']),
        null_safe(row['ProductName']),
        null_safe(row['ProductGroup']),
        null_safe(row['ProductCategory']),
        null_safe(row['LocalProductCategoryName']),
        null_safe(row['IsForeign']),
        null_safe(row['FlavourName']),
        null_safe(row['Manufacturer']),
    )
