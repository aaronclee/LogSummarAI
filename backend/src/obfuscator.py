import re

# Global mappings to store reversible tokenization.
email_mapping = {}
ip_mapping = {}
email_counter = 1
ip_counter = 1

def obfuscate(log_line):
    """
    Masks email addresses and IP addresses in the log line.
    Stores mappings for later recomposition.
    """
    global email_counter, ip_counter
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    
    # Obfuscate emails.
    emails = re.findall(email_pattern, log_line)
    for email in emails:
        if email not in email_mapping:
            token = f"USERNAME-{email_counter:02d}"
            email_mapping[email] = token
            email_counter += 1
        else:
            token = email_mapping[email]
        log_line = log_line.replace(email, token)
    
    # Obfuscate IP addresses.
    ips = re.findall(ip_pattern, log_line)
    for ip in ips:
        if ip not in ip_mapping:
            token = f"IP-ADDRESS-{ip_counter:02d}"
            ip_mapping[ip] = token
            ip_counter += 1
        else:
            token = ip_mapping[ip]
        log_line = log_line.replace(ip, token)
    
    return log_line

def deobfuscate(text):
    """
    Replaces obfuscated tokens with original sensitive data.
    """
    for original, token in email_mapping.items():
        text = text.replace(token, original)
    for original, token in ip_mapping.items():
        text = text.replace(token, original)
    return text