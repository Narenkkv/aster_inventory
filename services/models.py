from django.db import models
from datetime import datetime

# Create your models here.

class ProductMaster(models.Model):
    item_number = models.CharField(db_column='Item_number', primary_key=True, max_length=10, blank=True, null=False)  # Field name made lowercase.
    product_name = models.CharField(db_column='Product_name', max_length=500)  # Field name made lowercase.
    search_name = models.CharField(db_column='Search_name', max_length=600, blank=True, null=True,db_index=True)  # Field name made lowercase.
    item_reference = models.CharField(db_column='Item_reference', max_length=400, blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=300, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=30, blank=True, null=True)  # Field name made lowercase.
    item_group = models.CharField(db_column='Item_group', max_length=100, blank=True, null=True)  # Field name made lowercase.
    is_purchasse_b = models.CharField(db_column='IS_Purchasse_B', max_length=10, blank=True, null=True)  # Field name made lowercase.
    one_mdm_code = models.CharField(db_column='One_MDM_Code', max_length=400, blank=True, null=True)  # Field name made lowercase.
    is_sale_blocked = models.CharField(db_column='Is_Sale_Blocked', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ctg8 = models.CharField(db_column='CTG8', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ka_mdm = models.CharField(db_column='KA_MDM', max_length=400, blank=True, null=True)  # Field name made lowercase.
    kl_mdm = models.CharField(db_column='KL_MDM', max_length=400, blank=True, null=True)  # Field name made lowercase.
    tl_mdm = models.CharField(db_column='TL_MDM', max_length=400, blank=True, null=True)  # Field name made lowercase.
    pack_size = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_master'
    

class Usermaster(models.Model):
    user_code = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    date_of_creation = models.DateTimeField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    isdownload = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_master'


class ProductDetail(models.Model):
    store_id = models.CharField(max_length=50)
    item_code = models.CharField(max_length=10, blank=True, null=True)
    item_name = models.CharField(max_length=500, blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    mrp = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_created = models.DateTimeField(blank=True, null=True)
    rack_no = models.CharField(max_length=100, blank=True, null=True)
    exp_date = models.CharField(max_length=8, blank=True, null=True)
    pack_size = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'product_detail'

class StoreMaster(models.Model):
    store_code = models.CharField(db_column='Store_Code', primary_key=True, max_length=50)  # Field name made lowercase.
    email_id = models.CharField(db_column='Email_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    short_name = models.CharField(db_column='Short_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    zip_code = models.CharField(db_column='Zip_Code', max_length=7, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=100, blank=True, null=True)  # Field name made lowercase.
    d_365_store_id = models.CharField(db_column='D_365_Store_Id', max_length=100, blank=True, null=True)  # Field name made lowercase.
    store_name_as_per_d_365 = models.CharField(db_column='Store_Name_As_per_D_365', max_length=100, blank=True, null=True)  # Field name made lowercase.
    store_state = models.CharField(max_length=200, blank=True, null=True)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Store_master'

class ProductBarcodeMaster(models.Model):
    itemnumber = models.CharField(db_column='ITEMNUMBER', max_length=10)  # Field name made lowercase.
    productquantityunitsymbol = models.CharField(db_column='PRODUCTQUANTITYUNITSYMBOL', max_length=10,  blank=True, null=True)  # Field name made lowercase.
    barcodesetupid = models.CharField(db_column='BARCODESETUPID', max_length=10,  blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='BARCODE', max_length=100,  blank=True, null=True)  # Field name made lowercase.
    isdefaultdisplayedbarcode = models.CharField(db_column='ISDEFAULTDISPLAYEDBARCODE', max_length=10,  blank=True, null=True)  # Field name made lowercase.
    isdefaultprintedbarcode = models.CharField(db_column='ISDEFAULTPRINTEDBARCODE', max_length=10,  blank=True, null=True)  # Field name made lowercase.
    isdefaultscannedbarcode = models.CharField(db_column='ISDEFAULTSCANNEDBARCODE', max_length=50,  blank=True, null=True)  # Field name made lowercase.
    productdescription = models.CharField(db_column='PRODUCTDESCRIPTION', max_length=500,  blank=True, null=True)  # Field name made lowercase.
    productquantity = models.CharField(db_column='PRODUCTQUANTITY', max_length=10,  blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_barcode_master'

class EnteroItemLists(models.Model):
    entity_name = models.CharField(db_column='Entity_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sku_code = models.CharField(db_column='SKU_Code', max_length=11, blank=True, null=True)  # Field name made lowercase.
    sku_name = models.CharField(db_column='SKU_Name', max_length=500, blank=True, null=True)  # Field name made lowercase.
    batch_expiry_date = models.DateField(blank=True, null=True)
    batch_no = models.CharField(db_column='Batch_No', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qty_sold = models.FloatField(db_column='Qty_Sold', blank=True, null=True)  # Field name made lowercase.
    pts = models.DecimalField(db_column='PTS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mrp = models.DecimalField(db_column='MRP', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    vl_mrp = models.DecimalField(db_column='Vl_Mrp', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mdm = models.CharField(db_column='MDM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(max_length=100, blank=True, null=True)
    karnataka = models.IntegerField(blank=True, null=True)
    kerala = models.IntegerField(blank=True, null=True)
    telangana = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entero_item_lists'


class SupplierReturnItem(models.Model):
    store_id = models.CharField(max_length=50)
    item_code = models.CharField(max_length=10)
    item_name = models.CharField(max_length=500)
    batch_no = models.CharField(max_length=100)
    date_of_expiry = models.DateField()
    vendor_name = models.CharField(max_length=500)
    accepted_qty = models.DecimalField(max_digits=10, decimal_places=0)
    created_by = models.CharField(max_length=200)
    date_of_creation = models.DateTimeField()
    return_qty = models.DecimalField(max_digits=10, decimal_places=0)
    remaining_qty = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    productdetail_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supplier_return_item'

class StoreExpiryProductDetail(models.Model):
    store_id = models.CharField(max_length=50)
    item_code = models.CharField(max_length=10, blank=True, null=True)
    item_name = models.CharField(max_length=500, blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    mrp = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_created = models.DateTimeField(blank=True, null=True)
    rack_no = models.CharField(max_length=100, blank=True, null=True)
    exp_date = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_expiry_product_detail'

class ItemMaster(models.Model):
    aster_code = models.CharField(db_column='Aster_Code', primary_key=True, max_length=50)  # Field name made lowercase.
    product_form = models.CharField(db_column='Product_Form', max_length=50)  # Field name made lowercase.
    product_name = models.CharField(db_column='Product_name', max_length=600)  # Field name made lowercase.
    ean_upc = models.CharField(db_column='EAN_UPC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    product_type = models.CharField(db_column='Product_type', max_length=50)  # Field name made lowercase.
    sales_unit = models.CharField(db_column='Sales_Unit', max_length=10)  # Field name made lowercase.
    unique_key = models.CharField(max_length=700, blank=True, null=True)
    display_name = models.CharField(max_length=900, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_master'

class ProductNameList(models.Model):
    product_name = models.CharField(max_length=600)

    class Meta:
        managed = False
        db_table = 'product_name_list'

class BarcodeUpdate(models.Model):
    aster_code = models.CharField(max_length=50)
    item_name = models.CharField(max_length=700)
    bar_code = models.CharField(max_length=60, blank=True, null=True)
    created_user = models.CharField(max_length=60)
    date_of_creation = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'barcode_update'