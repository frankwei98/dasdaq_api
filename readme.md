# dasdaq api

## 注册 [POST]api.dasdaq.io/register/ 
### request
param => username,password, inviter(邀请码,可以为空)
### response
{'err_code', 'err_msg'}
```
err_code为0表示注册成功, 其他api均如此
要求用户名长度大于等于6位
密码长度大于等于6位 且必须包含大写字母 小写字母 和 数字
```

## 登录 [POST]api.dasdaq.io/login/
### request
param => username, password
### response
{'err_code', 'err_msg', 'user_info': {'username', 'email', 'invitation_code', 'inviter', 'eos_address', 'eth_address', 'avatar_url'}}

## 我的个人信息 [GET]api.dasdaq.io/get_my_info/
### request
param => 空
### response
{'err_code', 'err_msg', 'user_info': {'username', 'email', 'invitation_code', 'inviter', 'eos_address', 'eth_address', 'avatar_url'}}

## 修改密码 [POST]api.dasdaq.io/change_password/
### request
param => old_password, new_password
### response
{'err_code', 'err_msg'}

## 更新信息 [POST]api.dasdaq.io/update_profile/
### request
param => avatar_url(可以不传),eos_address,eth_address
### response
{'err_code', 'err_msg', 'user_info': 格式同上}

## 登出 [GET]api.dasdaq.io/logout/
### request
param => 空
### response
{'err_code', 'err_msg'}
