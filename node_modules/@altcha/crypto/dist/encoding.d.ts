declare const _default: {
    base64Decode: typeof base64Decode;
    base64Encode: typeof base64Encode;
};
export default _default;
export declare function base64Decode(b64: string, urlSafe?: boolean): Uint8Array;
export declare function base64Encode(ua: Uint8Array, urlSafe?: boolean): string;
export declare function arrayBufferToHex(ua: ArrayBuffer | Uint8Array): string;
