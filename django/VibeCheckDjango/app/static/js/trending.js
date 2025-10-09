
// animcije za fade out
gsap.registerPlugin(ScrollTrigger);

gsap.timeline({
    scrollTrigger: {
        start: "top top",
        end: "35% top",
        scrub: true,
    }
})
.to(".vibe-text", {
    opacity: 0,
    duration: 1,
    ease: "power2.out"
});

gsap.to(".scroll-indicator", {
    opacity: 0,
    scrollTrigger: {
        start: "top top",
        end: "10% top",
        scrub: true,
    }
});



