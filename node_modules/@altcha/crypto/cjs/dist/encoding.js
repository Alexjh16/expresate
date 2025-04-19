"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.arrayBufferToHex = exports.base64Encode = exports.base64Decode = void 0;
exports.default = {
    base64Decode,
    base64Encode,
};
function base64Decode(b64, urlSafe = false) {
    if (urlSafe) {
        b64 =
            b64.replace(/_/g, '/').replace(/-/g, '+') +
                '='.repeat(3 - ((3 + b64.length) % 4));
    }
    return Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
}
exports.base64Decode = base64Decode;
function base64Encode(ua, urlSafe = false) {
    const b64 = btoa(String.fromCharCode(...ua));
    if (urlSafe) {
        return b64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    }
    return b64;
}
exports.base64Encode = base64Encode;
function arrayBufferToHex(ua) {
    if (ua instanceof ArrayBuffer) {
        ua = new Uint8Array(ua);
    }
    return Array.from(ua)
        .map((b) => b.toString(16).padStart(2, '0'))
        .join('');
}
exports.arrayBufferToHex = arrayBufferToHex;
