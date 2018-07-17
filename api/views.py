import hashlib
from django.http import JsonResponse

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from api.models import UserEx


def get_invitation_code_by_index(index):
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    print('index', type(index))
    for i in range(4):
        print(index % len(chars))
        result = chars[index % len(chars)] + result
        index //= len(chars)
    return result


@csrf_exempt
def register_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    inviter = request.POST.get('inviter', '')
    password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()

    if len(username) < 6:
        return JsonResponse({'err_code': -1, 'err_msg': "非法的邮箱地址"})
    if '@' not in username:
        return JsonResponse({'err_code': -1, 'err_msg': "非法的邮箱地址"})
    if len(password) <6:
        return JsonResponse({'err_code': -1, 'err_msg': "密码长度要大于等于6"})
    has_lower = has_upper = has_digit = False
    for item in password:
        if item in '0123456789':
            has_digit = True
        if item in 'abcdefghijklmnopqrstuvwxyz':
            has_lower = True
        if item in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            has_upper = True
    if not (has_lower and has_upper and has_digit):
        return JsonResponse({'err_code': -1, 'err_msg': "密码需同时包含大写字母、小写字母、数字"})
    if UserEx.objects.filter(username=username).exists():
        return JsonResponse({'err_code': -1, 'err_msg': "该邮箱已被注册"})

    user = UserEx(username=username, email=username, password_md5=password_md5, invitation_code='', inviter=inviter)
    user.save()

    # 1234 for seems more people
    user.invitation_code = get_invitation_code_by_index(1234+user.pk)
    user.save()
    request.session['username'] = username
    return JsonResponse({'err_code': 0})


@csrf_exempt
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()

    user = UserEx.objects.filter(username=username)
    if len(user) == 0:
        return JsonResponse({'err_code': -1, 'err_msg': "用户名不存在"})
    if len(user) > 1:
        return JsonResponse({'err_code': -1, 'err_msg': '用户名非法, 请联系客服'})
    if password_md5 != user[0].password_md5:
        return JsonResponse({'err_code': -1, 'err_msg': '密码错误'})

    request.session['username'] = user[0].username
    return JsonResponse({'err_code': 0, 'user_info': user[0].to_dict()})


@csrf_exempt
def get_my_info_view(request):
    username = request.session.get('username')
    if not username:
        return JsonResponse({"err_code": -1,  'err_msg': '登录已失效, 请重新登录'})
    user = UserEx.objects.filter(username=username)
    if not user:
        return JsonResponse({'err_code': -1, 'err_msg': 'session非法'})
    user = user[0]
    return JsonResponse({'user_info': user.to_dict()})


@csrf_exempt
def change_password(request):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    username = request.session.get('username')
    if not username:
        return JsonResponse({"err_code": -1,  'err_msg': '登录已失效, 请重新登录'})
    user = UserEx.objects.filter(username=username)
    if not user:
        return JsonResponse({'err_code': -1, 'err_msg': 'session非法'})
    user = user[0]
    if hashlib.md5(old_password.encode('utf-8')).hexdigest() != user.password_md5:
        return JsonResponse({'err_code': -1, 'err_msg': '原始密码错误'})

    if len(new_password) < 6:
        return JsonResponse({'err_code': -1, 'err_msg': "密码长度要大于等于6"})
    has_lower = has_upper = has_digit = False
    for item in new_password:
        if item in '0123456789':
            has_digit = True
        if item in 'abcdefghijklmnopqrstuvwxyz':
            has_lower = True
        if item in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            has_upper = True
    if not (has_lower and has_upper and has_digit):
        return JsonResponse({'err_code': -1, 'err_msg': "密码需同时包含大写字母、小写字母、数字"})

    user.password_md5 = hashlib.md5(new_password.encode('utf-8')).hexdigest()
    user.save()
    return JsonResponse({'err_code': 0})


@csrf_exempt
def update_profile_view(request):
    # avatar_url, eos_address, eth_address
    avatar_url = request.POST.get('avatar_url')
    eos_address = request.POST.get('eos_address')
    eth_address = request.POST.get('eth_address')
    username = request.session.get('username')
    if not username:
        return JsonResponse({"err_code": -1,  'err_msg': '登录已失效, 请重新登录'})

    user = UserEx.objects.filter(username=username)
    if not user:
        return JsonResponse({'err_code': -1, 'err_msg': 'session非法'})
    user = user[0]
    if avatar_url:
        user.avatar_url = avatar_url
    if eos_address:
        user.eos_address = eos_address
    if eth_address:
        user.eth_address = eth_address
    user.save()
    return JsonResponse({'err_code': 0, 'user_info': user.to_dict()})


@csrf_exempt
def logout_view(request):
    request.session.flush()
    return JsonResponse({'err_code': 0})
