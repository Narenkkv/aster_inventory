from django.db import models
from datetime import datetime

# Create your models here.

class ProductMaster(models.Model):
    productcode = models.CharField(db_column='ProductCode', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    productname = models.TextField(db_column='ProductName', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    productfullname = models.TextField(db_column='ProductFullName', db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.    
    purchaseunit = models.CharField(db_column='PurchaseUnit', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    purchasetax = models.CharField(db_column='PurchaseTax', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salesunit = models.CharField(db_column='SalesUnit', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase. 
    salestax = models.CharField(db_column='SalesTax', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.   

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

class StoreSalesData(models.Model):
    storeid = models.TextField(db_column='Storeid', blank=True, null=True)  # Field name made lowercase.
    storename = models.TextField(db_column='StoreName', blank=True, null=True)  # Field name made lowercase.
    billno = models.CharField(db_column='BillNo', primary_key=True, max_length=16)  # Field name made lowercase.
    billdate = models.TextField(db_column='BillDate', blank=True, null=True)  # Field name made lowercase.
    billtime = models.TextField(db_column='BillTime', blank=True, null=True)  # Field name made lowercase.
    custname = models.TextField(db_column='CustName', blank=True, null=True)  # Field name made lowercase.
    mobilenum = models.CharField(db_column='MobileNum', blank=True, null=True,max_length=20)  # Field name made lowercase.
    affname = models.TextField(db_column='AffName', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    salesman = models.TextField(db_column='Salesman', blank=True, null=True)  # Field name made lowercase.
    transactiontype = models.TextField(db_column='TransactionType', blank=True, null=True)  # Field name made lowercase.
    doctor = models.TextField(db_column='Doctor', blank=True, null=True)  # Field name made lowercase.
    homedelivery = models.TextField(db_column='HomeDelivery', blank=True, null=True)  # Field name made lowercase.
    deliverdby = models.TextField(db_column='DeliverdBy', blank=True, null=True)  # Field name made lowercase.
    qty = models.TextField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    value = models.TextField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    gsv = models.TextField(db_column='GSV', blank=True, null=True)  # Field name made lowercase.
    itemdisc = models.TextField(db_column='ItemDisc', blank=True, null=True)  # Field name made lowercase.
    billdisc = models.TextField(db_column='BillDisc', blank=True, null=True)  # Field name made lowercase.
    totaldisccount = models.TextField(db_column='TotalDisccount', blank=True, null=True)  # Field name made lowercase.
    slab = models.TextField(db_column='Slab', blank=True, null=True)  # Field name made lowercase.
    basketsize = models.TextField(db_column='BasketSize', blank=True, null=True)  # Field name made lowercase.
    marginwotax = models.TextField(db_column='MarginWOtax', blank=True, null=True)  # Field name made lowercase.
    marginwtax = models.TextField(db_column='MarginWtax', blank=True, null=True)  # Field name made lowercase.
    cash = models.TextField(db_column='Cash', blank=True, null=True)  # Field name made lowercase.
    paytm = models.TextField(db_column='Paytm', blank=True, null=True)  # Field name made lowercase.
    paytmrecon = models.TextField(db_column='PaytmRecon', blank=True, null=True)  # Field name made lowercase.
    ezetap_card = models.TextField(db_column='Ezetap_Card', blank=True, null=True)  # Field name made lowercase.
    ezetap_cardrecon = models.TextField(db_column='Ezetap_CardRecon', blank=True, null=True)  # Field name made lowercase.
    ezetap_upi = models.TextField(db_column='Ezetap_UPI', blank=True, null=True)  # Field name made lowercase.
    ezetap_upirecon = models.TextField(db_column='Ezetap_UPIRecon', blank=True, null=True)  # Field name made lowercase.
    creditnote = models.TextField(db_column='CreditNote', blank=True, null=True)  # Field name made lowercase.
    totalvalue = models.TextField(db_column='TotalValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'store_sales_data'