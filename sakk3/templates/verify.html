<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAKK | Document Verification Result</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-success: #022c22;
            --bg-danger: #3b0707;
            --accent-success: #10b981;
            --accent-danger: #ef4444;
            --panel: rgba(15, 23, 42, 0.75);
            --border-valid: rgba(16, 185, 129, 0.3);
            --border-invalid: rgba(239, 68, 68, 0.3);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body { 
            background: {% if valid %}radial-gradient(circle at 50% 20%, #064e3b 0%, #022c22 60%, #050b14 100%){% else %}radial-gradient(circle at 50% 20%, #7f1d1d 0%, #3b0707 60%, #050b14 100%){% endif %}; 
            color: var(--text-main);
            font-family: var(--font-sans);
            padding: 24px 16px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            width: 100%;
            max-width: 520px;
            position: relative;
        }

        .card {
            background: var(--panel);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid {% if valid %}var(--border-valid){% else %}var(--border-invalid){% endif %};
            border-radius: 20px;
            padding: 32px 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 30px {% if valid %}rgba(16, 185, 129, 0.15){% else %}rgba(239, 68, 68, 0.2){% endif %};
            text-align: center;
        }

        .status-badge {
            width: 84px;
            height: 84px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px auto;
            background: {% if valid %}rgba(16, 185, 129, 0.15){% else %}rgba(239, 68, 68, 0.15){% endif %};
            border: 2px solid {% if valid %}var(--accent-success){% else %}var(--accent-danger){% endif %};
            box-shadow: 0 0 25px {% if valid %}rgba(16, 185, 129, 0.4){% else %}rgba(239, 68, 68, 0.4){% endif %};
            {% if not valid %}animation: pulseWarning 1.5s infinite;{% endif %}
        }

        @keyframes pulseWarning {
            0% { transform: scale(1); box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }
            50% { transform: scale(1.05); box-shadow: 0 0 35px rgba(239, 68, 68, 0.6); }
            100% { transform: scale(1); box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }
        }

        h1 {
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 6px;
            color: #fff;
        }

        .subtitle {
            font-size: 13px;
            color: {% if valid %}var(--accent-success){% else %}var(--accent-danger){% endif %};
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        .desc {
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 24px;
        }

        .section-title {
            text-align: left;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .info-card {
            background: rgba(10, 15, 29, 0.6);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 16px;
            text-align: left;
            margin-bottom: 18px;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 13px;
        }

        .info-row:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .info-row:first-child {
            padding-top: 0;
        }

        .info-label {
            color: var(--text-muted);
            font-size: 11px;
            flex-shrink: 0;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            min-width: 90px;
        }

        .info-value {
            color: #fff;
            font-weight: 600;
            word-break: break-word;
            text-align: right;
        }

        .highlight-val {
            color: #38bdf8;
            font-weight: 700;
            font-size: 14px;
        }

        .crypto-box {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 12px;
            text-align: left;
            margin-bottom: 20px;
        }

        .crypto-title {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
            display: flex;
            justify-content: space-between;
        }

        .crypto-hash {
            font-family: var(--font-mono);
            font-size: 11px;
            color: #cbd5e1;
            word-break: break-all;
            background: rgba(0,0,0,0.3);
            padding: 8px;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .zero-retention-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            color: #94a3b8;
            background: rgba(255, 255, 255, 0.05);
            padding: 6px 12px;
            border-radius: 20px;
            margin-bottom: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 100%;
            padding: 12px 20px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border-subtle);
            color: #fff;
            text-align: center;
            border-radius: 10px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .btn:hover {
            background: rgba(255, 255, 255, 0.16);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            {% if valid %}
            <div class="status-badge">
                <svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
            </div>
            <h1>Authentic & Verified Document</h1>
            <div class="subtitle">AUTHENTIC CRYPTOGRAPHIC SEAL</div>
            <p class="desc">The digital signature has been successfully verified. The file content and metadata are cryptographically intact with no tampering detected.</p>
            {% else %}
            <div class="status-badge">
                <svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            </div>
            <h1>Warning: Invalid or Tampered Document</h1>
            <div class="subtitle">FORGERY DETECTED / INVALID SEAL</div>
            <p class="desc" style="color: #fca5a5;">Verification failed! The file content or metadata may have been modified, or the seal is unauthorized.</p>
            {% endif %}

            <!-- Metadata Box -->
            {% if metadata and metadata|length > 0 %}
            <div class="section-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                <span>Seal Metadata</span>
            </div>
            <div class="info-card">
                {% for field in metadata %}
                <div class="info-row">
                    <span class="info-label">{{ field.key }}:</span>
                    <span class="info-value{% if loop.first %} highlight-val{% endif %}">{{ field.value }}</span>
                </div>
                {% endfor %}
            </div>
            {% endif %}

            <!-- Document Info -->
            <div class="section-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="3" x2="9" y2="21"/></svg>
                <span>Document Info</span>
            </div>
            <div class="info-card">
                <div class="info-row">
                    <span class="info-label">Filename:</span>
                    <span class="info-value" style="font-family: var(--font-mono); font-size: 12px;">{{ filename }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Timestamp:</span>
                    <span class="info-value" style="font-family: var(--font-mono); font-size: 12px;">{{ timestamp }}</span>
                </div>
            </div>

            <!-- Cryptographic Fingerprint -->
            <div class="crypto-box">
                <div class="crypto-title">
                    <span>SHA-256 Digest</span>
                    <span style="font-family: var(--font-mono); color: #38bdf8;">SECP256R1</span>
                </div>
                <div class="crypto-hash">{{ hash }}</div>
            </div>

            <div class="zero-retention-pill">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <span>Zero-Retention: Verified cryptographically without any external database lookup.</span>
            </div>

            <a href="/" class="btn" style="margin-bottom: 12px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                <span>Go to SAKK Dashboard</span>
            </a>
            
            <a href="https://github.com/abdllaouidjabere-cmyk/sakk1" target="_blank" class="btn" style="background-color: rgba(255, 255, 255, 0.1);">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                <span>View on GitHub</span>
            </a>
        </div>
    </div>
</body>
</html>
