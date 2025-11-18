# BHEH's AdminPBuster

<p align="center">
<a href="https://www.blackhatethicalhacking.com"><img src="https://www.blackhatethicalhacking.com/wp-content/uploads/2022/06/BHEH_logo.png" width="300px" alt="BHEH"></a>
</p>

<p align="center">

**If you think you can hide your Admin Panel, think again... Find it with AdminPBuster.**

</p>

---

**AdminPBuster** is written by **Chris "SaintDruG" Abou-Chabke** from **Black Hat Ethical Hacking** and is designed specifically for **Red Teams**, **Offensive Security Experts**, and **Bug Bounty Hunters** looking to discover hidden or obscured admin panels efficiently.

*(v4 Mod): This version has been updated to remove external system dependencies (like curl) and uses Python's native 'requests' library, making it fully cross-platform. It also includes more flexible scanning options.*

---

<p align="center">
<img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnFyZDBza3luMnl2c2gwNDcwMmp3YTY5YnA0dWI0ZjBocmR2Z3J0byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/11shDO8NnZDYpa/giphy.gif" width="500px" alt="Matrix Animation">
</p>


---

## Description

**AdminPBuster** is a Red Teaming Recon tool to find hidden admin panels on web applications using brute-forcing.
Instead of bundling a static wordlist and bloating the tool, it **fetches an updated admin panel wordlist** directly from our GitHub repository (or optionally, uses a local wordlist provided by you).

- This keeps the tool **lightweight** and **easy to maintain**.
- Whenever we update the hosted wordlist, **the tool automatically benefits**, without needing to update the script itself.

**Key technical goodies:**
- Multithreaded scanning using Python's native `requests` library
- Flexible protocol handling (`--http` or default `https`)
- Flexible domain handling (`--no-www` flag)
- Real redirect following (`allow_redirects=True`)
- No proxychains/Tor dependency
- Optional randomized User-Agent headers (`-ua`) to simulate real traffic
- Optional custom wordlist (`-w`)
- Optional custom status code reporting (`--status-codes`)

AdminPBuster focuses on **speed**, **reliability**, and **accuracy** while staying very simple to operate, going through 10,000+ wordlists.

---

## The Flow Behind It

- **Fetch/Load Wordlist**
  Downloads the latest `magic_admin_paths.txt` from GitHub or loads a user-specified local file.

- **Prepare Target Domain**
  Prepares the domain based on user flags (HTTP/HTTPS, www/non-www).

- **Build and Launch Requests**
  Constructs and sends lightweight web requests using Python's `requests` library.

- **Multithreaded Scanning**
  Scans many paths at once using multiple threads to improve speed.

- **Color-Coded Result Parsing**
  Displays results with colors based on HTTP response codes for easy reading:
  - 200 (OK) in green
  - 301/302 (Redirects) in cyan
  - 403 (Forbidden) in yellow
  - 404 (Not Found) in red
  - Other codes in magenta

- **Log Successful Admin Panels**
  Admin panels found (based on your specified status codes) are automatically saved inside a folder under `results/{target_domain}/found_panels.txt`.

---

## Features

- Lightweight and *truly* portable (single Python3 script, no external binaries)
- Automatic admin paths updates from GitHub (default)
- Support for custom local wordlists (`-w`)
- Flexible status code detection (e.g., `200,302,403`)
- Realistic User-Agent randomization with `-ua`
- Multithreaded scanning (default 5 threads, customizable)
- Flexible SSL/TLS and domain handling
- Color-coded live scan results
- Only desired status codes saved
- Fancy banners, motivational quotes, rainbow CLI styling!
- Over 10,000+ Wordlists Specifically Aimed for Admin Panel Search

---

## Quick Demo Preview

![adminPBuster_v3](https://github.com/user-attachments/assets/ad81e2f6-2ed3-4400-9484-9b4e945ad864)

---

# Compatibility:

This tool has been tested on Kali Linux, but v4 is cross-platform and should work on Windows, macOS, and other Linux distros with Python 3.

---

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/blackhatethicalhacking/AdminPBuster.git](https://github.com/blackhatethicalhacking/AdminPBuster.git)
   cd AdminPanelFetcher
Make the installer executable:

Bash

chmod +x installer.sh
Run the installer:

Bash

./installer.sh
What installer.sh does
Installs required Python3 libraries:

requests

termcolor

urllib3

(System dependencies curl, toilet, lolcat are no longer required for v4)

Makes AdminPBuster.py executable automatically

After installation, simply run:

Bash

./AdminPBuster.py -t example.com -th 10
Optionally with randomized User-Agent:

Bash

./AdminPBuster.py -t example.com -th 10 -ua
New v4 Usage Examples:

Scan for multiple status codes (e.g., found, redirect, forbidden):

Bash

./AdminPBuster.py -t example.com -th 10 --status-codes 200,302,403
Scan using your own local wordlist:

Bash

./AdminPBuster.py -t example.com -w /path/to/my_wordlist.txt
Scan a target on HTTP and without forcing 'www':

Bash

./AdminPBuster.py -t sub.example.com --http --no-www
Disclaimer
This tool is provided for educational and research purpose only. The author of this project are no way responsible for any misuse of this tool. We use it to test under NDA agreements with clients and their consents for pentesting purposes and we never encourage to misuse or take responsibility for any damage caused !

<h2 align="center"> <a href="https://store.blackhatethicalhacking.com/" target="_blank">BHEH Official Merch</a> </h2>

<p align="center"> Introducing our Merch Store, designed for the Offensive Security community. Explore a curated collection of apparel and drinkware, perfect for both professionals and enthusiasts. Our selection includes premium t-shirts, hoodies, and mugs, each featuring bold hacking-themed slogans and graphics that embody the spirit of red teaming and offensive security. Hack with style and showcase your dedication to hacker culture with gear that’s as dynamic and resilient as you are. 😊 </p>

<p align="center">

<img src="https://github.com/blackhatethicalhacking/blackhatethicalhacking/blob/main/Merch_Promo.gif" width="540px" height="540"> </p>