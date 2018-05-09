from django.shortcuts import render

# Create your views here.
from file_ftp import models
from django.shortcuts import render,redirect

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

def show_user_list(request):
    user_list = models.user_info.objects.values("id", "user_name")
    user_list_project = models.user_info.objects.values("id", "user_project__project_name")
    # print(user_list)
    # print(user_list_project)
    users = []

    for user_i in user_list:
        projects = []
        for project_i in user_list_project:
            if user_i["id"] == project_i["id"]:
                projects.append(project_i["user_project__project_name"])
        projects = list(set(projects))
        users.append({"id": user_i["id"], "user_name": user_i["user_name"], "user_project": projects})
    return users

def project_show():
    project_list=models.project.objects.values()
    return project_list
def add_user(request):

    if request.session.get("session_key", None):
        user_name=request.session.get("session_key", None)
        if request.method == "GET":
            project_list=project_show()
            return render(request, "add_user.html",{"project_list":project_list,"user_name":user_name})
        else:
            n_user = request.POST.get("n_user")
            n_pass = request.POST.get("n_pass")
            y_admin = request.POST.getlist("y_admin")
            if len(y_admin) == 1:
                user_permission=1
            else:
                user_permission=2
            s_project = request.POST.getlist("s_project")  #getlist获取对象多个值,返回的是一个列表
            project_list = project_show()
            check_user_status=models.user_info.objects.filter(user_name=n_user).count()
            if check_user_status == 0:
                models.user_info.objects.create(user_name=n_user,
                                                user_pwd=n_pass,
                                                user_permission=user_permission)
                n_user_obj=models.user_info.objects.get(user_name=n_user)
                for s_i in s_project:
                    project_num=models.project.objects.filter(project_name=s_i).values("id")
                    for i in project_num:
                        n_user_obj.user_project.add(i["id"])
                # return render(request, "add_user.html",
                #               {"project_list": project_list, "user_name": user_name,"info":"添加用户成功" })
                return redirect("/user_admin/user_list/")

            else:
                return render(request, "add_user.html", {"project_list": project_list, "user_name": user_name,"info":"用户存在"})

    else:
        return render(request, "login.html")
@check_login
def update_user(request):
    users=show_user_list(request)
    user_name = request.session.get("session_key", None)
    if request.method == "GET":
        if request.GET.get("update") != None:
            user_id=request.GET.get("update")
            user_info=models.user_info.objects.filter(id=user_id).values()

            project_all=models.project.objects.values("id","project_name")
            return render(request,"update_user.html",{"user_name":user_name,"user_info":user_info,"user_project":project_all})
        elif request.GET.get("delete") != None:
            user_id = request.GET.get("delete")
            obj=models.user_info.objects.get(id=user_id)
            ower_project=models.user_info.objects.filter(id=user_id).values("user_project__id")
            ower_project_id=[]
            for project_id in ower_project:
                ower_project_id.append(project_id["user_project__id"])
            models.user_info.objects.filter(id=user_id).delete()
            obj.user_project.remove(*ower_project_id)
            return redirect('/user_admin/user_list/')
        else:
            return redirect('/user_admin/user_list/')
        # return  render(request,"list_user.html",{"user_name": user_name,"users":users})

    else:
        user_id=request.POST.get("user_id")
        update_user_name=request.POST.get("user_name")
        user_pwd=request.POST.get("user_pwd")
        user_ower_project=request.POST.getlist("user_ower_project")
        user_project = models.user_info.objects.filter(id=user_id).values("user_project__id")
        user_obj=models.user_info.objects.get(id=user_id)
        # print(user_ower_project)
        # print(user_project)
        # print(request.POST.get("s_admin"))
        user_project_list=[]
        for user_project_i in user_project:
            user_project_list.append(user_project_i["user_project__id"])
        user_obj.user_project.remove(*user_project_list)    # 清除用户所有权限
        user_obj.user_project.add(*user_ower_project)   #设置新的权限
        return redirect("/user_admin/update_user/")

def user_list(request):
    if request.session.get("session_key", None):
        user_name=request.session.get("session_key", None)
        user_list = models.user_info.objects.values("id","user_name")
        user_list_project=models.user_info.objects.values("id","user_project__project_name")
        # print(user_list)
        # print(user_list_project)
        users=[]

        for user_i in user_list:
            projects = []
            for project_i in user_list_project:
                if user_i["id"] == project_i["id"]:
                    projects.append(project_i["user_project__project_name"])
            projects=list(set(projects))
            users.append({"id":user_i["id"],"user_name":user_i["user_name"],"user_project":projects})
        return render(request,"list_user.html",{"user_name":user_name,"users":users})
    else:
        return render(request,"login.html")
