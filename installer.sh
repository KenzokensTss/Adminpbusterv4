#!/bin/bash

echo "Installing AdminPBuster v4 dependencies..."

# Versi v4 tidak lagi memerlukan paket sistem eksternal
# seperti curl, toilet, atau lolcat.
echo "System package dependencies removed."

echo "Installing required Python packages..."
pip3 install requests termcolor urllib3 --break-system-packages

echo "Making AdminPBuster.py executable..."
# Ganti 'AdminPBuster.py' jika Anda menyimpan skrip Python dengan nama lain
chmod +x AdminPBuster.py

echo -e "\nInstallation complete!"
echo "Run basic scan: ./AdminPBuster.py -t example.com -th 10"
echo "Run with random agent: ./AdminPBuster.py -t example.com -th 10 -ua"
echo "Run with custom codes: ./AdminPBuster.py -t example.com --status-codes 200,302,403"
echo "Run with local wordlist: ./AdminPBuster.py -t example.com -w /path/to/my_list.txt"