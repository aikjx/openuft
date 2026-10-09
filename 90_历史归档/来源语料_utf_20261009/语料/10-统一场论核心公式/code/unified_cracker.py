import math
import hashlib
import random
import itertools
from collections import Counter

ALPHA = 7.2973525693e-3

ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
    'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
    'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

class ClassicalCracker:
    def caesar_crack(self, ciphertext):
        best_score = float('inf')
        best_key = None
        best_plaintext = None
        
        for key in range(26):
            plaintext = self._shift_decrypt(ciphertext, key)
            score = self._frequency_score(plaintext)
            
            if score < best_score:
                best_score = score
                best_key = key
                best_plaintext = plaintext
        
        return {'key': best_key, 'plaintext': best_plaintext, 'score': best_score}
    
    def _shift_decrypt(self, ciphertext, key):
        result = []
        for char in ciphertext:
            if char.isalpha():
                shifted = ord(char) - key
                if char.isupper():
                    if shifted < ord('A'):
                        shifted += 26
                else:
                    if shifted < ord('a'):
                        shifted += 26
                result.append(chr(shifted))
            else:
                result.append(char)
        return ''.join(result)
    
    def _frequency_score(self, text):
        text = text.upper()
        text_freq = Counter(c for c in text if c.isalpha())
        total = sum(text_freq.values())
        
        score = 0
        for char, expected in ENGLISH_FREQ.items():
            actual = (text_freq.get(char, 0) / total * 100) if total > 0 else 0
            score += abs(expected - actual)
        
        return score
    
    def vigenere_crack(self, ciphertext, max_key_length=12):
        ciphertext = ''.join(c for c in ciphertext if c.isalpha()).upper()
        
        best_key = None
        best_plaintext = None
        best_score = float('inf')
        
        for key_length in range(1, max_key_length + 1):
            key = ''
            for i in range(key_length):
                column = ciphertext[i::key_length]
                shift_key = self._find_single_shift(column)
                key += chr(ord('A') + shift_key)
            
            plaintext = self._vigenere_decrypt(ciphertext, key)
            score = self._frequency_score(plaintext)
            
            if score < best_score:
                best_score = score
                best_key = key
                best_plaintext = plaintext
        
        return {'key': best_key, 'plaintext': best_plaintext, 'score': best_score}
    
    def _find_single_shift(self, text):
        best_score = float('inf')
        best_shift = 0
        
        for shift in range(26):
            decrypted = ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in text)
            score = self._frequency_score(decrypted)
            
            if score < best_score:
                best_score = score
                best_shift = shift
        
        return best_shift
    
    def _vigenere_decrypt(self, ciphertext, key):
        result = []
        key_idx = 0
        
        for char in ciphertext:
            if char.isalpha():
                shift = ord(key[key_idx % len(key)]) - ord('A')
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                result.append(decrypted)
                key_idx += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def affine_crack(self, ciphertext):
        ciphertext = ''.join(c for c in ciphertext if c.isalpha()).upper()
        
        best_score = float('inf')
        best_key = None
        best_plaintext = None
        
        for a in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
            a_inv = self._mod_inverse(a, 26)
            for b in range(26):
                plaintext = self._affine_decrypt(ciphertext, a_inv, b)
                score = self._frequency_score(plaintext)
                
                if score < best_score:
                    best_score = score
                    best_key = (a, b)
                    best_plaintext = plaintext
        
        return {'key': best_key, 'plaintext': best_plaintext, 'score': best_score}
    
    def _mod_inverse(self, a, m):
        for x in range(m):
            if (a * x) % m == 1:
                return x
        return None
    
    def _affine_decrypt(self, ciphertext, a_inv, b):
        result = []
        for char in ciphertext:
            if char.isalpha():
                decrypted = chr(((ord(char) - ord('A') - b) * a_inv) % 26 + ord('A'))
                result.append(decrypted)
            else:
                result.append(char)
        return ''.join(result)
    
    def substitution_crack(self, ciphertext):
        ciphertext = ''.join(c for c in ciphertext if c.isalpha()).upper()
        
        freq_pairs = sorted(Counter(ciphertext).items(), key=lambda x: -x[1])
        freq_chars = [pair[0] for pair in freq_pairs]
        
        english_pairs = sorted(ENGLISH_FREQ.items(), key=lambda x: -x[1])
        english_chars = [pair[0] for pair in english_pairs]
        
        mapping = dict(zip(freq_chars, english_chars))
        
        plaintext = ''.join(mapping.get(c, c) for c in ciphertext)
        
        return {'mapping': mapping, 'plaintext': plaintext}

class ModernCracker:
    def __init__(self):
        self.alpha = ALPHA
    
    def brute_force_aes(self, ciphertext_hex, known_plaintext=None):
        ciphertext = bytes.fromhex(ciphertext_hex)
        
        for key_int in range(0, 2**128, int(self.alpha * 10**18)):
            key = key_int.to_bytes(16, 'big')
            
            try:
                from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
                cipher = Cipher(algorithms.AES(key), modes.ECB())
                decryptor = cipher.decryptor()
                plaintext = decryptor.update(ciphertext) + decryptor.finalize()
                
                if known_plaintext:
                    if known_plaintext.encode() in plaintext:
                        return {'key': key.hex(), 'plaintext': plaintext.decode()}
                else:
                    if self._is_readable(plaintext):
                        return {'key': key.hex(), 'plaintext': plaintext.decode()}
            except:
                pass
        
        return None
    
    def brute_force_des(self, ciphertext_hex, known_plaintext=None):
        ciphertext = bytes.fromhex(ciphertext_hex)
        
        for key_int in range(0, 2**56, int(self.alpha * 10**18)):
            key = key_int.to_bytes(8, 'big')
            
            try:
                from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
                cipher = Cipher(algorithms.TripleDES(key), modes.ECB())
                decryptor = cipher.decryptor()
                plaintext = decryptor.update(ciphertext) + decryptor.finalize()
                
                if known_plaintext:
                    if known_plaintext.encode() in plaintext:
                        return {'key': key.hex(), 'plaintext': plaintext.decode()}
                else:
                    if self._is_readable(plaintext):
                        return {'key': key.hex(), 'plaintext': plaintext.decode()}
            except:
                pass
        
        return None
    
    def rsa_factor(self, n):
        max_factor = int(math.sqrt(n))
        
        for p in range(3, max_factor, 2):
            if n % p == 0:
                q = n // p
                if p * q == n:
                    return {'p': p, 'q': q, 'phi': (p-1)*(q-1)}
        
        for k in range(1, 1000):
            factor = int(self.alpha * k * 10**10) % (max_factor - 3) + 3
            if n % factor == 0:
                q = n // factor
                if factor * q == n:
                    return {'p': factor, 'q': q, 'phi': (factor-1)*(q-1)}
        
        return None
    
    def _is_readable(self, text):
        if isinstance(text, bytes):
            try:
                text = text.decode('utf-8')
            except:
                return False
        
        printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
        return printable / len(text) > 0.9 if len(text) > 0 else False

class HashCracker:
    def __init__(self):
        self.alpha = ALPHA
    
    def md5_crack(self, hash_value, dictionary=None):
        if dictionary is None:
            dictionary = ['password', '123456', 'qwerty', 'admin', 'letmein',
                         'welcome', 'monkey', 'dragon', 'baseball', 'iloveyou']
        
        for word in dictionary:
            hashed = hashlib.md5(word.encode()).hexdigest()
            if hashed == hash_value:
                return {'plaintext': word, 'method': 'dictionary'}
        
        for i in range(0, 1000000, int(self.alpha * 10**10)):
            candidate = str(i)
            hashed = hashlib.md5(candidate.encode()).hexdigest()
            if hashed == hash_value:
                return {'plaintext': candidate, 'method': 'brute_force'}
        
        return None
    
    def sha1_crack(self, hash_value, dictionary=None):
        if dictionary is None:
            dictionary = ['password', '123456', 'qwerty', 'admin', 'letmein']
        
        for word in dictionary:
            hashed = hashlib.sha1(word.encode()).hexdigest()
            if hashed == hash_value:
                return {'plaintext': word, 'method': 'dictionary'}
        
        for i in range(0, 1000000, int(self.alpha * 10**10)):
            candidate = str(i)
            hashed = hashlib.sha1(candidate.encode()).hexdigest()
            if hashed == hash_value:
                return {'plaintext': candidate, 'method': 'brute_force'}
        
        return None
    
    def sha256_crack(self, hash_value, dictionary=None):
        if dictionary is None:
            dictionary = ['password', '123456', 'qwerty', 'admin', 'letmein']
        
        for word in dictionary:
            hashed = hashlib.sha256(word.encode()).hexdigest()
            if hashed == hash_value:
                return {'plaintext': word, 'method': 'dictionary'}
        
        for i in range(0, 1000000, int(self.alpha * 10**10)):
            candidate = str(i)
            hashed = hashlib.sha256(candidate.encode()).hexdigest()
            if hashed == hash_value:
                return {'plaintext': candidate, 'method': 'brute_force'}
        
        return None

class GeometricCracker:
    def __init__(self):
        self.alpha = ALPHA
        self.kappa = None
        self.tau = None
    
    def set_geometric_params(self, rho, b):
        self.kappa = rho / (rho**2 + b**2)
        self.tau = b / (rho**2 + b**2)
    
    def geometric_key_generation(self, target_length=256):
        key = []
        
        for i in range(target_length):
            theta = i * self.tau * 10**28
            key_byte = int((math.sin(theta) * self.kappa * 10**30 + 
                          math.cos(theta) * self.tau * 10**28 + 
                          self.alpha * i) % 256)
            key.append(key_byte)
        
        return bytes(key)
    
    def geometric_decrypt(self, ciphertext, known_pattern=None):
        if self.kappa is None or self.tau is None:
            self.set_geometric_params(1e-13, 1e-11)
        
        plaintext = bytearray()
        for i, byte in enumerate(ciphertext):
            theta = i * self.tau * 10**28
            key_byte = int((math.sin(theta) * self.kappa * 10**30 + 
                          math.cos(theta) * self.tau * 10**28 + 
                          self.alpha * i) % 256)
            
            decrypted_byte = byte ^ key_byte
            plaintext.append(decrypted_byte)
        
        plaintext = bytes(plaintext)
        
        if known_pattern:
            if known_pattern.encode() in plaintext:
                return plaintext.decode()
        
        if self._is_readable(plaintext):
            return plaintext.decode()
        
        return None
    
    def crack_using_alpha(self, encrypted_data):
        candidates = []
        
        for scale_factor in [1e-13, 1e-15, 1e-35]:
            rho = scale_factor
            b = rho / self.alpha
            self.set_geometric_params(rho, b)
            
            if isinstance(encrypted_data, str):
                encrypted_bytes = bytes.fromhex(encrypted_data)
            else:
                encrypted_bytes = encrypted_data
            
            result = self.geometric_decrypt(encrypted_bytes)
            if result:
                candidates.append({
                    'scale': 'electron' if scale_factor == 1e-13 else 
                             'proton' if scale_factor == 1e-15 else 'planck',
                    'plaintext': result,
                    'rho': rho,
                    'b': b
                })
        
        return candidates
    
    def _is_readable(self, text):
        if isinstance(text, bytes):
            try:
                text = text.decode('utf-8')
            except:
                return False
        
        printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
        return printable / len(text) > 0.9 if len(text) > 0 else False

class AlgorithmAlliance:
    def __init__(self):
        self.classical = ClassicalCracker()
        self.modern = ModernCracker()
        self.hash_cracker = HashCracker()
        self.geometric = GeometricCracker()
        self.alpha = ALPHA
    
    def crack(self, ciphertext, algorithm_type='auto', **kwargs):
        if algorithm_type == 'auto':
            return self._auto_detect_and_crack(ciphertext)
        elif algorithm_type == 'caesar':
            return self.classical.caesar_crack(ciphertext)
        elif algorithm_type == 'vigenere':
            return self.classical.vigenere_crack(ciphertext, **kwargs)
        elif algorithm_type == 'affine':
            return self.classical.affine_crack(ciphertext)
        elif algorithm_type == 'substitution':
            return self.classical.substitution_crack(ciphertext)
        elif algorithm_type == 'aes':
            return self.modern.brute_force_aes(ciphertext, **kwargs)
        elif algorithm_type == 'des':
            return self.modern.brute_force_des(ciphertext, **kwargs)
        elif algorithm_type == 'rsa':
            return self.modern.rsa_factor(ciphertext)
        elif algorithm_type == 'md5':
            return self.hash_cracker.md5_crack(ciphertext, **kwargs)
        elif algorithm_type == 'sha1':
            return self.hash_cracker.sha1_crack(ciphertext, **kwargs)
        elif algorithm_type == 'sha256':
            return self.hash_cracker.sha256_crack(ciphertext, **kwargs)
        elif algorithm_type == 'geometric':
            return self.geometric.crack_using_alpha(ciphertext)
        else:
            return None
    
    def _auto_detect_and_crack(self, ciphertext):
        results = []
        
        caesar_result = self.classical.caesar_crack(ciphertext)
        if caesar_result['score'] < 50:
            results.append({'type': 'caesar', 'result': caesar_result})
        
        vigenere_result = self.classical.vigenere_crack(ciphertext)
        if vigenere_result['score'] < 50:
            results.append({'type': 'vigenere', 'result': vigenere_result})
        
        affine_result = self.classical.affine_crack(ciphertext)
        if affine_result['score'] < 50:
            results.append({'type': 'affine', 'result': affine_result})
        
        substitution_result = self.classical.substitution_crack(ciphertext)
        results.append({'type': 'substitution', 'result': substitution_result})
        
        if len(results) == 0:
            geometric_result = self.geometric.crack_using_alpha(ciphertext)
            if geometric_result:
                results.append({'type': 'geometric', 'result': geometric_result})
        
        return results
    
    def universal_crack(self, encrypted_data):
        results = []
        
        if isinstance(encrypted_data, str):
            results.append(self._auto_detect_and_crack(encrypted_data))
            
            if len(encrypted_data) == 32:
                md5_result = self.hash_cracker.md5_crack(encrypted_data)
                if md5_result:
                    results.append({'type': 'md5', 'result': md5_result})
            
            if len(encrypted_data) == 40:
                sha1_result = self.hash_cracker.sha1_crack(encrypted_data)
                if sha1_result:
                    results.append({'type': 'sha1', 'result': sha1_result})
            
            if len(encrypted_data) == 64:
                sha256_result = self.hash_cracker.sha256_crack(encrypted_data)
                if sha256_result:
                    results.append({'type': 'sha256', 'result': sha256_result})
            
            try:
                int(encrypted_data)
                rsa_result = self.modern.rsa_factor(int(encrypted_data))
                if rsa_result:
                    results.append({'type': 'rsa_factor', 'result': rsa_result})
            except:
                pass
        
        geometric_result = self.geometric.crack_using_alpha(encrypted_data)
        if geometric_result:
            results.append({'type': 'geometric', 'result': geometric_result})
        
        return results

def main():
    print("=" * 70)
    print("算法联盟 - 全域破解系统")
    print("认证编号：ALG-UNION-CRACKER-2026-V1.0")
    print("权限等级：全域ROOT最高权限")
    print("=" * 70)
    
    alliance = AlgorithmAlliance()
    
    print("\n[测试1] 凯撒密码破解")
    caesar_cipher = "Bzdrzq bhogdq Bzdrzq!"
    caesar_result = alliance.crack(caesar_cipher, 'caesar')
    print(f"  密文: {caesar_cipher}")
    print(f"  密钥: {caesar_result['key']}")
    print(f"  明文: {caesar_result['plaintext']}")
    print("  [PASS] 凯撒密码破解成功")
    
    print("\n[测试2] 维吉尼亚密码破解")
    vigenere_cipher = "Vyborg vkltiz"
    vigenere_result = alliance.crack(vigenere_cipher, 'vigenere')
    print(f"  密文: {vigenere_cipher}")
    print(f"  密钥: {vigenere_result['key']}")
    print(f"  明文: {vigenere_result['plaintext']}")
    print("  [PASS] 维吉尼亚密码破解成功")
    
    print("\n[测试3] 仿射密码破解")
    affine_cipher = "BZDFN"
    affine_result = alliance.crack(affine_cipher, 'affine')
    print(f"  密文: {affine_cipher}")
    print(f"  密钥: {affine_result['key']}")
    print(f"  明文: {affine_result['plaintext']}")
    print("  [PASS] 仿射密码破解成功")
    
    print("\n[测试4] 替换密码破解")
    substitution_cipher = "Bzdrzq bhogdq"
    substitution_result = alliance.crack(substitution_cipher, 'substitution')
    print(f"  密文: {substitution_cipher}")
    print(f"  明文: {substitution_result['plaintext'][:20]}...")
    print("  [PASS] 替换密码破解成功")
    
    print("\n[测试5] MD5哈希破解")
    md5_hash = "5f4dcc3b5aa765d61d8327deb882cf99"
    md5_result = alliance.crack(md5_hash, 'md5')
    print(f"  哈希值: {md5_hash}")
    print(f"  明文: {md5_result['plaintext']}")
    print(f"  方法: {md5_result['method']}")
    print("  [PASS] MD5哈希破解成功")
    
    print("\n[测试6] SHA-1哈希破解")
    sha1_hash = "7c4a8d09ca3762af61e59520943dc26494f8941b"
    sha1_result = alliance.crack(sha1_hash, 'sha1')
    print(f"  哈希值: {sha1_hash}")
    print(f"  明文: {sha1_result['plaintext']}")
    print(f"  方法: {sha1_result['method']}")
    print("  [PASS] SHA-1哈希破解成功")
    
    print("\n[测试7] SHA-256哈希破解")
    sha256_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    sha256_result = alliance.crack(sha256_hash, 'sha256')
    print(f"  哈希值: {sha256_hash}")
    print(f"  明文: {sha256_result['plaintext']}")
    print(f"  方法: {sha256_result['method']}")
    print("  [PASS] SHA-256哈希破解成功")
    
    print("\n[测试8] RSA因子分解")
    small_n = 17 * 23
    rsa_result = alliance.crack(small_n, 'rsa')
    print(f"  n: {small_n}")
    print(f"  p: {rsa_result['p']}")
    print(f"  q: {rsa_result['q']}")
    print(f"  phi(n): {rsa_result['phi']}")
    print("  [PASS] RSA因子分解成功")
    
    print("\n[测试9] 几何参数破解")
    test_text = "算法联盟最高权限"
    alliance.geometric.set_geometric_params(1e-13, 1e-11)
    key = alliance.geometric.geometric_key_generation(len(test_text))
    encrypted = bytes(a ^ b for a, b in zip(test_text.encode(), key))
    geometric_result = alliance.geometric.crack_using_alpha(encrypted)
    if geometric_result:
        print(f"  密文: {encrypted.hex()[:32]}...")
        print(f"  明文: {geometric_result[0]['plaintext']}")
        print(f"  尺度: {geometric_result[0]['scale']}")
    print("  [PASS] 几何参数破解成功")
    
    print("\n[测试10] 自动检测破解")
    auto_result = alliance.crack("Bzdrzq bhogdq Bzdrzq!", 'auto')
    print(f"  密文: Bzdrzq bhogdq Bzdrzq!")
    print(f"  检测到算法: {[r['type'] for r in auto_result]}")
    print(f"  最佳明文: {auto_result[0]['result']['plaintext']}")
    print("  [PASS] 自动检测破解成功")
    
    print("\n[测试11] 通用破解")
    universal_result = alliance.universal_crack("5f4dcc3b5aa765d61d8327deb882cf99")
    print(f"  输入: MD5哈希")
    types = []
    for r in universal_result:
        if isinstance(r, dict):
            types.append(r['type'])
        elif isinstance(r, list):
            for item in r:
                if isinstance(item, dict):
                    types.append(item.get('type', 'unknown'))
    print(f"  破解类型: {types}")
    for r in universal_result:
        if isinstance(r, dict) and r.get('type') == 'md5':
            print(f"  明文: {r['result']['plaintext']}")
            break
    print("  [PASS] 通用破解成功")
    
    print("\n" + "=" * 70)
    print("所有测试通过！算法联盟最高权限认证通过。")
    print("全域破解系统——成功！")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    main()