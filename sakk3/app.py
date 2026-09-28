import os
import sqlite3
import hashlib
import json
import base64
from datetime import datetime
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
import random
import urllib.parse

from flask import Flask, request, jsonify, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

import qrcode
import cv2
import numpy as np

app = Flask(__name__)
# Secure secret key with fallback
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_cyber_key_sakk')

DB_FILE = 'sakk.db'
KEY_FILE = "private_key.pem"

PRIVATE_KEY = None
PUBLIC_KEY = None

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Audit Logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            file_hash TEXT,
            signature TEXT,
            timestamp TEXT
        )
    ''')
    try:
        c.execute("ALTER TABLE audit_logs ADD COLUMN user_id INTEGER")
    except Exception:
        pass
    # System Keys
    c.execute('''
        CREATE TABLE IF NOT EXISTS system_keys (
            id INTEGER PRIMARY KEY,
            public_key TEXT
        )
    ''')
    # Users for Authentication
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    try:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN current_otp TEXT")
    except Exception:
        pass
    
    # Init default admin
    c.execute("SELECT id FROM users WHERE username='admin'")
    if not c.fetchone():
        hashed = generate_password_hash("admin123")
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", hashed))
        
    conn.commit()
    conn.close()

def load_or_generate_keys():
    global PRIVATE_KEY, PUBLIC_KEY
    regenerate = False
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            try:
                PRIVATE_KEY = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                )
                if not isinstance(PRIVATE_KEY, ec.EllipticCurvePrivateKey):
                    regenerate = True
                else:
                    PUBLIC_KEY = PRIVATE_KEY.public_key()
            except Exception:
                regenerate = True
    else:
        regenerate = True
        
    if regenerate:
        # Generate ECDSA key
        PRIVATE_KEY = ec.generate_private_key(ec.SECP256R1())
        PUBLIC_KEY = PRIVATE_KEY.public_key()
        
        pem = PRIVATE_KEY.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(pem)
            
        pub_pem = PUBLIC_KEY.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO system_keys (id, public_key) VALUES (1, ?)", (pub_pem.decode('utf-8'),))
        conn.commit()
        conn.close()

def send_otp_email(to_email, otp_code):
    msg = MIMEText(f"Your SAKK verification code is: {otp_code}\n\nPlease enter this code to complete authentication.", "plain", "utf-8")
    msg['Subject'] = "SAKK Security: Verification Code"
    msg['From'] = "abdllaouidjabere@gmail.com"
    msg['To'] = to_email
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("abdllaouidjabere@gmail.com", "lten mrpy ubkl vkym")
    server.send_message(msg)
    server.quit()

# Automatically initialize DB and keys on startup
init_db()
load_or_generate_keys()

def is_logged_in():
    return session.get('logged_in', False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/public-key', methods=['GET'])
def get_public_key():
    """Retrieve public key for offline verification"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT public_key FROM system_keys WHERE id=1")
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({"public_key": row[0]}), 200
    return jsonify({"error": "Public key not found"}), 404

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, password_hash, email FROM users WHERE username=?", (username,))
    row = c.fetchone()
    
    if row and check_password_hash(row[1], password):
        user_id = row[0]
        email = row[2]
        
        # Generate and send OTP for login too
        otp = str(random.randint(100000, 999999))
        c.execute("UPDATE users SET current_otp=? WHERE id=?", (otp, user_id))
        conn.commit()
        conn.close()
        
        try:
            send_otp_email(email, otp)
            session['pending_user_id'] = user_id
            session['pending_username'] = username
            return jsonify({'success': True, 'requires_otp': True})
        except Exception as e:
            return jsonify({'success': False, 'error': f"Failed to send email: {e}"}), 500
            
    conn.close()
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    if not username or not password or not email:
        return jsonify({'success': False, 'error': 'Username, email and password are required.'}), 400
    if len(username) < 3:
        return jsonify({'success': False, 'error': 'Username must be at least 3 characters.'}), 400
    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters.'}), 400
    hashed = generate_password_hash(password)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)", (username, hashed, email))
        user_id = c.lastrowid
        
        otp = str(random.randint(100000, 999999))
        c.execute("UPDATE users SET current_otp=? WHERE id=?", (otp, user_id))
        conn.commit()
        conn.close()
        
        try:
            send_otp_email(email, otp)
            session['pending_user_id'] = user_id
            session['pending_username'] = username
            return jsonify({'success': True, 'requires_otp': True})
        except Exception as e:
            return jsonify({'success': False, 'error': f"Failed to send email: {e}"}), 500
    except Exception:
        conn.close()
        return jsonify({'success': False, 'error': 'Username already exists.'}), 409

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    otp = data.get('otp')
    user_id = session.get('pending_user_id')
    username = session.get('pending_username')
    
    if not user_id or not otp:
        return jsonify({"success": False, "error": "Session expired. Please login again."}), 400
        
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT current_otp FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    
    if row and row[0] == str(otp).strip():
        c.execute("UPDATE users SET current_otp=NULL WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        
        session.pop('pending_user_id', None)
        session.pop('pending_username', None)
        session['logged_in'] = True
        session['username'] = username
        session['user_id'] = user_id
        return jsonify({"success": True})
        
    conn.close()
    return jsonify({"success": False, "error": "Invalid verification code"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/me', methods=['GET'])
def me():
    if is_logged_in():
        return jsonify({"logged_in": True, "username": session.get('username')})
    return jsonify({"logged_in": False})

def compute_signature_digest(file_hash_hex, metadata=None):
    """Compute a signing digest that cryptographically binds the file hash with optional metadata.
    metadata: list of {"key": ..., "value": ...} dicts, or None/empty for legacy raw hash."""
    if metadata and isinstance(metadata, list) and len(metadata) > 0:
        # Sort by key for canonical deterministic ordering
        sorted_meta = sorted(metadata, key=lambda x: x.get('key', ''))
        canonical_str = file_hash_hex + '|' + '|'.join(
            f"{m.get('key', '')}={m.get('value', '')}" for m in sorted_meta
        )
        return hashlib.sha256(canonical_str.encode('utf-8')).digest()
    else:
        return bytes.fromhex(file_hash_hex)

def verify_crypto_signature(signature_b64, file_hash_hex, metadata=None):
    """Verify an ECDSA signature against file hash + optional metadata."""
    try:
        signature = base64.b64decode(signature_b64)
    except Exception:
        return False

    # Attempt 1: Verify with metadata-bound digest
    try:
        digest = compute_signature_digest(file_hash_hex, metadata)
        PUBLIC_KEY.verify(
            signature,
            digest,
            ec.ECDSA(utils.Prehashed(hashes.SHA256()))
        )
        return True
    except (InvalidSignature, Exception):
        pass

    # Attempt 2: Fallback to raw hash (legacy signatures without metadata)
    if metadata and len(metadata) > 0:
        try:
            raw_digest = bytes.fromhex(file_hash_hex)
            PUBLIC_KEY.verify(
                signature,
                raw_digest,
                ec.ECDSA(utils.Prehashed(hashes.SHA256()))
            )
            return True
        except (InvalidSignature, Exception):
            pass

    return False

def parse_metadata_from_form(form):
    """Extract metadata fields from form data. Accepts JSON string in 'metadata' field."""
    raw = form.get('metadata', '').strip()
    if not raw:
        return []
    try:
        meta = json.loads(raw)
        if isinstance(meta, list):
            return [m for m in meta if m.get('key', '').strip() and m.get('value', '').strip()]
        return []
    except Exception:
        return []

def parse_metadata_from_qr_param(qs_or_args):
    """Decode metadata from the 'm' query parameter (base64-encoded JSON)."""
    m_b64 = ''
    if isinstance(qs_or_args, dict):
        # parse_qs returns lists
        m_b64 = qs_or_args.get('m', [''])[0] if isinstance(qs_or_args.get('m'), list) else qs_or_args.get('m', '')
    else:
        m_b64 = qs_or_args
    if not m_b64:
        return []
    try:
        decoded = base64.urlsafe_b64decode(m_b64 + '==').decode('utf-8')
        meta = json.loads(decoded)
        if isinstance(meta, list):
            return meta
        return []
    except Exception:
        return []

@app.route('/api/sign', methods=['POST'])
def sign_file():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized access. Please login first.'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename) or file.filename
    file_bytes = file.read()

    if not file_bytes:
        return jsonify({'error': 'Empty file'}), 400

    # Extract dynamic metadata (Zero-Retention: NOT saved in DB)
    metadata = parse_metadata_from_form(request.form)

    # Compute SHA256 of file
    file_hash_bytes = hashlib.sha256(file_bytes).digest()
    file_hash_hex = file_hash_bytes.hex()

    # Compute digest binding file hash + metadata
    signing_digest = compute_signature_digest(file_hash_hex, metadata)

    # ECDSA Sign
    signature = PRIVATE_KEY.sign(
        signing_digest,
        ec.ECDSA(utils.Prehashed(hashes.SHA256()))
    )
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Audit trail only (no metadata stored)
    user_id = session.get('user_id')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO audit_logs (user_id, filename, file_hash, signature, timestamp) VALUES (?, ?, ?, ?, ?)",
              (user_id, filename, file_hash_hex, signature_b64, timestamp))
    conn.commit()
    conn.close()

    # Build QR payload
    qr_dict = {
        'f': filename,
        'h': file_hash_hex,
        's': signature_b64,
        't': timestamp
    }
    if metadata:
        meta_json = json.dumps(metadata, ensure_ascii=False, separators=(',', ':'))
        qr_dict['m'] = base64.urlsafe_b64encode(meta_json.encode('utf-8')).decode('utf-8').rstrip('=')

    params = urllib.parse.urlencode(qr_dict)

    base_url = request.form.get('base_url')
    if base_url:
        base_url = base_url.rstrip('/')
    else:
        base_url = request.host_url.rstrip('/')

    url_payload = f"{base_url}/v?{params}"

    # QR color customization
    qr_color = (request.form.get('qr_color') or '#000000').strip()
    # Validate hex color
    if not qr_color.startswith('#') or len(qr_color) != 7:
        qr_color = '#000000'

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url_payload)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=qr_color, back_color="white")

    # Convert to RGBA and make background transparent
    from PIL import Image
    qr_img = qr_img.convert("RGBA")
    datas = qr_img.getdata()
    new_data = []
    for item in datas:
        # Replace white/near-white with transparent
        if item[0] >= 240 and item[1] >= 240 and item[2] >= 240:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    qr_img.putdata(new_data)

    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_bytes = buffered.getvalue()
    qr_b64 = base64.b64encode(qr_bytes).decode('utf-8')

    # Check if we should stamp PDF (Zero-Retention: Fully in-memory)
    is_pdf_stamp = request.form.get('stamp_pdf') == 'true'
    final_file_b64 = None

    if is_pdf_stamp and filename.lower().endswith('.pdf'):
        try:
            import fitz  # PyMuPDF
            x_pct = float(request.form.get('x_pct', 0))
            y_pct = float(request.form.get('y_pct', 0))
            size_pct = float(request.form.get('size_pct', 0.2))

            doc = fitz.open(stream=file_bytes, filetype="pdf")
            page = doc[0]

            page_w = page.rect.width
            page_h = page.rect.height

            x0 = x_pct * page_w
            y0 = y_pct * page_h
            w = size_pct * page_w
            x1 = x0 + w
            y1 = y0 + w

            rect = fitz.Rect(x0, y0, x1, y1)
            page.insert_image(rect, stream=qr_bytes)

            out_pdf = BytesIO()
            doc.save(out_pdf)
            doc.close()
            final_file_b64 = base64.b64encode(out_pdf.getvalue()).decode('utf-8')
        except Exception as e:
            print("PDF Stamping Error:", e)
            pass

    return jsonify({
        'filename': filename,
        'hash': file_hash_hex,
        'signature': signature_b64,
        'timestamp': timestamp,
        'metadata': metadata,
        'qr_image': f"data:image/png;base64,{qr_b64}",
        'stamped_pdf': final_file_b64
    })

def _extract_qr_from_image(img):
    """Robustly extract QR from OpenCV image using pyzbar and OpenCV fallbacks."""
    import numpy as np
    import cv2
    
    # 1. Handle transparent background (if 4 channels)
    if len(img.shape) == 3 and img.shape[-1] == 4:
        bg = np.ones_like(img[:, :, :3]) * 255
        alpha = img[:, :, 3:] / 255.0
        img = (img[:, :, :3] * alpha + bg * (1 - alpha)).astype(np.uint8)
    
    # 2. Try pyzbar first (best for dense QRs and large metadata)
    try:
        from pyzbar.pyzbar import decode, ZBarSymbol
        decoded = decode(img, symbols=[ZBarSymbol.QRCODE])
        if decoded:
            return decoded[0].data.decode('utf-8')
    except Exception as e:
        pass
    
    # 3. Try WeChatQRCode if available (CNN based, very good)
    try:
        detector = cv2.wechat_qrcode_WeChatQRCode()
        res, _ = detector.detectAndDecode(img)
        if res and len(res) > 0:
            return res[0]
    except Exception:
        pass
        
    # 4. Fallback to standard OpenCV
    try:
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)
        if data:
            return data
    except Exception:
        pass
        
    return None

def scan_for_qr_in_file(file_bytes, filename):
    """Scan a file (PDF or image) for QR codes across ALL pages. Returns (qr_data_string, page_number) or (None, None)."""
    if filename.lower().endswith('.pdf'):
        try:
            import fitz
            import numpy as np
            import cv2
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page_num in range(len(doc)):
                page = doc[page_num]
                # High-res render for reliable QR detection
                mat = fitz.Matrix(3.0, 3.0)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img_bytes = pix.tobytes("png")
                nparr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if img is not None:
                    data = _extract_qr_from_image(img)
                    if data:
                        doc.close()
                        return data, page_num + 1
            doc.close()
            return None, None
        except Exception as e:
            print(f"Error scanning PDF: {e}")
            return None, None
    else:
        try:
            import numpy as np
            import cv2
            nparr = np.frombuffer(file_bytes, np.uint8)
            # Read with UNCHANGED to preserve alpha channel
            img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
            if img is None:
                return None, None
            data = _extract_qr_from_image(img)
            if data:
                return data, 1
            return None, None
        except Exception as e:
            print(f"Error scanning image: {e}")
            return None, None

@app.route('/api/verify', methods=['POST'])
def verify_file():
    """Auto-scan uploaded file for QR seal, extract payload, verify signature."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename) or file.filename
    file_bytes = file.read()

    if not file_bytes:
        return jsonify({'error': 'Empty file'}), 400

    # Scan ALL pages for QR code
    qr_data, page_num = scan_for_qr_in_file(file_bytes, filename)

    if not qr_data:
        return jsonify({
            'error': 'No QR seal found in the document. This file cannot be verified — it may not have been certified by SAKK.',
            'has_qr': False
        }), 400

    try:
        payload, metadata = _extract_payload_from_qr(qr_data)
        file_hash_hex = payload.get('hash', '')
        signature_b64 = payload.get('signature', '')

        if not file_hash_hex or not signature_b64:
            return jsonify({'error': 'QR seal found but contains incomplete cryptographic data.', 'has_qr': True}), 400

        is_valid = verify_crypto_signature(signature_b64, file_hash_hex, metadata)
        payload['metadata'] = metadata

        return jsonify({
            'valid': is_valid,
            'has_qr': True,
            'page': page_num,
            'payload': payload
        })
    except Exception as e:
        return jsonify({'error': f'QR seal found but data is corrupted: {str(e)}', 'has_qr': True}), 400

@app.route('/api/verify-qr', methods=['POST'])
def verify_qr():
    """Scan uploaded file (image/PDF) for QR code, extract and verify. Supports multi-page PDFs."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename) or file.filename
    file_bytes = file.read()

    if not file_bytes:
        return jsonify({'error': 'Empty file'}), 400

    # Multi-page QR scan
    qr_data, page_num = scan_for_qr_in_file(file_bytes, filename)

    if not qr_data:
        return jsonify({'error': 'No QR code found in the file. Ensure the image/document is clear and the QR seal is visible.'}), 400

    try:
        payload, metadata = _extract_payload_from_qr(qr_data)
        file_hash_hex = payload.get('hash', '')
        signature_b64 = payload.get('signature', '')
        is_valid = verify_crypto_signature(signature_b64, file_hash_hex, metadata)
        payload['metadata'] = metadata
    except Exception as e:
        return jsonify({'error': f'Invalid QR data structure or corrupted cryptographic signature. Details: {str(e)}'}), 400

    return jsonify({
        'valid': is_valid,
        'page': page_num,
        'payload': payload
    })

@app.route('/api/logs', methods=['GET'])
def get_logs():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    user_id = session.get('user_id')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT id, filename, file_hash, signature, timestamp FROM audit_logs WHERE user_id=? ORDER BY id DESC LIMIT 50",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()

    logs = []
    for r in rows:
        logs.append({
            'id': r[0],
            'filename': r[1],
            'hash': r[2],
            'signature': r[3][:25] + "...",
            'timestamp': r[4]
        })
    return jsonify(logs)

@app.route('/api/verify-qr-data', methods=['POST'])
def verify_qr_data():
    """Verify a QR payload decoded directly by the browser camera (no file upload needed)."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    try:
        raw = data.get('raw_data')
        payload, metadata = _extract_payload_from_qr(raw)

        file_hash_hex = payload.get('hash', '')
        signature_b64 = payload.get('signature', '')

        if not file_hash_hex or not signature_b64:
            return jsonify({'error': 'Missing hash or signature in QR payload'}), 400

        is_valid = verify_crypto_signature(signature_b64, file_hash_hex, metadata)
        payload['metadata'] = metadata
        return jsonify({'valid': is_valid, 'payload': payload})
    except Exception as e:
        return jsonify({'error': f'Invalid QR data: {str(e)}'}), 400

def _extract_payload_from_qr(raw_data):
    """Parse QR data (URL or JSON) and return (payload_dict, metadata_list)."""
    metadata = []
    if raw_data and raw_data.startswith('http'):
        parsed = urllib.parse.urlparse(raw_data)
        qs = urllib.parse.parse_qs(parsed.query)
        payload = {
            'filename': qs.get('f', [''])[0],
            'hash': qs.get('h', [''])[0],
            'signature': qs.get('s', [''])[0],
            'timestamp': qs.get('t', [''])[0]
        }
        metadata = parse_metadata_from_qr_param(qs)
    else:
        if isinstance(raw_data, str):
            try:
                payload = json.loads(raw_data)
            except Exception:
                payload = {}
        else:
            payload = raw_data if isinstance(raw_data, dict) else {}
        if 'metadata' in payload and isinstance(payload['metadata'], list):
            metadata = payload['metadata']
        elif 'm' in payload:
            metadata = parse_metadata_from_qr_param(payload.get('m', ''))
    return payload, metadata

@app.route('/v')
def verify_page():
    filename = request.args.get('f', 'Unknown')
    file_hash_hex = request.args.get('h', '')
    signature_b64 = request.args.get('s', '')
    timestamp = request.args.get('t', 'Unknown')
    m_b64 = request.args.get('m', '')
    metadata = parse_metadata_from_qr_param(m_b64) if m_b64 else []

    is_valid = verify_crypto_signature(signature_b64, file_hash_hex, metadata)

    return render_template(
        'verify.html',
        valid=is_valid,
        filename=filename,
        hash=file_hash_hex,
        timestamp=timestamp,
        metadata=metadata
    )

if __name__ == '__main__':
    init_db()
    load_or_generate_keys()
    app.run(debug=True, port=5000)
