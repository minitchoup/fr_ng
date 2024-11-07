#!/usr/bin/env python3
import argparse
import sys
import hashlib
import time

def sortKeySymbols(d):
    """
    'd' est le dictionnaire associé à une touche du clavier, résultat de l'opération de lecture du fichier.
    La clé sont les coordonnées (ligne, colonne) de l'identifiant/symbole de la touche.
    Par exemple, pour la première touche :
    d = {( 1, 8): 'TLDE',
         (17, 6): '☒',
         (17, 8): '✗',
         (18, 6): '☑',
         (18, 8): '✓',
         (33, 6): '▶',
         (33, 8): '◀',
         (34, 6): '▷',
         (34, 8): '◁'}
    Note : les coordonnées des symboles sont données (ligne, colonne).
    La présente fonction remplace les coordonnées par un couple d'index.
    Ces couples d'index vont ensuite déterminer le rang du symbole dans la liste résultat :

         ( 1, 8) → il n'est pas considéré (numéro de ligne le plus petit)
         (17, 6) → (0, 0) → Q0 → #1
         (17, 8) → (0, 1) → Q0 → #3
         (18, 6) → (1, 0) → Q0 → #0
         (18, 8) → (1, 1) → Q0 → #2     ⎧rank = (yi + 1) % 2 + xi * 2 + qi * 4
         (33, 6) → (2, 0) → Q1 → #5     ⎩  qi = yi // 2
         (33, 8) → (2, 1) → Q1 → #7     
         (34, 6) → (3, 0) → Q1 → #4     ⇔rank = (yi + 1) % 2 + (xi + (yi // 2) * 2) * 2
         (34, 8) → (3, 1) → Q1 → #6
    
    Ensuite à chaque couple d'index est associé le rang correspondant...
    """
    yset = set()
    xset = set()
    ymin = None
    # Il existe un unique «symbole» pour lequel le numéro de ligne est minimal; c'est l'ID de la touche.
    for y, x in d.keys():
        if ymin is None or y < ymin:
            ymin = y
    yxki = None
    ki = None
    for (y, x), s in d.items():
        if y != ymin:
            yset.add(y)
            xset.add(x)
        else:
            assert yxki is None
            yxki = (y, x)
            ki = s
    ylst = list(yset)
    xlst = list(xset)
    ylst.sort()
    xlst.sort()
    ymap = dict([(y, i) for i, y in enumerate(ylst)])
    xmap = dict([(x, i) for i, x in enumerate(xlst)])
    symbols = dict()
    for (y, x), s in d.items():
        if y != ymin:
            yi = ymap[y]
            xi = xmap[x]
            symbols[(yi, xi)] = s
    #print(f"{d=} {symbols=} \n{'='*80}")
    result = [ki] + [None] * 8
    for (yi, xi), s in symbols.items():
        rank = (yi + 1) % 2 + (xi + (yi // 2) * 2) * 2 + 1
        if rank >= len(result):
            print(f"{d=}: for ({yi=}, {xi=}), {rank=}")
        else:
            result[rank] = s
    return result
    
def sortKeySymbols_(d):
    """
    'd' est le dictionnaire associé à une touche du clavier, résultat de l'opération de lecture du fichier.
    La clé sont les coordonnées (ligne, colonne) de l'identifiant/symbole de la touche.
    Par exemple, pour la première touche :
    d = {( 1, 8): 'TLDE',
         (17, 6): '☒',
         (17, 8): '✗',
         (18, 6): '☑',
         (18, 8): '✓',
         (33, 6): '▶',
         (33, 8): '◀',
         (34, 6): '▷',
         (34, 8): '◁'}
    La présente fonction remplace les coordonnées par un couple d'index.
    Ces couples d'index vont ensuite déterminer le rang du symbole dans la liste résultat :

         ( 1, 8) → il n'est pas considéré (numéro de ligne le plus petit)
         (17, 6) → (0, 0)
         (17, 8) → (0, 1)
         (18, 6) → (1, 0)
         (18, 8) → (1, 1)
         (33, 6) → (2, 0)
         (33, 8) → (2, 1)
         (34, 6) → (3, 0)
         (34, 8) → (3, 1)

    Ensuite à chaque couple d'index est associé le rang correspondant...
    """
    yset = set()
    xset = set()
    ymin = None
    # Il existe un unique «symbole» pour lequel le numéro de ligne est minimal; c'est l'ID de la touche.
    for y, x in d.keys():
        if ymin is None or y < ymin:
            ymin = y
    yxki = None
    ki = None
    for (y, x), s in d.items():
        if y != ymin:
            yset.add(y)
            xset.add(x)
        else:
            assert yxki is None
            yxki = (y, x)
            ki = s
    ylst = list(yset)
    xlst = list(xset)
    ylst.sort()
    xlst.sort()
    ymap = dict([(y, i) for i, y in enumerate(ylst)])
    xmap = dict([(x, i) for i, x in enumerate(xlst)])
    symbols = dict()
    for (y, x), s in d.items():
        if y != ymin:
            yi = ymap[y]
            xi = xmap[x]
            symbols[(yi, xi)] = s
    #print(f"{d=} {symbols=} \n{'='*80}")
    result = [
        ki,
        symbols.get((1, 0), None), symbols.get((0, 0), None), symbols.get((1, 1), None), symbols.get((0, 1), None),
        symbols.get((3, 0), None), symbols.get((2, 0), None), symbols.get((3, 1), None), symbols.get((2, 1), None)  ]
    return result
    
def printKbd(kbd, margin, outputfile):
    GROUP = "EIGHT_LEVEL"
    alias = {
        None: "NoSymbol",
        "^": "dead_circumflex",
        "¨": "dead_diaeresis",
        "Tab": "tab",
        "BTab": "ISO_Left_Tab",
        "Space": "space",
        "BSpace": "backspace"
    }
    ho = hashlib.sha1()
    def wr(txt):
        ho.update(txt.encode())
        outputfile.write(txt)
    for rownum, row in enumerate(kbd):
        wr(f"""
{margin}// ╭───────────┄
{margin}// │ ROW {rownum}
{margin}// ╰───────────────┄
""")
        for key in row:
            if len(key) <= 1:
                continue
            symbols = sortKeySymbols(key)
            #print(f"{key} // {symbols}")
            symByLvl = []
            for s1 in symbols[1:]:
                s2 = alias.get(s1, None)
                if s2 is None:
                    s2 = f"U{ord(s1):04X}"
                symByLvl.append(f"{s2:>15}")
            symByLvlTxt = ", ".join(symByLvl)
            symTxt = " ".join([((s if len(s) == 1 else "▓") if s is not None else "▒") for s in symbols[1:]])
            kiTxt = f"<{symbols[0]}>"
            wr(f'{margin}key {kiTxt:>6} {{ type[group1] = "{GROUP}", [{symByLvlTxt}] }}; // {symTxt}\n')
    return ho


def parseInput(inputpath, outputpath):

    # with open(inputpath, "r") as f:
    #     lines = f.readlines()
    if inputpath is None or inputpath == "-":
        inputpath = sys.stdin.fileno()
    inputfile = open(inputpath, "r")
    lines = []
    while True:
        line = inputfile.readline()
        if line == "":
            break
        lines.append(line)
    inputfile.close()
    
    hi = hashlib.sha1()
    ho = None

    # if outputpath is None or outputpath == "-":
    #     outputfile = sys.stdout
    # else:
    #     outputfile = open(outputpath, "w")
    if outputpath is None or outputpath == "-":
        outputpath = sys.stdout.fileno()
    outputfile = open(outputpath, "w")
        
    kbd = [[{} for _ in range(16)] for _ in range(5)]  # 5 rangées de 16 touches max composées symboles (clé=(x, y), value=symbole).
    phase = 0
    escape = None
    carry = ""
    memory = []
    for linum, line in enumerate(lines):
        if not line.startswith("///"):
            continue
        if not line[3:].startswith("⍰"):
            hi.update(line.encode())
        line = line.rstrip()
        outputfile.write(line + "\n")
        if line[3:].startswith("●"):
            memory.append(line[4:])
            continue
        if line[3:].startswith("☛"):
            margin = line[4:].replace("␣", " ")
            for line in memory:
                outputfile.write(line + "\n")
            memory.clear()
            ho = printKbd(kbd, margin, outputfile)
            continue
        if not line[3:].startswith("○"):
            continue
        for conum, c in enumerate(line[4:]):
            conum += 4
            #print(f"LOOP {linum=} {conum=} '{c}'")
            if escape != conum:
                escape = None
            # if c == "\n":
            if conum == len(line) - 1:
                if phase == 2:
                    phase = 1
                break
            if escape is None and c == "\\":
                escape = conum + 1
                continue

            match phase:
                case 0: # Recherche du début de la description du clavier...
                    if escape is None and c in ("┌", "┏"):
                        idxRow = 0
                        row = None
                        key = None
                        phase = 1
                        break  # Le reste de la ligne est ignoré.
                case 1: # Recherche du début de la ligne de la rangée...
                    if escape is None and c in ("└", "┗"):
                        # Fin de la description du clavier.
                        phase = 0
                        break  # Le reste de la ligne est ignoré.
                    if escape is None and c in ("├", "┣", "┢", "┡"):
                        idxRow += 1
                        row = None
                        break  # Le reste de la ligne est ignoré.
                    if escape is None and c in ("│", "┃"):
                        # La première touche de la rangée
                        if row is None:
                            row = kbd[idxRow]
                        idxKey = 0
                        key = None
                        # idxLineKey = 0
                        # idxSymLineKey = 0
                        phase = 2
                case 2: # Traitement des touches de la rangée
                    if key is None:
                        key = row[idxKey]

                    if escape is None and c in (" ", "│", "┃") or escape is not None: 
                        # C'est un séparateur (le caractère escape '\' est considéré comme un séparateur):
                        # Il faut stocker 'carry' pour le symbole ciblé de la touche courante.
                        if len(carry) > 0:
                            scoord = (linum + 1, conum - 1 if escape is None else conum - 2)
                            key[scoord] = (carry if carry != "NA" else None)
                            carry = ""
                        if escape is None:
                            if c != " ":
                                # on passe à la touche suivante de la rangée
                                idxKey += 1
                                key = None
                        else:
                            carry = c
                    else:
                        if c != "▒":
                            carry += c
                        else:
                            carry = "NA"

    for line in memory:
        outputfile.write(line + "\n")
    outputfile.write(f"///⍰ Generation Date {time.strftime('%Y%m%d-%H%M%S')} - ISha1: {hi.hexdigest()} OSha1: {ho.hexdigest() if ho is not None else '-'}\n")
    outputfile.close()

if __name__ == "__main__":
    epilog = """
    
"""
    parser = argparse.ArgumentParser(
                prog='mkXKB',
                description=f'An XKB maker‼',
                argument_default=["-h"],
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=epilog)
    parser.add_argument("-i", "--input", default=None, help="File to process for XKB generation.")
    parser.add_argument("-I", "--in-place", action="store_true", default=False, help="The input file will be replaced by the result of the generation.")
    parser.add_argument("-o", "--output", default=None, help="File to generate.")
    args = parser.parse_args()
    if args.in_place and args.output is None:
        args.output = args.input
    parseInput(args.input, args.output)
