#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProgramAPS · Generador de presentación
--------------------------------------
Lee slides.json (contenido) y produce un deck HTML autocontenido.
El contenido vive en el JSON; el diseño vive aquí. Editar la
presentación no exige tocar una sola línea de código.

Diseño: editorial oscuro de gestión sanitaria. La firma visual es la
"barra de balance" (déficit a la izquierda, superávit a la derecha),
el mismo gesto con que la herramienta responde si la oferta alcanza.
"""
import json, html, pathlib

BASE = pathlib.Path(__file__).parent
data = json.loads((BASE / "slides.json").read_text(encoding="utf-8"))
meta = data["meta"]
slides = data["slides"]

def esc(s):
    return html.escape(str(s), quote=True)

def nl2br(s):
    return "<br>".join(esc(p) for p in str(s).split("\n"))

# ── paleta y tokens, derivados de la propia app ─────────────────────
CSS = """
:root{
  --void:#061A1D; --void2:#0A2529; --deep:#0E3339; --panel:#F4F7F7; --panel2:#FFFFFF;
  --ink:#0C1A1D; --ink2:#3B4E53; --ink3:#7C979B;
  --brand:#0E5F63; --brand-lite:#3E9A93; --mint:#7FD4C4; --mint-dim:#5BAEA2;
  --line:#D5E0E0; --line-dk:#1B4147;
  --ok:#3BB273; --ok-dk:#1E7B4F; --warn:#E0A63C; --warn-dk:#B47714;
  --crit:#E5645B; --crit-dk:#B3372F;
  --sans:'IBM Plex Sans',system-ui,sans-serif; --disp:'Archivo',sans-serif; --mono:'IBM Plex Mono',monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{background:#02090A;font-family:var(--sans);color:var(--ink);overflow:hidden}

/* ── escenario y láminas ── */
#stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
.slide{position:absolute;width:min(96vw,1600px);height:min(96vh,900px);
  aspect-ratio:16/9;border-radius:22px;overflow:hidden;
  opacity:0;visibility:hidden;transform:scale(.985) translateY(8px);
  transition:opacity .5s cubic-bezier(.2,.7,.2,1),transform .5s cubic-bezier(.2,.7,.2,1);
  box-shadow:0 40px 120px rgba(0,0,0,.55);pointer-events:none}
.slide.on{opacity:1;visibility:visible;transform:none;pointer-events:auto}
.slide.dark{background:radial-gradient(120% 120% at 82% 12%,var(--deep) 0%,var(--void2) 42%,var(--void) 100%);color:#EAF3F2}
.slide.light{background:var(--panel)}
.pad{position:absolute;inset:0;padding:clamp(2rem,4.4vh,3.8rem) clamp(2.4rem,4.4vw,4.6rem);display:flex;flex-direction:column}

/* ── tipografía compartida ── */
.kicker{font-family:var(--mono);font-size:clamp(.62rem,1.15vw,.82rem);letter-spacing:.28em;
  text-transform:uppercase;color:var(--brand-lite);display:flex;align-items:center;gap:.7rem}
.dark .kicker{color:var(--mint-dim)}
.kicker::before{content:"";width:26px;height:2px;background:currentColor;opacity:.7}
h1.t{font-family:var(--disp);font-weight:800;letter-spacing:-.028em;line-height:1.02;
  font-size:clamp(2rem,4.7vw,3.7rem);margin:.5rem 0 .2rem}
.dark h1.t{color:#fff}
.bajada{font-size:clamp(.95rem,1.5vw,1.18rem);color:var(--ink2);max-width:64ch;line-height:1.45}
.dark .bajada{color:#AFC9C6}
.remate{font-family:var(--disp);font-style:italic;font-weight:500;color:var(--ink2);
  font-size:clamp(.95rem,1.5vw,1.16rem);line-height:1.4}
.dark .remate{color:#B9D3D0}
.spacer{flex:1}

/* ── portada ── */
.cover .wm{position:absolute;right:-4%;top:-12%;font-family:var(--disp);font-weight:800;
  font-size:34vh;color:rgba(127,212,196,.05);letter-spacing:-.04em;pointer-events:none;user-select:none}
.cover .brand{font-family:var(--disp);font-weight:800;letter-spacing:-.03em;
  font-size:clamp(3.4rem,9vw,7rem);line-height:.92;color:#fff}
.cover .brand em{font-style:normal;color:var(--mint)}
.cover .sub{font-size:clamp(1.1rem,2.2vw,1.7rem);color:#CBE1DE;font-weight:500;margin-top:.6rem}
.cover .baj{font-family:var(--disp);font-style:italic;color:var(--mint-dim);
  font-size:clamp(.95rem,1.6vw,1.2rem);margin-top:.5rem}
.cover .foot{position:absolute;left:clamp(2.4rem,4.4vw,4.6rem);bottom:clamp(2rem,4vh,3.4rem);
  font-family:var(--mono);font-size:.76rem;letter-spacing:.06em;color:var(--mint-dim)}
/* firma: barra de balance en la portada */
.balance-sig{display:flex;align-items:center;gap:0;margin-top:2.4rem;height:12px;width:min(52%,540px)}
.balance-sig .neg{height:100%;background:linear-gradient(90deg,transparent,var(--crit));border-radius:6px 0 0 6px;flex:1}
.balance-sig .mid{width:2px;height:26px;background:var(--mint)}
.balance-sig .pos{height:100%;background:linear-gradient(90deg,var(--brand-lite),var(--mint));border-radius:0 6px 6px 0;flex:1}

/* ── pregunta / momento ── */
.big{font-family:var(--disp);font-weight:800;letter-spacing:-.03em;line-height:1.03;
  font-size:clamp(2.4rem,6vw,5rem)}
.big.two{color:var(--mint)}
.dark .qbody{color:#B9D3D0;font-size:clamp(1rem,1.6vw,1.25rem);max-width:70ch;line-height:1.5;margin-top:1.6rem}
.qremate{font-weight:700;font-style:italic;font-family:var(--disp);color:#fff;
  font-size:clamp(1.05rem,1.8vw,1.4rem);margin-top:1rem}
.blob{position:absolute;border-radius:50%;background:radial-gradient(circle at 40% 35%,var(--deep),transparent 70%);pointer-events:none}

/* ── grillas y tarjetas ── */
.grid{display:grid;gap:clamp(1rem,1.8vw,1.5rem)}
.g2{grid-template-columns:1fr 1fr}.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}.g6{grid-template-columns:repeat(6,1fr)}
.card{background:var(--panel2);border:1px solid var(--line);border-radius:16px;
  padding:clamp(1.1rem,2vw,1.6rem);box-shadow:0 2px 4px rgba(12,26,29,.04)}
.card.tint-ok{background:#EAF6EF;border-color:#CDE9DA}
.card.tint-warn{background:#FBF3E1;border-color:#F0E0BE}
.card.tint-crit{background:#FCEBE9;border-color:#F5D3CF}
.card.tint-info{background:#E7F1F1;border-color:#CADEDE}
.card.dark{background:rgba(255,255,255,.04);border-color:rgba(127,212,196,.18)}
.rot{font-family:var(--disp);font-weight:700;font-size:clamp(1.05rem,1.7vw,1.35rem);letter-spacing:-.01em}
.rot.ok{color:var(--ok-dk)}.rot.warn{color:var(--warn-dk)}.rot.crit{color:var(--crit-dk)}.rot.info{color:var(--brand)}
ul.clean{list-style:none;margin-top:.9rem;display:flex;flex-direction:column;gap:.6rem}
ul.clean li{position:relative;padding-left:1.4rem;font-size:clamp(.85rem,1.25vw,1rem);line-height:1.35;color:var(--ink)}
ul.clean li::before{content:"";position:absolute;left:0;top:.5em;width:7px;height:7px;border-radius:2px;background:var(--brand)}
ul.clean li.strong{font-weight:700}
ul.clean.ok li::before{background:var(--ok-dk)}
ul.clean.warn li::before{background:var(--warn-dk)}

/* índice numerado en círculo — motivo repetido del menú de la app */
.idx{width:clamp(2.6rem,4vw,3.4rem);height:clamp(2.6rem,4vw,3.4rem);border-radius:50%;
  background:var(--brand);color:#fff;display:flex;align-items:center;justify-content:center;
  font-family:var(--mono);font-weight:600;font-size:clamp(.9rem,1.5vw,1.2rem);flex:none}
.idx.warn{background:var(--warn-dk)}.idx.crit{background:var(--crit-dk)}.idx.ok{background:var(--ok-dk)}
.idx.ghost{background:rgba(127,212,196,.16);color:var(--mint)}

/* ── cifras enfrentadas ── */
.cifras{display:flex;align-items:stretch;gap:clamp(1rem,2vw,1.6rem)}
.cifra{flex:1;border-radius:16px;padding:clamp(1.2rem,2.4vw,2rem);border:1px solid var(--line);background:#fff}
.cifra.mint{background:linear-gradient(150deg,#0E3339,#0A2529);border-color:var(--line-dk)}
.cifra .cr{font-family:var(--mono);font-size:.8rem;letter-spacing:.05em;color:var(--ink3)}
.cifra.mint .cr{color:var(--mint-dim)}
.cifra .cv{font-family:var(--disp);font-weight:800;letter-spacing:-.03em;
  font-size:clamp(3rem,8vw,5.6rem);line-height:1;color:var(--ink);margin:.2rem 0}
.cifra.mint .cv{color:var(--mint)}
.cifra .cu{font-size:.92rem;color:var(--ink2)}.cifra.mint .cu{color:#9FC1BD}
.eq{display:flex;align-items:center;font-family:var(--disp);font-weight:800;
  font-size:clamp(1.8rem,3.5vw,3rem);color:var(--ink3)}
.sellos{display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center;margin-top:1.4rem}
.sello{font-family:var(--mono);font-size:clamp(.72rem,1.15vw,.9rem);background:var(--deep);color:var(--mint);
  border:1px solid var(--line-dk);border-radius:99px;padding:.4rem .95rem;font-weight:500}
.slide.light .sello{background:#E7F1F1;color:var(--brand);border-color:#CADEDE}

/* ── flujo ── */
.flowrow{display:flex;align-items:stretch;gap:.5rem;margin-top:.4rem}
.step{flex:1;background:#fff;border:1px solid var(--line);border-radius:14px;
  padding:clamp(.8rem,1.5vw,1.2rem);display:flex;flex-direction:column;align-items:center;text-align:center;gap:.5rem}
.step .st{font-family:var(--disp);font-weight:700;font-size:clamp(.95rem,1.5vw,1.2rem);color:var(--brand)}
.step .st.crit{color:var(--crit-dk)}.step .st.ok{color:var(--ok-dk)}
.step .sx{font-size:clamp(.72rem,1.1vw,.9rem);color:var(--ink2);line-height:1.3}
.arrow{display:flex;align-items:center;color:var(--ink3);font-size:1.5rem;font-weight:300}

/* ── barra de balance (gráfico nativo, la firma) ── */
.chartwrap{display:flex;flex-direction:column;gap:.55rem;margin-top:.3rem}
.bar-row{display:grid;grid-template-columns:8.5rem 1fr;align-items:center;gap:.8rem}
.bar-row .bn{font-size:clamp(.78rem,1.2vw,.98rem);color:var(--ink);text-align:right;font-weight:500}
.bar-track{position:relative;height:clamp(1.5rem,2.6vw,2rem);background:linear-gradient(90deg,#F0E3E2 0 50%,#E3EEEC 50% 100%);border-radius:6px}
.bar-track .axis{position:absolute;left:50%;top:-3px;bottom:-3px;width:2px;background:var(--ink3);opacity:.5}
.bar-fill{position:absolute;top:0;bottom:0;display:flex;align-items:center;border-radius:5px}
.bar-fill.pos{left:50%;background:linear-gradient(90deg,var(--brand),var(--brand-lite));justify-content:flex-end;padding-right:.5rem;color:#fff}
.bar-fill.neg{right:50%;background:linear-gradient(90deg,var(--crit),var(--crit-dk));justify-content:flex-start;padding-left:.5rem;color:#fff}
.bar-fill .bv{font-family:var(--mono);font-size:clamp(.66rem,1vw,.82rem);font-weight:500}
.axlabel{grid-column:2;font-family:var(--mono);font-size:.7rem;color:var(--ink3);display:flex;justify-content:space-between;margin-top:.1rem}

/* ── consola de cálculo ── */
.console{background:#06181B;border:1px solid var(--line-dk);border-radius:14px;
  padding:clamp(1rem,1.8vw,1.4rem);font-family:var(--mono);font-size:clamp(.78rem,1.2vw,.98rem);line-height:1.7}
.console .base{color:#DCEAE8}.console .tenue{color:#5F827E;font-size:.86em}
.console .acento{color:var(--mint);font-weight:500}

/* aviso embebido en tarjeta */
.aviso{border-radius:11px;padding:.75rem .9rem;margin-top:1rem;font-size:clamp(.78rem,1.15vw,.95rem);line-height:1.4}
.aviso.warn{background:#FBF3E1}.aviso.info{background:#E7F1F1}.aviso.crit{background:#FCEBE9}.aviso.ok{background:#EAF6EF}
.aviso b.warn{color:var(--warn-dk)}.aviso b.info{color:var(--brand)}.aviso b.crit{color:var(--crit-dk)}.aviso b.ok{color:var(--ok-dk)}

/* semáforo (lámina alerta) */
.semrow{display:flex;align-items:center;gap:.8rem;border-radius:11px;padding:.7rem .95rem;margin-top:.7rem;font-size:clamp(.82rem,1.25vw,1rem)}
.semrow.ok{background:#EAF6EF}.semrow.crit{background:#FCEBE9}
.semrow .dot{width:12px;height:12px;border-radius:50%;flex:none}
.semrow.ok .dot{background:var(--ok-dk)}.semrow.crit .dot{background:var(--crit-dk)}
.semrow .act{margin-left:auto;font-weight:700}
.semrow.ok .act{color:var(--ok-dk)}.semrow.crit .act{color:var(--crit-dk)}
.cifrabox{background:linear-gradient(155deg,#0E3339,#061A1D);border-radius:16px;padding:clamp(1.2rem,2.4vw,1.8rem);
  display:flex;flex-direction:column;justify-content:center;color:#EAF3F2;border:1px solid var(--line-dk)}
.cifrabox .pre{color:#9FC1BD;font-size:clamp(.85rem,1.3vw,1.02rem);line-height:1.35}
.cifrabox .big2{font-family:var(--disp);font-weight:800;font-size:clamp(3rem,7vw,5rem);color:var(--mint);line-height:1;margin:.3rem 0}
.cifrabox .aft{font-weight:700;font-size:clamp(1rem,1.5vw,1.2rem);color:#fff}
.cifrabox .nt{color:#84A7A3;font-style:italic;font-size:clamp(.78rem,1.15vw,.92rem);margin-top:.7rem;line-height:1.4}

/* pendientes */
.pendcard{display:flex;gap:.85rem;align-items:flex-start}
.pendcard .pdot{width:14px;height:14px;border-radius:50%;margin-top:.35rem;flex:none}
.pdot.crit{background:var(--crit-dk)}.pdot.warn{background:var(--warn-dk)}.pdot.mint{background:var(--brand)}
.pendcard .ph{font-family:var(--disp);font-weight:700;font-size:clamp(1rem,1.5vw,1.25rem)}
.ph.crit{color:var(--crit-dk)}.ph.warn{color:var(--warn-dk)}.ph.mint{color:var(--brand)}
.pendcard .px{font-size:clamp(.8rem,1.2vw,.96rem);color:var(--ink2);line-height:1.35;margin-top:.15rem}

/* cierre */
.cierre h1.t{font-size:clamp(1.9rem,4.2vw,3.4rem);max-width:20ch}
.cierre .baj{color:var(--mint-dim);font-family:var(--disp);font-style:italic;
  font-size:clamp(1rem,1.7vw,1.35rem);margin-top:1.4rem;max-width:52ch;line-height:1.4}
.cierre .rem{color:#CBE1DE;font-size:clamp(.95rem,1.5vw,1.15rem);margin-top:.8rem;font-weight:600}

/* split cifra (por estamento) */
.mintbox{background:linear-gradient(155deg,#0E3339,#061A1D);border-radius:16px;padding:clamp(1.2rem,2.2vw,1.7rem);
  color:#EAF3F2;border:1px solid var(--line-dk);display:flex;flex-direction:column}
.mintbox .mr{font-family:var(--disp);font-weight:700;font-size:clamp(1.05rem,1.6vw,1.3rem);color:#fff}
.mintbox .ms{color:#9FC1BD;font-size:clamp(.82rem,1.2vw,.98rem);margin-top:.3rem}
.mintbox .mv{font-family:var(--disp);font-weight:800;font-size:clamp(3rem,6.5vw,4.6rem);color:var(--mint);line-height:1;margin:.5rem 0 .2rem}
.mintbox .mt{font-size:clamp(.92rem,1.4vw,1.12rem);color:#fff}
.mintbox .mn{color:#84A7A3;font-style:italic;font-size:clamp(.78rem,1.15vw,.92rem);margin-top:.7rem;line-height:1.4}

/* remate a pie de lámina */
.footremate{border-radius:12px;padding:.8rem 1.1rem;font-size:clamp(.82rem,1.25vw,1.02rem);
  text-align:center;font-weight:600;line-height:1.4}
.footremate.crit{background:#FCEBE9;color:var(--crit-dk)}
.footremate.ok{background:#EAF6EF;color:var(--ok-dk)}
.footremate.plain{color:var(--ink2);font-style:italic;font-weight:500}

/* campos con viñeta circular */
.field{display:flex;gap:.7rem;align-items:flex-start;margin-top:.75rem}
.field .fd{width:.75rem;height:.75rem;border-radius:50%;background:var(--brand);margin-top:.3rem;flex:none}
.field .fh{font-weight:700;font-size:clamp(.9rem,1.35vw,1.08rem);color:var(--brand)}
.field .fx{font-size:clamp(.8rem,1.2vw,.96rem);color:var(--ink2);line-height:1.3}

/* ── chrome: progreso, navegación, notas ── */
#bar{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--brand),var(--mint));z-index:50;transition:width .4s ease}
#hud{position:fixed;bottom:14px;right:18px;z-index:50;display:flex;align-items:center;gap:12px;
  font-family:var(--mono);font-size:.72rem;color:#4A6E6A}
#hud button{background:rgba(255,255,255,.06);border:1px solid rgba(127,212,196,.22);color:#9FC1BD;
  width:30px;height:30px;border-radius:8px;font-size:.9rem;cursor:pointer;transition:.15s}
#hud button:hover{background:rgba(127,212,196,.16);color:#fff}
#hud #count{min-width:3.4rem;text-align:center}
#notes{position:fixed;left:0;right:0;bottom:0;z-index:49;background:rgba(4,12,13,.96);
  color:#CBE1DE;border-top:1px solid rgba(127,212,196,.2);padding:1rem 1.4rem 3rem;
  font-size:.92rem;line-height:1.5;max-height:42vh;overflow:auto;transform:translateY(100%);
  transition:transform .3s ease;white-space:pre-wrap}
#notes.on{transform:none}
#notes .nh{font-family:var(--mono);font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:#5BAEA2;margin-bottom:.5rem}
#hint{position:fixed;bottom:14px;left:18px;z-index:50;font-family:var(--mono);font-size:.68rem;color:#3A5C58}
@media (max-width:640px){#hint{display:none}}
@media (prefers-reduced-motion:reduce){.slide{transition:opacity .01s}}
@media print{.slide{position:relative;page-break-after:always;opacity:1!important;visibility:visible!important;transform:none!important;
  width:100%;height:auto;aspect-ratio:16/9;box-shadow:none;border-radius:0}#bar,#hud,#notes,#hint{display:none!important}
  #stage{display:block;position:static}body{overflow:visible}}
"""

# ── renderizadores por tipo de lámina ───────────────────────────────
def r_portada(s):
    return f"""<div class="pad cover">
      <div class="wm">A</div>
      <div class="spacer"></div>
      <div class="brand">{esc(s['marca'])}<em>{esc(s['marca_acento'])}</em></div>
      <div class="sub">{esc(s['titulo'])}</div>
      <div class="baj">{esc(s['bajada'])}</div>
      <div class="balance-sig"><div class="neg"></div><div class="mid"></div><div class="pos"></div></div>
      <div class="spacer"></div>
      <div class="foot">{esc(meta['pie'])}</div>
    </div>"""

def r_pregunta(s):
    body = ""
    if s.get("titulo2"):
        body += f'<div class="big two" style="margin-top:.3rem">{esc(s["titulo2"])}</div>'
    if s.get("cuerpo"):
        body += f'<div class="qbody">{esc(s["cuerpo"])}</div>'
    if s.get("remate"):
        body += f'<div class="qremate">{esc(s["remate"])}</div>'
    elif s.get("remate") is None and s.get("titulo2") is None and s.get("cuerpo") is None and s.get("remate"):
        pass
    rem_simple = f'<div class="qremate" style="color:var(--mint)">{esc(s["remate"])}</div>' if (s.get("remate") and not s.get("cuerpo")) else ""
    return f"""<div class="pad">
      <div class="blob" style="width:44vh;height:44vh;left:-12vh;bottom:-14vh"></div>
      <div class="spacer"></div>
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="big" style="margin-top:1rem;max-width:20ch">{esc(s['titulo'])}</h1>
      {body if (s.get('titulo2') or s.get('cuerpo')) else rem_simple}
      <div class="spacer"></div>
    </div>"""

def r_comparar(s):
    def col(c):
        lis = "".join(f'<li class="{"strong" if i==len(c["items"])-1 else ""}">{esc(x)}</li>'
                      for i,x in enumerate(c["items"]))
        return f'<div class="card tint-{c["tono"]}"><div class="rot {c["tono"]}">{esc(c["rotulo"])}</div><ul class="clean {c["tono"]}">{lis}</ul></div>'
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1.3rem">{esc(s['bajada'])}</div>
      <div class="grid g2" style="flex:1;align-content:center">{col(s['izq'])}{col(s['der'])}</div>
    </div>"""

def r_cifras(s):
    cards = []
    for i,p in enumerate(s["pares"]):
        cls = "cifra mint" if p["tono"]=="mint" else "cifra"
        cards.append(f'<div class="{cls}"><div class="cr">{esc(p["rotulo"])}</div><div class="cv">{esc(p["valor"])}</div><div class="cu">{esc(p["unidad"])}</div></div>')
        if i==0: cards.append('<div class="eq">=</div>')
    sellos = "".join(f'<span class="sello">{esc(x)}</span>' for x in s["sellos"])
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1.4rem">{esc(s['bajada'])}</div>
      <div class="cifras">{''.join(cards)}</div>
      <div class="sellos">{sellos}</div>
      <div class="spacer"></div>
      <div class="remate" style="text-align:center">{esc(s['remate'])}</div>
    </div>"""

def r_tarjetas(s):
    cs = "".join(
      f'<div class="card"><div class="idx">{esc(t["n"])}</div>'
      f'<div class="rot" style="margin-top:1rem">{esc(t["titulo"])}</div>'
      f'<div class="px" style="margin-top:.5rem;color:var(--ink2);font-size:clamp(.82rem,1.2vw,.98rem);line-height:1.4">{esc(t["texto"])}</div></div>'
      for t in s["tarjetas"])
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="grid g3" style="flex:1;align-content:center;margin:1rem 0">{cs}</div>
      <div class="footremate ok">{esc(s['remate'])}</div>
    </div>"""

def r_flujo(s):
    parts=[]
    for i,p in enumerate(s["pasos"]):
        tone = p.get("tono","")
        parts.append(f'<div class="step"><div class="idx {tone}">{esc(p["n"])}</div>'
                     f'<div class="st {tone}">{esc(p["titulo"])}</div><div class="sx">{esc(p["texto"])}</div></div>')
        if i < len(s["pasos"])-1: parts.append('<div class="arrow">›</div>')
    tone = s.get("remate_tono","plain")
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1.2rem">{esc(s['bajada'])}</div>
      <div class="flowrow" style="flex:1;align-items:center">{''.join(parts)}</div>
      <div class="footremate {tone}" style="margin-top:1.1rem">{esc(s['remate'])}</div>
    </div>"""

def r_dos_modulos(s):
    def mod(m):
        lis="".join(f'<li>{esc(x)}</li>' for x in m["items"])
        av=m.get("aviso")
        avh=(f'<div class="aviso {av["tono"]}"><b class="{av["tono"]}">{esc(av["fuerte"])}</b> {esc(av["texto"])}</div>' if av else "")
        return (f'<div class="card"><div style="display:flex;align-items:center;gap:.8rem">'
                f'<div class="idx">{esc(m["n"])}</div><div class="rot">{esc(m["titulo"])}</div></div>'
                f'<ul class="clean">{lis}</ul>{avh}</div>')
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1.2rem">{esc(s['bajada'])}</div>
      <div class="grid g2" style="flex:1;align-content:center">{mod(s['modulos'][0])}{mod(s['modulos'][1])}</div>
    </div>"""

def r_tres_modulos(s):
    def mod(m):
        tone=m.get("tono","")
        return (f'<div class="card"><div style="display:flex;align-items:center;gap:.75rem">'
                f'<div class="idx {tone}">{esc(m["n"])}</div><div class="rot {tone}">{esc(m["titulo"])}</div></div>'
                f'<div class="px" style="margin-top:.9rem;color:var(--ink2);font-size:clamp(.8rem,1.15vw,.95rem);line-height:1.4">{nl2br(m["texto"])}</div></div>')
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1rem">{esc(s['bajada'])}</div>
      <div class="grid g3" style="flex:1;align-content:center">{''.join(mod(m) for m in s['modulos'])}</div>
      <div class="footremate {s.get('remate_tono','crit')}" style="margin-top:1rem">{esc(s['remate'])}</div>
    </div>"""

def r_alerta(s):
    sem="".join(f'<div class="semrow {r["tono"]}"><span class="dot"></span><span>{esc(r["texto"])}</span>'
                f'<span class="act">→ {esc(r["accion"])}</span></div>' for r in s["semaforo"])
    c=s["cifra"]
    return f"""<div class="pad">
      <div class="kicker" style="color:var(--crit-dk)">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1.1rem">{esc(s['bajada'])}</div>
      <div class="grid" style="grid-template-columns:1.55fr 1fr;flex:1;align-content:center">
        <div class="card">
          <div class="rot" style="margin-bottom:.4rem">{esc(s['explicacion']['titulo'])}</div>
          <div class="px" style="color:var(--ink2);font-size:clamp(.82rem,1.2vw,.98rem);line-height:1.45">{esc(s['explicacion']['texto'])}</div>
          {sem}
        </div>
        <div class="cifrabox">
          <div class="pre">{esc(c['antes'])}</div>
          <div class="big2">{esc(c['valor'])} {esc(c['sufijo'])}</div>
          <div class="aft">{esc(c['despues'])}</div>
          <div class="nt">{esc(c['nota'])}</div>
        </div>
      </div>
    </div>"""

def r_calculo(s):
    campos="".join(f'<div class="field"><div class="fd"></div><div><span class="fh">{esc(c["titulo"])}</span>'
                   f'<div class="fx">{esc(c["texto"])}</div></div></div>' for c in s["campos"])
    lineas="".join((f'<div class="{ln["c"]}">{esc(ln["t"]) or "&nbsp;"}</div>') for ln in s["consola"]["lineas"])
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1rem">{esc(s['bajada'])}</div>
      <div class="grid g2" style="flex:1;align-content:center">
        <div class="card"><div class="rot" style="font-size:clamp(1rem,1.5vw,1.2rem)">Haz clic en una prestación y se abre el detalle</div>{campos}
          <div class="px" style="margin-top:1rem;color:var(--ink3);font-style:italic;font-size:.85rem">Usa los filtros de arriba para no perderte entre 236 filas.</div></div>
        <div class="card tint-info"><div class="rot info" style="margin-bottom:.7rem">{esc(s['consola']['titulo'])}</div>
          <div class="console">{lineas}</div>
          <div class="px" style="margin-top:.8rem;font-weight:700;color:var(--brand)">{esc(s['remate'])}</div></div>
      </div>
    </div>"""

def r_grafico(s):
    mx=max(abs(d["valor"]) for d in s["datos"])
    rows=""
    for d in s["datos"]:
        v=d["valor"]; w=abs(v)/mx*48
        if v>=0:
            fill=f'<div class="bar-fill pos" style="width:{w:.1f}%"><span class="bv">+{v:.1f}</span></div>'
        else:
            fill=f'<div class="bar-fill neg" style="width:{w:.1f}%"><span class="bv">{v:.1f}</span></div>'
        rows+=f'<div class="bar-row"><div class="bn">{esc(d["nombre"])}</div><div class="bar-track"><div class="axis"></div>{fill}</div></div>'
    p=s["panel"]
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:.8rem">{esc(s['bajada'])}</div>
      <div class="grid" style="grid-template-columns:1.7fr 1fr;flex:1;align-content:center">
        <div>
          <div class="chartwrap">{rows}</div>
          <div class="axlabel"><span>← faltan horas · déficit</span><span>{esc(s['unidad'])}</span><span>sobran horas · superávit →</span></div>
        </div>
        <div class="card tint-crit">
          <div class="rot crit" style="font-size:clamp(1.05rem,1.6vw,1.35rem)">{esc(p['titulo'])}</div>
          <div class="px" style="margin-top:.6rem;color:var(--ink);font-size:clamp(.82rem,1.2vw,.98rem);line-height:1.4">{esc(p['texto'])}</div>
          <div class="remate" style="margin-top:.7rem;font-size:clamp(.82rem,1.2vw,.98rem)">{esc(p['enfasis'])}</div>
          <div style="background:#fff;border-radius:10px;padding:.7rem .9rem;margin-top:.9rem;font-weight:700;color:var(--brand);font-size:clamp(.78rem,1.1vw,.92rem)">{esc(p['pie'])}</div>
        </div>
      </div>
    </div>"""

def r_split_cifra(s):
    l=s["izq"]; d=s["der"]
    lis="".join(f'<li>{esc(x)}</li>' for x in l["items"])
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1.1rem">{esc(s['bajada'])}</div>
      <div class="grid g2" style="flex:1;align-content:center">
        <div class="card"><div style="display:flex;align-items:center;gap:.8rem"><div class="idx">{esc(l["n"])}</div>
          <div class="rot">{esc(l["titulo"])}</div></div><ul class="clean">{lis}</ul>
          <div class="aviso info"><b class="info">{esc(l["pie"])}</b></div></div>
        <div class="mintbox"><div class="mr">{esc(d["rotulo"])}</div><div class="ms">{esc(d["sub"])}</div>
          <div class="mv">{esc(d["valor"])}</div><div class="mt">{esc(d["texto"])}</div><div class="mn">{esc(d["nota"])}</div></div>
      </div>
    </div>"""

def r_pendientes(s):
    cs="".join(f'<div class="card pendcard"><div class="pdot {i["tono"]}"></div><div>'
               f'<div class="ph {i["tono"]}">{esc(i["titulo"])}</div><div class="px">{esc(i["texto"])}</div></div></div>'
               for i in s["items"])
    return f"""<div class="pad">
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="bajada" style="margin-bottom:1rem">{esc(s['bajada'])}</div>
      <div class="grid g2" style="flex:1;align-content:center">{cs}</div>
      <div class="footremate plain" style="margin-top:1rem">{esc(s['remate'])}</div>
    </div>"""

def r_cierre(s):
    return f"""<div class="pad cierre">
      <div class="blob" style="width:52vh;height:52vh;right:-14vh;bottom:-16vh"></div>
      <div class="spacer"></div>
      <div class="kicker">{esc(s['kicker'])}</div>
      <h1 class="t">{esc(s['titulo'])}</h1>
      <div class="baj">{esc(s['bajada'])}</div>
      <div class="rem">{esc(s['remate'])}</div>
      <div class="spacer"></div>
    </div>"""

R = {"portada":r_portada,"pregunta":r_pregunta,"comparar":r_comparar,"cifras":r_cifras,
     "tarjetas":r_tarjetas,"flujo":r_flujo,"dos_modulos":r_dos_modulos,"tres_modulos":r_tres_modulos,
     "alerta":r_alerta,"calculo":r_calculo,"grafico":r_grafico,"split_cifra":r_split_cifra,
     "pendientes":r_pendientes,"cierre":r_cierre}

DARK = {"portada","pregunta","cierre"}

slide_html=[]
notes_js=[]
for i,s in enumerate(slides):
    theme = "dark" if s["tipo"] in DARK else "light"
    inner = R[s["tipo"]](s)
    slide_html.append(f'<section class="slide {theme}" data-i="{i}">{inner}</section>')
    notes_js.append(json.dumps(s.get("notas","")))

DOC = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(meta['titulo'])} · {esc(meta['subtitulo'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div id="bar"></div>
<div id="stage">
{chr(10).join(slide_html)}
</div>
<div id="hint">← → navegar · N notas · F pantalla completa</div>
<div id="hud">
  <button id="prev" aria-label="Anterior">‹</button>
  <span id="count">1 / {len(slides)}</span>
  <button id="next" aria-label="Siguiente">›</button>
  <button id="tnotes" aria-label="Notas del orador">N</button>
</div>
<div id="notes"><div class="nh">Notas del orador</div><div id="notes-body"></div></div>
<script>
const NOTES=[{",".join(notes_js)}];
const slides=[...document.querySelectorAll('.slide')];
const N=slides.length; let cur=0;
const bar=document.getElementById('bar'),count=document.getElementById('count'),
      notes=document.getElementById('notes'),nbody=document.getElementById('notes-body');
function show(i){{
  cur=Math.max(0,Math.min(N-1,i));
  slides.forEach((s,k)=>s.classList.toggle('on',k===cur));
  bar.style.width=((cur+1)/N*100)+'%';
  count.textContent=(cur+1)+' / '+N;
  nbody.textContent=NOTES[cur]||'—';
  location.hash=cur+1;
}}
function next(){{show(cur+1)}} function prev(){{show(cur-1)}}
document.getElementById('next').onclick=next;
document.getElementById('prev').onclick=prev;
document.getElementById('tnotes').onclick=()=>notes.classList.toggle('on');
addEventListener('keydown',e=>{{
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' ')  {{e.preventDefault();next();}}
  else if(e.key==='ArrowLeft'||e.key==='PageUp') {{e.preventDefault();prev();}}
  else if(e.key==='Home') show(0);
  else if(e.key==='End') show(N-1);
  else if(e.key.toLowerCase()==='n') notes.classList.toggle('on');
  else if(e.key.toLowerCase()==='f'){{ if(!document.fullscreenElement)document.documentElement.requestFullscreen(); else document.exitFullscreen(); }}
}});
let sx=null;
addEventListener('touchstart',e=>sx=e.touches[0].clientX,{{passive:true}});
addEventListener('touchend',e=>{{ if(sx===null)return; const dx=e.changedTouches[0].clientX-sx;
  if(Math.abs(dx)>50){{dx<0?next():prev();}} sx=null; }},{{passive:true}});
const h=parseInt(location.hash.slice(1)); show(isNaN(h)?0:h-1);
</script>
</body>
</html>"""

out = BASE / "ProgramAPS_Presentacion.html"
out.write_text(DOC, encoding="utf-8")
print(f"OK · {len(slides)} láminas · {len(DOC):,} bytes → {out.name}")
