# ElGamal Homomorphic Property

ElGamal encryption exhibits a **multiplicative homomorphic property**, meaning that multiplying two ciphertexts results in an encryption of their product.

## How It Works

Given:
- \( (c1_1, c2_1) \) as the encryption of \( m1 \)
- \( (c1_2, c2_2) \) as the encryption of \( m2 \)

Multiplying the ciphertext components:

$$
c1 = (c1_1 \times c1_2) \mod p
$$

$$
c2 = (c2_1 \times c2_2) \mod p
$$

Decrypting the modified ciphertext \( (c1, c2) \) reveals:

$$
m = (m1 \times m2) \mod p
$$

Thus, **ElGamal supports multiplication over encrypted values without needing to decrypt them first.**
