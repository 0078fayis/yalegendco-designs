// Liquid ripple between the opening photos. A tiny WebGL quad blends the outgoing and incoming shot with a
// circular wave and radial displacement; the CSS crossfade still runs underneath, so if WebGL is missing or
// a texture is not ready, the hero simply fades as before. Textures are made from the <img> already on the page.
const VS = 'attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;v.y=1.-v.y;gl_Position=vec4(p,0,1);}';
const FS = `precision mediump float;varying vec2 v;uniform sampler2D a,b;uniform vec2 sa,sb,fa,fb;uniform float t,asp;
vec2 fit(vec2 uv,vec2 s,vec2 f){return f+(uv-f)*s;}
void main(){
  vec2 c=v-vec2(.5,.42);c.x*=asp;float d=length(c);
  float e=smoothstep(0.,1.,t);
  float wave=sin(d*22.-t*14.)*(1.-e)*e*4.*0.028;              // ring that travels outwards and dies away
  float mask=smoothstep(e*1.5-.35,e*1.5+.05,d);                // 0 inside the wavefront (new image), 1 outside
  vec2 dir=d>0.001?normalize(c)/vec2(asp,1.):vec2(0.);
  vec2 ua=fit(v+dir*wave*mask,sa,fa);
  vec2 ub=fit(v-dir*wave*(1.-mask)*1.5,sb,fb);
  vec4 ca=texture2D(a,ua),cb=texture2D(b,ub);
  gl_FragColor=mix(cb,ca,mask);
}`;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

export function makeRipple(frame: HTMLElement) {
  if (reduce) return null;
  const cv = document.createElement('canvas'); cv.className = 'ripple'; frame.appendChild(cv);
  const gl = cv.getContext('webgl', { alpha: false, antialias: false, premultipliedAlpha: false }); if (!gl) { cv.remove(); return null; }
  const sh = (t: number, src: string) => { const s = gl.createShader(t)!; gl.shaderSource(s, src); gl.compileShader(s); return s; };
  const pr = gl.createProgram()!; gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr); gl.useProgram(pr);
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const U = (n: string) => gl.getUniformLocation(pr, n);
  gl.uniform1i(U('a'), 0); gl.uniform1i(U('b'), 1);
  const texes = new Map<HTMLImageElement, WebGLTexture>();
  const tex = (img: HTMLImageElement) => {
    let t = texes.get(img); if (t) return t;
    if (!img.complete || !img.naturalWidth) return null;
    t = gl.createTexture()!; gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    try { gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img); } catch { return null; }
    texes.set(img, t); return t;
  };
  // cover-fit like object-fit:cover with the image's object-position, plus the 1.08 zoom the CSS applies
  const fitOf = (img: HTMLImageElement) => {
    const ia = img.naturalWidth / img.naturalHeight, ca = cv.width / cv.height;
    const s = ia > ca ? [ca / ia, 1] : [1, ia / ca];
    const pos = getComputedStyle(img).objectPosition.split(' ').map((x) => parseFloat(x) / 100);
    return { s: [s[0] / 1.08, s[1] / 1.08], f: [isNaN(pos[0]) ? 0.5 : pos[0], isNaN(pos[1]) ? 0.5 : pos[1]] };
  };
  let raf = 0;
  return (from: HTMLImageElement, to: HTMLImageElement, ms = 1500) => {
    const dpr = Math.min(devicePixelRatio || 1, 1.5), w = Math.round(frame.clientWidth * dpr), h = Math.round(frame.clientHeight * dpr);
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; gl.viewport(0, 0, w, h); }
    const ta = tex(from), tb = tex(to); if (!ta || !tb) return false;
    const A = fitOf(from), B = fitOf(to);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, ta); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, tb);
    gl.uniform2fv(U('sa'), A.s); gl.uniform2fv(U('fa'), A.f); gl.uniform2fv(U('sb'), B.s); gl.uniform2fv(U('fb'), B.f); gl.uniform1f(U('asp'), w / h);
    cancelAnimationFrame(raf); const t0 = performance.now(); cv.classList.add('on');
    const step = (now: number) => {
      const k = Math.min(1, (now - t0) / ms);
      gl.uniform1f(U('t'), k); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      cv.style.opacity = String(k < 0.1 ? k / 0.1 : k > 0.8 ? (1 - k) / 0.2 : 1);
      if (k < 1) raf = requestAnimationFrame(step); else cv.classList.remove('on');
    };
    raf = requestAnimationFrame(step);
    return true;
  };
}
