import socket
import random
from sympy import isprime
import threading
import time

def generate_large_prime(n):
    while True:
        p = random.getrandbits(n)
        if isprime(p):
            return p

def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1
    while True:
        g = random.randint(2, p - 1)
        if not (pow(g, (p - 1) // p1, p) == 1):
            if not pow(g, (p - 1) // p2, p) == 1:
                return g

def elgamal_encryption(p, g, n, m):
    r = random.randint(1, p - 1)
    c1 = pow(g, r, p)
    s = pow(pow(g, n, p), r, p)
    c2 = (m * s) % p
    print(f"Encryption: m={m}, r={r}, c1={c1}, s={s}, c2={c2}")
    return c1, c2, s

def elgamal_decryption(p, s, c2):
    decrypted = (c2 * pow(s, p - 2, p)) % p
    print(f"Decryption: s={s}, c2={c2}, decrypted={decrypted}")
    return decrypted

def elgamal_homomorphic_property(p, g, n, m1, m2):
    c1_1, c2_1, s1 = elgamal_encryption(p, g, n, m1)
    c1_2, c2_2, s2 = elgamal_encryption(p, g, n, m2)
    c1 = (c1_1 * c1_2) % p
    c2 = (c2_1 * c2_2) % p
    decrypted_m = elgamal_decryption(p, (s1 * s2) % p, c2)
    print(f"Homomorphic Property: Encrypted {m1} * {m2}, Decrypted result: {decrypted_m}")
    return decrypted_m == (m1 * m2) % p

def handle_client(client_socket, p, g, n):
    print("Handling new client connection...")
    client_socket.sendall(f"{p},{g},{n}".encode())
    data = client_socket.recv(1024).decode()
    print(f"Received encrypted data: {data}")
    c1, c2 = map(int, data.split(","))
    s = pow(c1, n, p)
    decrypted_msg = elgamal_decryption(p, s, c2)
    client_socket.sendall(f"Decrypted message: {decrypted_msg}".encode())
    print("Sent decrypted message back to client.")
    client_socket.close()

def server():
    p = generate_large_prime(256)
    g = find_primitive_root(p)
    n = random.randint(1, p)
    print(f"Server setup complete with p={p}, g={g}, n={n}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("Server listening on port 9999...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, p, g, n))
        client_thread.start()

def client(message):
    print("Client starting...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 9999))
    data = client_socket.recv(1024).decode()
    print(f"Received server parameters: {data}")
    p, g, n = map(int, data.split(","))
    c1, c2, _ = elgamal_encryption(p, g, n, message)
    print(f"Sending encrypted data: {c1},{c2}")
    client_socket.sendall(f"{c1},{c2}".encode())
    response = client_socket.recv(1024).decode()
    print(f"Received response from server: {response}")
    client_socket.close()

if __name__ == "__main__":
    server_thread = threading.Thread(target=server)
    server_thread.start()
    
    
    time.sleep(2)
    client(1337)
    print("Testing homomorphic property:")
    m1, m2 = 1337, 7331
    result = elgamal_homomorphic_property(generate_large_prime(4096), find_primitive_root(generate_large_prime(4096)), random.randint(1, generate_large_prime(4096)), m1, m2)
    print(f"Homomorphic property verified: {result}")
    exit(0)