gsap.registerPlugin(ScrollTrigger);

// dodavanje random slike umesto miach
const images = [
    "img1.jfif",
    "img2.jpg",
    "img3.jfif",
    "img4.jfif",
    "img5.jfif",
    "img6.jfif",
    "img7.jfif",
    "miach.jpg",
    "song3.jpg"
];

const i = Math.floor(Math.random() * images.length);
const elem = document.getElementById("random-image");
elem.src = `../static/images/${images[i]}`;

// pravljenje timelinea za kretanje ploce i dohvatanje prvih vrednosti
const getResponsiveValues = () => {
    const isMobile = window.innerWidth <= 768;
    const isSmallMobile = window.innerWidth <= 480;
    
    return {
        xOffset: isMobile ? -window.innerWidth * 0.3 : -window.innerWidth * 0.4,
        yOffset: isMobile ? window.innerHeight * 0.4 : window.innerHeight * 0.4,
        scale: isSmallMobile ? 1.5 : isMobile ? 1.8 : 2
    };
};

const updateAnimations = () => {
    // dohvati nove vrednosti za p
    const responsive = getResponsiveValues();
    ScrollTrigger.getAll().forEach(trigger => trigger.kill());
    
    // pakao za da se ploca pomera :(
    gsap.timeline({
        scrollTrigger: {
            trigger: ".scroll-container",
            start: "top top",
            end: "bottom bottom",
            scrub: 1,
        }
    })
    .to(".record-container", {
        x: responsive.xOffset,
        y: responsive.yOffset,
        scale: responsive.scale,
        duration: 1,
        ease: "power2.inOut"
    });

    // fade out za Vibe i Check
    gsap.timeline({
        scrollTrigger: {
            trigger: ".scroll-container",
            start: "top top",
            end: "50% top",
            scrub: 1,
        }
    })
    .to(".vibe-left", {
        opacity: 0,
        duration: 1,
        ease: "power2.out"
    })
    .to(".vibe-right", {
        opacity: 0,
        duration: 1,
        ease: "power2.out"
    }, "<");

    // fade out za trending i login dugmad
    gsap.timeline({
        scrollTrigger: {
            trigger: ".scroll-container",
            start: "top top",
            end: "50% top",
            scrub: true,
        }
    })
    .to(".trending-btn", { opacity: 0, pointerEvents: "none", ease: "power1.out" })
    .to(".login-btn", { opacity: 0, pointerEvents: "none", ease: "power1.out" }, "<");
    
    // top left deo sa logom
    gsap.timeline({
        scrollTrigger: {
            trigger: ".scroll-container",
            start: "40% top",
            end: "70% top",
            scrub: true,
        }
    }).to(".top-left", {
        opacity: 1,
        pointerEvents: "auto",
        ease: "power2.inOut"
    });


    // saktij scroll indicator
    gsap.to(".scroll-indicator", {
        opacity: 0,
        scrollTrigger: {
            trigger: ".scroll-container",
            start: "5% top",
            end: "10% top",
            scrub: true,
        }
    });

    // Unleash the beat!
    ScrollTrigger.create({
        trigger: ".scroll-container",
        start: "70% bottom",
        end: "95% bottom",
        scrub: true,
        onUpdate: self => {
            const opacity = self.progress;
            const button = document.querySelector(".get-started-btn");
            const recordLink = document.querySelector(".record-link");

            if (opacity > 0.05) {
                button.disabled = false;
                button.style.cursor = "pointer";
                recordLink.style.pointerEvents = "auto";
                recordLink.style.cursor = "pointer";
            } else {
                button.disabled = true;
                button.style.cursor = "default";
                recordLink.style.pointerEvents = "none";
                recordLink.style.cursor = "default";
            }
            gsap.set(".unleash-the-beat-section", { opacity: opacity });
        }
    });
    
    // fade in and out za promenu slike na ploci
    gsap.timeline({
        scrollTrigger: {
            trigger: ".scroll-container",
            start: "70% bottom",
            end: "90% bottom",
            scrub: true,
        }
    })
    .to(".record-caption", {
        opacity: 1,
        ease: "power1.out"
    })
    .to(".record-label", {
        opacity: 0,
        ease: "power1.in"
    }, "<0.5");
};

// odradi sve inicijalno
updateAnimations();

// lupi update na svaki resize zbog pozicije ploce
window.addEventListener('resize', () => {
    updateAnimations();
});