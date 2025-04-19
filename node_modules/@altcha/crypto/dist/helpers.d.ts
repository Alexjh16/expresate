declare const _default: {
    wrapLines: typeof wrapLines;
    compareByteArrays: typeof compareByteArrays;
    convertPemToUint8Array: typeof convertPemToUint8Array;
};
export default _default;
export declare function wrapLines(str: string, lineWidth?: number): string;
export declare function convertPemToUint8Array(pem: string): Uint8Array;
export declare function compareByteArrays(a: Uint8Array, b: Uint8Array): boolean;
