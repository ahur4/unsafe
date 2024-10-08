from unsafe import network

ports = [
    80, 443, 9001, 27017
]

scanner = network.port_scanner(host="127.0.0.1", ports=ports)
if scanner:
    print("This ports are open :", scanner)
