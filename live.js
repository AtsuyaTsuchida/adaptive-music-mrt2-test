document.title = "live — realtime control";
document.head.append(Object.assign(document.createElement("style"), {textContent: `
  :root { --env: #4da3ff; --gen: #ff9b45; }
  body { font-family: -apple-system, sans-serif; background: #0d0d0f; color: #eee;
         max-width: 760px; margin: 2rem auto; padding: 0 1rem; }
  h1 { font-size: 1.25rem; }
  .note { color: #888; font-size: .8rem; }
  .panel { background: #121216; border: 1px solid #222; border-radius: 8px;
           padding: .9rem 1rem; margin: .8rem 0; }
  .ctl { display: grid; grid-template-columns: 150px 1fr 64px; gap: .8rem;
         align-items: center; margin: .7rem 0; }
  .ctl label { font-size: .85rem; color: #bbb; }
  .ctl output { font-size: .85rem; text-align: right; font-variant-numeric: tabular-nums; }
  input[type=range] { width: 100%; accent-color: #6cf; }
  select, input[type=text], button {
    background: #1a1a20; color: #eee; border: 1px solid #333; border-radius: 6px;
    padding: .45rem .6rem; font-size: .85rem; }
  input[type=text] { width: 100%; box-sizing: border-box; }
  .drums button { margin-right: .4rem; min-width: 64px; cursor: pointer; }
  .drums button.on { background: #2a3a55; border-color: #6cf; color: #fff; }
  .levels { display: grid; grid-template-columns: 84px 1fr 64px; gap: .6rem;
            align-items: center; font-size: .8rem; margin: .35rem 0; }
  .bar { height: 10px; background: #1c1c22; border-radius: 5px; overflow: hidden; }
  .bar div { height: 100%; width: 0%; transition: width .15s; }
  #envbar div { background: var(--env); } #genbar div { background: var(--gen); }
  #stat { color: #777; font-size: .75rem; font-variant-numeric: tabular-nums; }
`}));
const el = (tag, props = {}, ...children) => {
  const n = document.createElement(tag);
  const {style, dataset, ...rest} = props;
  Object.assign(n, rest);
  if (style) n.style.cssText = style;
  if (dataset) Object.assign(n.dataset, dataset);
  n.append(...children);
  return n;
};
const stat = el("div", {id: "stat", textContent: "connecting…"});
const playpause = el("button", {id: "playpause", textContent: "…",
  style: "font-size:1.05rem; min-width:96px; cursor:pointer"});

const level = (id, label, colorVar) => el("div", {className: "levels"},
  el("span", {textContent: label, style: `color:var(${colorVar})`}),
  el("div", {className: "bar", id}, el("div")),
  el("output", {id: id.replace("bar", "rms"), value: "—"}));

const slider = (id, labelNode, min, max) => el("div", {className: "ctl"},
  labelNode,
  el("input", {type: "range", id, min, max, step: 0.01}),
  el("output", {htmlFor: id}));

const wAudioLabel = el("label", {}, "w_audio", el("br"),
  el("span", {className: "note", textContent: "1.0 = env embedding / 0.0 = text"}));

const drumsRow = el("div", {className: "ctl drums"},
  el("label", {textContent: "drums"}),
  el("div", {},
    el("button", {textContent: "auto", dataset: {v: "-1"}}),
    el("button", {textContent: "off", dataset: {v: "0"}}),
    el("button", {textContent: "on", dataset: {v: "1"}})),
  el("span"));

const envSelect = el("select", {id: "env"});
const promptInput = el("input", {type: "text", id: "prompt"});

document.body.append(
  el("h1", {textContent: "live — realtime synthesis & balance control"}),
  el("div", {className: "panel"},
    el("div", {style: "display:flex; gap:.8rem; align-items:center; margin-bottom:.5rem"},
      playpause, stat),
    level("envbar", "env level", "--env"),
    level("genbar", "gen level", "--gen")),
  el("div", {className: "panel"},
    slider("w_audio", wAudioLabel, 0, 1),
    slider("env_gain", el("label", {textContent: "env gain"}), 0, 1.5),
    slider("gen_gain", el("label", {textContent: "gen gain"}), 0, 1.5),
    drumsRow,
    el("div", {className: "ctl"}, el("label", {textContent: "env source"}), envSelect, el("span")),
    el("div", {className: "ctl"}, el("label", {textContent: "text prompt"}), promptInput, el("span"))),
);
const $ = id => document.getElementById(id);
const post = obj => fetch("/set", {method: "POST", body: JSON.stringify(obj)});
let editing = null;
const pending = {};
setInterval(() => {
  const keys = Object.keys(pending);
  if (keys.length) { post({...pending}); keys.forEach(k => delete pending[k]); }
}, 250);
for (const id of ["w_audio", "env_gain", "gen_gain"]) {
  const s = $(id), out = document.querySelector(`output[for=${id}]`);
  s.addEventListener("input", () => { out.value = (+s.value).toFixed(2); editing = id; pending[id] = +s.value; });
  s.addEventListener("change", () => { editing = null; pending[id] = +s.value; });
}
document.querySelectorAll(".drums button").forEach(b =>
  b.addEventListener("click", () => post({drums: +b.dataset.v})));
let isPlaying = true;
playpause.addEventListener("click", () => post({playing: !isPlaying}));
envSelect.addEventListener("change", () => post({env: envSelect.value}));
promptInput.addEventListener("change", () => post({prompt: promptInput.value}));

fetch("/sources").then(r => r.json()).then(list =>
  envSelect.append(...list.map(s => el("option", {textContent: s}))));
async function poll() {
  try {
    const {params, status} = await (await fetch("/state")).json();
    for (const id of ["w_audio", "env_gain", "gen_gain"]) {
      if (editing !== id && document.activeElement !== $(id)) {
        $(id).value = params[id];
        document.querySelector(`output[for=${id}]`).value = (+params[id]).toFixed(2);
      }
    }
    document.querySelectorAll(".drums button").forEach(b =>
      b.classList.toggle("on", +b.dataset.v === params.drums));
    isPlaying = params.playing;
    playpause.textContent = isPlaying ? "⏸ pause" : "▶ play";
    if (document.activeElement !== promptInput) promptInput.value = params.prompt;
    if (document.activeElement !== envSelect) envSelect.value = params.env;

    const e = status.env_rms, g = status.gen_rms;
    $("envbar").firstElementChild.style.width = Math.min(100, e * 600) + "%";
    $("genbar").firstElementChild.style.width = Math.min(100, g * 600) + "%";
    $("envrms").value = e.toFixed(3); $("genrms").value = g.toFixed(3);
    stat.textContent =
      `generated ${status.chunks * 2}s / buffer ${status.buffer}s / underruns ${status.underruns}`;
  } catch { stat.textContent = "server offline"; }
  setTimeout(poll, 250);
}
poll();
