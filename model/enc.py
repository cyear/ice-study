from hashlib import md5
import time

def enc():
    m_time = str(int(time.time() * 1000))
    m_token = '4faa8662c59590c6f43ae9fe5b002b42'
    m_encrypt_str = 'token=' + m_token + '&_time=' + m_time + '&DESKey=Z(AfY@XS'
    m_inf_enc = md5(m_encrypt_str.encode('utf-8')).hexdigest()
    return m_time, m_inf_enc
