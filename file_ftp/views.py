from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from file_ftp import models
import  os
import time

def login(request):
    if request.method == "GET":
        if request.session.get("session_key",None):  #判断浏览器session的值是否存在
            user_name=request.session.get("session_key")
            return redirect("/file_admin/ftp/")
        else:
            return render(request,"login.html")
    elif request.method == "POST":
        user_name=request.POST.get("user_name")
        user_pwd = request.POST.get("user_pwd")
        user_remember=request.POST.get("remember")
        if models.user_info.objects.filter(user_name=user_name,user_pwd=user_pwd ):
            request.session['session_key']=user_name     #设置session,把用户名当成seesion的值
            if user_remember == "on":
                pass                            #如果选择记住密码，默认就是2周有效期
            else:
                request.session.set_expiry(0)   # 设置当前用户关闭浏览器后session失效
                return redirect("/file_admin/ftp/")


        else:
            return render(request, "login.html",{"login_errors":"帐号或者密码错误"})
    else:
       pass
def loginout(request):
    del request.session["session_key"]
    return redirect('/login/')      #当用户点击退出后直接跳转到登录页面
def ftp(request):
    global user_name,user_project_dict,user_project,project_name,user_name,dir_time
    if request.method == "GET":
        if request.session.get("session_key") == None:
            return render(request,'login.html')
        else:
            user_name = request.session.get("session_key")
            user_project=models.user_info.objects.filter(user_name="%s" %(user_name)).values('user_project__project_name')
            user_project_dict={}
            count=0 #计数器
            for i in user_project:      #获取用户拥有哪些项目
                user_project_dict["k"+str(count)]=i["user_project__project_name"]
                count +=1
            return render(request, 'ftp.html', {"user_name":user_name, "user_project":user_project_dict})
    else:
        file_obj = request.FILES.get("file_name")
        dir_time=time.strftime("%Y%m%d")
        project_name=request.POST.get("project_select")
        file_path=os.path.join('static',project_name,dir_time,file_obj.name)
        file_name=file_obj.name
        file_md5 = request.POST.get("file_md5").lower()
        file_dir=os.path.join('static',project_name,dir_time)
        print(file_path)
        file_down="".join(("/down/?file=",file_path))
        print(file_down)

        if os.path.exists(file_dir):
            with open(file_path,mode='wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
        else:
            os.makedirs(file_dir)
            with open(file_path,mode='wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)



        file_time=time.strftime("%Y%m%d%H%M%S")
        file_num=file_md5 + file_time
        print(project_name)
        print(file_name)
        print(file_dir)
        file_status=models.file_admin.objects.values("file_name").filter(file_name=file_name,
                                                                  file_dir=dir_time,
                                                                  file_project__project_name=project_name).count()
        print(file_status)
        if file_status == 0:
            models.file_admin.objects.create(
                file_name=file_obj.name,
                file_download=file_down,
                file_dir=dir_time,
                file_md5=file_md5,
                file_time=file_time,
                file_num=file_num,
            )
        else:
            file_id = models.file_admin.objects.values("id").filter(file_name=file_name,
                                                                  file_dir=dir_time,
                                                                  file_project__project_name=project_name)
            print(file_id)
            models.file_admin.objects.filter(id=file_id[0]["id"]).update(
                file_name=file_obj.name,
                file_download=file_down,
                file_dir=dir_time,
                file_md5=file_md5,
                file_time=file_time,
                file_num=file_num,
            )
        file_admin_obj=models.file_admin.objects.get(file_num=file_num)
        file_project_obj=models.project.objects.get(project_name=project_name)
        file_ower_obj=models.user_info.objects.get(user_name=user_name)
        file_admin_obj.file_project.set([file_project_obj,])
        file_admin_obj.file_owner.set([file_ower_obj,])




        return render(request, 'ftp.html', {"down_url":file_down,
                                            "file_md5":file_md5,
                                                   "user_name":user_name,
                                                   "user_project":user_project_dict})
def ftp_list(request):

    global user_name
    if request.method == "GET":
        if request.session.get("session_key",None) == None:
            user_name=request.session.get("session_key", None)
            return render(request, 'login.html')
        else:
            user_name=request.session.get("session_key", None)
            user_permissions_tmp=models.user_info.objects.filter(user_name=user_name).values("user_permission")
            user_permissions=user_permissions_tmp[0]["user_permission"]
            if user_permissions == 1:
                project_list = models.project.objects.values("project_name")
                result_list = models.file_admin.objects.values("file_name",
                                                               "file_download",
                                                               "file_md5",
                                                               'file_time',
                                                               "file_dir",
                                                               'file_owner__user_name',
                                                               'file_project__project_name').all().order_by("-id")[:20]

            else:
                user_name = request.session.get("session_key",None)
                project_list = models.project.objects.values("project_name").filter(user_info__user_name=user_name)
                result_list=models.file_admin.objects.values("file_name",
                                                             "file_download",
                                                             "file_md5",
                                                             'file_time',
                                                             "file_dir",
                                                             'file_owner__user_name',
                                                             'file_project__project_name').filter(
                    file_owner__user_name='%s' %(user_name)).order_by("-id")[:10]

            return render(request, 'ftp_list.html', {"user_name": user_name,"ftp_list":result_list,"project_list":project_list})
    else:
        user_name = request.session.get("session_key", None)

        s_projectname=request.POST.get("s_project")
        s_time=request.POST.get("s_time")

        if s_time:
            s_time_tmp="".join(s_time.split("-"))
            s_time=s_time_tmp
        else:
            s_time=time.strftime("%Y%m%d")
        result_list = models.file_admin.objects.values("file_name",
                                                       "file_download",
                                                       "file_md5",
                                                       'file_time',
                                                       "file_dir",
                                                       'file_owner__user_name',
                                                       'file_project__project_name').filter(
            file_dir=s_time, file_project__project_name=s_projectname).order_by("-id")[:20]
        if user_name == "admin":
            project_list = models.project.objects.values("project_name").all()
            result_list = models.file_admin.objects.values("file_name",
                                                           "file_download",
                                                           "file_md5",
                                                           'file_time',
                                                           "file_dir",
                                                           'file_owner__user_name',
                                                           'file_project__project_name').filter(
                file_dir=s_time, file_project__project_name=s_projectname).order_by("-id")[:20]
        else:
            project_list = models.project.objects.values("project_name").filter(user_info__user_name=user_name)
            result_list = models.file_admin.objects.values("file_name",
                                                           "file_download",
                                                           "file_md5",
                                                           'file_time',
                                                           "file_dir",
                                                           'file_owner__user_name',
                                                           'file_project__project_name').filter(
                file_dir=s_time, file_project__project_name=s_projectname,file_owner__user_name=user_name).order_by("-id")[:20]

        return render(request,'ftp_list.html',{"user_name": user_name,"project_list":project_list,"ftp_list":result_list})
def readme(request):
    return render(request,"readme.html")

def check_login(func):
    """
    登录检测装饰器
    :param func:
    :return:
    """
    def wrapper(request,*args,**kwargs):
        if request.session.get("session_key", None) == None:
            return render(request,"login.html")
        return func(request,*args,**kwargs)
    return wrapper
@check_login
def add_classify(request):
    user_name=request.session.get("session_key", None)
    if request.method == "GET":
        return render(request,"add_classify.html",{"user_name":user_name})
    else:
        n_project=request.POST.get("classify")
        check_project=models.project.objects.filter(project_name=n_project).count()
        if check_project == 0:
            models.project.objects.create(project_name=n_project)
            return render(request,"add_classify.html",{"user_name":user_name,"info":"添加成功"})
        else:
            return render(request, "add_classify.html", {"user_name": user_name, "info": "添加失败，分类存在"})


@check_login
def admin_classify(request):
    user_name = request.session.get("session_key", None)
    if request.method ==  "GET":
        if request.GET.get("delete") != None:
            models.project.objects.filter(id=request.GET.get("delete")).delete()
            return redirect("/file_admin/admin_classify/")
        elif request.GET.get("update") != None:
            pass
            return redirect("/file_admin/admin_classify/")
        else:
            classify_list=models.project.objects.all()
            return render(request, "list_classify.html", {"user_name": user_name,"classify_list":classify_list })
    else:
        return render(request,"list_classify.html",{"user_name": user_name,})





