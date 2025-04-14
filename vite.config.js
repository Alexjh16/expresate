import { defineConfig } from 'vite'

export default defineConfig({
    build: {
        outDir: 'static/js',  // Aquí generará los archivos compilados
        rollupOptions: {
            input: './static/theme/static_src/js/embla-init.js',  // Archivo de entrada
            output: {
                entryFileNames: 'embla.js'  // Nombre final del archivo
            }
        }
    }
})