#!/usr/bin/env python3

import requests
import signal
import sys
import os
import queue
import argparse
import time
import random
from threading import Thread, Lock
from urllib.parse import urlparse
import urllib3
from pathlib import Path
from termcolor import colored

# --- CATATAN MODIFIKASI (v4.0 oleh Kenzo & Gemini) ---
# Skrip ini adalah versi modifikasi dari AdminPBuster v3.0 asli.
# Modifikasi ini mematuhi lisensi GNU General Public License v3 (GPL v3).
#
# Changelog (v4.0):
# - Menghapus ketergantungan pada alat sistem eksternal: 'curl', 'toilet', 'lolcat'.
# - Semua permintaan web sekarang ditangani secara native di Python menggunakan library 'requests'.
# - Menambahkan fleksibilitas penanganan URL:
#   - '--http': Memindai HTTP, bukan memaksa HTTPS.
#   - '--no-www': Mencegah pemaksaan awalan 'www.' pada domain.
# - Menambahkan deteksi kode status yang fleksibel:
#   - '--status-codes': Memungkinkan pengguna menentukan kode yang dilaporkan (misal: "200,302,403").
# - Menambahkan dukungan wordlist lokal:
#   - '-w, --wordlist': Menggunakan file lokal, bukan mengambil dari URL.
# - Mengganti panggilan 'lolcat'/'toilet' dengan 'termcolor' untuk banner.
# --- AKHIR CATATAN MODIFIKASI ---

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Informasi Asli
VERSION = "3.0 (Modded)"
AUTHOR = "Chris 'SaintDruG' Abou-Chabke"
TEAM = "Black Hat Ethical Hacking"
PATHS_URL = "https://raw.githubusercontent.com/blackhatethicalhacking/AdminPBuster/refs/heads/main/magic_admin_paths.txt"

request_counter = 0
counter_lock = Lock()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
]

def handle_interrupt(signal, frame):
    print(colored("\n[!] Dihentikan oleh pengguna. Keluar...", "red", attrs=["bold"]))
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

def rainbow_text(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    return ''.join(colored(char, colors[i % len(colors)], attrs=["bold"]) if char != " " else " " for i, char in enumerate(text))

def print_ascii_and_quote():
    print("")
    quotes = [
        "The supreme art of war is to subdue the enemy without fighting.",
        "All warfare is based on deception.",
        "He who knows when he can fight and when he cannot, will be victorious.",
        "The whole secret lies in confusing the enemy, so that he cannot fathom our real intent.",
        "To win one hundred victories in one hundred battles is not the acme of skill. To subdue the enemy without fighting is the acme of skill."
    ]
    random_quote = random.choice(quotes)
    print(rainbow_text(f"Offensive Security Tip: {random_quote} - Sun Tzu"))
    time.sleep(1)
    print(rainbow_text("MEANS, IT'S ☕ 1337 ⚡ TIME, 369 ☯"))
    time.sleep(1)

def print_toilet_banner_lolcat():
    os.system("clear" if os.name == 'posix' else 'cls')
    print(rainbow_text("AdminPBuster"))

def print_help_colored():
    print_ascii_and_quote()
    print_toilet_banner_lolcat()
    print(colored(f"\nVersi: {VERSION}", "yellow"))
    print(colored(f"Penulis Asli: {AUTHOR}", "yellow"))
    print(colored(f"Tim: {TEAM}\n", "yellow"))

    print(colored("Penggunaan: ", "cyan", attrs=["bold"]) + colored("./AdminPBuster.py -t example.com", "white"))
    print(colored("(Berikan domain saja tanpa kurung atau https)\n", "yellow"))

    print(colored("Opsi:", "cyan", attrs=["bold"]))
    print(colored("  -h, --help             ", "white") + "Tampilkan pesan bantuan ini dan keluar")
    print(colored("  -t, --target TARGET    ", "white") + "Target domain (misal: example.com)")
    print(colored("  -th, --threads THREADS ", "white") + "Jumlah threads (default: 5)")
    print(colored("  -ua, --random-agent    ", "white") + "Gunakan User-Agent acak yang realistis")
    print(colored("  -w, --wordlist FILE    ", "white") + "Gunakan file wordlist lokal (bukan dari URL)")
    print(colored("  --http                 ", "white") + "Pindai menggunakan HTTP, bukan HTTPS (default: HTTPS)")
    print(colored("  --no-www               ", "white") + "Jangan paksakan awalan 'www.' pada domain")
    print(colored("  --status-codes CODES   ", "white") + 'Kode HTTP untuk dilaporkan, dipisah koma (default: "200")\n')

    print(colored("Ditulis oleh ", "green") + colored(f"{AUTHOR}", "magenta") + colored(f" untuk {TEAM}", "green"))
    print(colored("© Hak Cipta Dilindungi 2025 — Gunakan Hanya Untuk Pengujian Etis.", "yellow"))
    print(colored("BHEH tidak bertanggung jawab atas penyalahgunaan alat ini.", "red"))

def print_rainbow_banner():
    os.system("clear" if os.name == 'posix' else 'cls')
    print("\n" + rainbow_text("Admin Panel Buster"))
    print(colored(f"\nVersi: {VERSION}", "yellow"))
    print(colored(f"Penulis Asli: {AUTHOR}", "yellow"))
    print(colored(f"Tim: {TEAM}", "yellow"))

def countdown():
    print(colored("\nMemulai serangan dalam:", "cyan", attrs=["bold"]))
    for i in range(5, 0, -1):
        print(colored(str(i), "cyan", attrs=["bold"]))
        time.sleep(1)
    print(colored("\n[+] Serangan Dimulai!\n", "green", attrs=["bold"]))

def fetch_admin_paths():
    try:
        print(colored(f"[+] Mengambil wordlist dari {PATHS_URL}...", "cyan"))
        response = requests.get(PATHS_URL, timeout=10)
        response.raise_for_status()
        return [line.strip() for line in response.text.splitlines() if line.strip()]
    except Exception as e:
        print(colored(f"[!] Gagal mengambil admin paths: {e}", "red", attrs=["bold"]))
        sys.exit(1)

def load_local_paths(filepath):
    try:
        print(colored(f"[+] Memuat wordlist dari {filepath}...", "cyan"))
        with open(filepath, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(colored(f"[!] Gagal memuat file wordlist lokal: {e}", "red", attrs=["bold"]))
        sys.exit(1)

def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
    except:
        print(colored("[!] Tidak ada koneksi internet!", "red", attrs=["bold"]))
        sys.exit(1)

def clean_domain(domain_url):
    parsed = urlparse(domain_url)
    domain = parsed.netloc or parsed.path
    return domain.replace(":", "_")

def color_for_status(code):
    if code == "200":
        return "green"
    elif code in ["301", "302"]:
        return "cyan"
    elif code == "403":
        return "yellow"
    elif code == "404":
        return "red"
    else:
        return "magenta"

def scan_url(session, target_domain, path_queue, results, timeout, random_ua, use_http, force_www, target_codes):
    global request_counter
    while not path_queue.empty():
        path = path_queue.get()

        protocol = "http" if use_http else "https"
        
        if force_www and not target_domain.startswith("www."):
            fixed_domain = "www." + target_domain
        else:
            fixed_domain = target_domain

        full_url = f"{protocol}://{fixed_domain.rstrip('/')}/{path.lstrip('/')}"

        with counter_lock:
            request_counter += 1
            number = request_counter

        headers = {}
        if random_ua:
            headers['User-Agent'] = random.choice(USER_AGENTS)

        try:
            response = session.get(full_url, timeout=timeout, verify=False, allow_redirects=True, headers=headers)
            http_code = str(response.status_code)

        except requests.exceptions.RequestException as e:
            http_code = "Koneksi Gagal"

        color = color_for_status(http_code)
        print(colored(f"[{number}] {full_url} -> (HTTP {http_code})", color, attrs=["bold"]))

        if http_code in target_codes:
            results.append(full_url)

        path_queue.task_done()

def admin_panel_buster(target_domain, threads, random_ua, wordlist_file, use_http, force_www, target_codes):
    
    if wordlist_file:
        paths = load_local_paths(wordlist_file)
    else:
        paths = fetch_admin_paths()
    
    print(colored(f"[+] Total {len(paths)} path untuk dipindai.", "cyan"))

    q = queue.Queue()
    for path in paths:
        q.put(path)

    results = []
    thread_list = []

    domain_folder = f"results/{clean_domain(target_domain)}"
    os.makedirs(domain_folder, exist_ok=True)
    output_file = os.path.join(domain_folder, "found_panels.txt")

    # Buat satu session untuk semua thread
    session = requests.Session()

    for _ in range(threads):
        t = Thread(target=scan_url, args=(session, target_domain, q, results, 5, random_ua, use_http, force_www, target_codes))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    if results:
        print(colored(f"\n[✓] Ditemukan {len(results)} kemungkinan panel admin!", "green", attrs=["bold"]))
        unique_results = sorted(list(set(results)))
        with open(output_file, "w") as f:
            for url in unique_results:
                print(colored(f" - {url}", "green"))
                f.write(url + "\n")
        print(colored(f"\n[+] Hasil disimpan ke {output_file}", "cyan", attrs=["bold"]))
    else:
        print(colored("\n[!] Tidak ada panel admin yang ditemukan.", "yellow"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-t", "--target", help="Target domain (misal: example.com)")
    parser.add_argument("-th", "--threads", type=int, default=5, help="Jumlah threads (default: 5)")
    parser.add_argument("-ua", "--random-agent", action="store_true", help="Gunakan User-Agent acak yang realistis")
    parser.add_argument("-w", "--wordlist", help="Gunakan file wordlist lokal (bukan dari URL)")
    parser.add_argument("--http", action="store_true", help="Pindai menggunakan HTTP, bukan HTTPS (default: HTTPS)")
    parser.add_argument("--no-www", action="store_true", help="Jangan paksakan awalan 'www.' pada domain")
    parser.add_argument("--status-codes", default="200", help='Kode HTTP untuk dilaporkan, dipisah koma (default: "200")')
    parser.add_argument("-h", "--help", action="store_true", help="Tampilkan pesan bantuan dan keluar")
    
    ARGS = parser.parse_args()

    if ARGS.help or not ARGS.target:
        print_help_colored()
        sys.exit(0)

    print_rainbow_banner()
    if not ARGS.wordlist:
        check_internet_connection() # Hanya periksa koneksi jika kita perlu mengunduh wordlist
    
    countdown()

    force_www = not ARGS.no_www
    target_codes = [code.strip() for code in ARGS.status_codes.split(',')]

    admin_panel_buster(ARGS.target, ARGS.threads, ARGS.random_agent, ARGS.wordlist, ARGS.http, force_www, target_codes)