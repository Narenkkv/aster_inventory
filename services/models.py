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

    class Meta:
        managed = False
        db_table = 'product_master'
    

class Usermaster(models.Model):
    user_code = models.TextField(primary_key=True, blank=True, null=False)
    name = models.TextField()
    password = models.TextField()
    date_of_creation = models.DateTimeField(blank=True, null=True)
    created_user = models.TextField(blank=True, null=True)
    isdownload = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'usermaster'


class ProductDetail(models.Model):
    item_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    item_name = models.CharField(max_length=500, blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    qty = models.TextField(blank=True, null=True)  # This field type is a guess.
    mrp = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_detail'