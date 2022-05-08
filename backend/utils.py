type_value = {
        'Domain': 0,
        'IP': 1,
        'Cert': 2,
        'Whois_Name': 3,
        'Whois_Phone': 4,
        'Whois_Email': 5,
        'IP_C': 6,
        'ASN': 7
    }
value = {
        'Domain': 1,
        'IP': 1,
        'Cert': 1,
        'Whois_Name': 0.1,
        'Whois_Phone': 0.1,
        'Whois_Email': 0.1,
        'IP_C': 0.01,
        'ASN': 0.01
    }
link_priority = {
    'r_cert': 1,            # 很强
    'r_subdomain': 1,
    'r_request_jump': 1,
    'r_dns_a': 1,
    'r_whois_name': 2,      # 较强
    'r_whois_email': 2,
    'r_whois_phone': 2,
    'r_cert_chain': 3,      # 一般
    'r_cname': 3,
    'r_asn': 4,             # 较弱
    'r_cidr': 4
}
def d_weight(type):
    weight = {
        'r_cert': 18,  # 很强
        'r_subdomain': 1,
        'r_request_jump': 2,
        'r_dns_a': 10,
        'r_whois_name': 0.1,  # 较强
        'r_whois_email': 0.1,
        'r_whois_phone': 0.1,
        'r_cert_chain': 0,  # 一般
        'r_cname': 0.02,
        'r_asn': 0,  # 较弱
        'r_cidr': 0
    }
    if type == 'r_subdomain' or type == 'r_request_jump':
        return weight[type]
    else:
        return weight[type]
def ip_weight(type):
    weight = {
        'r_cert': 0,  # 很强
        'r_subdomain': 0,
        'r_request_jump': 0,
        'r_dns_a': 1,
        'r_whois_name': 0,  # 较强
        'r_whois_email': 0,
        'r_whois_phone': 0,
        'r_cert_chain': 0,  # 一般
        'r_cname': 0,
        'r_asn': 0.01,  # 较弱
        'r_cidr': 0.01
    }
    if type == 'r_dns_a':
        return weight[type]
    else:
        return weight[type]
def c_weight(type):
    weight = {
        'r_cert': 1,  # 很强
        'r_subdomain': 0,
        'r_request_jump': 0,
        'r_dns_a': 0,
        'r_whois_name': 0,  # 较强
        'r_whois_email': 0,
        'r_whois_phone': 0,
        'r_cert_chain': 0.1,  # 一般
        'r_cname': 0,
        'r_asn': 0,  # 较弱
        'r_cidr': 0
    }
    if type == 'r_cert':
        return weight[type]
    else:
        return weight[type]
