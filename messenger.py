import paho.mqtt.client as mqtt
from telegram import Bot
import asyncio
import sys

# change default print file to stderr
sys.stdout = sys.stderr


# print both on stdout and stderr
print("Starting Pudim Messenger")

# hostname is at /config/hostname and port is at /config/port
with open('/config/hostname', 'r') as file:
    mqttBrokerHost = file.read().replace('\n', '')
with open('/config/port', 'r') as file:
    mqttBrokerPort = int(file.read().replace('\n', ''))


mqttTopics = []
with open('/config/topics', 'r') as file:
    for line in file:
        mqttTopics.append(line.replace('\n', ''))

botTokens = []
with open('/secret/tokens', 'r') as file:
    for line in file:
        botTokens.append(line.replace('\n', ''))

chatIDs = []
with open('/secret/chatids', 'r') as file:
    for line in file:
        chatIDs.append(line.replace('\n', ''))


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    for topic in mqttTopics:
        client.subscribe(topic)


def on_message(client, userdata, msg):
    print("Message received from MQTT Broker")
    print(msg.topic + " " + str(msg.payload))

    for i in range(len(mqttTopics)):
        if msg.topic == mqttTopics[i]:
            send_to_telegram(msg.payload.decode("utf-8"), botTokens[i], chatIDs[i])


def send_to_telegram(message, botToken, chatId):
    print("Sending message to user " + chatId)
    print(message)
    bot = Bot(botToken)
    asyncio.run(bot.sendMessage(chatId, message, parse_mode="HTML"))


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(mqttBrokerHost, mqttBrokerPort, 60)
mqtt_client.loop_forever()
