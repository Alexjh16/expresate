import { base64Decode } from './encoding.js';
export default {
    wrapLines,
    compareByteArrays,
    convertPemToUint8Array,
};
export function wrapLines(str, lineWidth = 80) {
    let result = '';
    while (str.length > 0) {
        result += str.slice(0, lineWidth) + '\n';
        str = str.slice(lineWidth);
    }
    return result;
}
export function convertPemToUint8Array(pem) {
    return base64Decode(pem
        .split(/\r?\n/)
        .filter((line) => !line.startsWith('-----'))
        .join(''));
}
export function compareByteArrays(a, b) {
    return a.length === b.length && Array.from(a).every((v, i) => v === b[i]);
}
