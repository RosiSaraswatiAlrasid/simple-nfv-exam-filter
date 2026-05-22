#!/bin/bash

# =========================
# NONAKTIFKAN MODE UJIAN
# =========================

# hapus semua rules OUTPUT
iptables -F OUTPUT

# =========================
# BERSIHKAN HOSTS
# =========================

sed -i '/google\|youtube\|youtu\.be\|gemini\|bard\|chatgpt\|deepseek/d' /etc/hosts

# =========================
# FLUSH DNS CACHE
# =========================

resolvectl flush-caches 2>/dev/null || true

echo "UJIAN SELESAI - INTERNET NORMAL"
