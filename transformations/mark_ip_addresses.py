
def handler(data, log):
    ip = data.get('ip_address', '')
    masked_ip = '.'.join(ip.split('.')[:-1] + ['0'])
    data['ip_address'] = masked_ip

    return data