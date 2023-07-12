gsap.registerPlugin(ScrollTrigger);

gsap.set(".footer-item",{autoAlpha:0,y:5})
gsap.set("#footer-border-top-1",{scale:0})
gsap.set("#footer-border-top-2",{scale:0})

const borderanim1 = gsap.to("#footer-border-top-1", {
    scale:1,
    duration:1,
    paused:true,
});

const borderanim2 = gsap.to("#footer-border-top-2", {
    scale:1,
    delay:.25,
    duration:.75,
    paused:true,
    ease:"power1.easeIn"
});

const itemanim = gsap.to(".footer-item", {
    delay: 1,
    duration: .5,
    autoAlpha: 1,
    y:0,
    ease: "power3.out",
    stagger: {
        amount: 1.5
    },
    paused:true,
});

const itemanim2 = gsap.to(".footer-text-gradient-slide",{
    delay: 2,
    duration: .75,
    backgroundPositionX: "-200%",
    ease: "power0.inOut",
    stagger: {
        amount: 1.5
    },
    paused:true,
    onComplete() {
        $(".footer-text-gradient-slide").css({transition:"background-position-x 350ms ease-in-out"})
    }
})

ScrollTrigger.create({
    trigger:"footer",
    start:"top bottom",
    onEnter: () => {
        borderanim1.play()
        borderanim2.play()
        itemanim.play()
        itemanim2.play()
    }
})

ScrollTrigger.create({
    trigger:"footer",
    start:"top-=10px bottom",
    onLeaveBack: () => {
        borderanim1.pause(0)
        borderanim2.pause(-.25)
        itemanim.pause(-1)
        itemanim2.pause(-2)
        $(".footer-text-gradient-slide").css({transition:"none"})
    }
})