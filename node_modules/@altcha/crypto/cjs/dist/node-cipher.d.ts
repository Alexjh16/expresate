/// <reference types="node" />
import { Readable, Writable } from 'node:stream';
export declare function encryptStream(publicKeyRSA: CryptoKey, input: Readable, output: Writable): Promise<unknown>;
export declare function decryptStream(privateKeyRSA: CryptoKey, input: Readable, output: Writable): Promise<unknown>;
