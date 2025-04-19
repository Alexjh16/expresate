declare const _default: {
    generateKey: typeof generateKey;
    exportKey: typeof exportKey;
    importKey: typeof importKey;
    decrypt: typeof decrypt;
    encrypt: typeof encrypt;
};
export default _default;
export declare function generateKey(length?: number): Promise<CryptoKey>;
export declare function exportKey(key: CryptoKey): Promise<Uint8Array>;
export declare function importKey(key: Uint8Array): Promise<CryptoKey>;
export declare function encrypt(key: CryptoKey, data: Uint8Array, ivLen?: number): Promise<{
    encrypted: Uint8Array;
    iv: Uint8Array;
}>;
export declare function decrypt(key: CryptoKey, data: Uint8Array, iv: Uint8Array): Promise<Uint8Array>;
