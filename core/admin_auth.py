import os
import secrets

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

SESSION_SECRET = os.getenv("SESSION_SECRET", "cloverky-session-secret-change-in-prod")


def check_credentials(username: str, password: str) -> bool:
    ok_u = secrets.compare_digest(username.encode(), ADMIN_USERNAME.encode())
    ok_p = secrets.compare_digest(password.encode(), ADMIN_PASSWORD.encode())
    return ok_u and ok_p


_BASE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>cloverky</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :not(input):not(textarea) {{
      user-select: none;
      -webkit-user-select: none;
    }}

    body {{
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #060c07;
      font-family: 'Inter', -apple-system, sans-serif;
      overflow: hidden;
      position: relative;
    }}

    body::before {{
      content: '';
      position: fixed;
      top: -15%;
      right: -5%;
      width: 55%;
      height: 55%;
      background: radial-gradient(ellipse, rgba(34,197,94,0.11) 0%, transparent 68%);
      animation: pulse 9s ease-in-out infinite;
      pointer-events: none;
    }}

    body::after {{
      content: '';
      position: fixed;
      bottom: -20%;
      left: -8%;
      width: 50%;
      height: 60%;
      background: radial-gradient(ellipse, rgba(16,85,40,0.09) 0%, transparent 68%);
      animation: pulse 9s ease-in-out infinite reverse;
      pointer-events: none;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 0.7; transform: scale(1); }}
      50%       {{ opacity: 1;   transform: scale(1.12); }}
    }}

    @keyframes float {{
      0%, 100% {{ transform: translateY(0); }}
      50%       {{ transform: translateY(-5px); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      body::before, body::after, .logo-icon {{ animation: none; }}
    }}

    .card {{
      position: relative;
      z-index: 1;
      background: rgba(11, 20, 12, 0.85);
      border: 1px solid rgba(34, 197, 94, 0.18);
      border-radius: 22px;
      padding: 52px 44px 46px;
      width: 100%;
      max-width: 390px;
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      box-shadow:
        0 0 0 1px rgba(34, 197, 94, 0.04),
        0 28px 64px rgba(0, 0, 0, 0.65),
        0 0 100px rgba(34, 197, 94, 0.05);
    }}

    .logo {{
      text-align: center;
      margin-bottom: 42px;
    }}

    .logo-icon {{
      font-size: 56px;
      display: block;
      margin-bottom: 14px;
      filter: drop-shadow(0 0 14px rgba(34, 197, 94, 0.55));
      animation: float 3.5s ease-in-out infinite;
    }}

    .logo-name {{
      font-family: 'DM Serif Display', Georgia, serif;
      font-size: 30px;
      color: #f0fdf4;
      letter-spacing: -0.2px;
    }}

    .logo-sub {{
      font-size: 11px;
      font-weight: 500;
      color: rgba(74, 222, 128, 0.45);
      letter-spacing: 2.5px;
      text-transform: uppercase;
      margin-top: 7px;
    }}

    .error-box {{
      background: rgba(239, 68, 68, 0.07);
      border: 1px solid rgba(239, 68, 68, 0.22);
      border-radius: 10px;
      padding: 12px 15px;
      font-size: 13px;
      color: #fca5a5;
      margin-bottom: 24px;
    }}

    label {{
      display: block;
      font-size: 11px;
      font-weight: 600;
      color: rgba(134, 239, 172, 0.65);
      letter-spacing: 1.8px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}

    input {{
      width: 100%;
      background: rgba(6, 12, 7, 0.65);
      border: 1px solid rgba(34, 197, 94, 0.14);
      border-radius: 11px;
      padding: 13px 16px;
      font-size: 15px;
      font-family: 'Inter', sans-serif;
      color: #f0fdf4;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
      margin-bottom: 20px;
    }}

    input::placeholder {{ color: rgba(240, 253, 244, 0.18); }}

    input:focus {{
      border-color: rgba(34, 197, 94, 0.6);
      box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.09);
    }}

    button {{
      width: 100%;
      background: #22c55e;
      color: #060c07;
      border: none;
      border-radius: 11px;
      padding: 14px;
      font-size: 15px;
      font-family: 'Inter', sans-serif;
      font-weight: 600;
      cursor: pointer;
      margin-top: 6px;
      transition: background 0.2s, transform 0.1s;
      letter-spacing: 0.2px;
    }}

    button:hover  {{ background: #16a34a; }}
    button:active {{ transform: scale(0.99); }}
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">
      <span class="logo-icon">🍀</span>
      <div class="logo-name">cloverky</div>
      <div class="logo-sub">Admin Access</div>
    </div>
    {error_block}
    <form method="post" action="/login">
      <label>아이디</label>
      <input type="text" name="username" placeholder="아이디를 입력하세요" autocomplete="username" required autofocus>
      <label>비밀번호</label>
      <input type="password" name="password" placeholder="비밀번호를 입력하세요" autocomplete="current-password" required>
      <button type="submit">로그인</button>
    </form>
  </div>
</body>
</html>"""

_ERROR_BLOCK = '<div class="error-box">아이디 또는 비밀번호가 올바르지 않습니다.</div>'


def get_login_html(error: bool = False) -> str:
    return _BASE.format(error_block=_ERROR_BLOCK if error else "")
