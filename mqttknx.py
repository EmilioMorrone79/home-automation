"""Example for daemon mode within XKNX."""
import asyncio
import paho.mqtt.client as mqtt

from xknx import XKNX
from xknx.devices import Switch





def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    if obj == 0:
        print("First connection:")
    elif obj == 1:
        print("Second connection:")
    elif obj == 2:
        print("Third connection (with clean session=True):")
    print("    Session present: " + str(flags['session present']))
    print("    Connection result: " + str(rc))

	

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


def on_disconnect(mqttc, obj, rc):
    mqttc.user_data_set(obj + 1)
    if obj == 0:
        mqttc.reconnect()
	
	
# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.username_pw_set(username="homeassistant",password="password")

mqttc.connect("192.168.1.7",1883,60)
mqttc.loop_start()
















@asyncio.coroutine
def device_updated_cb(device):
    """Do someting with the updated device."""
    print("Callback received from {0}".format(device.name))
    print("Callback state from {0}".format(device.state))
    if device.state :
       mqttc.publish("0C2C1C/light/switch", "ON",0)
       print("ON")
    else:
       mqttc.publish("0C2C1C/light/switch", "OFF",0)
       print("OFF")
	

async def main():
    """Connect to KNX/IP device and listen if a switch was updated via KNX bus."""
    xknx = XKNX(device_updated_cb=device_updated_cb)
    switch = Switch(xknx,
                    name='TestOutlet',
                    group_address='0/1/6')
    xknx.devices.add(switch)

    # Wait until Ctrl-C was pressed
    await xknx.start(daemon_mode=True)

    await xknx.stop()


# pylint: disable=invalid-name
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()