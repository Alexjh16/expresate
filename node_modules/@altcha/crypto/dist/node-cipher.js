import { createCipheriv, createDecipheriv } from 'node:crypto';
import { pipeline } from 'node:stream/promises';
import aes from './aes.js';
import rsa from './rsa.js';
import { START_BYTES, AES_IV_LEN, AES_KEY_LEN, readHead } from './cipher.js';
import { compareByteArrays } from './helpers.js';
const ALG = 'aes-256-gcm';
const AUTH_TAG_LEN = 16;
export async function encryptStream(publicKeyRSA, input, output) {
    const iv = crypto.getRandomValues(new Uint8Array(AES_IV_LEN));
    const key = await aes.generateKey(AES_KEY_LEN);
    const keyBytes = await aes.exportKey(key);
    const encKey = await rsa.encrypt(publicKeyRSA, keyBytes);
    const cipher = createCipheriv(ALG, keyBytes, iv);
    output.write(new Uint8Array([
        ...START_BYTES,
        ...new Uint8Array([encKey.length]),
        ...new Uint8Array([iv.length]),
        ...encKey,
        ...iv,
    ]));
    return new Promise((resolve, reject) => {
        output.on('finish', resolve);
        cipher.on('data', (chunk) => {
            output.write(chunk);
        });
        input.on('end', () => {
            cipher.end();
            output.write(cipher.getAuthTag());
            output.end();
        });
        input.on('error', reject);
        input.on('data', (chunk) => {
            cipher.write(chunk);
        });
    });
}
export async function decryptStream(privateKeyRSA, input, output) {
    let decipher = null;
    return new Promise((resolve, reject) => {
        let buf = Buffer.from('');
        const write = (chunk) => {
            if (decipher) {
                if (chunk === null && buf.length) {
                    decipher.setAuthTag(buf.subarray(-1 * AUTH_TAG_LEN));
                    buf = buf.subarray(0, -1 * AUTH_TAG_LEN);
                }
                if (buf.length) {
                    decipher.write(buf);
                }
                if (chunk?.length) {
                    buf = chunk;
                }
                if (chunk === null) {
                    decipher.end();
                }
            }
        };
        output.on('finish', resolve);
        input.on('end', () => write(null));
        input.on('error', reject);
        input.on('data', (chunk) => {
            if (!decipher) {
                const { encKey, iv, startBytes, tail } = readHead(new Uint8Array(chunk.buffer.slice(chunk.byteOffset, chunk.byteOffset + chunk.byteLength)));
                if (!compareByteArrays(startBytes, START_BYTES)) {
                    return reject(new Error('Invalid data.'));
                }
                input.pause();
                rsa
                    .decrypt(privateKeyRSA, encKey)
                    .then((key) => {
                    decipher = createDecipheriv(ALG, key, iv);
                    pipeline(decipher, output);
                    write(Buffer.from(tail));
                    if (input.closed) {
                        write(null);
                    }
                    else {
                        input.resume();
                    }
                })
                    .catch(reject);
            }
            else {
                write(chunk);
            }
        });
    });
}
