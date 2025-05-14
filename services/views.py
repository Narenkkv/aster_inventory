from django.shortcuts import render,redirect
from services.models import *
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import smart_str
from django.db.models import Q, F, Func, Value,Case,When,IntegerField
from  django.db.models.functions import Upper
from django.db import transaction
import pandas as pd
import pyodbc
import os
import sqlite3
import json
import io
import pytz
# Create your views here.


def index(request):
    try:
        if request.method == "POST" and 'login' in request.POST:
            username = request.POST['username'].lower()
            password = request.POST['pass'].lower()
            storeid = request.POST.get('store_name')
            rackNo = request.POST['rackno']
            if storeid:
                request.session['storeid'] = storeid
            request.session['rackNo'] = rackNo
            userNameCheck = Usermaster.objects.filter(name=username).all()
            if not userNameCheck:
                messages.error(request,'Invalid User Name !...')
                return redirect('index')
            else:
                passwordCheck = Usermaster.objects.filter(password=password).all()
                if not passwordCheck:
                    messages.error(request,'Incorrect Password !...')
                    return redirect('index')
                else:
                    request.session['username'] = username
                    username =  Usermaster.objects.filter(name=username).get()
                    if username.isdownload == 1:
                        return redirect('download_data')
                    elif username.isdownload == 2:
                        return redirect('store_expiry_data_entry')
                    elif username.isdownload == 3:
                        return redirect('expirydownload_data')
                    else:
                        return redirect('productentry')
        return render(request, 'login/index.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')

def productentry(request):
    try:
        if request.method == "POST": 
            if 'recordsave' in request.POST:
                with transaction.atomic():
                    product_code = request.POST['item_name']
                    packsize = request.POST['packsize']
                    batch = request.POST['batch'].upper()
                    qty = request.POST['qty']
                    mrp = request.POST['mrp']
                    expMonth = request.POST['expMonth']
                    expYear = request.POST['expYear']
                    prodName = ItemMaster.objects.get(aster_code = product_code)
                    ProductDetail.objects.create(
                        store_id = request.session['storeid'],
                        item_code = product_code,
                        item_name = prodName.product_name,
                        batch = batch,
                        qty = qty,
                        mrp = mrp,
                        user_name = request.session['username'],
                        date_of_created = datetime.now(),
                        rack_no = request.session['rackNo'],
                        exp_date = expMonth+'-'+expYear,
                        pack_size = packsize
                    )
                return redirect('productentry')
        return render(request, 'productEntry.html')
    except Exception as e:
        print(e)
        messages.error(request,e)
        return render(request, 'login/index.html')


def productlist(request, search):
    try:
        result = []
        if search == '-':
            data = ItemMaster.objects.all().order_by('aster_code')[:50]
        else:
            search_terms = search.split()  # Split search query into words
            query = Q()
            for term in search_terms:
                query &= Q(product_name__icontains=term)  # Apply AND condition for all terms
            data = ItemMaster.objects.filter(query).order_by('aster_code')[:50]
        for i in data:
            result.append({
                'item_code': i.aster_code,
                'item_name': i.display_name
            })
        return JsonResponse(result, safe=False)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'errorMsg': str(e)}), 500)
   
def download_data(request):
    try:
        if request.method == "POST" and 'downloadrecord' in request.POST:
            fromDate = request.POST['fromdate']
            toDate = request.POST['todate']
            checkboxStatus = request.POST.get('allstore')
            connection_string = ('DRIVER={ODBC Driver 17 for SQL Server};'
                            f"SERVER={os.environ["HOST"]};"
                            f"DATABASE={os.environ["DB_NAME"]};"
                            f"UID={os.environ["DB_USER"]};"
                            f"PWD={os.environ["DB_PASSWORD"]};")
            conn = pyodbc.connect(connection_string)
            if checkboxStatus is None:
                storeCodeList  = request.POST.getlist('storeName')
                storeCode = storeCodeList[0] if storeCodeList else None
                query = """
                SELECT id, store_id, item_code, 
                       item_name + '_' + pack_size AS item_name, 
                       CAST(batch AS NVARCHAR) AS batch, 
                       qty, mrp, user_name, 
                       date_of_created, rack_no, 
                        '01'+'-'+exp_date as exp_date, pack_size
                FROM product_detail
                WHERE CAST(date_of_created AS DATE) BETWEEN ? AND ? AND store_id = ?
                """
                data = pd.read_sql_query(query, conn, params=(fromDate, toDate,storeCode))
            else:
                query = """
                SELECT id, store_id, item_code, 
                       item_name + '_' + pack_size AS item_name, 
                       CAST(batch AS NVARCHAR) AS batch, 
                       qty, mrp, user_name, 
                       date_of_created, rack_no, 
                        '01'+'-'+exp_date as exp_date, pack_size
                FROM product_detail
                WHERE CAST(date_of_created AS DATE) BETWEEN ? AND ?
                """
                data = pd.read_sql_query(query, conn, params=(fromDate, toDate))

            # Convert batch column to string explicitly
            data['batch'] = data['batch'].astype(str)
            data['exp_date'] = data['exp_date'].astype(str)

            # Convert date_of_created from UTC to IST (UTC+5:30)
            utc_zone = pytz.utc
            ist_zone = pytz.timezone('Asia/Kolkata')

            data['date_of_created'] = pd.to_datetime(data['date_of_created'], utc=True)
            data['date_of_created'] = data['date_of_created'].dt.tz_convert(ist_zone)
            data['date_of_created'] = data['date_of_created'].dt.strftime('%Y-%m-%d %H:%M:%S')  # Format as string

            # Prepare Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, sheet_name='Audit_Data', index=False)

                # Get the workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Audit_Data']

                # Define text format for batch column
                text_format = workbook.add_format({'num_format': '@'})  # '@' forces text format
                batch_column_index = data.columns.get_loc("batch")  # Get the index of batch column

                # Apply format to the entire column
                worksheet.set_column(batch_column_index, batch_column_index, None, text_format)

                # for expiry date
                text_format = workbook.add_format({'num_format': '@'})  # '@' forces text format
                expiry_column_index = data.columns.get_loc("exp_date")  # Get the index of batch column

                # Apply format to the entire column
                worksheet.set_column(expiry_column_index, expiry_column_index, None, text_format)

            output.seek(0)
            response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={smart_str("Audit_Data_" + fromDate + '_'+ toDate + ".xlsx")}'

            conn.close()
            return response
        return render(request, 'download_data.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')

    
def storelist(request,search):
    try:
        result = []
        if search == "-":
            data = StoreMaster.objects.filter(active = 1).all().order_by('d_365_store_id')[:50]
            for i in data:
                res={
                    'store_code':i.d_365_store_id,
                    'store_name':i.d_365_store_id+'_'+i.store_name_as_per_d_365
                }
                result.append(res)
        else:   
            data = StoreMaster.objects.filter(Q(short_name__icontains=search) | Q(d_365_store_id__icontains=search),active = 1).all().order_by('d_365_store_id')[:50]
            for i in data:
                res = {
                    'store_code':i.d_365_store_id,
                    'store_name':i.d_365_store_id+'_'+i.short_name
                }
                result.append(res)
        return JsonResponse(result,safe = False)
    except Exception as e:  
        print(e)
        return HttpResponse(json.dumps({'errorMsg': str(e)}), 500)  
    
def logout(request):
    try:
        if 'username' in request.session:
            del request.session['username']
            del request.session['rackNo']
        if 'storeid' in request.session:
            del request.session['storeid']
        return redirect('index')
    except Exception as e:
        print(e)
        return redirect('index')
    
def scanbarcode(request):
    if request.method == "POST":
        try:
            barCode = request.POST.get('barcode')
            product = ItemMaster.objects.filter(ean_upc=barCode).first()
            if product:
                return JsonResponse({
                    'success': True,
                    'product': {'ids': product.aster_code, 'name': product.product_name}
                })
            else:
                return JsonResponse({'success': False, 'error': 'Product not found.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def store_expiry_report_download_data(request):
    try:
        if request.method == "POST" and 'storedownloadrecord' in request.POST:
            fromDate = request.POST['fromdate']
            toDate = request.POST['todate']
            connection_string = ('DRIVER={ODBC Driver 17 for SQL Server};'
                        f"SERVER={os.environ["HOST"]};"
                        f"DATABASE={os.environ["DB_NAME"]};"
                        f"UID={os.environ["DB_USER"]};"
                        f"PWD={os.environ["DB_PASSWORD"]};")
            conn = pyodbc.connect(connection_string)
            query = """
                SELECT a.store_id as Store_Code ,a.item_code as Item_code,a.item_name as Item_Name,a.batch as Batch,a.qty as Return_Qty,a.mrp as Mrp,b.vendor_name,c.store_state as Store_State 
                FROM  store_expiry_product_detail a  left join  supplier_return_item b
                    ON a.store_id = b.store_id AND a.item_code = b.item_code AND a.batch = b.batch_no AND a.id = b.productdetail_id
                    LEFT JOIN store_master c ON a.store_id = c.D_365_Store_Id
                            WHERE CAST(a.date_of_created AS DATE) BETWEEN ? AND ? and b.store_id = ?
                """
            print(query)
            filename = f'Expiry_Data_{fromDate}_{toDate}'
            data = pd.read_sql_query(query, conn, params=(fromDate, toDate,request.session['storeid']))
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, sheet_name='Audit_Data', index=False)
            output.seek(0)
            response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={smart_str(filename + ".xlsx")}'
            conn.close()
            return response
        return render(request, 'store_expiry_download.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')
    
def store_expiry_data_entry(request):
    try:
        if request.method == "POST": 
            if 'expiryrecordsave' in request.POST:
                with transaction.atomic():
                    productcode = request.POST['item_name']
                    productname = ProductMaster.objects.filter(productcode = productcode).get()
                    batch = request.POST['batch'].upper()
                    qty = request.POST['qty']
                    mrp = request.POST['mrp']
                    expMonth = request.POST['expMonth']
                    expYear = request.POST['expYear']
                    print(productcode)
                    print(batch)
                    newentry = StoreExpiryProductDetail.objects.create(
                        store_id = request.session['storeid'],
                        item_code = productcode,
                        item_name = productname.productname,
                        batch = batch,
                        qty = qty,
                        mrp = mrp,
                        user_name = request.session['username'],
                        date_of_created = datetime.now(),
                        rack_no = request.session['rackNo'],
                        exp_date = expMonth+'-'+expYear
                    )
                    getproductdetailsid = newentry.id
                    state = StoreMaster.objects.get(d_365_store_id = request.session['storeid'])
                    print(state.store_state)
                    itemList = EnteroItemLists.objects.annotate(batch_no_upper = Upper('batch_no')).filter(sku_code = productname.productcode, batch_no_upper = batch)
                    print(itemList)
                    date_string = expMonth+'-'+expYear
                    date_object = datetime.strptime(date_string, "%m-%Y")
                    formatted_date = date_object.strftime("%Y-%m-%d")
                    if itemList.filter(state = state.store_state).exists():
                        print('inside state')
                        selected_vendor = None
                        details =  itemList.order_by(state.store_state.lower())
                        state_column_prefix = f"{state.store_state.lower()}"
                        print(state_column_prefix)
                        for item in details:
                            print(item.state)
                            # if float(item.qty_sold) >= float(qty):
                            selected_vendor = item.entity_name
                            break 
                            # else:
                            #     selected_vendor = 'Others'
                        print(selected_vendor)
                        SupplierReturnItem.objects.create(
                            store_id = request.session['storeid'],
                            item_code = productcode,
                            item_name = productname.productname,
                            batch_no = batch,
                            date_of_expiry = formatted_date,
                            vendor_name = selected_vendor,
                            accepted_qty = item.qty_sold,
                            created_by = request.session['username'],
                            date_of_creation = datetime.now(),
                            return_qty = qty,
                            remaining_qty = (float(item.qty_sold) - float(qty)),
                            productdetail_id = getproductdetailsid
                        )
                        if selected_vendor != 'Others':
                            itemList = EnteroItemLists.objects.annotate(batch_no_upper = Upper('batch_no')).filter(sku_code = productname.productcode, 
                                                        batch_no_upper = batch, entity_name = selected_vendor).update(qty_sold = (float(item.qty_sold) - float(qty)))
                    elif itemList.exists():
                        selected_vendor = None
                        details =  itemList.order_by(state.store_state.lower())
                        state_column_prefix = f"{state.store_state.lower()}"
                        print(state_column_prefix)
                        for item in details:
                            # if float(item.qty_sold) >= float(qty):
                            selected_vendor = item.entity_name
                            break 
                            # else:
                            #     selected_vendor = 'Others'
                        print(selected_vendor)
                        SupplierReturnItem.objects.create(
                            store_id = request.session['storeid'],
                            item_code = productcode,
                            item_name = productname.productname,
                            batch_no = batch,
                            date_of_expiry = formatted_date,
                            vendor_name = selected_vendor,
                            accepted_qty = item.qty_sold,
                            created_by = request.session['username'],
                            date_of_creation = datetime.now(),
                            return_qty = qty,
                            remaining_qty = (float(item.qty_sold) - float(qty)),
                            productdetail_id = getproductdetailsid
                        )
                        if selected_vendor != 'Others':
                            itemList = EnteroItemLists.objects.annotate(batch_no_upper = Upper('batch_no')).filter(sku_code = productname.productcode, 
                                                        batch_no_upper = batch, entity_name = selected_vendor).update(qty_sold = (float(item.qty_sold) - float(qty)))
                    else:
                        SupplierReturnItem.objects.create(
                            store_id = request.session['storeid'],
                            item_code = productcode,
                            item_name = productname.productname,
                            batch_no = batch,
                            date_of_expiry = formatted_date,
                            vendor_name = 'Others',
                            accepted_qty = qty,
                            created_by = request.session['username'],
                            date_of_creation = datetime.now(),
                            return_qty = qty,
                            remaining_qty = 0,
                            productdetail_id = getproductdetailsid
                        )
                return redirect('store_expiry_data_entry')
        return render(request, 'store_expiry_product_entry.html')
    except Exception as e:
        print(e)
        messages.error(request,e)
        return render(request, 'login/index.html')
    
def getpacksize(request):
    try:
        productCode = request.GET.get('value', '')
        getdetails = ItemMaster.objects.filter(aster_code = productCode).all().order_by('sales_unit')
        packList = [i.sales_unit for i in getdetails]
        return JsonResponse({'success': True,'product': {'packSize': packList}})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': str(e)})

def storeproductlist(request,search):
   try:
        result = []
        if search == '-':
            data = ProductMaster.objects.all().order_by('productname')[:50]
            for i in data:
                res = {
                    'item_code':i.productcode,
                    'item_name':i.productname
                }
                result.append(res)
        else:
            data = ProductMaster.objects.filter(productname__icontains = search).all().order_by('productname')[:50]
            for i in data:
                res = {
                    'item_code':i.productcode,
                    'item_name':i.productname
                }
                result.append(res)
        return JsonResponse(result,safe = False)
   except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'errorMsg': str(e)}), 500)
   
def barcodeEntry(request):
    try:
        if request.method == 'POST':
            if 'barcodesave' in request.POST:
                barcode = request.POST['enterBarcode']
                productcode = request.POST['item_name']
                productName = ItemMaster.objects.get(aster_code = productcode)
                BarcodeUpdate.objects.create(
                    aster_code = productcode,
                    item_name = productName.product_name,
                    bar_code = barcode,
                    created_user = request.session['username'],
                    date_of_creation = datetime.now()
                )
                ItemMaster.objects.filter(aster_code = productcode).update(ean_upc = barcode)
                messages.success(request,'Barcode updated successfully')
                return redirect('barcodeEntry')
        return render(request,'barcodeEntry.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')
    
def expirydownload_data(request):
    try:
        if request.method == "POST" and 'downloadrecord' in request.POST:
            fromDate = request.POST['fromdate']
            toDate = request.POST['todate']
            checkboxStatus = request.POST.get('allstore')
            connection_string = ('DRIVER={ODBC Driver 17 for SQL Server};'
                            f"SERVER={os.environ["HOST"]};"
                            f"DATABASE={os.environ["DB_NAME"]};"
                            f"UID={os.environ["DB_USER"]};"
                            f"PWD={os.environ["DB_PASSWORD"]};")
            conn = pyodbc.connect(connection_string)
            if checkboxStatus is None:
                storeCodeList  = request.POST.getlist('region')
                regionCode = storeCodeList[0] if storeCodeList else None
                print(regionCode)
                storeId = None
                if regionCode == '0':
                    storeId = '29%'
                elif regionCode == '1':
                    storeId = '32%'
                elif regionCode == '2':
                    storeId = '36%'
                print(storeId)
                query = """
                select store_id,item_code,item_name,batch_no,date_of_expiry,vendor_name,return_qty,created_by,date_of_creation 
                from supplier_return_item where CAST(date_of_creation AS DATE) BETWEEN ? AND ? and store_id like ? 
                """
                data = pd.read_sql_query(query, conn, params=(fromDate, toDate,storeId))
            else:
                query = """
                select store_id,item_code,item_name,batch_no,date_of_expiry,vendor_name,return_qty,created_by,date_of_creation 
                from supplier_return_item where CAST(date_of_creation AS DATE) BETWEEN ? AND ? 
                """
                data = pd.read_sql_query(query, conn, params=(fromDate, toDate))

            # Convert batch column to string explicitly
            data['batch_no'] = data['batch_no'].astype(str)
            data['date_of_expiry'] = data['date_of_expiry'].astype(str)

            # Convert date_of_created from UTC to IST (UTC+5:30)
            utc_zone = pytz.utc
            ist_zone = pytz.timezone('Asia/Kolkata')

            data['date_of_creation'] = pd.to_datetime(data['date_of_creation'], utc=True)
            data['date_of_creation'] = data['date_of_creation'].dt.tz_convert(ist_zone)
            data['date_of_creation'] = data['date_of_creation'].dt.strftime('%Y-%m-%d %H:%M:%S')  # Format as string

            # Prepare Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, sheet_name='Expiry_Data', index=False)

                # Get the workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Expiry_Data']

                # Define text format for batch column
                text_format = workbook.add_format({'num_format': '@'})  # '@' forces text format
                batch_column_index = data.columns.get_loc("batch_no")  # Get the index of batch column

                # Apply format to the entire column
                worksheet.set_column(batch_column_index, batch_column_index, None, text_format)

                # for expiry date
                text_format = workbook.add_format({'num_format': '@'})  # '@' forces text format
                expiry_column_index = data.columns.get_loc("date_of_expiry")  # Get the index of batch column

                # Apply format to the entire column
                worksheet.set_column(expiry_column_index, expiry_column_index, None, text_format)

            output.seek(0)
            response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={smart_str("Expiry_Data" + fromDate + '_'+ toDate + ".xlsx")}'

            conn.close()
            return response
        return render(request, 'expiry_download_data.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')
    
def storeSalesData(request):
    try:
        saleData = StoreSalesData.objects.raw("""SELECT 
                                                    a.storeid as storeid,
                                                    a.storename as storename,
                                                    a.custname as custname,
                                                    a.billno as BillNo,
                                                    a.billdate as billdate,
                                                    a.mobilenum as mobilenum,
                                                    b.itemdescription as itemdescription,
                                                    b.Quantity as qty,
                                                    a.totalvalue as totalvalue
                                                FROM store_sales_data a LEFT JOIN store_detail_sales_data b
                                                ON a.BillNo = b.BillNo where a.Storeid = %s """,[request.session['storeid']])
        return render(request,'store_sales_data.html',{'saleData':saleData})
    except Exception as e:
        print(e)
        messages.error(request,e)
        return render(request, 'login/index.html')