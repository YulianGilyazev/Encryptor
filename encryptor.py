#!/usr/bin/env python3
import argparse
import string

alphabet = string.ascii_lowercase
ALPHABET = string.ascii_uppercase
alphLen = len(alphabet)


def _encode(key, str):
    out = list()
    for alpha in str:
        if alpha.islower():
            out.append(alphabet[(alphabet.find(alpha, 0, alphLen) + key) % alphLen])
        elif alpha.isupper():
             out.append(ALPHABET[(ALPHABET.find(alpha, 0, alphLen) + key) % alphLen])
        else:
            out.append(alpha)
    return ''.join(out)


def mk_model(train_str):
    model_dict = dict()
    alpha_count = 0
    for alpha in alphabet:
        model_dict[alpha] = 0
    for alpha in train_str:
        if alpha.isalpha():
            alpha_count += 1
            model_dict[alpha.lower()] += 1
    for alpha in alphabet:
        model_dict[alpha] /= alpha_count
    return(model_dict)


def _hack(model_dict, input_str):
    min_disp = alphLen
    min_key = 0
    zero_key_model = mk_model(input_str)
    my_dc = dict()
    for ind in range(alphLen):
        for j in range(alphLen):
            my_dc[alphabet[j]] = zero_key_model[alphabet[(j - ind) % alphLen]]
        disp = 0
        for alpha in alphabet:
            disp += (model_dict[alpha] - my_dc[alpha])**2
        if disp < min_disp:
            min_disp = disp
            min_key = ind
    return _encode(min_key, input_str)


def vigenere_hack(model_dict, input_str):
    alpha_count = 0
    for symbol in input_str:
        if symbol.isalpha():
            alpha_count += 1
    max_len = int(alpha_count / 100)
    key_len = 0
    max_ind = 0
    for cur_len in range(max_len, 1, -1):
        s = list()
        for i in range(cur_len):
            s.append(input_str[i::cur_len])
        cur_ind_of_coinc = 0
        for i in range(cur_len):
            dc = mk_model(s[i])
            for alpha in alphabet:
                cur_ind_of_coinc += dc[alpha] ** 2
        cur_ind_of_coinc /= cur_len
        if max_ind < cur_ind_of_coinc * 1.06:
            max_ind = cur_ind_of_coinc
            key_len = cur_len
    key = ''
    s = list()
    for ind in range(key_len):
        s.append(_hack(model_dict, input_str[ind::key_len]))
    out = list()
    for ind in range(len(input_str)):
        out.append(s[ind % key_len][int(ind / key_len)])
    return ''.join(out)


def vigenere_cipher(input_str, key):
    out_str = list()
    key = key.lower()
    for ind in range(len(input_str)):
        if input_str[ind].islower():
            out_str.append(alphabet[(alphabet.find(key[ind % len(key)], 0, alphLen) + alphabet.find(input_str[ind], 0, alphLen)) % alphLen])
        elif input_str[ind].isupper():
            out_str.append(ALPHABET[(alphabet.find(key[ind % len(key)], 0, alphLen) + ALPHABET.find(input_str[ind], 0, alphLen)) % alphLen])
        else:
            out_str.append(input_str[ind])
    return ''.join(out_str)


def vernam_cipher(input_str, key):
    _alphabet = ''.join([alphabet, '!@#$%^'])
    _alphLen = len(_alphabet)
    if len(key) < len(input_str):
        return 'INCORRECT'
    out_str = list()
    key = key.lower()
    for ind in range(len(input_str)):
        if _alphabet.find(input_str[ind]) != -1:
            out_str.append(_alphabet[(alphabet.find(input_str[ind]) ^ _alphabet.find(key[ind])) % _alphLen])
        else:
            out_str.append(input_str[ind])
    return ''.join(out_str)


def _read(inp):
    if inp is not None:
        with open(inp, 'r') as file:
            input_str = file.read()
    else:
        input_str = input()
    return input_str


def _write(output_str, outp):
    if outp is not None:
        with open(outp, 'w') as file:
            file.write(output_str)
    else:
        print(output_str)


def encode_action(key, inp, outp, cipher):
    input_str = _read(inp)
    if cipher == 'caesar':
        key = int(key)
        out_str = _encode(key, input_str)
        _write(out_str, outp)
    if cipher == 'vigenere':
        out_str = vigenere_cipher(input_str, key)
        _write(out_str, outp)
    if cipher == 'vernam':
        out_str = vernam_cipher(input_str, key)
        _write(out_str, outp)


def get_args():
    action = None
    cipher = None
    key = None
    inp = None
    outp = None
    text = None
    model = None
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='action')
    encode = subs.add_parser('encode', help='Encode')
    encode.add_argument('--cipher', help='Cipher')
    encode.add_argument('--key', dest='key', help='Key')
    encode.add_argument('--input-file', dest='input', help='Input file')
    encode.add_argument('--output-file', dest='output', help='Ouput file')
    decode = subs.add_parser('decode', help='Decode')
    decode.add_argument('--cipher', help='Cipher')
    decode.add_argument('--key', dest='key', help='Key')
    decode.add_argument('--input-file', dest='input', help='Input file')
    decode.add_argument('--output-file', dest='output', help='Ouput file')
    train = subs.add_parser('train', help='Train')
    train.add_argument('--text-file', dest='text', help='Text file')
    train.add_argument('--model-file', dest='model', help='Model file')
    hack = subs.add_parser('hack', help='Hack')
    hack.add_argument('--input-file', dest='input', help='Input file')
    hack.add_argument('--output-file', dest='output', help='Ouput file')
    hack.add_argument('--model-file', dest='model', help='Model file')
    args = parser.parse_args()
    return args


def read_model(model):
    str = _read(model)
    ind = 0
    model_dict = dict()
    cur_dig = ''
    for alpha in str:
        if alpha.isdigit() or alpha == '.':
            cur_dig = ''.join([cur_dig, alpha])
        elif cur_dig != '':
            model_dict[alphabet[ind]] = float(cur_dig)
            cur_dig = ''
            ind += 1
    return model_dict


def main():
    args = get_args()
    if args.action == 'encode':
        encode_action(args.key, args.input, args.output, args.cipher)
    if args.action == 'decode':
        if args.cipher == 'caesar':
            encode_action((alphLen - int(args.key)) % alphLen, args.input, args.output, args.cipher)
        if args.action == 'vernam':
            encode_action(args.key, args.input, args.output, args.cipher)
        if args.cipher == 'vigenere':
            _key = ''
            args.key = args.key.lower()
            for i in args.key:
                _key += alphabet[(-alphabet.find(i) + alphLen) % alphLen]
            encode_action(_key, args.input, args.output, args.cipher)
    if args.action == 'train':
        text_str = _read(args.text)
        model_dict = mk_model(text_str)
        _write(str(model_dict), args.model)
    if args.action == 'hack':
        input_str = _read(args.input)
        model_dict = read_model(args.model)
        out_str = vigenere_hack(model_dict, input_str)
        _write(out_str, args.output)


if __name__ == '__main__':
    main()
