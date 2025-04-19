"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.decryptStream = exports.encryptStream = void 0;
const node_crypto_1 = require("node:crypto");
const promises_1 = require("node:stream/promises");
const aes_js_1 = __importDefault(require("./aes.js"));
const rsa_js_1 = __importDefault(require("./rsa.js"));
const cipher_js_1 = require("./cipher.js");
const helpers_js_1 = require("./helpers.js");
const ALG = 'aes-256-gcm';
const AUTH_TAG_LEN = 16;
async function encryptStream(publicKeyRSA, input, output) {
    const iv = crypto.getRandomValues(new Uint8Array(cipher_js_1.AES_IV_LEN));
    const key = await aes_js_1.default.generateKey(cipher_js_1.AES_KEY_LEN);
    const keyBytes = await aes_js_1.default.exportKey(key);
    const encKey = await rsa_js_1.default.encrypt(publicKeyRSA, keyBytes);
    const cipher = (0, node_crypto_1.createCipheriv)(ALG, keyBytes, iv);
    output.write(new Uint8Array([
        ...cipher_js_1.START_BYTES,
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
exports.encryptStream = encryptStream;
async function decryptStream(privateKeyRSA, input, output) {
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
                const { encKey, iv, startBytes, tail } = (0, cipher_js_1.readHead)(new Uint8Array(chunk.buffer.slice(chunk.byteOffset, chunk.byteOffset + chunk.byteLength)));
                if (!(0, helpers_js_1.compareByteArrays)(startBytes, cipher_js_1.START_BYTES)) {
                    return reject(new Error('Invalid data.'));
                }
                input.pause();
                rsa_js_1.default
                    .decrypt(privateKeyRSA, encKey)
                    .then((key) => {
                    decipher = (0, node_crypto_1.createDecipheriv)(ALG, key, iv);
                    (0, promises_1.pipeline)(decipher, output);
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
exports.decryptStream = decryptStream;
