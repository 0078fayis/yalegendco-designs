import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const loader = document.getElementById('loader');
const frame = document.getElementById('frame');
const heroH = document.getElementById('hero-h');

if (loader && frame && heroH && !reduce) {
  // Keep the page still while the opening plays
  document.documentElement.style.overflow = 'hidden';
  const n = { v: 0 };
  const nEl = document.getElementById('loader-n')!;
  const lines = heroH.querySelectorAll('.r-line > span');
  const rest = document.querySelectorAll('.r-hero');

  const tl = gsap.timeline({
    defaults: { ease: 'power3.out' },
    onComplete() { document.documentElement.style.overflow = ''; loader.remove(); },
  });
  tl.to(n, { v: 100, duration: 1.4, ease: 'power2.inOut', onUpdate: () => { nEl.textContent = String(Math.round(n.v)).padStart(2, '0'); } })
    .to('#loader-n span', { yPercent: -110, duration: 0.7, ease: 'power3.in' }, '+=0.1')
    .to('.loader-mark', { yPercent: -110, duration: 0.5, ease: 'power3.in' }, '<')
    .to(loader, { yPercent: -100, duration: 1.1, ease: 'power4.inOut' }, '-=0.2')
    .fromTo(frame, { scale: 1.06, filter: 'brightness(1.08)' }, { scale: 1, filter: 'brightness(1)', duration: 2, ease: 'power3.out' }, '-=0.8')
    .to(lines, { y: 0, duration: 1.5, ease: 'power4.out', stagger: 0.14 }, '-=1.6')
    .to(rest, { opacity: 1, y: 0, duration: 1.1, stagger: 0.1 }, '-=1.0');

  // Second campaign shot crossfades in after the opening, then alternates
  const shots = frame.querySelectorAll('.shot');
  let i = 0;
  setInterval(() => { i = (i + 1) % shots.length; shots.forEach((s, k) => s.classList.toggle('on', k === i)); }, 7000);

  // Scroll: the frame shrinks into an inset with the bone page around it; copy parts and fades
  const mq = matchMedia('(max-width: 760px)').matches;
  gsap.timeline({
    scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom bottom', scrub: 0.6,
      onUpdate(self) { frame.classList.toggle('inset', self.progress > 0.35); } },
  })
    .to(frame, { clipPath: mq ? 'inset(10vh 16px 14vh 16px)' : 'inset(8vh 8vw 10vh 8vw)', ease: 'none' }, 0)
    .fromTo(frame, { clipPath: 'inset(0px 0px 0px 0px)' }, { clipPath: mq ? 'inset(10vh 16px 14vh 16px)' : 'inset(8vh 8vw 10vh 8vw)', ease: 'none' }, 0)
    .to(frame.querySelectorAll('.shot img'), { scale: 1.0, ease: 'none' }, 0)
    .to('.hero-copy', { yPercent: 30, opacity: 0, ease: 'none' }, 0)
    .to('.scroll-hint', { opacity: 0, ease: 'none' }, 0);
} else if (loader) {
  loader.remove();
}
