import binascii
import os.path as osp
import numpy as np
import random

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    '''Convert string to list of binary packets of length 7 bit'''
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    bits = bits.zfill(8 * ((len(bits) + 7) // 8))
    split_bits = [bits[i+1:i+8] for i in range(0, len(bits), 8)]
    return split_bits

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    '''Convert list of binary packets of length 7 to string'''
    bits = '0' + '0'.join(bits)
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    '''Convert int to bytes'''
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def generate_K(length=1):
    '''Generate random DNA string sequence of `length` symbols long'''
    nucleotides = ['A', 'T', 'G', 'C']
    secure_random = random.SystemRandom()
    K = ''.join([secure_random.choice(nucleotides) for i in range(length)])
    return K

def wat_comp(dna):
    '''Returns Watson-complimentary of DNA string'''
    comp_dict = {'A': 'T', 'T': 'A', 'G': "C", 'C': 'G'}

    complimentary = ''
    for i, nucleotide in enumerate(dna):
        complimentary += comp_dict.get(nucleotide, dna[i])
    return complimentary

def pairing_successful(A, B):
    '''Returns True if A and B can be paired with 100% match'''
    if wat_comp(A) == B:
        return True
    else:
        return False

def encrypt(K, M):
    '''Encrypt list of binary strings of length 7 bits `M` to DNA using key `K`'''
    C = []         # Список пакетов зашифрованного сообщения
    M = ''.join(M) # Всё сообщение одной строкой
    seq = 0        # номер пакета
    for i, bit in enumerate(M):
        if int(bit):
            key_part = K[len(K)-10 -10*i : len(K) - 10*i] # 10-мер справа длиной 10 от ключа
            packet = wat_comp(key_part) + str(seq)
            C.append(packet)
            seq += 1
    return C

def decrypt(K, C):
    '''Decrypt DNA string `C` to list of binary strings of length 7 `M_bin` using key `K`'''
    M_bin = ''
    K_parts = [K[i:i+10] for i in range(0, len(K), 10)]

    search_idx = len(K_parts)
    for packet in C:
        msg_id = int(packet[10:])
        msg = packet[:10]

        for part in K_parts[search_idx-1::-1]:
            if pairing_successful(part, msg):
                M_bin += '1'
                search_idx -= 1
                break
            else:
                M_bin += '0'
                search_idx -= 1
    split_bits = [M_bin[i:i+7] for i in range(0, len(M_bin), 7)]
    return split_bits