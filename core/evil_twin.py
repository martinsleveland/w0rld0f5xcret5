def run_bash_script(self):
        try:
            # Run the bash script (make sure it's executable)
            result = subprocess.run(["./evil_twin.sh"], capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            self.output_box.setText(output)
        except Exception as e:
            self.output_box.setText(f"💥 Error: {e}")