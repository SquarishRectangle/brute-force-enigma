from enigma.machine import EnigmaMachine
import argparse
from tqdm import tqdm


CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def brute_force(code: str, dictionary: list):
    reflectors = ['B', 'C']
    rotors = ['I', 'II', 'III', 'IV', 'V']
    rotor_combinations = [f'{a} {b} {c}' for a in rotors for b in rotors for c in rotors]
    ring_settings = [f'{a} {b} {c}' for a in CHARSET for b in CHARSET for c in CHARSET]
    res = {}
    for reflector in tqdm(reflectors, desc='Reflectors', position=0, leave=None):
        for rotor_combination in tqdm(rotor_combinations, desc='Rotors', position=1, leave=None):
            for ring_setting in tqdm(ring_settings, desc='Rings', position=2, leave=None):
                e = EnigmaMachine.from_key_sheet(rotor_combination, ring_setting, reflector, plugboard_settings='HI')
                dec = e.process_text(code)
                score = 0
                for word in dictionary:
                    if word in dec:
                        score += 1
                if not score:
                    continue
                rotor_settings = [f'{r}:{s}' for r, s in zip(rotor_combination.split(' '), ring_setting.split(' '))]
                res[f'{dec} | [{" ".join(rotor_settings)}] + {reflector}'] = score

    res = dict(sorted(res.items(), key=lambda x: x[1], reverse=True))
    with open('results.txt', 'w') as f:
        for k, v in res.items():
            f.write(f'{v} | {k}\n')



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", '-c', help="Code to crack")
    parser.add_argument("--dictionary", '-d', help="Dictionary file")
    args = parser.parse_args()
    with open(args.dictionary, 'r') as f:
        dictionary = f.read().splitlines()
        dictionary = [word.upper() for word in dictionary if len(word) >= 3]
    code = args.code.upper()
    while ' ' in code:
        code = code.replace(' ', '')
    brute_force(code, dictionary)


if __name__ == '__main__':
    main()