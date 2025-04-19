"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.readHead = exports.decrypt = exports.encrypt = exports.AES_IV_LEN = exports.AES_KEY_LEN = exports.START_BYTES = void 0;
const aes_js_1 = __importDefault(require("./aes.js"));
const rsa_js_1 = __importDefault(require("./rsa.js"));
const helpers_js_1 = require("./helpers.js");
exports.START_BYTES = new Uint8Array([1, 0, 1]);
exports.AES_KEY_LEN = 256;
exports.AES_IV_LEN = 16;
exports.default = {
    encrypt,
    decrypt,
    readHead,
};
async function encrypt(publicKeyRSA, data, options = {}) {
    const { aesIVLength = exports.AES_IV_LEN, aesKeyLength = exports.AES_KEY_LEN } = options;
    const key = await aes_js_1.default.generateKey(aesKeyLength);
    const { encrypted, iv } = await aes_js_1.default.encrypt(key, data, aesIVLength);
    const encKey = await rsa_js_1.default.encrypt(publicKeyRSA, await aes_js_1.default.exportKey(key));
    return new Uint8Array([
        ...exports.START_BYTES,
        ...new Uint8Array([encKey.length]),
        ...new Uint8Array([iv.length]),
        ...encKey,
        ...iv,
        ...encrypted,
    ]);
}
exports.encrypt = encrypt;
async function decrypt(privateKeyRSA, data) {
    const { encKey, iv, startBytes, tail } = readHead(data);
    if (!(0, helpers_js_1.compareByteArrays)(exports.START_BYTES, startBytes)) {
        throw new Error('Invalid data.');
    }
    const key = await rsa_js_1.default.decrypt(privateKeyRSA, encKey);
    return aes_js_1.default.decrypt(await aes_js_1.default.importKey(key), tail, iv);
}
exports.decrypt = decrypt;
function readHead(data) {
    const view = new DataView(data.buffer);
    const startBytes = data.subarray(0, exports.START_BYTES.length);
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
exports.readHead = readHead;
