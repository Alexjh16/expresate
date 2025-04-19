"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.decrypt = exports.encrypt = exports.importKey = exports.exportKey = exports.generateKey = void 0;
exports.default = {
    generateKey,
    exportKey,
    importKey,
    decrypt,
    encrypt,
};
async function generateKey(length = 256) {
    return crypto.subtle.generateKey({
        name: 'AES-GCM',
        length,
    }, true, ['encrypt', 'decrypt']);
}
exports.generateKey = generateKey;
async function exportKey(key) {
    return new Uint8Array(await crypto.subtle.exportKey('raw', key));
}
exports.exportKey = exportKey;
async function importKey(key) {
    return crypto.subtle.importKey('raw', key, {
        name: 'AES-GCM',
    }, true, ['encrypt', 'decrypt']);
}
exports.importKey = importKey;
async function encrypt(key, data, ivLen = 16) {
    const iv = crypto.getRandomValues(new Uint8Array(ivLen));
    const encrypted = new Uint8Array(await crypto.subtle.encrypt({
        name: 'AES-GCM',
        iv,
    }, key, data));
    return {
        encrypted,
        iv,
    };
}
exports.encrypt = encrypt;
async function decrypt(key, data, iv) {
    return new Uint8Array(await crypto.subtle.decrypt({
        name: 'AES-GCM',
        iv,
    }, key, data));
}
exports.decrypt = decrypt;
