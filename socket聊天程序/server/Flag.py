class Flag:
    Error = 0  # From: server or client.异常提示，客户端网络中断，或者服务器未开启
    Login = 1  # To: server.客户端刚登录时发给服务器的标记，服务器根据此标记去数据库查询账号密码是否正确
    LoginSuccess = 2  # To: client.账号或密码正确，同意客户端连接服务器。
    LoginFailed = 3  # To: client.账号或密码错误
    MsgText = 4  # 文本消息类型
    NewFriend = 5  # 刚登录时，给在线人的通知。
    OnlineFriend = 6  # 刚登录时，把已经在线人的的人发给自己。
    FriendExit = 7  # 好友退出后，服务器需要通知在线的好友