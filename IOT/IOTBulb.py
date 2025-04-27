# system imports
import ssl
import certifi
import sys

# mqtt imports
import paho.mqtt.client as mqtt
import paho.mqtt.enums

# pyqt imports
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

# Configuration
MQTT_BROKER = "8f02f1f20a4b41ea87204ef2a48b6c60.s1.eu.hivemq.cloud"  # Your MQTT broker
MQTT_PORT = 8883
MQTT_USERNAME = "bhavith"  # If required, else keep blank
MQTT_PASSWORD = "Bhavith@123"  # If required, else keep blank
MQTT_TOPIC = "bulb"  # Topic for subscription
MQTT_CLIENT_ID = "7730u0"

# Create SSL context for secure MQTT connection
ssl_context = ssl.create_default_context(cafile=certifi.where())

class IOTBulb(QWidget):
    """Main window to simulate the IoT bulb."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IOT Bulb Simulation")
        self.setGeometry(100, 100, 400, 400)
        self.is_on = False  # Initially, the bulb is off

    def paintEvent(self, event):
        """Handle the painting of the bulb (green when on, grey when off)."""
        painter = QPainter(self)
        
        # Set the bulb color based on the state
        if self.is_on:
            painter.setBrush(QColor(0, 255, 0))  # Green for "on" (lit)
        else:
            painter.setBrush(QColor(169, 169, 169))  # Grey for "off" (unlit)
        
        # Draw the bulb body (ellipse shape)
        painter.drawEllipse(150, 100, 100, 150)  # Bulb body shape
        
        # Draw the base of the bulb (rectangle)
        painter.setBrush(QColor(100, 100, 100))  # Gray for the base
        painter.drawRect(170, 240, 60, 20)  # Bulb base shape

    def turnOnBulb(self):
        """Turn the bulb on."""
        self.is_on = True
        self.update()

    def turnOffBulb(self):
        """Turn the bulb off."""
        self.is_on = False
        self.update()


class MQTTClient:
    """MQTT client to manage MQTT connection and messaging."""
    
    def __init__(self, bulb_window):
        self.bulb_window = bulb_window
        self.client = mqtt.Client(
            callback_api_version = paho.mqtt.enums.CallbackAPIVersion.VERSION2, 
            client_id=MQTT_CLIENT_ID)
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD) if MQTT_USERNAME else None
        self.client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    
    def on_connect(self, client, userdata, flags, reasonCode, properties):
        """Callback when connected to the MQTT broker."""
        if reasonCode == 0:
            print("✅ Connected successfully to MQTT broker!")
            client.subscribe(MQTT_TOPIC)
        else:
            print(f"❌ Failed to connect, return code {reasonCode}")

    def on_message(self, client, userdata, msg):
        """Callback when a message is received from the MQTT broker."""
        message = msg.payload.decode()
        print(f"📩 Received message: {message} on topic: {msg.topic}")
        # If message is "toggle", change the bulb state
        if message == "1":
            if self.bulb_window.is_on:
                self.bulb_window.turnOffBulb()
            else:
                self.bulb_window.turnOnBulb()

    def connect(self):
        """Connect to the MQTT broker and start listening for messages."""
        print("Connecting to MQTT broker...")
        self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        self.client.loop_start()

    def publish(self, message):
        """Publish a message to the MQTT broker."""
        print("Publishing message...")
        self.client.publish(MQTT_TOPIC, message)


def main():
    """Main function to set up the PyQt app and MQTT client."""
    app = QApplication(sys.argv)
    iot_bulb = IOTBulb()
    mqtt_client = MQTTClient(iot_bulb)
    
    # Start the MQTT client to listen for events
    mqtt_client.connect()

    # Optionally, publish a test message
    mqtt_client.publish("Hello from Python MQTT Client!")

    iot_bulb.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()