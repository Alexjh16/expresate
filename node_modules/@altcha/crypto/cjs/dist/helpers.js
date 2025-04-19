"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.compareByteArrays = exports.convertPemToUint8Array = exports.wrapLines = void 0;
const encoding_js_1 = require("./encoding.js");
exports.default = {
    wrapLines,
    compareByteArrays,
    convertPemToUint8Array,
};
function wrapLines(str, lineWidth = 80) {
    let result = '';
    while (str.length > 0) {
        result += str.slice(0, lineWidth) + '\n';
        str = str.slice(lineWidth);
    }
    return result;
}
exports.wrapLines = wrapLines;
function convertPemToUint8Array(pem) {
    return (0, encoding_js_1.base64Decode)(pem
        .split(/\r?\n/)
        .filter((line) => !line.startsWith('-----'))
        .join(''));
}
exports.convertPemToUint8Array = convertPemToUint8Array;
function compareByteArrays(a, b) {
    return a.length === b.length && Array.from(a).every((v, i) => v === b[i]);
}
exports.compareByteArrays = compareByteArrays;
