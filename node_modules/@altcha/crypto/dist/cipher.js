import aes from './aes.js';
import rsa from './rsa.js';
import { compareByteArrays } from './helpers.js';
export const START_BYTES = new Uint8Array([1, 0, 1]);
export const AES_KEY_LEN = 256;
export const AES_IV_LEN = 16;
export default {
    encrypt,
    decrypt,
    readHead,
};
export async function encrypt(publicKeyRSA, data, options = {}) {
    const { aesIVLength = AES_IV_LEN, aesKeyLength = AES_KEY_LEN } = options;
    const key = await aes.generateKey(aesKeyLength);
    const { encrypted, iv } = await aes.encrypt(key, data, aesIVLength);
    const encKey = await rsa.encrypt(publicKeyRSA, await aes.exportKey(key));
    return new Uint8Array([
        ...START_BYTES,
        ...new Uint8Array([encKey.length]),
        ...new Uint8Array([iv.length]),
        ...encKey,
        ...iv,
        ...encrypted,
    ]);
}
export async function decrypt(privateKeyRSA, data) {
    const { encKey, iv, startBytes, tail } = readHead(data);
    if (!compareByteArrays(START_BYTES, startBytes)) {
        throw new Error('Invalid data.');
    }
    const key = await rsa.decrypt(privateKeyRSA, encKey);
    return aes.decrypt(await aes.importKey(key), tail, iv);
}
export function readHead(data) {
    const view = new DataView(data.buffer);
    const startBytes = data.subarray(0, START_BYTES.length);
    const offset = startBytes.length + 2;
    const encKeyLen = view.getUint8(startBytes.length) || 256;
    const ivLen = view.getUint8(startBytes.length + 1);
    const encKey = data.subarray(offset, offset + encKeyLen);
    const iv = data.subarray(offset + encKeyLen, offset + encKeyLen + ivLen);
    const tail = data.subarray(offset + encKeyLen + ivLen);
    return {
        encKey,
        iv,
        startBytes,
        tail,
    };
}
