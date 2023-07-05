from django.shortcuts import render, redirect, HttpResponse
from .models import Moment, User, Contact, Comment, Video
from .form import RegisterForm, LoginForm, SubmitForm, ContactForm, MoreInfoForm
from datetime import datetime


def check_login(name):
    res = True
    info = ''
    context = {}

    if name == None:
        info = '请先进行登录'
        context = {'info': info}
        res = False
    else:
        if not User.objects.filter(name=name):
            info = '请先进行登录'
            context = {'info': info}
            res = False
        else:
            user_now = User.objects.get(name=name)

            # 判断用户是否在线，不在线就提示先登录
            if user_now.if_login:
                res = True
            else:
                state = False
                info = '请先进行登录'
                context = {'info': info}
                res = False

    return res, context


# Create your views here.

def index(request):
    moments = Moment.objects.all()[:10]  # 先只获取前10个帖子
    users = User.objects.all()

    name = request.session.get('name')
    info = request.session.get('info')

    state = False
    status = False

    if name == None:
        info = '请先进行登录'
        context = {'info': info}
        return render(request, 'login.html', context)
    else:
        if not User.objects.filter(name=name):
            info = '请先进行登录'
            context = {'info': info}
            return render(request, 'login.html', context)
        else:
            user_now = User.objects.get(name=name)

            # 判断用户是否在线，不在线就提示先登录
            if user_now.if_login:
                state = True
            else:
                state = False
                info = '请先进行登录'
                context = {'info': info}
                return render(request, 'login.html', context)

            # 判断身份是游客还是管理员
            if user_now.if_tourist:
                status = False
            else:
                status = True

            # 展示前3位用户
            user_shows = []
            cnt = 0
            for user in users:
                cnt = cnt + 1
                if cnt > 3:
                    break
                user_shows.append([user.profile, user.name])

            # 展示前8帖子种类
            kinds = set()
            for moment in moments:
                if moment.is_valid and len(kinds) <= 8:
                    kinds.add(moment.kind)

            context = {'moments': moments, 'kinds': kinds, 'user_shows': user_shows,
                       'state': state, 'status': status, 'name': name, 'info': info}

            # 用户名就不删了
            info = request.session.pop('info', None)  # 将提示信息删除

            return render(request, 'index.html', context)


def about(request):
    name = request.session.get('name')

    context = {'name': name}

    return render(request, 'about.html', context)


def contact(request):
    name = request.session.get('name')
    user_now = User.objects.get(name=name)

    # 先判断有没有登录
    res, context = check_login(name)
    if not res:
        return render(request, 'login.html', context)

    state = res

    if user_now.if_tourist:
        status = False
    else:
        status = True

    if request.method == "GET":
        context = {'name': name, 'state': state, 'status': status}
        return render(request, 'contact.html', context)
    else:
        form = ContactForm(request.POST, request.FILES)

        user = User.objects.get(name=name)

        if form.is_valid():
            real_name = form.cleaned_data.get('real_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            subject = form.cleaned_data.get('subject')
            content = form.cleaned_data.get('content')

            contact = Contact()
            contact.real_name = real_name
            contact.date = datetime.now()
            contact.email = email
            contact.phone_number = phone_number
            contact.content = content
            contact.subject = subject

            contact.save()

            request.session['info'] = "提交成功！请耐心等待我们的回复"

            return redirect("/")
        else:
            return render(request, 'contact.html', {"error": "内容填写错误"})


def submit(request):
    name = request.session.get('name')
    user_now = User.objects.get(name=name)

    # 先判断有没有登录
    res, context = check_login(name)
    if not res:
        return render(request, 'login.html', context)

    state = res

    if request.method == "GET":
        if user_now.if_tourist:
            status = False
        else:
            status = True

        context = {'name': name, 'state': state, 'status': status}

        return render(request, 'submit.html', context)
    else:
        form = SubmitForm(request.POST, request.FILES)

        if form.is_valid():
            pic = form.cleaned_data.get('pic')
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            kind = form.cleaned_data.get('kind')

            moment = Moment()
            moment.pic = pic
            moment.date = datetime.now()
            moment.title = title
            moment.content = content
            moment.author_name = name
            moment.email = user_now.email
            moment.kind = kind
            moment.is_valid = False

            moment.save()

            request.session['info'] = " 提交成功！请耐心等待审核。\\n 请先欣赏其他人的贴子吧~"

            return redirect("/")
        else:
            return render(request, 'submit.html', {"error": "填写错误"})


def logout(request):
    name = request.session.get('name')
    user = User.objects.get(name=name)

    user.if_login = False

    user.save()

    return redirect('/')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            user_flag = User.objects.filter(name=name, pwd=pwd)

            if user_flag:
                user = User.objects.get(name=name)
                user.if_login = True
                user.save()
                request.session['name'] = name

                return redirect("/")
            else:
                return render(request, "login.html", {"error": "输入账号或密码错误"})
        else:
            return render(request, 'login.html', {"error": "输入账号或密码错误"})


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            user_flag = User.objects.filter(name=name)
            if user_flag:
                return render(request, 'register.html', {'register_done': '该用户名已被注册'})
            else:
                user = User()
                user.name = name
                user.pwd = pwd
                user.save()
                request.session['name'] = name
                return redirect('more_info')
        else:
            return render(request, 'register.html', {'error': '输入账号或密码格式错误'})


def more_info(request):
    if request.method == "GET":
        return render(request, 'more_info.html')
    else:
        form = MoreInfoForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.cleaned_data.get('pic')
            email = form.cleaned_data.get('email')

            name = request.session.get('name')
            user_now = User.objects.get(name=name)

            state = True

            user_now.profile = pic
            user_now.email = email

            user_now.if_login = True
            user_now.save()

            request.session['info'] = " 注册成功！快去看看其他人的贴子吧~"

            return redirect("/")
        else:
            return render(request, 'more_info.html', {'error': '输入内容格式错误'})


def dianzan(request):
    name = request.session.get('name')
    user_now = User.objects.get(name=name)

    # 先判断有没有登录
    res, context = check_login(name)
    if not res:
        return render(request, 'login.html', context)

    state = res

    if user_now.if_tourist:
        status = False
    else:
        status = True

    moment_id = request.GET.get('moment_id')

    moment_now = Moment.objects.get(id=moment_id)
    moment_now.dianzan_count += 1
    moment_now.save()

    moment_id = request.GET.get('moment_id')
    moment_now = Moment.objects.get(id=moment_id)
    comments = Comment.objects.filter(moment_id=moment_id)
    lattest_comment = comments.last()

    context = {'name': name, 'state': state, 'status': status, 'moment_now': moment_now, 'comments': comments,
               'lattest_comment': lattest_comment}

    return render(request, 'detail.html', context)


def detail(request):
    name = request.session.get('name')
    user_now = User.objects.get(name=name)

    # 先判断有没有登录
    res, context = check_login(name)
    if not res:
        return render(request, 'login.html', context)

    state = res

    if user_now.if_tourist:
        status = False
    else:
        status = True

    moment_id = request.GET.get('moment_id')
    moment_now = Moment.objects.get(id=moment_id)
    comments = Comment.objects.filter(moment_id=moment_id)
    lattest_comment = comments.last()

    context = {'name': name, 'state': state, 'status': status, 'moment_now': moment_now, 'comments': comments,
               'lattest_comment': lattest_comment}

    return render(request, 'detail.html', context)


def add_comment(request):
    name = request.session.get('name')
    user_now = User.objects.get(name=name)

    # 先判断有没有登录
    res, context = check_login(name)
    if not res:
        return render(request, 'login.html', context)

    state = res

    if user_now.if_tourist:
        status = False
    else:
        status = True

    if request.method == "GET":
        moment_id = request.GET.get('moment_id')
        moment_now = Moment.objects.get(id=moment_id)
        content = request.GET.get('content')

        comment = Comment()
        comment.moment_id = moment_id
        comment.date = datetime.now()
        comment.content = content
        comment.author_name = name
        comment.save()

        info = "评论添加成功"

        comments = Comment.objects.filter(moment_id=moment_id)
        lattest_comment = comments.last()

        context = {'name': name, 'state': state, 'status': status, 'moment_now': moment_now, 'comments': comments,
                   'lattest_comment': lattest_comment, 'info': info}

        return render(request, 'detail.html', context)


def mypost(request):
    name = request.session.get('name')
    user_now = User.objects.get(name=name)

    # 先判断有没有登录
    res, context = check_login(name)
    if not res:
        return render(request, 'login.html', context)

    state = res

    if user_now.if_tourist:
        status = False
    else:
        status = True

    moments = Moment.objects.filter(author_name=name)

    context = {'name': name, 'state': state, 'status': status, 'moments': moments}

    return render(request, 'mypost.html', context)


def edit(request, moment_id):
    name = request.session.get('name')
    user_now = User.objects.get(name=name)

    # 先判断有没有登录
    res, context = check_login(name)
    if not res:
        return render(request, 'login.html', context)

    state = res

    if user_now.if_tourist:
        status = False
    else:
        status = True

    moment_now = Moment.objects.get(id=moment_id)

    if request.method == "GET":
        if user_now.if_tourist:
            status = False
        else:
            status = True

        context = {'name': name, 'state': state, 'status': status, 'moment_now': moment_now}

        return render(request, 'edit.html', context)
    else:
        form = SubmitForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            kind = form.cleaned_data.get('kind')

            moment = Moment.objects.get(id=moment_id)
            moment.date = datetime.now()
            moment.title = title
            moment.content = content
            moment.author_name = name
            moment.email = user_now.email
            moment.kind = kind
            moment.is_valid = False

            moment.save()

            request.session['info'] = " 修改成功！请耐心等待审核。\\n 请先欣赏其他人的贴子吧~"

            return redirect("mypost.html")
        else:
            return redirect('/')


def cinema(request):
    name = request.session.get('name')
    user_now = User.objects.get(name=name)

    # 先判断有没有登录
    res, context = check_login(name)
    if not res:
        return render(request, 'login.html', context)

    state = res

    if user_now.if_tourist:
        status = False
    else:
        status = True

    videos = Video.objects.all()
    video = videos[0]

    # 聊天室号码
    num = request.GET.get('num')

    context = {'num': num, 'name': name, 'state': state, 'status': status, 'video': video}

    return render(request, 'cinema.html', context)


def admin(request):
    return redirect('admin')
