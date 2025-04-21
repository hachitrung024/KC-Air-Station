#!/bin/bash

set -e

# Kiểm tra python3 đã cài chưa
if ! command -v python3 &> /dev/null
then
    echo "Python 3 chưa được cài. Cài bằng: sudo apt install python3"
    exit 1
fi

# Kiểm tra python3-venv đã có chưa
if ! dpkg -s python3-venv &> /dev/null
then
    echo "Chưa có python3-venv. Cài bằng: sudo apt install python3-venv"
    exit 1
fi

# Tạo virtual environment (kế thừa gói hệ thống)
[ -d "venv" ] || python3 -m venv venv --system-site-packages

# Kích hoạt venv
source venv/bin/activate

# Cập nhật pip và cài requirements
pip install --upgrade pip
pip install -r requirements.txt
