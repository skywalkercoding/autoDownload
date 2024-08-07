from django.shortcuts import render
from apps.CreateAPP.BaseCreate.BaseCreateView import BaseCreateView
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from apps.CreateAPP.models import CreateApp
# Create your views here.
class DisplayCreateView(BaseCreateView):
    def get(self,request):
        appsList=self.displayCreateApp()
        return  render(request,'creating.html',{"apps":appsList})


class ModelUploadView(BaseCreateView):
    def post(self,request):
        excelFiles = request.FILES.get("excel.file")

        if excelFiles is None:
            print("文件不能为空")
            data = {'success': False, 'message': 'Please upload Excel aaaa'}


        else:

            excel_path = self.uploadCommonFile(request, 'excel.file')
            print("当前目录："+excel_path)
            if excelFiles.name.split('.')[-1] not in ['xls', 'xlsx']:
                data = {'success': False, 'message': 'excel type no support '}

            else:
                isUpEDxce, message = self.readExcel(excel_path)
                if isUpEDxce:
                    data = {'success': True, 'message': message}

                else:
                    data = {'success': False, 'message': message}

        return JsonResponse(data)


class DeleteClearDataView(BaseCreateView):
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        pkgnames = self.getStrParam(request, 'id')
        print("获取当前包名：" + str(len(pkgnames)))
        if len(pkgnames) == 0:
            success = False
            print("至少选择一条")
            message = "至少选择一条"
            return JsonResponse({"success": success, "message": message})
        pkgnames = pkgnames.split(',')
        count = 0

        try:
            for pkgname in pkgnames:

                print("当前要删除：" + str(pkgname))
                # BaseApp.objects.all().delete()
                if self.primaryKeyExist(pkgname):
                    CreateApp.objects.filter(pkgname=pkgname.strip()).delete()

                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = str(e)
            print(e)
            success = False
        return JsonResponse({"success": success, "message": message})

class DownloadIconView(BaseCreateView):
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)
    def handle(self, request):
        pkgnames = self.getStrParam(request, 'id')
        print("获取当前包名：" + str(pkgnames))
        if len(pkgnames) == 0:
            success = False
            print("至少选择一条")
            message = "至少选择一条"
            return JsonResponse({"success": success, "message": message})
        pkgnames = pkgnames.split(',')
        success,message=self.downloadIcon(pkgnames)
        return JsonResponse({"success": success, "message": message})

class ReporteExcelView(BaseCreateView):
    def get(self,request):
        getctList=self.displayCreateApp()
        excelname="test.xlsx"
        excelRepPath=self.createExcelrep(excelname,getctList)
        response = StreamingHttpResponse(self.file_iterator(request, excelRepPath))
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = 'attachment;filename=' + excelname
        return response


class UploadIconView(BaseCreateView):
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        pkgnames = self.getStrParam(request, 'id')
        print("获取当前包名：" + str(len(pkgnames)))
        if len(pkgnames) == 0:
            success = False
            print("至少选择一条")
            message = "至少选择一条"
            return JsonResponse({"success": success, "message": message})
        pkgnames = pkgnames.split(',')
        getCtList=self.uploadIcon(pkgnames)
        if len(getCtList)==0:
             success=False
             message='Start Web Failed'
        else:
            status,message=self.updateCreateStatus(getCtList)
            success = status
            message = message
        return JsonResponse({"success": success, "message": message})

