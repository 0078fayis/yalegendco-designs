import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);
document.documentElement.classList.remove('no-js');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// One Lenis for the life of the tab (it survives view transitions)
let lenis: Lenis | null = null;
if (!reduce) {
  lenis = new Lenis({ duration: 1.25, easing: (t) => 1 - Math.pow(1 - t, 3), smoothWheel: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis!.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
}

function init() {
  // Kill triggers from the previous page (hero.ts makes its own and also re-inits on page-load)
  ScrollTrigger.getAll().forEach((t) => t.kill());
  lenis?.scrollTo(0, { immediate: true });

  document.querySelectorAll<HTMLAnchorElement>('a[href^="#"]').forEach((a) =>
    a.addEventListener('click', (e) => {
      const el = document.querySelector(a.getAttribute('href')!);
      if (el && lenis) { e.preventDefault(); lenis.scrollTo(el as HTMLElement, { offset: -20 }); }
    })
  );

  document.querySelectorAll<HTMLElement>('[data-split]:not([data-done])').forEach((el) => {
    el.dataset.done = '1';
    const parts = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = parts.map((p) => `<span class="r-line"><span>${p.trim()}</span></span>`).join('');
  });
  if (reduce) return;

  document.querySelectorAll<HTMLElement>('[data-split]').forEach((el) => {
    gsap.to(el.querySelectorAll('.r-line > span'), { y: 0, duration: 1.4, ease: 'power4.out', stagger: 0.12,
      scrollTrigger: { trigger: el, start: 'top 85%', once: true } });
  });
  document.querySelectorAll<HTMLElement>('.r-fade').forEach((el) => {
    gsap.to(el, { opacity: 1, y: 0, duration: 1.2, ease: 'power3.out', delay: Number(el.dataset.delay) || 0,
      scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
  });
  document.querySelectorAll<HTMLElement>('.r-img').forEach((box) => {
    const img = box.querySelector('img'); if (!img) return;
    gsap.to(img, { scale: 1, duration: 1.6, ease: 'power3.out', scrollTrigger: { trigger: box, start: 'top 90%', once: true } });
    const depth = Number(box.dataset.depth || 0.08);
    gsap.fromTo(img, { yPercent: -depth * 100 }, { yPercent: depth * 100, ease: 'none',
      scrollTrigger: { trigger: box, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  document.dispatchEvent(new CustomEvent('kora:motion-ready'));
}

init();
document.addEventListener('astro:page-load', init);
