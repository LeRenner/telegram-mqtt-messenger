import paho.mqtt.client as mqtt
from telegram import Bot
import sys

# print both on stdout and stderr
print("Starting Pudim Messenger", file=sys.stderr)


# MQTT settings
# hostname is at /config/hostname and port is at /config/port
# read files and assign to variables
with open('/config/hostname', 'r') as file:
    mqtt_broker_host = file.read().replace('\n', '')
with open('/config/port', 'r') as file:
    mqtt_broker_port = int(file.read().replace('\n', ''))
mqtt_topic = "pudimMessenger"

# Telegram settings
# token is at /config/token and chat_id is at /config/chat_id
# read files and assign to variables
with open('/secret/token', 'r') as file:
    telegram_bot_token = file.read().replace('\n', '')
with open('/secret/chat_id', 'r') as file:
    telegram_chat_id = file.read().replace('\n', '')

# debug prints
print("MQTT Broker Host: " + mqtt_broker_host, file=sys.stderr)
print("MQTT Broker Port: " + str(mqtt_broker_port), file=sys.stderr)
print("MQTT Topic: " + mqtt_topic, file=sys.stderr)
print("Telegram Chat ID: " + telegram_chat_id, file=sys.stderr)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker", file=sys.stderr)
    client.subscribe(mqtt_topic)


def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print("Message received: " + message, file=sys.stderr)
    send_to_telegram(message)


def send_to_telegram(message):
    print("Sending message to Telegram", file=sys.stderr)
    bot = Bot(token=telegram_bot_token)
    bot.send_message(chat_id=telegram_chat_id, text=message)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)

mqtt_client.loop_forever()
