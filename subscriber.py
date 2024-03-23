from config import mqtt_server, TOPIC
from controller import Controller

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from loguru import logger
logger.add(
    'log.log',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",
    level="INFO",
)

controller = Controller()   #TODO: config
client = mqtt.Client(CallbackAPIVersion.VERSION2)  # version2 add a properties in callback


@client.connect_callback()  # bind function
def on_connect(client: mqtt.Client, userdata, flags, reason_code, properties):
    """
    回调函数。当尝试与 MQTT broker 建立连接时，触发该函数。
    @client:    本次连接的客户端实例。
    @userdata:  用户的信息，一般为空。但如果有需要，也可以通过 user_data_set 函数设置。
    @flags:     保存服务器响应标志的字典。
    @rc:        响应码。一般情况下，我们只需要关注 rc 响应码是否为 0 就可以了。
    @properties: version 2 加入的参数
    """
    if reason_code == 0:
        logger.info("Connected success")
    else:
        rc_msg = {
            0: '连接成功',
            1: '不正确的协议版本',
            2: '无效的客户端标识符',
            3: '服务器不可用',
            4: '错误的用户名或密码',
            5: '未授权',
            6-255: '未定义',
        }
        logger.error(f"Connected fail with code {reason_code}: {rc_msg.get(reason_code, '未定义')}")
        raise ConnectionError


@client.message_callback()
def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    """
    @param client: the client instance for this callback
    @param userdata: the private user data as set in Client() or user_data_set()
    @param message: the received message.
            This is a class with members topic, payload, qos, retain.
    """
    logger.info(f'receive message from topic "{message.topic}": {message.payload.decode()}')
    controller.handle(message.topic, message.payload.decode())


client.connect(mqtt_server.broker, mqtt_server.port, keepalive=60) 

client.subscribe(TOPIC.lock)

client.loop_forever()  # blocked
