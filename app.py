from flask import Flask, render_template_string
import subprocess
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HTML = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <title>NFV SDN Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

    <style>
        :root {
            --black: #0a0a0a;
            --white: #f5f2eb;
            --green: #00e87a;
            --red: #ff3b3b;
            --muted: #5a5a5a;
            --card-bg: #141414;
            --border: #1e1e1e;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: var(--black);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'DM Sans', sans-serif;
            padding: 24px;
            overflow: hidden;
        }

        /* Background grid */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 48px 48px;
            pointer-events: none;
            z-index: 0;
        }

        /* Glow blob */
        body::after {
            content: '';
            position: fixed;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(0,232,122,0.06) 0%, transparent 70%);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 0;
            animation: pulse 6s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1); }
            50% { opacity: 1; transform: translate(-50%, -50%) scale(1.15); }
        }

        .container {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 480px;
            animation: fadeUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(32px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* Top badge */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 6px 14px;
            font-size: 11px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--green);
            font-weight: 500;
            margin-bottom: 28px;
        }

        .badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--green);
            animation: blink 1.4s ease-in-out infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.2; }
        }

        /* Main card */
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 40px;
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0,232,122,0.4), transparent);
        }

        /* Corner decoration */
        .card-corner {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 32px;
            opacity: 0.15;
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            color: var(--white);
            letter-spacing: -2px;
            user-select: none;
        }

        h1 {
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            font-size: 40px;
            color: var(--white);
            line-height: 1.05;
            letter-spacing: -0.03em;
            margin-bottom: 12px;
        }

        h1 span {
            color: var(--green);
        }

        p {
            color: var(--muted);
            font-size: 14px;
            line-height: 1.7;
            font-weight: 300;
            margin-bottom: 36px;
            max-width: 340px;
        }

        /* Divider */
        .divider {
            height: 1px;
            background: var(--border);
            margin-bottom: 32px;
        }

        /* Buttons */
        .btn-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 16px 20px;
            border-radius: 14px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            font-family: 'DM Sans', sans-serif;
            letter-spacing: 0.01em;
            transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
            border: 1px solid transparent;
            position: relative;
            overflow: hidden;
        }

        .btn::after {
            content: '';
            position: absolute;
            inset: 0;
            background: rgba(255,255,255,0.06);
            opacity: 0;
            transition: opacity 0.15s ease;
        }

        .btn:hover::after { opacity: 1; }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn:active {
            transform: translateY(0px);
        }

        .btn-start {
            background: var(--green);
            color: #0a0a0a;
            box-shadow: 0 0 0 0 rgba(0,232,122,0.4);
        }

        .btn-start:hover {
            box-shadow: 0 8px 24px rgba(0,232,122,0.25);
        }

        .btn-stop {
            background: transparent;
            color: var(--red);
            border-color: rgba(255,59,59,0.25);
        }

        .btn-stop:hover {
            background: rgba(255,59,59,0.08);
            border-color: rgba(255,59,59,0.5);
            box-shadow: 0 8px 24px rgba(255,59,59,0.1);
        }

        .btn-icon {
            font-size: 16px;
            line-height: 1;
        }

        /* Info strip */
        .info-strip {
            margin-top: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(0,232,122,0.05);
            border: 1px solid rgba(0,232,122,0.12);
            border-radius: 10px;
            padding: 12px 16px;
            color: rgba(245,242,235,0.5);
            font-size: 12px;
            line-height: 1.5;
        }

        .info-icon {
            font-size: 16px;
            flex-shrink: 0;
        }

        /* Animated number decoration */
        .deco-number {
            position: absolute;
            bottom: -10px;
            right: 32px;
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            font-size: 120px;
            color: rgba(255,255,255,0.02);
            letter-spacing: -8px;
            line-height: 1;
            user-select: none;
            pointer-events: none;
        }
    </style>
</head>
<body>

<div class="container">

    <div class="badge">
        <span class="badge-dot"></span>
        NFV Exam Controller
    </div>

    <div class="card">
        <div class="card-corner">01</div>
        <div class="deco-number">SYS</div>

        <h1>Exam<br><span>System</span></h1>

        <p>
            Sistem ujian berbasis NFV untuk mengontrol akses internet
            selama ujian berlangsung secara otomatis.
        </p>

        <div class="divider"></div>

        <div class="btn-group">
            <a href="/start" class="btn btn-start">
                <span class="btn-icon">▶</span>
                Start Exam
            </a>
            <a href="/stop" class="btn btn-stop">
                <span class="btn-icon">■</span>
                Stop Exam
            </a>
        </div>

        <div class="info-strip">
            <span class="info-icon">🔒</span>
            Quizizz & Google Forms tetap dapat diakses selama mode ujian aktif.
        </div>
    </div>

</div>

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/start')
def start():
    subprocess.run([
        'sudo',
        'bash',
        f'{BASE_DIR}/block.sh'
    ])

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Syne:wght@800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
        <style>
            * { margin:0; padding:0; box-sizing:border-box; }
            body {
                background: #0a0a0a;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                font-family: "DM Sans", sans-serif;
                gap: 8px;
                overflow: hidden;
            }
            body::before {
                content: "";
                position: fixed;
                inset: 0;
                background: radial-gradient(circle at center, rgba(0,232,122,0.12) 0%, transparent 65%);
                pointer-events: none;
                animation: expand 0.6s ease both;
            }
            @keyframes expand {
                from { opacity:0; transform:scale(0.8); }
                to   { opacity:1; transform:scale(1); }
            }
            .status-dot {
                width: 12px; height: 12px;
                background: #00e87a;
                border-radius: 50%;
                box-shadow: 0 0 20px rgba(0,232,122,0.8);
                animation: blink 1.2s ease-in-out infinite;
                margin-bottom: 12px;
            }
            @keyframes blink {
                0%,100%{opacity:1;} 50%{opacity:0.3;}
            }
            h1 {
                font-family: "Syne", sans-serif;
                font-weight: 800;
                font-size: clamp(32px, 8vw, 60px);
                color: #00e87a;
                letter-spacing: -0.03em;
                text-align: center;
                animation: slideUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.1s both;
            }
            p {
                color: rgba(255,255,255,0.35);
                font-size: 14px;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin-bottom: 36px;
                animation: slideUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.2s both;
            }
            @keyframes slideUp {
                from { opacity:0; transform:translateY(20px); }
                to   { opacity:1; transform:translateY(0); }
            }
            a {
                background: transparent;
                color: rgba(255,255,255,0.5);
                padding: 12px 28px;
                border-radius: 12px;
                text-decoration: none;
                font-size: 14px;
                border: 1px solid rgba(255,255,255,0.1);
                transition: 0.2s ease;
                animation: slideUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.3s both;
            }
            a:hover {
                background: rgba(255,255,255,0.05);
                color: white;
                border-color: rgba(255,255,255,0.2);
            }
        </style>
    </head>
    <body>
        <div class="status-dot"></div>
        <h1>MODE UJIAN AKTIF</h1>
        <p>Akses internet sedang dibatasi</p>
        <a href="/">← Kembali</a>
    </body>
    </html>
    '''

@app.route('/stop')
def stop():
    subprocess.run([
        'sudo',
        'bash',
        f'{BASE_DIR}/unblock.sh'
    ])

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Syne:wght@800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
        <style>
            * { margin:0; padding:0; box-sizing:border-box; }
            body {
                background: #0a0a0a;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                font-family: "DM Sans", sans-serif;
                gap: 8px;
                overflow: hidden;
            }
            body::before {
                content: "";
                position: fixed;
                inset: 0;
                background: radial-gradient(circle at center, rgba(255,59,59,0.10) 0%, transparent 65%);
                pointer-events: none;
                animation: expand 0.6s ease both;
            }
            @keyframes expand {
                from { opacity:0; transform:scale(0.8); }
                to   { opacity:1; transform:scale(1); }
            }
            .status-dot {
                width: 12px; height: 12px;
                background: #ff3b3b;
                border-radius: 50%;
                box-shadow: 0 0 20px rgba(255,59,59,0.8);
                margin-bottom: 12px;
            }
            h1 {
                font-family: "Syne", sans-serif;
                font-weight: 800;
                font-size: clamp(28px, 7vw, 56px);
                color: #ff3b3b;
                letter-spacing: -0.03em;
                text-align: center;
                animation: slideUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.1s both;
            }
            p {
                color: rgba(255,255,255,0.35);
                font-size: 14px;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin-bottom: 36px;
                animation: slideUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.2s both;
            }
            @keyframes slideUp {
                from { opacity:0; transform:translateY(20px); }
                to   { opacity:1; transform:translateY(0); }
            }
            a {
                background: transparent;
                color: rgba(255,255,255,0.5);
                padding: 12px 28px;
                border-radius: 12px;
                text-decoration: none;
                font-size: 14px;
                border: 1px solid rgba(255,255,255,0.1);
                transition: 0.2s ease;
                animation: slideUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.3s both;
            }
            a:hover {
                background: rgba(255,255,255,0.05);
                color: white;
                border-color: rgba(255,255,255,0.2);
            }
        </style>
    </head>
    <body>
        <div class="status-dot"></div>
        <h1>MODE UJIAN NONAKTIF</h1>
        <p>Akses internet telah dipulihkan</p>
        <a href="/">← Kembali</a>
    </body>
    </html>
    '''

app.run(host='0.0.0.0', port=5000)
