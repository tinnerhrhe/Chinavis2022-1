node_priority = {
    'Domain': 1,            # 非常重要
    'IP': 1,
    'Cert': 1,
    'Whois_Name': 2,        # 重要
    'Whois_Phone': 2,
    'Whois_Email': 2,
    'IP_CIDR': 3,              # 一般
    'ASN': 3
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

# 推荐的最大跳转数
link_limit = {
    4: 1,
    3: 2,
    2: 3,
    1: 4
}
