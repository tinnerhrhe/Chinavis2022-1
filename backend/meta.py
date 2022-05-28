node_priority = {
    'Domain': 1,            # 非常重要
    'IP': 1,
    'Cert': 1,
    'Whois_Name': 2,        # 重要
    'Whois_Phone': 2,
    'Whois_Email': 2,
    'IP_CIDR': 3,           # 一般
    'IP_C': 3,              
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

# 网络限制
net_limit = {
    'small' : { 'node': 400, 'edge': 800, 'corelimit': 6 },
    'medium': { 'node': 800, 'edge': 1600, 'corelimit': 10 },
    'large': { 'node': 3000, 'edge': 6000, 'corelimit': 20 }
}

## DEBUG USE ONLY
# net_limit = {
#     'small' : { 'node': 10, 'edge': 20, 'corelimit': 1 },
#     'medium': { 'node': 20, 'edge': 40, 'corelimit': 2 },
#     'large': { 'node': 30, 'edge': 80, 'corelimit': 3 }
# }

# 线索
evidence = [
    ["Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9", "small"],
    ["IP_400c19e584976ff2a35950659d4d148a3d146f1b71692468132b849b0eb8702c", "medium"],
    ["Domain_24acfd52f9ceb424d4a2643a832638ce1673b8689fa952d9010dd44949e6b1d9", "medium"],
    ["IP_7e730b193c2496fc908086e8c44fc2dbbf7766e599fabde86a4bcb6afdaad66e", "large"],
    ["IP_21ce145cae6730a99300bf677b83bbe430cc0ec957047172e73659372f0031b8","large"]
]