# Simple NFV Exam Filter

Mini project sistem filtering internet saat ujian menggunakan Flask, IPTables, dan `/etc/hosts` berbasis konsep NFV sederhana.

---

## Features

- Start / Stop Exam Mode
- Hybrid Filtering System
- Website Blocking
- Simple Flask Interface
- Linux-based Network Control

---

## Technologies Used

- Python
- Flask
- IPTables
- Linux Ubuntu

---

## Project Structure

```bash
app.py
block.sh
unblock.sh
README.md
```

---

## How to Run

### 1. Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install flask
```

### 2. Give Execute Permission

```bash
chmod +x block.sh
chmod +x unblock.sh
```

### 3. Run Application

```bash
python3 app.py
```

---

## Open Browser

```text
http://localhost:5000
```

---

## Usage

### Start Exam Mode
Click:
```text
Start Exam
```

### Stop Exam Mode
Click:
```text
Stop Exam
```

---

## Notes

This project is a simple NFV-based prototype for educational purposes.
