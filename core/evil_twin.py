import requests
from scapy.all import *

print("If you want to put network card in monitor mode,")
print("then you need to type airmon-ng wlan mon or somthing i dont remember")


def run_bash_script(self):
        try:
            # Run the bash script (make sure it's executable)
            result = subprocess.run(["./evil_twin.sh"], capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            self.output_box.setText(output)
        except Exception as e:
            self.output_box.setText(f"💥 Error: {e}")
        
def run_deauth(self, ssid, channel, interface, workers):
        target_ssid = input("ssid: ")
        target_channel = input("Channel: ")
        interface = input("Choose WiFi adapter(wlan0mon): ")
        amount_workers = input("Amount of workers: ")
        
        
        self.ssid = target_ssid
        self.channel = target_channel
        self.workers = amount_workers
        
        
        