#!/bin/bash

# =========================
# NFV EXAM MODE - WHITELIST WAYGROUND ONLY
# =========================

# reset rule lama biar tidak numpuk
iptables -F OUTPUT

# =========================
# IZINKAN LOCALHOST & DNS
# =========================
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# =========================
# BLOCK GOOGLE & AI TOOLS VIA HOSTS
# =========================

# hapus dulu biar tidak duplicate
sed -i '/google\|youtube\|youtu\.be\|gemini\|bard\|chatgpt\|deepseek/d' /etc/hosts

# google
echo "127.0.0.1 google.com" >> /etc/hosts
echo "127.0.0.1 www.google.com" >> /etc/hosts
echo "127.0.0.1 accounts.google.com" >> /etc/hosts
echo "127.0.0.1 docs.google.com" >> /etc/hosts
echo "127.0.0.1 gmail.com" >> /etc/hosts
echo "127.0.0.1 drive.google.com" >> /etc/hosts

# youtube
echo "127.0.0.1 youtube.com" >> /etc/hosts
echo "127.0.0.1 www.youtube.com" >> /etc/hosts
echo "127.0.0.1 youtu.be" >> /etc/hosts

# gemini
echo "127.0.0.1 gemini.google.com" >> /etc/hosts
echo "127.0.0.1 bard.google.com" >> /etc/hosts

# AI lain
echo "127.0.0.1 chatgpt.com" >> /etc/hosts
echo "127.0.0.1 chat.deepseek.com" >> /etc/hosts

# =========================
# WHITELIST WAYGROUND
# =========================

# contoh IP Wayground
# ganti sesuai hasil nslookup/dig terbaru
WAYGROUND_IPS="104.18.18.97 104.18.19.97"

for ip in $WAYGROUND_IPS; do
    iptables -A OUTPUT -p tcp -d $ip --dport 443 -j ACCEPT
    echo "Allowed: $ip (Wayground)"
done

# =========================
# BLOCK SEMUA HTTP/HTTPS LAIN
# =========================
iptables -A OUTPUT -p tcp --dport 80 -j REJECT
iptables -A OUTPUT -p tcp --dport 443 -j REJECT

echo "MODE UJIAN AKTIF - HANYA WAYGROUND DIIZINKAN"
