import sys
import os
import subprocess
from typing import Literal
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtCore import QProcess, QProcessEnvironment


class VPNWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state: Literal["Connected", "Disconnected"] = self.get_vpn_state()

        # Configure main window
        self.setWindowTitle("Cisco VPN Connector")
        self.setFixedSize(400, 400)

        # Create widgets
        self.server_input = QLineEdit("vpn.shanghai.nyu.edu")
        self.user_input = QLineEdit()
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.log_output = QTextEdit()
        self.connect_btn = QPushButton()
        self.update_button_state()

        # Check environment variables and set default values
        username_env = os.getenv(
            "VPN_USER"
        )  # Check if VPN_USER is set in the environment
        password_env = os.getenv(
            "VPN_PASS"
        )  # Check if VPN_PASS is set in the environment

        if username_env:
            self.user_input.setText(
                username_env
            )  # Prefill with environment variable value
        else:
            self.user_input.setText("")  # Leave empty if not set

        if password_env:
            self.pass_input.setText(
                password_env
            )  # Prefill with environment variable value
        else:
            self.pass_input.setText("")  # Leave empty if not set

        # Layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("VPN Server:"))
        layout.addWidget(self.server_input)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.pass_input)
        layout.addWidget(self.connect_btn)
        layout.addWidget(QLabel("Connection Log:"))
        layout.addWidget(self.log_output)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Process handling
        self.process = None
        self.connect_btn.clicked.connect(self.toggle_connection)

    def get_vpn_state(self) -> Literal["Connected", "Disconnected"]:
        """Synchronously check VPN connection state"""
        try:
            result = subprocess.check_output(
                ["/opt/cisco/secureclient/bin/vpn", "-s", "stats"],
                stderr=subprocess.STDOUT,
                text=True,
            )
            return "Connected" if "state: Connected" in result else "Disconnected"
        except Exception as e:
            print(f"Error checking VPN state: {str(e)}")
            return "Unknown"

    def update_button_state(self):
        """Update button based on current VPN state"""
        if self.state == "Connected":
            self.connect_btn.setText("Disconnect VPN")
            self.server_input.setReadOnly(True)
            self.user_input.setReadOnly(True)
            self.pass_input.setReadOnly(True)
            self.connect_btn.clicked.connect(self.disconnect_vpn)
        else:
            self.connect_btn.setText("Connect VPN")

            self.server_input.setReadOnly(False)
            self.user_input.setReadOnly(False)
            self.pass_input.setReadOnly(False)
            self.connect_btn.clicked.connect(self.connect_vpn)

    def toggle_connection(self):
        if (
            self.process
            and self.process.state() == QProcess.ProcessState.Running
            and self.state == "Disconnected"
        ):
            self.process.terminate()
            self.connect_btn.setText("Connect")
        else:
            self.connect_vpn()

    def connect_vpn(self):
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        self.process.finished.connect(self.connection_finished)

        # Build command
        vpn_command = [
            "/opt/cisco/secureclient/bin/vpn",
            "-s",
            "connect",
            self.server_input.text(),
        ]

        self.log_output.clear()
        self.log_output.append("Starting connection...")

        # Set environment variables for credentials
        env = QProcessEnvironment.systemEnvironment()
        env.insert("VPN_USER", self.user_input.text())
        env.insert("VPN_PASS", self.pass_input.text())
        self.process.setProcessEnvironment(env)

        self.process.start(vpn_command[0], vpn_command[1:])
        self.state = "Connected"
        self.update_button_state()

    def disconnect_vpn(self):
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        self.process.finished.connect(self.connection_finished)

        # Build command
        vpn_command = [
            "/opt/cisco/secureclient/bin/vpn",
            "-s",
            "disconnect",
        ]

        self.log_output.clear()
        self.log_output.append("Disonnecting...")
        self.process.start(vpn_command[0], vpn_command[1:])

        self.state = "Disconnected"
        self.update_button_state()

    def handle_output(self):
        data = self.process.readAllStandardOutput()
        self.log_output.append(data.data().decode().strip())

    def handle_error(self):
        data = self.process.readAllStandardError()
        self.log_output.append(
            f"<font color='red'>{data.data().decode().strip()}</font>"
        )

    def connection_finished(self):
        self.connect_btn.setText("Connect")
        self.log_output.append("Connection closed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VPNWindow()
    window.show()
    sys.exit(app.exec())
