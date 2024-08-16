# Import the required modules
import base64
from EC import ECDH_SECP256R1

# Create an instance of the ECDH_SECP256R1 class
ecdh_secp256r1 = ECDH_SECP256R1()

# Generate the keypair
ecdh_secp256r1.generate_keypair()

# Get the public key
public_key = ecdh_secp256r1.get_pubkey()

# Get the private key
private_key = ecdh_secp256r1.get_privkey()

# Convert the keys to hexadecimal and base64
public_key_hex = public_key.hex()
private_key_hex = private_key.hex()

public_key_base64 = base64.b64encode(public_key).decode('utf-8')
private_key_base64 = base64.b64encode(private_key).decode('utf-8')

# Print the keys in both formats
print("Public Key (hex):", public_key_hex)
print("Public Key (base64):", public_key_base64)
print("Private Key (hex):", private_key_hex)
print("Private Key (base64):", private_key_base64)
