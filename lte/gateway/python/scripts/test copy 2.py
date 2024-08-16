import base64
import zlib
from typing import NamedTuple
from EC import ECDH_SECP256R1

class home_network_key_pair(NamedTuple):
    home_network_public_key: bytes
    home_network_private_key: bytes

class HomeNetworkKeyPairGen(object):
    """
    Class to generate public/private keys for ProfileB
    """

    def __init__(self):
        """
        Init the class object
        """
        self.home_network_key_pair = home_network_key_pair(b'', b'')

    def core_home_network_key_gen(self):
        """
        Generate keys for ProfileB
        """
        ec = ECDH_SECP256R1()
        ec.generate_keypair()

        self.home_network_key_pair = home_network_key_pair(
            ec.get_pubkey(),
            ec.get_privkey(),
        )

    def get_home_network_public_key(self):
        """
        Get ProfileB public key
        """
        return self.home_network_key_pair.home_network_public_key

    def get_home_network_private_key(self):
        """
        Get ProfileB private key
        """
        return self.home_network_key_pair.home_network_private_key

    def print_key_pair(self):
        """
        Print the ProfileB key pair in hexadecimal and base64 formats
        """
        public_key_hex = self.home_network_key_pair.home_network_public_key.hex()
        private_key_hex = self.home_network_key_pair.home_network_private_key.hex()

        public_key_compressed = zlib.compress(self.home_network_key_pair.home_network_public_key)
        private_key_compressed = zlib.compress(self.home_network_key_pair.home_network_private_key)

        public_key_base64 = base64.b64encode(public_key_compressed).decode('utf-8')
        private_key_base64 = base64.b64encode(private_key_compressed).decode('utf-8')

        print("ProfileB Public Key (hexadecimal):", public_key_hex)
        print("ProfileB Private Key (hexadecimal):", private_key_hex)
        print("ProfileB Public Key (compressed, base64):", public_key_base64)
        print("ProfileB Private Key (compressed, base64):", private_key_base64)

def generate_profileb_keypair_and_print():
    """
    Generate ProfileB keypair and print the keys in hexadecimal and base64 formats.
    """
    home_network_keypair_gen = HomeNetworkKeyPairGen()
    home_network_keypair_gen.core_home_network_key_gen()
    home_network_keypair_gen.print_key_pair()

if __name__ == "__main__":
    generate_profileb_keypair_and_print()
