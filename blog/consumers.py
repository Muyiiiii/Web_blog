from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 接受链接
        self.accept()

        # 获取群号
        group = self.scope['url_route']['kwargs'].get('group')

        # 将对象加存储起来（内存或redis）
        # 将异步转同步
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)  # 后面的是用户名

    def websocket_receive(self, message):
        text = message['text']
        print("接收到的消息-->", text)  # {'type': 'websocket.receive', 'text': '123'}

        if text == "close":
            # 服务端主动关闭连接
            # 会执行websocket_disconnect函数，或者自己主动执行   raise StopConsumer()，使得下面的函数的只处理客户端的断开连接
            self.close()
            return

        res = "{}SB".format(text)
        print(res)

        # 获取群号
        group = self.scope['url_route']['kwargs'].get('group')

        # 通知组内所有的客户端，执行xx_oo的方法，集体发送
        async_to_sync(self.channel_layer.group_send)(group, {"type": "xx.oo", "message": message})

    # 这里的是给组里的每一个人发送
    def xx_oo(self, event):
        text = event['message']['text']
        self.send(text)

    def websocket_disconnect(self, message):
        print("[连接断开]")
        # 获取群号
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        self.send("[连接断开]")
        raise StopConsumer()
