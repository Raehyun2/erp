from django.shortcuts import render, redirect
import openpyxl
from .models import Upload_Excel, Receipts_page, Issue_page, Stock_page


def main(request):
    return render(request, 'main/main.html')

def excel_col_read(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    worksheet = wb.active
    excel_data = list()
    for col in worksheet.iter_cols():
        col_data = list()
        for cell in col:
            col_data.append(str(cell.value))
        excel_data.append(col_data)
    return excel_data

def overview(request):
    return render(request,'main/overview.html')

def issue_page(request):
    if request.method == 'POST':
        if request.FILES.get('excel', False) == False:
            if 'view' in request.POST:
                if Receipts_page.objects.all().filter(user=request.user).exists() == False:
                    return render(request, 'main/receipts_page.html', {'error_message_0':"상품이 존재하지 않습니다."})
                data = Issue_page.objects.all().filter(user=request.user)
                return render(request, 'main/Issue_page.html', {'issues': data})

            elif 'confirm' in request.POST:
                if Issue_page.objects.all().filter(user=request.user).exists():
                    object_issue = Issue_page.objects.all().filter(user=request.user)
                    for object in object_issue:
                        object_receipt = Receipts_page.objects.all().filter(user=request.user, product_number=object.product_number).get()
                        object_receipt.remain_product -= object.remain_product
                        object_receipt.save()

                    Issue_page.objects.all().filter(user=request.user).delete()
                    return render(request, 'main/issue_page.html',{'confirm_message_1':"판매되었습니다."})
                else:
                    pass
            return render(request, 'main/issue_page.html',{'error_message_1':"판매 상품을 업로드해주세요."})

        else:
            if 'view' in request.POST:
                data = Issue_page.objects.all().filter(user=request.user)
                return render(request, 'main/Issue_page.html', {'issues':data})

            elif 'add' in request.POST:
                if Issue_page.objects.all().filter(user=request.user).exists():
                    return render(request, 'main/issue_page.html',{'error_message_2':"기존 판매 상품을 확정지어주세요."})
                else:
                    Upload_Excel.file = request.FILES['excel']
                    excel = excel_col_read(Upload_Excel.file)
                    for i in range(1, len(excel[0])):
                        if Receipts_page.objects.all().filter(user=request.user,product_number=excel[2][i]).exists():
                            print(Receipts_page.objects.all().filter(user=request.user,product_number=excel[2][i]).get().remain_product)
                            if Receipts_page.objects.all().filter(user=request.user,product_number=excel[2][i]).get().remain_product >= int(excel[5][i]):
                                Issue_page(
                                    user=request.user,
                                    date=excel[0][i],
                                    barcode=excel[1][i],
                                    product_number=excel[2][i],
                                    product_name=excel[3][i],
                                    product_place=excel[4][i],
                                    remain_product=int(excel[5][i]),
                                ).save()
                                object_stock = Stock_page.objects.all().filter(user=request.user,product_number=excel[2][i]).get()
                                object_stock.remain_product -= int(excel[5][i])
                                object_stock.save()
                            else:
                                return render(request, 'main/issue_page.html', {'error_message_2': "제품의 재고가 부족합니다."})
                        else:
                            return render(request, 'main/issue_page.html', {'error_message_3': "입고되지 않은 상품이 존재합니다."})
                    data = Issue_page.objects.all().filter(user=request.user)
                    return render(request, 'main/issue_page.html', {'issues': data})

            return render(request, 'main/issue_page.html')

    else:
        return render(request, 'main/issue_page.html')


def stock_page(request):
    if request.method == 'POST':
        if 'view' in request.POST:
            data = Stock_page.objects.all().filter(user=request.user)
            return render(request,'main/stock_page.html',{'stock':data})
    return render(request,'main/stock_page.html')



def receipts_page(request):
    if request.method == 'POST':
        if request.FILES.get('excel', False) == False:
            if 'view' in request.POST:
                if Receipts_page.objects.all().filter(user=request.user).exists() == False:
                    return render(request, 'main/receipts_page.html', {'error_message_0':"상품이 존재하지 않습니다."})
                data = Receipts_page.objects.all().filter(user=request.user)
                return render(request, 'main/receipts_page.html', {'receipts':data})
            elif 'delete' in request.POST:
                Receipts_page.objects.all().filter(user=request.user).delete()
                Issue_page.objects.all().filter(user=request.user).delete()
                Stock_page.objects.all().filter(user=request.user).delete()
                return render(request, 'main/receipts_page.html', {'confirm_message_1': "삭제하였습니다."})

            return render(request, 'main/receipts_page.html', {'error_message_1': "상품 파일을 선택해주세요."})

        else:
            if 'view' in request.POST:
                data = Receipts_page.objects.all().filter(user=request.user)
                return render(request, 'main/receipts_page.html', {'receipts':data})

            elif 'delete' in request.POST:
                Receipts_page.objects.all().filter(user=request.user).delete()
                Issue_page.objects.all().filter(user=request.user).delete()
                Stock_page.objects.all().filter(user=request.user).delete()
                return render(request, 'main/receipts_page.html', {'confirm_message_1': "삭제하였습니다."})

            elif 'upload' in request.POST:
                if Receipts_page.objects.all().filter(user=request.user).exists():
                    return render(request, 'main/receipts_page.html', {'error_message_2': "기존 상품을 삭제하십시오."})
                else:
                    Upload_Excel.file = request.FILES['excel']
                    excel = excel_col_read(Upload_Excel.file)

                    for i in range(1,len(excel[0])):
                        Receipts_page(
                            user=request.user,
                            date=excel[0][i],
                            barcode=excel[1][i],
                            product_number=excel[2][i],
                            product_name=excel[3][i],
                            product_place=excel[4][i],
                            remain_product=int(excel[5][i]),
                        ).save()

                        Stock_page(
                            user=request.user,
                            date=excel[0][i],
                            barcode=excel[1][i],
                            product_number=excel[2][i],
                            product_name=excel[3][i],
                            product_place=excel[4][i],
                            remain_product=int(excel[5][i]),
                        ).save()

                    data = Receipts_page.objects.all().filter(user=request.user)
                    return render(request, 'main/receipts_page.html', {'receipts': data})

            elif 'add' in request.POST:
                if Receipts_page.objects.all().filter(user=request.user).exists():
                    Upload_Excel.file = request.FILES['excel']
                    excel = excel_col_read(Upload_Excel.file)

                    for i in range(1,len(excel[0])):

                        if Receipts_page.objects.all().filter(user=request.user,product_number=excel[2][i]).exists():
                            object = Receipts_page.objects.all().filter(user=request.user,product_number=excel[2][i]).get()
                            object.remain_product += int(excel[5][i])
                            object.save()

                            object_stock = Stock_page.objects.all().filter(user=request.user,product_number=excel[2][i]).get()
                            object_stock.remain_product += int(excel[5][i])
                            object_stock.save()

                        else:
                            Receipts_page(
                                user=request.user,
                                date=excel[0][i],
                                barcode=excel[1][i],
                                product_number=excel[2][i],
                                product_name=excel[3][i],
                                product_place=excel[4][i],
                                remain_product=int(excel[5][i]),
                            ).save()

                            Stock_page(
                                user=request.user,
                                date=excel[0][i],
                                barcode=excel[1][i],
                                product_number=excel[2][i],
                                product_name=excel[3][i],
                                product_place=excel[4][i],
                                remain_product=int(excel[5][i]),
                            ).save()

                    data = Receipts_page.objects.all().filter(user=request.user)
                    return render(request, 'main/receipts_page.html', {'receipts':data})

                else:
                    return render(request, 'main/receipts_page.html', {'error_message_3': "초기 업로드를 먼저 진행하세요."})

            else:
                return render(request, 'main/receipts_page.html')
    else:
        return render(request, 'main/receipts_page.html')

