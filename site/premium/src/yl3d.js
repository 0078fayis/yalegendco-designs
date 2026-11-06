/* YaLegendCo floating-tee showcase. No libraries. Reads tee data from the JSON script inside each .yl root. */
(function(){
  var uid=0;
  function teeSVG(t){
    var id='ylg'+(uid++), c=t.tee||'#16181d';
    return '<svg viewBox="0 0 400 470" role="img" aria-label="'+esc(t.name)+' tee">'+
      '<defs><linearGradient id="'+id+'s" x1="0" x2="1">'+
      '<stop offset="0" stop-color="#000" stop-opacity=".5"/><stop offset=".22" stop-color="#000" stop-opacity="0"/>'+
      '<stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset=".72" stop-color="#000" stop-opacity="0"/>'+
      '<stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient>'+
      '<linearGradient id="'+id+'v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".07"/><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient></defs>'+
      '<path d="M146 26 Q200 64 254 26 L334 50 Q368 66 398 118 L352 166 L322 146 L322 432 Q322 446 306 448 Q200 458 94 448 Q78 446 78 432 L78 146 L48 166 L2 118 Q32 66 66 50 Z" fill="'+c+'"/>'+
      '<path d="M146 26 Q200 64 254 26 L334 50 Q368 66 398 118 L352 166 L322 146 L322 432 Q322 446 306 448 Q200 458 94 448 Q78 446 78 432 L78 146 L48 166 L2 118 Q32 66 66 50 Z" fill="url(#'+id+'s)"/>'+
      '<path d="M146 26 Q200 64 254 26 L334 50 Q368 66 398 118 L352 166 L322 146 L322 432 Q322 446 306 448 Q200 458 94 448 Q78 446 78 432 L78 146 L48 166 L2 118 Q32 66 66 50 Z" fill="url(#'+id+'v)" stroke="#fff" stroke-opacity=".09" stroke-width="1.5"/>'+
      '<path d="M146 26 Q200 64 254 26" fill="none" stroke="#fff" stroke-opacity=".13" stroke-width="10" stroke-linecap="round"/>'+
      '<path d="M146 26 Q200 72 254 26" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="2"/>'+
      '<path d="M78 146 Q90 120 84 96 M322 146 Q310 120 316 96 M110 440 Q130 380 118 300 M296 438 Q276 390 286 320" fill="none" stroke="#000" stroke-opacity=".22" stroke-width="5" stroke-linecap="round"/>'+
      '<image href="'+t.img+'" x="122" y="96" width="156" height="196" preserveAspectRatio="xMidYMin meet"/>'+
      '</svg>';
  }
  function esc(s){return String(s||'').replace(/[&<>"]/g,function(m){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]})}

  function init(root){
    var dataEl=root.querySelector('.yl-data'); if(!dataEl) return;
    var tees; try{tees=JSON.parse(dataEl.textContent)}catch(e){return}
    if(!tees.length) return;
    var n=tees.length, show=root.querySelector('.yl-show'), stage=root.querySelector('.yl-stage'),
        ring=root.querySelector('.yl-ring'), nameEl=root.querySelector('.yl-name'), tagEl=root.querySelector('.yl-tag'),
        cur=root.querySelector('.yl-cur'), tot=root.querySelector('.yl-tot'), buy=root.querySelector('.yl-buy'),
        grid=root.querySelector('.yl-grid');
    if(tot) tot.textContent=String(n).padStart(2,'0');
    var rail=root.classList.contains('yl--rail'), railSvg=null;
    var HANGER='<svg class="yl-hanger" viewBox="0 0 400 120" aria-hidden="true"><path d="M200 70 L200 46 Q200 36 210 32 Q222 26 220 14 Q216 2 202 2 Q190 3 188 14" fill="none" stroke="#9aa0aa" stroke-width="7" stroke-linecap="round"/><path d="M200 70 L52 112 Q40 116 52 118 L348 118 Q360 116 348 112 Z" fill="#c9a77c" stroke="#a88758" stroke-width="3"/></svg>';
    if(rail){ railSvg=document.createElementNS('http://www.w3.org/2000/svg','svg'); railSvg.setAttribute('class','yl-railbar'); railSvg.setAttribute('aria-hidden','true'); ring.appendChild(railSvg); }
    var items=tees.map(function(t,i){
      var a=document.createElement('a'); a.className='yl-tee'; a.href=t.url||'#'; a.tabIndex=-1;
      a.innerHTML='<div class="yl-float" style="--yl-d:'+(-i*0.8)+'s">'+(rail?HANGER:'')+teeSVG(t)+'<div class="yl-shadow" style="--yl-d:'+(-i*0.8)+'s"></div></div>';
      ring.appendChild(a); return a;
    });
    if(grid) tees.forEach(function(t){
      var a=document.createElement('a'); a.className='yl-card'; a.href=t.url||'#'; a.style.setProperty('--c',t.accent||'#f2b544');
      a.innerHTML='<div class="yl-cardtee">'+teeSVG(t)+'</div><div class="yl-meta"><span>'+esc(t.colour||'Black')+' tee</span><b>Shop &rarr;</b></div><h3>'+esc(t.name)+'</h3><p>'+esc(t.tag)+'</p>';
      if(window.matchMedia('(hover:hover)').matches) {
        a.addEventListener('pointermove',function(e){var r=a.getBoundingClientRect();
          a.style.setProperty('--ry',((e.clientX-r.left)/r.width-.5)*14+'deg');a.style.setProperty('--rx',(.5-(e.clientY-r.top)/r.height)*10+'deg')});
        a.addEventListener('pointerleave',function(){a.style.setProperty('--ry','0deg');a.style.setProperty('--rx','0deg')});
      }
      grid.appendChild(a);
    });

    var active=-1, vw=0, teew=0, pos=0, target=0, auto=false, lastAct=0, hint=root.querySelector('.yl-hint');
    var still=window.matchMedia('(prefers-reduced-motion:reduce)').matches;
    // Embedded viewers (some app previews) grow the frame to the page height, so the page never scrolls.
    // Then the rack spins by itself and can be swiped instead.
    function detect(){
      var tall=window.innerHeight>Math.max(screen.height||0,900)*1.25;
      if(tall!==auto){ auto=tall; root.classList.toggle('yl--auto',auto); if(hint) hint.textContent=auto?'Swipe or tap the arrows':'Scroll to spin the rack'; }
    }
    function size(){ detect(); vw=stage.clientWidth; var rh=ring.clientHeight; teew=Math.max(130,Math.min(vw*(rail?0.56:0.46),rail?320:340,rh*(rail?0.62:0.66))); stage.style.setProperty('--yl-teew',teew+'px'); if(rail) drawRail(); }
    // rail mode: hooks sit on a bowed chrome rail; the rail dips toward the viewer in the middle
    function railY(x){ var W=Math.max(vw,1)/2, u=Math.min(1,Math.abs(x)/W); return Math.max(ring.clientHeight*0.05,(ring.clientHeight-teew*1.42)*0.42)+teew*0.09*(1-u*u); }
    function drawRail(){
      var w=ring.clientWidth, pts=[]; for(var i=0;i<=40;i++){ var x=-w/2+w*i/40*1; pts.push((x+w/2).toFixed(1)+','+railY(x).toFixed(1)); }
      railSvg.setAttribute('viewBox','0 0 '+w+' '+ring.clientHeight); railSvg.setAttribute('width',w); railSvg.setAttribute('height',ring.clientHeight);
      railSvg.innerHTML='<defs><linearGradient id="ylchrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".45" stop-color="#b9bec7"/><stop offset=".55" stop-color="#7d838d"/><stop offset="1" stop-color="#e4e7ec"/></linearGradient></defs>'+
        '<polyline points="'+pts.join(' ')+'" fill="none" stroke="rgba(0,0,0,.12)" stroke-width="9" stroke-linecap="round" transform="translate(0,6)"/>'+
        '<polyline points="'+pts.join(' ')+'" fill="none" stroke="url(#ylchrome)" stroke-width="8" stroke-linecap="round"/>';
    }
    function scrollP(){ var r=show.getBoundingClientRect(), span=show.offsetHeight-stage.offsetHeight; return span>0?Math.min(1,Math.max(0,-r.top/span)):0; }
    function go(d){ lastAct=Date.now();
      var k=Math.max(0,Math.min(n-1,Math.round(target)+d));
      if(auto){ target=k; return; }
      var span=show.offsetHeight-stage.offsetHeight, top=show.getBoundingClientRect().top+window.scrollY;
      window.scrollTo({top:top+span*k/(n-1)+1,behavior:still?'auto':'smooth'});
    }
    function render(){
      var p=pos/(n-1), R=Math.min(vw*0.62,560);
      stage.style.setProperty('--yl-p',p);
      if(rail){ items.forEach(function(el,i){
        var rel=i-pos, ab=Math.abs(rel), sp=teew*(vw<600?0.62:0.78);
        var x=rel*sp*(1-Math.min(ab,3)*0.08), s=Math.max(0.42,1-ab*0.3), hy=railY(x);
        var ry=Math.max(-50,Math.min(50,-rel*26));
        el.style.transform='translate3d('+x.toFixed(1)+'px,'+hy.toFixed(1)+'px,0) rotateY('+ry.toFixed(1)+'deg) scale('+s.toFixed(3)+')';
        el.style.opacity=ab>3.4?0:Math.max(0.2,1-ab*0.22).toFixed(3);
        el.style.zIndex=100-Math.round(ab*10);
      }); } else
      items.forEach(function(el,i){
        var rel=i-pos, a=rel*0.62, ab=Math.abs(rel);
        var x=Math.sin(a)*R, z=(Math.cos(a)-1)*R*1.1 - ab*40, y=ab*ab*6;
        var ry=Math.max(-60,Math.min(60,-rel*32)), s=ab<1?1.12-ab*0.12:1;
        el.style.transform='translate3d('+x.toFixed(1)+'px,'+y.toFixed(1)+'px,'+z.toFixed(1)+'px) rotateY('+ry.toFixed(1)+'deg) scale('+s.toFixed(3)+')';
        el.style.opacity=ab>3.2?0:Math.max(0.12,1-ab*0.32).toFixed(3);
        el.style.zIndex=100-Math.round(ab*10);
      });
      var k=Math.round(pos);
      if(k!==active){ active=k; var t=tees[k];
        nameEl.textContent=t.name; tagEl.textContent=t.tag||'';
        if(cur) cur.textContent=String(k+1).padStart(2,'0');
        if(buy) buy.href=t.url||'#';
        root.style.setProperty('--yl-accent',t.accent||'#f2b544');
        items.forEach(function(el,i){el.tabIndex=i===k?0:-1});
      }
    }
    function loop(){
      if(auto){
        if(!still && Date.now()-lastAct>3200){ lastAct=Date.now(); target=Math.round(target)+1; if(target>n-1) target=0; }
      } else target=scrollP()*(n-1);
      var d=target-pos; pos=Math.abs(d)<0.001?target:pos+d*(still?1:0.12);
      render(); requestAnimationFrame(loop);
    }
    // swipe (auto mode) and arrow buttons (both modes)
    var sx=null;
    stage.addEventListener('touchstart',function(e){ if(auto) sx=e.touches[0].clientX },{passive:true});
    stage.addEventListener('touchend',function(e){ if(sx===null) return; var dx=e.changedTouches[0].clientX-sx; sx=null; if(Math.abs(dx)>30) go(dx<0?1:-1) },{passive:true});
    var pv=root.querySelector('.yl-prev'), nx=root.querySelector('.yl-next');
    if(pv) pv.addEventListener('click',function(){go(-1)}); if(nx) nx.addEventListener('click',function(){go(1)});
    size(); target=auto?0:scrollP()*(n-1); pos=target; lastAct=Date.now(); render(); requestAnimationFrame(loop);
    window.addEventListener('resize',size);
  }
  function boot(){ document.querySelectorAll('.yl').forEach(function(r){ if(!r.dataset.ylReady){r.dataset.ylReady=1;init(r)} }) }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot); else boot();
  document.addEventListener('shopify:section:load',boot);
})();
