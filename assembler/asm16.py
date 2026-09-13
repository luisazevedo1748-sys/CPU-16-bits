#!/usr/bin/env python3
"""
asm16 - assemblador para a CPU de 16 bits

Uso:
    python asm16.py programa.asm            -> escreve programa.hex
    python asm16.py programa.asm saida.hex

O ficheiro .hex e' carregado no Digital com:
    botao direito na ROM -> Dados -> Editar -> Arquivo -> Abrir
"""

import sys
import re

# opcode -> (codigo, formato)
# formatos:
#   N  sem operandos
#   R  rd, ra, rb
#   L  rd, (ra)
#   S  rdado, (ra)
#   I  rd, imm6
#   J  endereco
#   B  ra, rb, endereco
#   P  ra          (PUSH, registo no campo RA2)
#   O  rd          (POP, registo no campo WA)
#   C  (ra)        (CALL indireto, registo no campo RA1)
OPCODES = {
    'NOP':   (0b0000, 'N'),
    'ADD':   (0b0001, 'R'),
    'SUB':   (0b0010, 'R'),
    'MUL':   (0b0011, 'R'),
    'DIV':   (0b0100, 'R'),
    'SHL':   (0b0101, 'R'),
    'SHR':   (0b0110, 'R'),
    'AND':   (0b0111, 'R'),
    'OR':    (0b1000, 'R'),
    'XOR':   (0b1001, 'R'),
    'LOAD':  (0b1010, 'L'),
    'LDI':   (0b1011, 'I'),
    'JMP':   (0b1100, 'J'),
    'BEQ':   (0b1101, 'B'),
    'BNE':   (0b1110, 'B'),
    'STORE': (0b1111, 'S'),
}

# instrucoes tipo F: opcode 0000 com o campo funct nos bits 8-6
FUNCT = {
    'PUSH':  (1, 'P'),
    'POP':   (2, 'O'),
    'CALL':  (3, 'C'),
    'RET':   (4, 'N'),
    'MFHI':  (5, 'O'),
    'HLT':   (6, 'N'),
}

MAX_PROG = 256


class ErroAsm(Exception):
    pass


def limpa(linha):
    """Remove comentarios (; ou #) e espaco supérfluo."""
    linha = re.split(r'[;#]', linha, maxsplit=1)[0]
    return linha.strip()


def reg(tok, nl):
    """Converte R0..R3 no numero do registo."""
    m = re.fullmatch(r'[Rr]([0-3])', tok.strip())
    if not m:
        raise ErroAsm(f"linha {nl}: '{tok}' nao e' um registo valido (R0 a R3)")
    return int(m.group(1))


def reg_indireto(tok, nl):
    """Converte (R1) no numero do registo."""
    m = re.fullmatch(r'\(\s*[Rr]([0-3])\s*\)', tok.strip())
    if not m:
        raise ErroAsm(f"linha {nl}: '{tok}' nao e' um endereco indireto valido, "
                      f"esperava (R0) a (R3)")
    return int(m.group(1))


def numero(tok, nl):
    """Aceita decimal, 0x hex, 0b binario."""
    tok = tok.strip()
    try:
        if tok.lower().startswith('0x'):
            return int(tok, 16)
        if tok.lower().startswith('0b'):
            return int(tok, 2)
        return int(tok, 10)
    except ValueError:
        raise ErroAsm(f"linha {nl}: '{tok}' nao e' um numero")


def separa(resto, n, nl, mnem):
    """Parte os operandos por virgulas e confirma a quantidade."""
    if not resto.strip():
        partes = []
    else:
        partes = [p.strip() for p in resto.split(',')]
    if len(partes) != n:
        raise ErroAsm(f"linha {nl}: {mnem} espera {n} operando(s), "
                      f"recebeu {len(partes)}")
    return partes


def primeira_passagem(linhas):
    """Recolhe as etiquetas e a lista de instrucoes com a sua posicao."""
    etiquetas = {}
    instrucoes = []   # (posicao, num_linha, mnemonica, resto)
    pos = 0

    for nl, bruta in enumerate(linhas, 1):
        linha = limpa(bruta)
        if not linha:
            continue

        # etiquetas: uma ou mais no inicio da linha
        while True:
            m = re.match(r'^([A-Za-z_]\w*)\s*:\s*(.*)$', linha)
            if not m:
                break
            nome = m.group(1)
            if nome.upper() in OPCODES or nome.upper() in FUNCT:
                raise ErroAsm(f"linha {nl}: '{nome}' e' uma mnemonica, "
                              f"nao pode ser etiqueta")
            if nome in etiquetas:
                raise ErroAsm(f"linha {nl}: etiqueta '{nome}' repetida")
            etiquetas[nome] = pos
            linha = m.group(2).strip()

        if not linha:
            continue

        partes = linha.split(None, 1)
        mnem = partes[0].upper()
        resto = partes[1] if len(partes) > 1 else ''

        if mnem == '.WORD':
            for tok in resto.split(','):
                instrucoes.append((pos, nl, '.WORD', tok.strip()))
                pos += 1
            continue

        if mnem not in OPCODES and mnem not in FUNCT:
            raise ErroAsm(f"linha {nl}: instrucao desconhecida '{partes[0]}'")

        instrucoes.append((pos, nl, mnem, resto))
        pos += 1

    if pos > MAX_PROG:
        raise ErroAsm(f"programa com {pos} palavras, o maximo e' {MAX_PROG} "
                      f"(o campo de endereco tem 8 bits)")

    return etiquetas, instrucoes, pos


def resolve_endereco(tok, etiquetas, nl):
    tok = tok.strip()
    if re.fullmatch(r'[A-Za-z_]\w*', tok):
        if tok not in etiquetas:
            raise ErroAsm(f"linha {nl}: etiqueta '{tok}' nao existe")
        return etiquetas[tok]
    return numero(tok, nl)


def montar(linhas):
    etiquetas, instrucoes, tamanho = primeira_passagem(linhas)
    palavras = [0] * tamanho

    for pos, nl, mnem, resto in instrucoes:

        if mnem == '.WORD':
            v = resolve_endereco(resto, etiquetas, nl)
            if not 0 <= v <= 0xFFFF:
                raise ErroAsm(f"linha {nl}: valor {v} nao cabe em 16 bits")
            palavras[pos] = v
            continue

        if mnem in FUNCT:
            funct, fmt = FUNCT[mnem]
            base = funct << 6
            if fmt == 'N':
                separa(resto, 0, nl, mnem)
                palavras[pos] = base
            elif fmt == 'P':
                a, = separa(resto, 1, nl, mnem)
                palavras[pos] = base | (reg(a, nl) << 2)
            elif fmt == 'O':
                a, = separa(resto, 1, nl, mnem)
                palavras[pos] = base | (reg(a, nl) << 4)
            elif fmt == 'C':
                a, = separa(resto, 1, nl, mnem)
                palavras[pos] = base | reg_indireto(a, nl)
            continue

        codigo, fmt = OPCODES[mnem]

        if fmt == 'N':
            separa(resto, 0, nl, mnem)
            palavra = codigo << 12

        elif fmt == 'R':
            a, b, c = separa(resto, 3, nl, mnem)
            wa, ra1, ra2 = reg(a, nl), reg(b, nl), reg(c, nl)
            palavra = (codigo << 12) | (wa << 4) | (ra2 << 2) | ra1

        elif fmt == 'L':
            a, b = separa(resto, 2, nl, mnem)
            wa, ra1 = reg(a, nl), reg_indireto(b, nl)
            palavra = (codigo << 12) | (wa << 4) | ra1

        elif fmt == 'S':
            a, b = separa(resto, 2, nl, mnem)
            ra2, ra1 = reg(a, nl), reg_indireto(b, nl)
            palavra = (codigo << 12) | (ra2 << 2) | ra1

        elif fmt == 'I':
            a, b = separa(resto, 2, nl, mnem)
            wa = reg(a, nl)
            imm = resolve_endereco(b, etiquetas, nl)
            if not 0 <= imm <= 63:
                raise ErroAsm(f"linha {nl}: imediato {imm} fora de 0..63 "
                              f"(o campo tem 6 bits)")
            palavra = (codigo << 12) | (imm << 6) | (wa << 4)

        elif fmt == 'J':
            a, = separa(resto, 1, nl, mnem)
            addr = resolve_endereco(a, etiquetas, nl)
            if not 0 <= addr <= 255:
                raise ErroAsm(f"linha {nl}: endereco {addr} fora de 0..255")
            palavra = (codigo << 12) | (addr << 4)

        elif fmt == 'B':
            a, b, c = separa(resto, 3, nl, mnem)
            ra1, ra2 = reg(a, nl), reg(b, nl)
            addr = resolve_endereco(c, etiquetas, nl)
            if not 0 <= addr <= 255:
                raise ErroAsm(f"linha {nl}: endereco {addr} fora de 0..255")
            palavra = (codigo << 12) | (addr << 4) | (ra2 << 2) | ra1

        palavras[pos] = palavra

    return palavras, etiquetas


def escreve_hex(palavras, caminho):
    """Formato que o Digital le: cabecalho v2.0 raw + valores em hex."""
    with open(caminho, 'w') as f:
        f.write('v2.0 raw\n')
        for i in range(0, len(palavras), 8):
            f.write(' '.join('%x' % p for p in palavras[i:i + 8]) + '\n')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2] if len(sys.argv) > 2 else re.sub(r'\.asm$', '', entrada) + '.hex'

    try:
        with open(entrada) as f:
            linhas = f.readlines()
    except OSError as e:
        print(f"erro: nao consegui abrir {entrada}: {e}")
        sys.exit(1)

    try:
        palavras, etiquetas = montar(linhas)
    except ErroAsm as e:
        print(f"ERRO: {e}")
        sys.exit(1)

    escreve_hex(palavras, saida)

    print(f"{len(palavras)} palavras -> {saida}\n")
    for i, p in enumerate(palavras):
        nomes = [n for n, v in etiquetas.items() if v == i]
        etiq = ('  <- ' + ', '.join(nomes)) if nomes else ''
        print(f"  {i:3d}  0x{p:04X}{etiq}")


if __name__ == '__main__':
    main()
