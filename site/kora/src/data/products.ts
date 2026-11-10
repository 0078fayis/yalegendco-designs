export type Product = {
  id: string; name: string; type: 'top' | 'pant' | 'hoodie' | 'dress' | 'shirt' | 'shoe'; price: number;
  cols: [string, string][]; fab: string; desc: string; tag?: string; look: number;
  img?: string; // hanger or floor product photo (dresses, shirts, shoes)
  mate?: string; // explicit "complete the look" partner
};
export const SIZES = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL'];
export const SHOE_SIZES = ['36', '37', '38', '39', '40', '41', '42', '43', '44', '45'];
export const sizesFor = (p: Product) => (p.type === 'shoe' ? SHOE_SIZES : SIZES);
export const kind = (p: Product) => (p.type === 'dress' ? 'Dress' : p.type === 'shirt' ? 'Shirt' : p.type === 'shoe' ? 'Shoes' : p.type === 'pant' ? 'Bottom' : 'Top');
export const P: Product[] = [
  { id: 'coal-tee', name: 'Charcoal Boxy Tee', type: 'top', price: 69, cols: [['Charcoal', '#4a4844'], ['Bone', '#ece7dc'], ['Black', '#141414']], fab: '280 gsm combed cotton jersey', desc: 'Boxy, dropped shoulder, heavy ribbed neck. Garment-washed so the fit you buy is the fit you keep.', tag: 'Core', look: 1 },
  { id: 'light-denim', name: 'Light Wash Wide Denim', type: 'pant', price: 139, cols: [['Light wash', '#9fb3c4'], ['Grey wash', '#8a8a86']], fab: '12 oz rigid denim', desc: 'Straight wide leg, high rise, button fly. Rinsed once, no stretch, no distressing.', tag: 'Core', look: 1 },
  { id: 'bone-knit', name: 'Cream Boxy Knit', type: 'top', price: 119, cols: [['Cream', '#efe7d2'], ['Olive', '#7a7a55']], fab: 'Cotton and merino, 7 gauge', desc: 'Square body, wide neck, rolled edges. Warm without weight.', look: 2 },
  { id: 'sand-pant', name: 'Sand Wide Trouser', type: 'pant', price: 119, cols: [['Sand', '#c8b08a'], ['Brown', '#6b4f3a'], ['Navy', '#1f2436']], fab: 'Brushed cotton twill', desc: 'Single pleat, wide leg, cut to break once on the shoe.', look: 2 },
  { id: 'black-hoodie', name: 'Black Heavy Hoodie', type: 'hoodie', price: 129, cols: [['Black', '#141414'], ['Rust', '#b5552f']], fab: '400 gsm loopback fleece', desc: 'Double-layer hood, no drawcord, kangaroo pocket, heavy ribbed hem.', tag: 'New', look: 3 },
  { id: 'black-pant', name: 'Black Wide Pant', type: 'pant', price: 119, cols: [['Black', '#141414'], ['Navy', '#1f2436']], fab: 'Brushed cotton twill', desc: 'Elastic back waist, flat front, wide leg.', look: 3 },
  { id: 'olive-crew', name: 'Olive Crew', type: 'top', price: 109, cols: [['Olive', '#7a7a55'], ['Bone', '#ece7dc']], fab: '400 gsm loopback fleece', desc: 'Raglan crew, long cuffs, dropped hem.', look: 4 },
  { id: 'brown-pant', name: 'Brown Wide Trouser', type: 'pant', price: 119, cols: [['Brown', '#6b4f3a'], ['Sand', '#c8b08a']], fab: 'Brushed cotton twill', desc: 'Single pleat, wide leg, cut to break once on the shoe.', look: 4 },
  { id: 'white-tee', name: 'White Boxy Tee', type: 'top', price: 69, cols: [['White', '#f6f4ee'], ['Charcoal', '#4a4844']], fab: '280 gsm combed cotton jersey', desc: 'Same body as the charcoal, in optic white. Opaque at 280 gsm.', tag: 'Core', look: 5 },
  { id: 'grey-denim', name: 'Grey Wash Wide Denim', type: 'pant', price: 139, cols: [['Grey wash', '#8a8a86'], ['Light wash', '#9fb3c4']], fab: '12 oz rigid denim', desc: 'Straight wide leg, high rise, button fly.', look: 5 },
  { id: 'rust-hoodie', name: 'Rust Heavy Hoodie', type: 'hoodie', price: 129, cols: [['Rust', '#b5552f'], ['Black', '#141414']], fab: '400 gsm loopback fleece', desc: 'Double-layer hood, no drawcord, kangaroo pocket, heavy ribbed hem.', tag: 'New', look: 6 },
  { id: 'navy-pant', name: 'Navy Wide Pant', type: 'pant', price: 119, cols: [['Navy', '#1f2436'], ['Black', '#141414']], fab: 'Brushed cotton twill', desc: 'Elastic back waist, flat front, wide leg.', look: 6 },
  // Drop 01.5 · dresses
  { id: 'coal-tee-dress', name: 'Charcoal Tee Dress', type: 'dress', price: 109, cols: [['Charcoal', '#4a4844'], ['Bone', '#ece7dc']], fab: '280 gsm combed cotton jersey', desc: 'The boxy tee, cut to the shin. Dropped shoulder, side splits, heavy ribbed neck.', tag: 'New', look: 1, img: '/range/d1.webp', mate: 'bone-trainer' },
  { id: 'bone-shirt-dress', name: 'Bone Shirt Dress', type: 'dress', price: 149, cols: [['Bone', '#ece7dc'], ['Charcoal', '#4a4844']], fab: 'Heavy cotton poplin', desc: 'Long, straight and plain. Hidden placket, deep side pockets, cuffs that roll.', tag: 'New', look: 2, img: '/range/d2.webp', mate: 'sand-mule' },
  { id: 'olive-smock-dress', name: 'Olive Smock Dress', type: 'dress', price: 139, cols: [['Olive', '#7a7a55'], ['Navy', '#1f2436']], fab: 'Brushed cotton twill', desc: 'Gathered square neck, wide three-quarter sleeves, pockets you can lose a phone in.', tag: 'New', look: 4, img: '/range/d3.webp', mate: 'black-crepe-derby' },
  { id: 'rust-tank-dress', name: 'Rust Tank Dress', type: 'dress', price: 89, cols: [['Rust', '#b5552f'], ['Black', '#141414']], fab: '280 gsm combed cotton jersey', desc: 'A column of heavy jersey. Scoop neck, no seams at the side, falls to the ankle.', tag: 'New', look: 6, img: '/range/d4.webp', mate: 'bone-trainer' },
  { id: 'sand-pinafore', name: 'Sand Pinafore Dress', type: 'dress', price: 129, cols: [['Sand', '#c8b08a'], ['Charcoal', '#4a4844']], fab: 'Brushed cotton twill', desc: 'Wide straps, bib pocket, one hip pocket. Wear it over the tee or the knit.', tag: 'New', look: 2, img: '/range/d5.webp', mate: 'white-tee' },
  { id: 'navy-tiered-dress', name: 'Navy Tiered Dress', type: 'dress', price: 149, cols: [['Navy', '#1f2436'], ['Bone', '#ece7dc']], fab: 'Soft cotton voile, lined', desc: 'Two gentle tiers, long sleeves, ankle length. Loose everywhere, on purpose.', tag: 'New', look: 6, img: '/range/d6.webp', mate: 'black-crepe-derby' },
  // shirts
  { id: 'bone-overshirt', name: 'Bone Overshirt', type: 'shirt', price: 129, cols: [['Bone', '#ece7dc'], ['Olive', '#7a7a55']], fab: 'Heavy cotton poplin', desc: 'Two patch pockets, dropped shoulder, boxy body. A shirt that works as a jacket.', tag: 'New', look: 5, img: '/range/s1.webp', mate: 'grey-denim' },
  { id: 'coal-camp-shirt', name: 'Charcoal Camp Shirt', type: 'shirt', price: 119, cols: [['Charcoal', '#4a4844'], ['Bone', '#ece7dc']], fab: 'Brushed cotton twill', desc: 'Open camp collar, one pocket, long sleeves. Soft from the first wear.', tag: 'New', look: 3, img: '/range/s2.webp', mate: 'black-pant' },
  { id: 'olive-camp-shirt', name: 'Olive Camp Shirt', type: 'shirt', price: 99, cols: [['Olive', '#7a7a55'], ['Sand', '#c8b08a']], fab: 'Heavy cotton poplin', desc: 'Short sleeves, camp collar, straight hem. Cut wide so it hangs, not clings.', tag: 'New', look: 4, img: '/range/s3.webp', mate: 'brown-pant' },
  { id: 'navy-overshirt', name: 'Navy Overshirt', type: 'shirt', price: 139, cols: [['Navy', '#1f2436'], ['Charcoal', '#4a4844']], fab: 'Brushed cotton flannel', desc: 'Two flap pockets, heavy flannel, boxy. The winter layer in the palette.', tag: 'New', look: 1, img: '/range/s4.webp', mate: 'light-denim' },
  // shoes
  { id: 'bone-trainer', name: 'Bone Canvas Trainer', type: 'shoe', price: 159, cols: [['Bone', '#ece7dc'], ['Charcoal', '#4a4844']], fab: 'Cotton canvas, gum rubber sole', desc: 'A plain low-top on a natural gum sole. Cotton laces, leather heel tab, no logo.', tag: 'New', look: 5, img: '/range/f1.webp', mate: 'coal-tee-dress' },
  { id: 'black-crepe-derby', name: 'Black Crepe Derby', type: 'shoe', price: 219, cols: [['Black', '#141414'], ['Sand', '#c8b08a']], fab: 'Suede, natural crepe sole', desc: 'Moccasin-toe derby on a thick crepe sole. Soft from day one, resoleable.', tag: 'New', look: 3, img: '/range/f2.webp', mate: 'navy-tiered-dress' },
  { id: 'sand-mule', name: 'Sand Leather Mule', type: 'shoe', price: 169, cols: [['Sand', '#c8b08a'], ['Black', '#141414']], fab: 'Nubuck leather, rubber sole', desc: 'Closed-toe slip-on with a single seam. Step in, step out.', tag: 'New', look: 2, img: '/range/f3.webp', mate: 'bone-shirt-dress' },
  { id: 'coal-hightop', name: 'Charcoal High-Top', type: 'shoe', price: 149, cols: [['Charcoal', '#4a4844'], ['Bone', '#ece7dc']], fab: 'Cotton canvas, rubber sole', desc: 'High-top canvas with an off-white sole and laces. The only sneaker you need in winter.', tag: 'New', look: 1, img: '/range/f4.webp', mate: 'light-denim' },
];
export const RANGE = (t: Product['type']) => P.filter((p) => p.type === t);
export const money = (n: number) => 'A$' + n.toFixed(2);
