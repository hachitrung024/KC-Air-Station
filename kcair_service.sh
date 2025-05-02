#!/bin/bash
# How to use:
# chmod +x kcair_service.sh
# Install: 
# ./kcair_service.sh
# Unistall: 
# ./kcair_service.sh --remove
SERVICE_NAME="kcair"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
WORK_DIR="/home/hachi/KC-Air-Station"
RUN_SCRIPT="${WORK_DIR}/run.sh"
USER_NAME="hachi"

install_service() {
    echo "Installing systemd service '${SERVICE_NAME}'..."

    if [ ! -f "$RUN_SCRIPT" ]; then
        echo "Error: ${RUN_SCRIPT} not found. Please check the path."
        exit 1
    fi

    # Create systemd service file
    sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=KC Air Station - Read from ttyACM0
After=dev-ttyACM0.device
Requires=dev-ttyACM0.device

[Service]
Type=simple
WorkingDirectory=${WORK_DIR}
ExecStart=/bin/bash ${RUN_SCRIPT}
Restart=always
RestartSec=10
User=${USER_NAME}
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable/start the service
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_NAME}
    sudo systemctl start ${SERVICE_NAME}

    echo "Service '${SERVICE_NAME}' installed and started successfully."
    echo "Use 'sudo systemctl status ${SERVICE_NAME}' to check status."
}

remove_service() {
    echo "Removing systemd service '${SERVICE_NAME}'..."

    sudo systemctl stop ${SERVICE_NAME}
    sudo systemctl disable ${SERVICE_NAME}
    sudo rm -f ${SERVICE_FILE}
    sudo systemctl daemon-reload

    echo "Service '${SERVICE_NAME}' removed."
}

# Command line argument handling
case "$1" in
    --remove)
        remove_service
        ;;
    *)
        install_service
        ;;
esac
