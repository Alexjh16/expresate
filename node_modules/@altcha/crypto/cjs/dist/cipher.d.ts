import type { ICipherEncryptOptions } from './types.js';
export declare const START_BYTES: Uint8Array;
export declare const AES_KEY_LEN = 256;
export declare const AES_IV_LEN = 16;
declare const _default: {
    encrypt: typeof encrypt;
    decrypt: typeof decrypt;
    readHead: typeof readHead;
};
export default _default;
export declare function encrypt(publicKeyRSA: CryptoKey, data: Uint8Array, options?: ICipherEncryptOptions): Promise<Uint8Array>;
export declare function decrypt(privateKeyRSA: CryptoKey, data: Uint8Array): Promise<Uint8Array>;
export declare function readHead(data: Uint8Array): {
    encKey: Uint8Array;
    iv: Uint8Array;
    startBytes: Uint8Array;
    tail: Uint8Array;
};
