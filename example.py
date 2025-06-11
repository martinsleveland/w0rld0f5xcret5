def show_subdomain_enum_screen(self):
        self.subdomain_enum_screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Webshell generator")
        label.setFont(QFont("Courier", 18))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.subdomain_enum_target_input = QLineEdit()
        self.subdomain_enum_target_input.setPlaceholderText("Enter target URL: ")
        layout.addWidget(self.subdomain_enum_target_input)

        run_btn = QPushButton("Run webshell generator")
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

