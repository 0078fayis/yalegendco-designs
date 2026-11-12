// "Take it off the rail": tapping a hanger or a floating shoe opens the piece in place, with sizes and
// Add to bag, instead of leaving the page. The rail steps back; the piece flies to its card (FLIP).
import { money } from '../data/products';
type Card = { id: string; name: string; price: number; fab: string; desc: string; cols: [string, string][]; sizes: string[]; img: string };
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const ease = 'cubic-bezier(.2,.65,.2,1)';

function cardHTML(c: Card, kind: string) {
  const def = c.sizes.includes('M') ? 'M' : c.sizes[Math.floor(c.sizes.length / 2)];
  return `<button class="fb-close" type="button">Close <span>×</span></button>
  <div class="fb-pic"><img src="${c.img}" alt="${c.name}" width="900" height="1200"></div>
  <div class="fb-info">
    <span class="label">KORA · ${kind} · ${c.fab}</span>
    <h3>${c.name}</h3><span class="pr">${money(c.price)}</span>
    <p>${c.desc}</p>
    <div class="fb-k sw" aria-label="Colour">${c.cols.map(([n, h], i) => `<button type="button" class="${i ? '' : 'on'}" aria-label="${n}" title="${n}"><i style="background:${h}"></i></button>`).join('')}</div>
    <div class="fb-k sz" aria-label="Size">${c.sizes.map((s) => `<button type="button" class="${s === def ? 'on' : ''}" data-s="${s}">${s}</button>`).join('')}</div>
    <div class="fb-row"><button class="btn solid" type="button" data-add="${c.id}" data-size="${def}">Add to bag</button><a class="lnk" href="/p/${c.id}/">View details</a></div>
  </div>`;
}

function fly(from: DOMRect, to: HTMLElement, src: string) {
  if (still) return Promise.resolve();
  const r = to.getBoundingClientRect(); if (!r.width) return Promise.resolve();
  const g = document.createElement('img'); g.src = src; g.className = 'fly'; g.style.cssText = `left:${from.left}px;top:${from.top}px;width:${from.width}px;height:${from.height}px;object-fit:contain;box-shadow:none;background:none`;
  document.body.appendChild(g);
  const a = g.animate([{ transform: 'none' }, { transform: `translate(${r.left - from.left + (r.width - from.width) / 2}px,${r.top - from.top + (r.height - from.height) / 2}px) scale(${r.width / from.width},${r.height / from.height})` }], { duration: 750, easing: ease, fill: 'forwards' });
  return a.finished.then(() => g.remove());
}

function openRow(row: HTMLElement, src: HTMLElement, kind: string) {
  const c = JSON.parse(src.dataset.open!) as Card;
  const fb = row.querySelector<HTMLElement>('.fb')!; fb.innerHTML = cardHTML(c, kind); fb.classList.remove('in');
  const img = src.querySelector('img')!, from = img.getBoundingClientRect();
  row.classList.add('open'); src.classList.add('on');
  const pic = fb.querySelector<HTMLElement>('.fb-pic')!; pic.style.opacity = '0';
  fly(from, pic, c.img).then(() => { pic.style.opacity = ''; fb.classList.add('in'); });
  fb.querySelector('.fb-close')!.addEventListener('click', () => closeRow(row));
  fb.addEventListener('click', (e) => {
    const b = (e.target as HTMLElement).closest<HTMLElement>('.fb-k button'); if (!b) return;
    b.parentElement!.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
    if (b.dataset.s) fb.querySelector<HTMLElement>('[data-add]')!.dataset.size = b.dataset.s;
  });
}
function closeRow(row: HTMLElement) { row.classList.remove('open'); row.querySelectorAll('.on').forEach((x) => x.classList.remove('on')); }

// ---------- shoe wall layout: a loose grid with a little scatter, bigger pairs nearer the front ----------
function placeShoes(sky: HTMLElement) {
  const shoes = Array.from(sky.querySelectorAll<HTMLElement>('.sh')), narrow = sky.clientWidth < 640;
  const cols = narrow ? 3 : 4, rows = Math.ceil(shoes.length / cols);
  shoes.forEach((el, i) => {
    const c = i % cols, r = Math.floor(i / cols), j = Math.sin(i * 12.9898) * 43758.5453, jx = (j - Math.floor(j)) - 0.5, jy = (Math.sin(j) + 1) / 2 - 0.5;
    const w = (narrow ? 27 : 18) * (0.9 + 0.2 * ((i * 7) % 3) / 2);
    const x = ((c + 0.5) / cols) * 100 + jx * 9 - w / 2, y = ((r + 0.5) / rows) * 100 + jy * 10 - (w * 0.75) / 2 * (sky.clientWidth / sky.clientHeight);
    el.style.width = w + '%'; el.style.left = Math.max(1, Math.min(99 - w, x)) + '%'; el.style.top = Math.max(2, Math.min(78, y)) + '%';
    el.style.setProperty('--bobt', (6 + ((i * 5) % 4)) + 's'); el.style.setProperty('--bobd', -((i * 1.7) % 6) + 's'); el.style.zIndex = String(1 + ((i * 7) % 3));
  });
}

function init() {
  const sec = document.getElementById('range'); if (!sec || sec.dataset.ready) return; sec.dataset.ready = '1';
  // rails
  sec.addEventListener('click', (e) => {
    const t = e.target as HTMLElement;
    const hang = t.closest<HTMLElement>('.hang[data-open]');
    if (hang) { e.preventDefault(); e.stopPropagation(); const row = hang.closest<HTMLElement>('.rng-row')!; if (row.classList.contains('open')) return; openRow(row, hang, row.dataset.row === 'dress' ? 'Dress' : 'Shirt'); return; }
    const sh = t.closest<HTMLElement>('.sh[data-open]');
    if (sh) { const sky = document.getElementById('sky')!; if (sky.classList.contains('focus')) return; openShoe(sky, sh); }
  }, true);
  addEventListener('keydown', (e) => { if (e.key === 'Escape') sec.querySelectorAll<HTMLElement>('.rng-row.open').forEach(closeRow), closeShoe(); });

  // shoe wall
  const sky = document.getElementById('sky'); if (!sky) return;
  placeShoes(sky); addEventListener('resize', () => placeShoes(sky));
  const title = sec.querySelector<HTMLElement>('.sh-title')!, shoes = Array.from(sky.querySelectorAll<HTMLElement>('.sh'));
  const show = (el: HTMLElement) => {
    const c = JSON.parse(el.dataset.open!) as Card, i = +el.dataset.i!;
    (document.getElementById('sh-no')!).textContent = `${String(i + 1).padStart(2, '0')} / ${String(shoes.length).padStart(2, '0')}`;
    (document.getElementById('sh-name')!).textContent = c.name; (document.getElementById('sh-price')!).textContent = money(c.price);
    (document.getElementById('sh-link') as HTMLAnchorElement).href = `/p/${c.id}/`;
    if (!still) { title.classList.remove('swap'); void title.offsetWidth; title.classList.add('swap'); }
  };
  shoes.forEach((el) => el.addEventListener('pointerenter', () => { if (!sky.classList.contains('focus')) show(el); }));
  // light parallax: the wall shifts a touch with the pointer (or the phone's tilt via --px/--py set by hero.ts when present)
  sky.addEventListener('pointermove', (e) => {
    if (sky.classList.contains('focus') || still) return; const r = sky.getBoundingClientRect(), mx = (e.clientX - r.left) / r.width - 0.5, my = (e.clientY - r.top) / r.height - 0.5;
    shoes.forEach((el) => { const z = +el.style.zIndex || 1; el.style.translate = `${(-mx * 14 * z).toFixed(1)}px ${(-my * 10 * z).toFixed(1)}px`; });
  });
  sky.addEventListener('pointerleave', () => shoes.forEach((el) => (el.style.translate = '')));

  function openShoe(sky: HTMLElement, el: HTMLElement) {
    const c = JSON.parse(el.dataset.open!) as Card; show(el);
    const fb = sky.querySelector<HTMLElement>('.fb')!; fb.innerHTML = cardHTML(c, 'Shoes'); fb.classList.remove('in');
    sky.classList.add('focus'); el.classList.add('on'); sky.parentElement!.classList.add('open');
    // move the chosen pair to the picture slot of the card (or the middle on a phone)
    const pic = fb.querySelector<HTMLElement>('.fb-pic')!, r0 = el.getBoundingClientRect(), s = sky.getBoundingClientRect();
    const pr = pic.offsetParent ? pic.getBoundingClientRect() : { left: s.left + s.width * 0.1, top: s.top + s.height * 0.03, width: s.width * 0.8, height: s.height * 0.32 };
    const k = Math.min(pr.width / r0.width, (pr.height / r0.height)) * 0.92;
    const dx = pr.left + pr.width / 2 - (r0.left + r0.width / 2), dy = pr.top + pr.height / 2 - (r0.top + r0.height / 2);
    el.style.transition = still ? 'none' : `transform .85s ${ease}`; el.style.zIndex = '9'; el.style.translate = ''; el.style.transform = `translate(${dx}px,${dy}px) scale(${k})`;
    setTimeout(() => fb.classList.add('in'), still ? 0 : 300);
    fb.querySelector('.fb-close')!.addEventListener('click', closeShoe);
    fb.addEventListener('click', (e) => {
      const b = (e.target as HTMLElement).closest<HTMLElement>('.fb-k button'); if (!b) return;
      b.parentElement!.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
      if (b.dataset.s) fb.querySelector<HTMLElement>('[data-add]')!.dataset.size = b.dataset.s;
    });
  }
  function closeShoe() {
    if (!sky!.classList.contains('focus')) return; sky!.classList.remove('focus'); sky!.parentElement!.classList.remove('open');
    const on = sky!.querySelector<HTMLElement>('.sh.on'); if (on) { on.classList.remove('on'); on.style.transform = ''; setTimeout(() => { on.style.transition = ''; on.style.zIndex = String(1 + ((+on.dataset.i! * 7) % 3)); }, 900); }
  }
}
init();
document.addEventListener('astro:page-load', init);
