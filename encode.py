from enigma.machine import EnigmaMachine
import argparse


def encode(msg: str, rotors: str, reflector: str, ring_settings: str, plugs: str):
    e = EnigmaMachine.from_key_sheet(rotors=rotors, reflector=reflector, ring_settings=ring_settings, plugboard_settings=plugs)
    print(e.process_text(msg))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--msg', '-m', help='Message to encode')
    parser.add_argument('--rotors', '-ro', help='Rotors to use')
    parser.add_argument('--reflector', '-rf', help='Reflector to use')
    parser.add_argument('--ring_settings', '-ri', help='Ring settings')
    parser.add_argument('--plugs', '-p', help='Plugboard settings')
    args = parser.parse_args()
    encode(args.msg, args.rotors, args.reflector, args.ring_settings, args.plugs)


if __name__ == '__main__':
    main()