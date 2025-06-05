import requests


def run_bash_script(self):
        try:
            # Run the bash script (make sure it's executable)
            result = subprocess.run(["./evil_twin.sh"], capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            self.output_box.setText(output)
        except Exception as e:
            self.output_box.setText(f"💥 Error: {e}")
        
def run_deauth(self, ssid, channel, workers):
        
        target_ssid = input("ssid: ")
        target_channel = input("Channel: ")
        amount_workers = input("Amount of workers: ")
        
        self.ssid = target_ssid
        self.channel = target_channel
        self.workers = amount_workers