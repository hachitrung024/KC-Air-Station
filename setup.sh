#!/bin/bash

set -e

# Kiểm tra python3.11 đã cài chưa
if ! command -v python3.11 &> /dev/null
then
    echo "Python 3.11 chưa được cài. Cài bằng: sudo apt install python3.11 python3.11-venv python3.11-dev"
    exit 1
fi

# Tạo virtual environment (kế thừa gói hệ thống)
[ -d "venv" ] || python3.11 -m venv venv --system-site-packages

# Kích hoạt venv
source venv/bin/activate

# Cập nhật pip và cài requirements
pip install --upgrade pip
pip install -r requirements.txt
