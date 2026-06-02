# Study Notes: Cryptographic Hash Functions

A **cryptographic hash function** maps an input of arbitrary length to a
fixed-size output (the **digest**). Three security properties matter:

1. **Preimage resistance.** Given a digest `h`, it is computationally
   infeasible to find any input `m` such that `H(m) = h`.

2. **Second preimage resistance.** Given an input `m1`, it is infeasible to
   find a different input `m2` such that `H(m1) = H(m2)`.

3. **Collision resistance.** It is infeasible to find any two distinct inputs
   `m1`, `m2` such that `H(m1) = H(m2)`.

## Modern hash functions

- **SHA-256** (part of the SHA-2 family). 256-bit output. Widely deployed.
- **SHA-3** (Keccak). 224, 256, 384, or 512-bit output. Designed differently
  from SHA-2, providing diversity in case SHA-2 is broken.
- **BLAKE2** and **BLAKE3**. Fast modern hashes used in checksums and
  content-addressable storage.

## Broken hashes

- **MD5** (1992). Collisions found in 2004. Do not use for security.
- **SHA-1** (1995). Collision demonstrated by Google's SHAttered (2017).
  Do not use for security; OK for non-security purposes like Git object IDs.

## Common uses

- Verifying integrity of downloads (the checksum next to the file).
- Storing password verifiers (with a slow, salted hash like Argon2 or bcrypt).
- Content addressing (Git, IPFS).
- Commitment schemes in cryptographic protocols.
