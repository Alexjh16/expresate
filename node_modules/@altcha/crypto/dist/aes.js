export default {
    generateKey,
    exportKey,
    importKey,
    decrypt,
    encrypt,
};
export async function generateKey(length = 256) {
    return crypto.subtle.generateKey({
        name: 'AES-GCM',
        length,
    }, true, ['encrypt', 'decrypt']);
}
export async function exportKey(key) {
    return new Uint8Array(await crypto.subtle.exportKey('raw', key));
}
export async function importKey(key) {
    return crypto.subtle.importKey('raw', key, {
        name: 'AES-GCM',
    }, true, ['encrypt', 'decrypt']);
}
export async function encrypt(key, data, ivLen = 16) {
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
export async function decrypt(key, data, iv) {
    return new Uint8Array(await crypto.subtle.decrypt({
        name: 'AES-GCM',
        iv,
    }, key, data));
}
