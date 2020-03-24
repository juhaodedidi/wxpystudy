#导入模块
from wxpy import *

#导入消息撤回模块
from xml.etree import ElementTree as ETree

#初始化机器人，扫码登陆
bot=Bot(cache_path=True)

#向文件传输助手发送消息
bot.file_helper.send('机器人已启动')
print('开始工作')
#设置好友消息防撤回
@bot.register(chats=None, msg_types=NOTE, except_self=False)
def get_revoked(msg):
    print('当前有系统提示',msg)

    #检查NOTE中是否有撤回信息
    revoked=ETree.fromstring(msg.raw['Content']).find('revokemsg')
    #判断是否是撤回消息类型
    if revoked:
        #拿到撤回消息的具体内容
        #根据找到撤回消息的id找到bot.messages中的原消息
        revoked_msg=bot.messages.search(id=int(revoked.find('msgid').text))[0]
        #找到消息的发送者
        #原发送者（群聊时为群员）
        sender=msg.member or msg.sender
        #把消息转发到文件传输助手
        revoked_msg.forward(
            bot.file_helper,
            prefix='{} 撤回了：'.format(sender.name)
        )

#设置消息自动回复
# @bot.register(Friend,TEXT)
# def auto_reply(msg):
#     if '尼格罗' in msg.text:
#         return '莫虎！啊，莫虎！'
#     elif '双螺丝' in msg.text:
#         return '是啊，是滴啊'
#     elif '莫虎' in msg.text:
#         return '骚骚卡'


#仅仅堵塞线程
bot.join()