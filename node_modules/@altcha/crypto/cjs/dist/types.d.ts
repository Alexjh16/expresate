export type TCurveName = 'P-256' | 'P-384' | 'P-521';
export type THashName = 'SHA-256' | 'SHA-384' | 'SHA-521';
export interface ICipherEncryptOptions {
    aesKeyLength?: number;
    aesIVLength?: number;
}
