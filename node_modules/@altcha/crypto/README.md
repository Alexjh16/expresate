# ALTCHA JS Crypto Library

A lightweight library simplifying asymmetric data encryption using Web Crypto. It employs a hybrid approach combining RSA keys and AES encryption for enhanced security.

## Features

- Simplified hybrid encryption using RSA + AES
- Compatible with all modern browsers supporting Web Crypto
- Supports node.js streams, facilitating encryption of large files

## Compatibility

- Node.js 20+
- Bun 1+
- Deno 1+
- Modern browsers

## Usage

```ts
import { cipher, rsa } from '@altcha/crypto';

const keyPair = await rsa.generateKeyPair();

const encrypted = await cipher.encrypt(keyPair.publicKey, new TextEncoder().encode('Hello World'));

const decrypted = await cipher.decrypt(keyPair.privateKey, encrypted);
```

Node.js streams:

```ts
import { createReadStream, createWriteStream } from 'node:fs';
import { nodeCipher, rsa } from '@altcha/crypto';

const keyPair = await rsa.generateKeyPair();

await nodeCipher.encryptStream(keyPair.publicKey, createReadStream('./input.txt'), createWriteStream('./output.txt.enc'));
```

## API

TODO

## License

MIT