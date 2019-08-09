import itchat

# 获取微信好友头像
itchat.auto_login(hotReload=True)

friends = itchat.get_friends()[0:]
a = friends[0]['UserName']
# for i in friends: # RemarkName
#     img = itchat.get_head_img(userName=i['UserName'])
#     if i['RemarkName'] != '':
#         path = f"微信好友头像/{i['RemarkName']}.jpg"
#         # print('备注名:', i['RemarkName'])
#     else:
#         # print('昵称:', i['NickName'])
#         path = f"微信好友头像/{i['NickName']}.jpg"

    # try:
    #     with open(path, 'wb') as f:
    #         f.write(img)
    # except Exception as e:
    #     print(repr(e))

itchat.run()
