# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import iotc
from iotc import IOTConnectType, IOTLogLevel
from random import randint
from cellulariot import cellulariot
import time

node = cellulariot.CellularIoTApp()
node.setupGPIO()

node.disable()
time.sleep(1)
node.enable()

deviceId = "DEVICEID"
scopeId = "SCOPEID"
deviceKey = "DEVICEKEY"

iotc = iotc.Device(scopeId, deviceKey, deviceId, IOTConnectType.IOTC_CONNECT_SYMM_KEY)
iotc.setLogLevel(IOTLogLevel.IOTC_LOGGING_API_ONLY)

gCanSend = False
gCounter = 0

def onconnect(info):
  global gCanSend
  print("- [onconnect] => status:" + str(info.getStatusCode()))
  if info.getStatusCode() == 0:
     if iotc.isConnected():
       gCanSend = True

def onmessagesent(info):
  print("\t- [onmessagesent] => " + str(info.getPayload()))

def oncommand(info):
  print("- [oncommand] => " + info.getTag() + " => " + str(info.getPayload()))

def onsettingsupdated(info):
  print("- [onsettingsupdated] => " + info.getTag() + " => " + info.getPayload())

iotc.on("ConnectionStatus", onconnect)
iotc.on("MessageSent", onmessagesent)
iotc.on("Command", oncommand)
iotc.on("SettingsUpdated", onsettingsupdated)

iotc.connect()

while iotc.isConnected():
  iotc.doNext() # do the async work needed to be done for MQTT
	
  if gCanSend == True:
    if gCounter % 20 == 0:
      gCounter = 0
	
      # reading real sensor data
      acceleration = node.readAccel()
      humidity = str(node.readHum())
      temperature = str(node.readTemp())

      print("Sending telemetry..")
      iotc.sendTelemetry("{ \
\"temp\": " + temperature + ", \
\"humidity\": " + humidity + ", \
\"accelerometerX\": " + str(acceleration['x']) + ", \
\"accelerometerY\": " + str(acceleration['y']) + ", \
\"accelerometerZ\": " + str(acceleration['z']) + "}")

    gCounter += 1
