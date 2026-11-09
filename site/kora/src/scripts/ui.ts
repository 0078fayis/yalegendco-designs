// Header behaviour, menu, bag drawer, page-transition wipe. Persisted elements survive view transitions,
// so these bindings are made once per full load and re-synced on every astro:page-load.
import { P, money } from '../data/products';

type Line = { id: string; size: string; qty: number };
const KEY = 'kora-bag';
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T | null;

// ---------- bag store ----------
const load = (): Line[] => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; } };
const save = (b: Line[]) => { try { localStorage.setItem(KEY, JSON.stringify(b)); } catch {} };
let bag = load();

function renderBag() {
  const items = $('bag-items'), aside = $('bag'), count = $('bag-count');
  if (!items || !aside) return;
  const n = bag.reduce((s, l) => s + l.qty, 0);
  if (count) count.textContent = String(n);
  $('bag-n')!.textContent = n ? `· ${n} item${n > 1 ? 's' : ''}` : '';
  aside.classList.toggle('empty', n === 0);
  items.innerHTML = bag.map((l, i) => {
    const p = P.find((x) => x.id === l.id)!;
    return `<div class="item" style="animation-delay:${i * 0.06}s">
      <img src="/models/look${p.look}.webp" alt="" width="72" height="96">
      <div><div class="nm">${p.name}</div><div class="mt">${p.cols[0][0]} · Size ${l.size}</div>
        <div><span class="q"><button type="button" data-d="-1" data-i="${i}" aria-label="Less">−</button><span>${l.qty}</span><button type="button" data-d="1" data-i="${i}" aria-label="More">+</button></span><button type="button" class="rm" data-rm="${i}">Remove</button></div></div>
      <div class="pr">${money(p.price * l.qty)}</div></div>`;
  }).join('');
  const sub = bag.reduce((s, l) => s + P.find((x) => x.id === l.id)!.price * l.qty, 0);
  $('bag-sub')!.textContent = money(sub);
  $('bag-gst')!.textContent = money(sub / 11);
}
export function addToBag(id: string, size: string, qty = 1) {
  const f = bag.find((l) => l.id === id && l.size === size);
  if (f) f.qty += qty; else bag.push({ id, size, qty });
  save(bag); renderBag(); openBag();
  const c = $('bag-count'); c?.parentElement?.classList.add('bump'); setTimeout(() => c?.parentElement?.classList.remove('bump'), 400);
}
function openBag() { $('bag')?.classList.add('open'); $('bag-veil')?.classList.add('on'); $('bag')?.setAttribute('aria-hidden', 'false'); $('bag-btn')?.setAttribute('aria-expanded', 'true'); }
function closeBag() { $('bag')?.classList.remove('open'); $('bag-veil')?.classList.remove('on'); $('bag')?.setAttribute('aria-hidden', 'true'); $('bag-btn')?.setAttribute('aria-expanded', 'false'); }

// ---------- menu ----------
function setMenu(open: boolean) {
  $('menu')?.classList.toggle('open', open); $('menu')?.setAttribute('aria-hidden', String(!open));
  $('top-bar')?.classList.toggle('menu-open', open); $('menu-btn')?.setAttribute('aria-expanded', String(open));
  document.documentElement.classList.toggle('lock', open);
  if (open) { const t = $('menu-time'); if (t) t.textContent = new Date().toLocaleTimeString('en-AU', { timeZone: 'Australia/Melbourne', hour: '2-digit', minute: '2-digit' }); }
}

// ---------- header hide / solid ----------
let lastY = 0;
function onScroll() {
  const y = scrollY, top = $('top-bar'); if (!top) return;
  top.classList.toggle('solid', y > innerHeight * 0.9);
  top.classList.toggle('hide', y > lastY && y > 120 && !top.classList.contains('menu-open'));
  lastY = y;
}

// ---------- page transition wipe ----------
function wipe(dir: 'in' | 'out') {
  let w = $('wipe');
  if (!w) { w = document.createElement('div'); w.id = 'wipe'; document.body.appendChild(w); }
  return new Promise<void>((res) => {
    w!.classList.remove('in', 'out'); void w!.offsetWidth; w!.classList.add(dir);
    setTimeout(res, dir === 'in' ? 620 : 700);
  });
}

let bound = false;
function bindOnce() {
  if (bound) return; bound = true;
  document.addEventListener('click', (e) => {
    const t = e.target as HTMLElement;
    if (t.closest('#bag-btn')) { e.preventDefault(); openBag(); }
    if (t.closest('#bag-x') || t.closest('#bag-veil')) closeBag();
    if (t.closest('#menu-btn')) setMenu(!$('menu')?.classList.contains('open'));
    if (t.closest('#menu a')) setMenu(false);
    const add = t.closest<HTMLElement>('[data-add]'); if (add) { e.preventDefault(); addToBag(add.dataset.add!, add.dataset.size || 'M'); }
    const q = t.closest<HTMLElement>('.item .q button'); if (q) { const i = +q.dataset.i!; bag[i].qty = Math.max(1, bag[i].qty + +q.dataset.d!); save(bag); renderBag(); }
    const rm = t.closest<HTMLElement>('[data-rm]'); if (rm) { bag.splice(+rm.dataset.rm!, 1); save(bag); renderBag(); }
    if (t.closest('#bag-checkout')) { const b = t.closest('#bag-checkout') as HTMLElement; b.textContent = 'Checkout opens at launch'; setTimeout(() => (b.innerHTML = 'Checkout <span>→</span>'), 1800); }
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { closeBag(); setMenu(false); } });
  addEventListener('scroll', onScroll, { passive: true });
  document.addEventListener('astro:before-preparation', (e: any) => { const orig = e.loader; e.loader = async () => { await wipe('in'); await orig(); }; });
  document.addEventListener('astro:after-swap', () => { scrollTo(0, 0); wipe('out'); setMenu(false); closeBag(); });
}

export function initUI() { bindOnce(); renderBag(); onScroll(); }
initUI();
document.addEventListener('astro:page-load', initUI);
