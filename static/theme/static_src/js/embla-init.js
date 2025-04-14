import EmblaCarousel from 'embla-carousel'

document.addEventListener('DOMContentLoaded', () => {
    const emblaNode = document.querySelector('.embla')
    if (emblaNode) {
        const embla = EmblaCarousel(emblaNode, { loop: true, speed: 5 })
    }
})

const emblaNode = document.querySelector('.embla')
const options = {
    loop: true,
    align: 'center',
    containScroll: 'trimSnaps',
    dragFree: true,
    skipSnaps: false,
    slidesToScroll: 1,
    startIndex: 1,
    // Esto hace que se vean los slides adyacentes
    slidesToShow: 1.5,
}

const autoplayOptions = {
    delay: 4000,
    rootNode: (emblaNode) => emblaNode.parentElement,
    stopOnInteraction: false,
    stopOnMouseEnter: true,
}

const embla = EmblaCarousel(emblaNode, options)
const autoplay = Autoplay(autoplayOptions)

embla.on('init', () => {
    // Activar autoplay
    embla.plugins().autoplay.play()
})

// Añadir el plugin de autoplay
embla.plugins().add(autoplay)