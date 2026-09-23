#!/usr/bin/env python3
"""Build the self-contained, offline facilitator guide from content.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


HERE = Path(__file__).resolve().parent


def require_text(value: object, where: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{where} must be a string")
    return value


def require_list(value: object, where: str) -> list:
    if not isinstance(value, list):
        raise ValueError(f"{where} must be a list")
    return value


def read_content(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("content.json must contain an object")
    for key in ("title", "subtitle", "version", "base_sha", "share_url"):
        require_text(data[key], key)
    for key in ("stages", "prompts", "sources"):
        require_list(data[key], key)
    if not data["stages"]:
        raise ValueError("stages must contain at least one stage")

    prompt_ids = set()
    for index, prompt in enumerate(data["prompts"]):
        where = f"prompts[{index}]"
        if not isinstance(prompt, dict):
            raise ValueError(f"{where} must be an object")
        for key in ("id", "title", "file", "hint"):
            require_text(prompt[key], f"{where}.{key}")
        if prompt["id"] in prompt_ids:
            raise ValueError(f"duplicate prompt id: {prompt['id']}")
        prompt_ids.add(prompt["id"])
        prompt_path = (path.parent / prompt["file"]).resolve()
        if not prompt_path.is_relative_to(path.parent.resolve()):
            raise ValueError(f"{where}.file must stay within {path.parent}")
        prompt["body"] = prompt_path.read_text(encoding="utf-8")

    stage_ids = set()
    for index, stage in enumerate(data["stages"]):
        where = f"stages[{index}]"
        if not isinstance(stage, dict):
            raise ValueError(f"{where} must be an object")
        for key in ("id", "title", "time", "say", "see"):
            require_text(stage[key], f"{where}.{key}")
        if stage["id"] in stage_ids:
            raise ValueError(f"duplicate stage id: {stage['id']}")
        stage_ids.add(stage["id"])
        for key in ("actions", "send", "recovery", "prompt_ids"):
            require_list(stage[key], f"{where}.{key}")
        for item in stage["actions"]:
            require_text(item, f"{where}.actions item")
        for item in stage["prompt_ids"]:
            require_text(item, f"{where}.prompt_ids item")
            if item not in prompt_ids:
                raise ValueError(f"{where} refers to unknown prompt id: {item}")
        for item in stage["send"]:
            for key in ("label", "text"):
                require_text(item[key], f"{where}.send.{key}")
        for item in stage["recovery"]:
            for key in ("symptom", "action"):
                require_text(item[key], f"{where}.recovery.{key}")
    for index, source in enumerate(data["sources"]):
        require_text(source["label"], f"sources[{index}].label")
        url = require_text(source["url"], f"sources[{index}].url")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError(f"sources[{index}].url must be an HTTPS URL")
    share = urlparse(data["share_url"])
    if share.scheme != "https" or not share.netloc or share.username or share.password:
        raise ValueError("share_url must be an HTTPS URL")
    return data


CSS = r"""
:root{--paper:#f6f3e9;--card:#fffdf7;--ink:#20362f;--muted:#61716b;--green:#235a46;--green-dark:#173d31;--line:#d9dfd3;--sage:#e9f0e5;--accent:#d99b56;--shadow:0 14px 42px rgba(25,55,41,.08)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button,input{font:inherit}button{cursor:pointer}button:focus-visible,input:focus-visible,summary:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:3px}a{color:var(--green);text-underline-offset:.18em}.eyebrow{text-transform:uppercase;letter-spacing:.17em;font-size:.7rem;font-weight:800;color:var(--green)}h1,h2,h3,p{margin-top:0}h1,h2,.serif{font-family:Georgia,"Times New Roman",serif;font-weight:normal}h1{font-size:clamp(2.25rem,5vw,4.4rem);line-height:1.05;letter-spacing:-.045em;max-width:15ch;margin:.22em 0}h2{font-size:clamp(2rem,3vw,2.85rem);line-height:1.1;letter-spacing:-.03em;margin:.15em 0 .25em}h3{font-size:1.08rem;letter-spacing:.01em;margin:0 0 .55rem}small,.muted{color:var(--muted)}.masthead{border-bottom:1px solid var(--line);padding:2.1rem clamp(1.1rem,4vw,4rem) 1.5rem;background:radial-gradient(circle at 88% 5%,#e6eddd,transparent 32%),var(--paper)}.masthead-inner{max-width:1500px;margin:auto;display:flex;justify-content:space-between;gap:2rem;align-items:end}.subtitle{max-width:65ch;color:#43564d;font-size:1.08rem;margin:.8rem 0 0}.meta{text-align:right;min-width:12rem}.meta p{margin:.22rem 0}.pill{display:inline-block;border:1px solid #bdd0ba;border-radius:99px;padding:.25rem .7rem;background:#eff4ea;color:#345e48;font-size:.75rem;font-weight:700}.layout{max-width:1500px;margin:auto;display:grid;grid-template-columns:minmax(235px,290px) minmax(0,1fr);gap:clamp(1.2rem,3.2vw,3.4rem);padding:2rem clamp(1.1rem,4vw,4rem) 5rem}.rail{align-self:start;position:sticky;top:1rem}.rail-card,.setup,.stage,.foot-card{background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow)}.rail-card{padding:1.25rem}.rail-head{display:flex;justify-content:space-between;align-items:baseline;gap:.5rem}.progress-track{height:6px;background:#e4eade;border-radius:99px;overflow:hidden;margin:.8rem 0 1.2rem}.progress-bar{height:100%;width:0;background:var(--green);transition:width .2s}.stage-nav{list-style:none;padding:0;margin:0}.stage-nav li+li{border-top:1px solid var(--line)}.nav-button{border:0;background:none;text-align:left;width:100%;padding:.76rem .25rem;display:flex;gap:.75rem;align-items:start;color:var(--ink);border-radius:8px}.nav-button:hover,.nav-button[aria-current=step]{background:var(--sage)}.nav-number{font-size:.73rem;font-weight:800;background:#e9eee3;color:var(--green);border-radius:50%;height:1.7rem;min-width:1.7rem;display:grid;place-items:center}.nav-copy{flex:1}.nav-copy strong{display:block;font-size:.89rem;line-height:1.25}.nav-copy small{font-size:.72rem}.nav-done{color:var(--green);font-weight:bold}.rail-actions{margin-top:1rem;display:flex;gap:.4rem;flex-wrap:wrap}.text-button{border:0;background:none;color:var(--green);padding:.35rem .15rem;text-decoration:underline;text-underline-offset:.18em;font-size:.82rem}.main{min-width:0}.setup{padding:clamp(1.2rem,2.4vw,2rem);margin-bottom:1.2rem}.setup-header{display:flex;justify-content:space-between;gap:1rem;align-items:baseline;flex-wrap:wrap}.setup h3{font-family:Georgia,"Times New Roman",serif;font-size:1.5rem;font-weight:normal;margin:0}.setup-note{font-size:.84rem;color:var(--muted);margin:.45rem 0 1rem}.fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem}.field label{display:block;font-size:.76rem;font-weight:750;letter-spacing:.02em;margin-bottom:.3rem}.field input{width:100%;border:1px solid #cbd6c8;border-radius:9px;background:white;padding:.7rem .8rem;color:var(--ink);min-width:0}.field input[aria-invalid=true]{border-color:#ad604c;background:#fff9f5}.field .error{font-size:.72rem;color:#934b39;min-height:1.2em;margin:.22rem 0 0}.validation{font-size:.83rem;color:#52665b;margin:.5rem 0 0}.stage{padding:clamp(1.2rem,3vw,2.5rem);display:none}.stage.active{display:block}.stage-top{display:flex;justify-content:space-between;gap:1rem;align-items:start;border-bottom:1px solid var(--line);padding-bottom:1.25rem}.stage-time{white-space:nowrap;font-size:.76rem;font-weight:750;color:#3f6854;background:var(--sage);padding:.35rem .7rem;border-radius:99px}.stage-intro{color:var(--muted);font-size:.91rem}.stage-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1.5rem 2rem;margin:1.7rem 0}.block{min-width:0}.block.wide{grid-column:1/-1}.block-label{display:flex;align-items:center;gap:.5rem;color:var(--green);font-size:.7rem;text-transform:uppercase;letter-spacing:.13em;font-weight:800;margin-bottom:.65rem}.block-label:after{content:"";height:1px;background:var(--line);flex:1}.say{font-family:Georgia,"Times New Roman",serif;font-size:1.25rem;line-height:1.5;white-space:pre-wrap;margin:0}.see{font-size:.94rem;white-space:pre-wrap;margin:0}.action-list{padding-left:1.25rem;margin:.2rem 0}.action-list li{padding-left:.15rem;margin:.45rem 0}.send-list{display:grid;gap:.7rem}.send-card,.prompt-card{border:1px solid var(--line);border-radius:12px;background:#fafbf6;padding:.85rem 1rem}.send-card{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:.6rem 1rem}.send-card strong{font-size:.89rem}.button{border-radius:9px;border:1px solid var(--green);background:var(--green);color:white;padding:.59rem .9rem;font-weight:700;font-size:.8rem;white-space:nowrap;min-height:2.5rem}.button:hover{background:var(--green-dark)}.button.secondary{color:var(--green);background:transparent}.button.secondary:hover{background:var(--sage)}.button:disabled{opacity:.45;cursor:not-allowed}.prompt-card+ .prompt-card{margin-top:.7rem}.prompt-card summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:.7rem}.prompt-card summary::-webkit-details-marker{display:none}.prompt-card summary:before{content:"+";color:var(--green);font-size:1.3rem;line-height:1}.prompt-card[open] summary:before{content:"−"}.prompt-card summary strong{font-size:.9rem}.prompt-hint{font-size:.8rem;color:var(--muted);margin:.5rem 0 0 1.7rem}.prompt-body{white-space:pre-wrap;overflow-wrap:anywhere;background:white;border:1px solid var(--line);border-radius:8px;padding:1rem;font: .85rem/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;max-height:26rem;overflow:auto}.prompt-actions{display:flex;gap:.5rem;flex-wrap:wrap}.recovery details{border-top:1px solid var(--line);padding:.75rem 0}.recovery summary{cursor:pointer;color:var(--green);font-weight:700;font-size:.88rem}.recovery p{font-size:.88rem;margin:.6rem 0 0;white-space:pre-wrap}.stage-bottom{border-top:1px solid var(--line);padding-top:1.2rem;display:flex;gap:1rem;justify-content:space-between;align-items:center;flex-wrap:wrap}.complete{display:flex;align-items:center;gap:.55rem;font-size:.88rem;font-weight:700}.complete input{accent-color:var(--green);width:1.2rem;height:1.2rem}.stage-controls{display:flex;gap:.5rem}.foot-card{padding:1.3rem 1.5rem;margin-top:1.2rem}.foot-card h3{font-family:Georgia,"Times New Roman",serif;font-size:1.35rem;font-weight:normal}.source-list{padding-left:1.1rem;font-size:.85rem}.source-list li{margin:.3rem 0}.status{position:fixed;z-index:20;left:50%;bottom:1.2rem;transform:translateX(-50%);background:var(--ink);color:white;border-radius:10px;padding:.7rem 1rem;box-shadow:var(--shadow);font-size:.86rem;max-width:min(90vw,650px)}.status:empty{display:none}.fallback{position:fixed;z-index:30;inset:0;background:rgba(20,40,31,.54);display:grid;place-items:center;padding:1rem}.fallback[hidden]{display:none}.fallback-panel{background:var(--card);border-radius:14px;padding:1.4rem;width:min(700px,100%);max-height:90vh;display:flex;flex-direction:column}.fallback-panel h3{font-family:Georgia,"Times New Roman",serif;font-weight:normal;font-size:1.5rem}.fallback textarea{width:100%;min-height:15rem;resize:vertical;font:.86rem/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;border:1px solid var(--line);border-radius:8px;padding:.8rem;flex:1}.fallback .button{align-self:end;margin-top:.8rem}.print-note{display:none}.send-text{grid-column:1/-1;white-space:pre-wrap;overflow-wrap:anywhere;background:white;border:1px solid var(--line);border-radius:7px;padding:.7rem;margin:0;color:#40564a;font:.78rem/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media(max-width:850px){.layout{grid-template-columns:1fr;gap:1rem;padding-top:1rem}.rail{position:static}.rail-card{padding:1rem}.stage-nav{display:flex;overflow-x:auto;gap:.5rem;padding-bottom:.2rem}.stage-nav li{border:0!important;min-width:10rem}.nav-button{padding:.55rem}.fields{grid-template-columns:1fr 1fr}.masthead-inner{align-items:start}.meta{font-size:.8rem}.stage-grid{gap:1.2rem}}
@media(max-width:600px){.masthead-inner{display:block}.meta{text-align:left;margin-top:1rem}.fields,.stage-grid{grid-template-columns:1fr}.block.wide{grid-column:auto}.stage-top{display:block}.stage-time{display:inline-block;margin-top:.5rem}.send-card{grid-template-columns:1fr}.send-card .button{justify-self:start}.stage-bottom{align-items:start;flex-direction:column}.stage-controls{width:100%}.stage-controls .button{flex:1}}
@media print{*{box-shadow:none!important}body{background:white;color:black;font-size:10pt}.masthead,.layout{padding:0}.masthead{border:0}.masthead-inner{display:block}.meta{text-align:left}.layout{display:block}.rail,.setup,.stage-bottom,.status,.fallback,.prompt-actions,.send-card .button{display:none!important}.stage{display:block!important;border:0;border-top:1px solid #999;border-radius:0;padding:1.2rem 0;break-inside:avoid}.stage-grid{display:block;margin:1rem 0}.block{margin:.8rem 0}.block-label{color:black}.prompt-card,.send-card{background:white}.send-card{display:block}.send-text{display:block;white-space:pre-wrap;overflow-wrap:anywhere;margin:.4rem 0 0;font:8pt/1.4 ui-monospace,monospace}.prompt-card{break-inside:avoid}.prompt-card .prompt-body{display:block;max-height:none;overflow:visible;white-space:pre-wrap}.prompt-card:not([open]) .prompt-body,.prompt-card:not([open]) .prompt-hint{display:block}.prompt-card summary:before{display:none}.recovery details>*{display:block}.recovery details p{display:block!important}.foot-card{border:0;padding:0;margin:1rem 0}.print-note{display:block;font-size:.8rem} .source-list a,.meta a{color:black;text-decoration:none}.source-list a:after,.meta a:after{content:" (" attr(href) ")";font-size:.75em;overflow-wrap:anywhere}h1{font-size:28pt}h2{font-size:21pt}.stage{page-break-inside:avoid}}
"""


CSS += "\n@media screen and (min-width:851px){.rail{max-height:calc(100vh - 2rem);overflow-y:auto}}\n"

JS = r"""
(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('guide-data').textContent);
  const byId = id => document.getElementById(id);
  byId('guide-title').textContent = data.title;
  byId('guide-subtitle').textContent = data.subtitle;
  byId('version').textContent = 'Version ' + data.version;
  byId('base-sha').textContent = 'Template ' + data.base_sha;
  byId('share-link').href = data.share_url;
  document.title = data.title + ' · facilitator guide';
  const state = { index: 0, done: {}, storage: false };
  const key = 'itsadoor-facilitator-progress-v1';
  const fields = { HANDLE: byId('handle'), VAULT_REPO: byId('vault-repo') };
  const labels = { HANDLE: 'GitHub handle', VAULT_REPO: 'vault repository name' };
  const tokenRe = /\{\{(HANDLE|VAULT_REPO)\}\}/g;
  let statusTimer;
  let fallbackReturnFocus = null;
  try { const saved = JSON.parse(localStorage.getItem(key) || '{}'); if (saved && typeof saved === 'object' && !Array.isArray(saved)) state.done = saved; state.storage = true; } catch (_) { state.done = {}; }
  function el(tag, cls, content) { const node = document.createElement(tag); if (cls) node.className = cls; if (content !== undefined) node.textContent = content; return node; }
  function validate(name) {
    const value = fields[name].value.trim();
    if (!value) return 'Enter ' + labels[name] + ' to use this text.';
    if (name === 'HANDLE' && (value.length > 39 || !/^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$/.test(value))) return 'Use 1–39 letters or numbers, with single internal hyphens.';
    if (name !== 'HANDLE' && !/^[A-Za-z0-9._-]{1,100}$/.test(value)) return 'Use 1–100 letters, numbers, periods, underscores, or hyphens.';
    if (name !== 'HANDLE' && (value === '.' || value === '..' || value.endsWith('.git'))) return 'Enter the repository name without .git.';
    return '';
  }
  function required(text) { return [...new Set([...text.matchAll(tokenRe)].map(match => match[1]))]; }
  function resolved(text) {
    const missing = required(text).filter(name => validate(name));
    if (missing.length) return { error: 'Fill in a valid ' + missing.map(name => labels[name]).join(', ') + ' before copying.' };
    return { text: text.replace(tokenRe, (_, name) => fields[name].value.trim()) };
  }
  function preview(text) { return text.replace(tokenRe, (token, name) => validate(name) ? token : fields[name].value.trim()); }
  function updateFields() {
    const stage = data.stages[state.index];
    const promptText = stage.prompt_ids.map(id => data.prompts.find(item => item.id === id).body).join('\n');
    const needed = [...new Set(required(stage.send.map(item => item.text).join('\n') + promptText))];
    for (const [name, input] of Object.entries(fields)) {
      const error = validate(name);
      const show = needed.includes(name) || !!input.value.trim();
      input.setAttribute('aria-invalid', show && error ? 'true' : 'false');
      byId(name.toLowerCase().replace('_', '-') + '-error').textContent = show ? error : '';
    }
    const missing = needed.filter(name => validate(name));
    byId('validation').textContent = missing.length ? 'This step needs a valid ' + missing.map(name => labels[name]).join(', ') + ' before its text can be copied.' : 'The values used by this step are ready.';
    document.querySelectorAll('[data-preview]').forEach(node => { node.textContent = preview(node.dataset.preview); });
    document.querySelectorAll('[data-copy]').forEach(button => {
      const missing = required(button.dataset.copy).filter(name => validate(name));
      button.title = missing.length ? 'Needs valid ' + missing.map(name => labels[name]).join(', ') : '';
      button.setAttribute('aria-disabled', missing.length ? 'true' : 'false');
    });
  }
  function announce(message) {
    const status = byId('status'); status.textContent = message;
    clearTimeout(statusTimer); statusTimer = setTimeout(() => { status.textContent = ''; }, 5500);
  }
  function showFallback(text) {
    const box = byId('fallback'); const area = byId('fallback-text');
    fallbackReturnFocus = document.activeElement;
    area.value = text; box.hidden = false; area.focus(); area.select();
  }
  function closeFallback() { byId('fallback').hidden = true; if (fallbackReturnFocus && fallbackReturnFocus.focus) fallbackReturnFocus.focus(); }
  async function copy(text, label) {
    const result = resolved(text);
    if (result.error) { announce(result.error); return; }
    try { if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard API unavailable'); await navigator.clipboard.writeText(result.text); announce(label + ' copied.'); return; } catch (_) {}
    const area = document.createElement('textarea'); area.value = result.text; area.style.position = 'fixed'; area.style.opacity = '0'; document.body.append(area); area.select();
    let worked = false; try { worked = document.execCommand('copy'); } catch (_) {} area.remove();
    if (worked) announce(label + ' copied.'); else { showFallback(result.text); announce('Clipboard access failed. Select and copy the text shown.'); }
  }
  function download(text, filename) {
    const result = resolved(text);
    if (result.error) { announce(result.error); return; }
    try {
      const url = URL.createObjectURL(new Blob([result.text], { type: 'text/markdown;charset=utf-8' }));
      const link = el('a'); link.href = url; link.download = filename; document.body.append(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1500); announce('Prompt download started.');
    } catch (_) { showFallback(result.text); announce('Download failed. Select and save the text shown.'); }
  }
  function button(label, cls, action) { const node = el('button', cls, label); node.type = 'button'; node.addEventListener('click', action); return node; }
  function block(label, wide = false) { const node = el('section', 'block' + (wide ? ' wide' : '')); node.append(el('div', 'block-label', label)); return node; }
  function stageNode(stage, index) {
    const article = el('article', 'stage'); article.id = 'stage-' + index; article.setAttribute('aria-labelledby', 'stage-title-' + index);
    const top = el('div', 'stage-top'); const titleBox = el('div'); titleBox.append(el('div', 'eyebrow', 'Step ' + String(index + 1).padStart(2, '0') + ' / ' + String(data.stages.length).padStart(2, '0')));
    const title = el('h2', '', stage.title); title.id = 'stage-title-' + index; title.tabIndex = -1; titleBox.append(title); top.append(titleBox, el('span', 'stage-time', stage.time)); article.append(top);
    const grid = el('div', 'stage-grid');
    const say = block('Say'); say.append(el('p', 'say', stage.say)); grid.append(say);
    const acts = block('Guide the steps'); const list = el('ol', 'action-list'); stage.actions.forEach(action => list.append(el('li', '', action))); acts.append(list); grid.append(acts);
    const see = block('Look for'); see.append(el('p', 'see', stage.see)); grid.append(see);
    if (stage.send.length) {
      const send = block('Send or copy'); const cards = el('div', 'send-list');
      stage.send.forEach(item => { const card = el('div', 'send-card'); const strong = el('strong', '', item.label); const copyButton = button('Copy message', 'button secondary', () => copy(item.text, item.label)); copyButton.dataset.copy = item.text; const printText = el('pre', 'send-text', item.text); printText.dataset.preview = item.text; card.append(strong, copyButton, printText); cards.append(card); });
      send.append(cards); grid.append(send);
    }
    if (stage.prompt_ids.length) {
      const prompts = block('Prompts', true);
      stage.prompt_ids.forEach(id => {
        const prompt = data.prompts.find(item => item.id === id); const details = el('details', 'prompt-card');
        const summary = el('summary'); summary.append(el('strong', '', prompt.title)); details.append(summary);
        if (prompt.hint) details.append(el('p', 'prompt-hint', prompt.hint));
        const body = el('pre', 'prompt-body'); body.dataset.preview = prompt.body; body.textContent = preview(prompt.body); details.append(body);
        const actions = el('div', 'prompt-actions'); const copyButton = button('Copy full prompt', 'button', () => copy(prompt.body, prompt.title)); copyButton.dataset.copy = prompt.body;
        const filename = prompt.file.split('/').pop() || 'prompt.md'; const downloadButton = button('Download .md', 'button secondary', () => download(prompt.body, filename)); downloadButton.dataset.copy = prompt.body;
        actions.append(copyButton, downloadButton); details.append(actions); prompts.append(details);
      }); grid.append(prompts);
    }
    if (stage.recovery.length) {
      const recover = block('If something goes wrong', true); recover.classList.add('recovery');
      stage.recovery.forEach(item => { const details = el('details'); details.append(el('summary', '', item.symptom), el('p', '', item.action)); recover.append(details); }); grid.append(recover);
    }
    article.append(grid);
    const bottom = el('div', 'stage-bottom'); const complete = el('label', 'complete'); const checkbox = el('input'); checkbox.type = 'checkbox'; checkbox.checked = !!state.done[stage.id]; checkbox.addEventListener('change', () => { state.done[stage.id] = checkbox.checked; if (state.storage) { try { localStorage.setItem(key, JSON.stringify(state.done)); } catch (_) { state.storage = false; } } updateProgress(); }); complete.append(checkbox, document.createTextNode('Mark this step complete'));
    const controls = el('div', 'stage-controls'); const back = button('← Back', 'button secondary', () => select(index - 1)); back.disabled = index === 0; const next = button(index === data.stages.length - 1 ? 'Back to first' : 'Next step →', 'button', () => select(index === data.stages.length - 1 ? 0 : index + 1)); controls.append(back, next); bottom.append(complete, controls); article.append(bottom);
    return article;
  }
  function updateProgress() {
    const count = data.stages.filter(stage => !!state.done[stage.id]).length;
    byId('progress-count').textContent = count + ' / ' + data.stages.length;
    byId('progress-bar').style.width = (count / data.stages.length * 100) + '%';
    document.querySelectorAll('.nav-done').forEach((node, index) => { node.textContent = state.done[data.stages[index].id] ? '✓' : ''; });
  }
  function select(index, scroll = true) {
    if (index < 0 || index >= data.stages.length) return;
    state.index = index;
    document.querySelectorAll('.stage').forEach((node, i) => { const active = i === index; node.classList.toggle('active', active); node.setAttribute('aria-hidden', active ? 'false' : 'true'); });
    document.querySelectorAll('.nav-button').forEach((node, i) => { if (i === index) node.setAttribute('aria-current', 'step'); else node.removeAttribute('aria-current'); });
    updateFields();
    if (scroll) { byId('stage-' + index).scrollIntoView({ block: 'start', behavior: 'smooth' }); byId('stage-title-' + index).focus({ preventScroll: true }); }
  }
  data.stages.forEach((stage, index) => {
    const li = el('li'); const nav = button('', 'nav-button', () => select(index)); nav.append(el('span', 'nav-number', String(index + 1).padStart(2, '0')));
    const copy = el('span', 'nav-copy'); copy.append(el('strong', '', stage.title), el('small', '', stage.time)); nav.append(copy, el('span', 'nav-done')); li.append(nav); byId('stage-nav').append(li);
    byId('stages').append(stageNode(stage, index));
  });
  data.sources.forEach(source => { const li = el('li'); const link = el('a', '', source.label); link.href = source.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; li.append(link); byId('sources').append(li); });
  for (const input of Object.values(fields)) input.addEventListener('input', updateFields);
  byId('print-guide').addEventListener('click', () => window.print());
  byId('new-call').addEventListener('click', () => { for (const input of Object.values(fields)) input.value = ''; state.done = {}; if (state.storage) { try { localStorage.removeItem(key); } catch (_) {} } document.querySelectorAll('.complete input').forEach(node => { node.checked = false; }); updateFields(); updateProgress(); select(0); announce('New call started. Progress and fields cleared.'); });
  byId('fallback-close').addEventListener('click', closeFallback);
  byId('fallback').addEventListener('click', event => { if (event.target === byId('fallback')) closeFallback(); });
  document.addEventListener('keydown', event => {
    if (byId('fallback').hidden) return;
    if (event.key === 'Escape') { closeFallback(); return; }
    if (event.key === 'Tab') { event.preventDefault(); (document.activeElement === byId('fallback-text') ? byId('fallback-close') : byId('fallback-text')).focus(); }
  });
  let printOpen = [];
  window.addEventListener('beforeprint', () => { printOpen = [...document.querySelectorAll('.prompt-card:not([open]), .recovery details:not([open])')]; printOpen.forEach(node => { node.open = true; }); });
  window.addEventListener('afterprint', () => { printOpen.forEach(node => { node.open = false; }); printOpen = []; });
  updateFields(); updateProgress(); select(0, false);
})();
"""


def render(data: dict) -> str:
    # Escaping '<' keeps content from closing the JSON script element. The UI uses
    # textContent for all authored prose, so content is never parsed as HTML.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    title = "Offline facilitator guide"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<header class="masthead"><div class="masthead-inner"><div><div class="eyebrow">A calm, practical walkthrough</div><h1 id="guide-title"></h1><p class="subtitle" id="guide-subtitle"></p></div><div class="meta"><span class="pill">Offline ready</span><p id="version"></p><p id="base-sha"></p><p><a id="share-link" target="_blank" rel="noopener noreferrer">Open share page ↗</a></p></div></div></header>
<div class="layout">
<aside class="rail" aria-label="Guide steps"><div class="rail-card"><div class="rail-head"><span class="eyebrow">The call</span><strong id="progress-count">0 / 0</strong></div><div class="progress-track" role="presentation"><div id="progress-bar" class="progress-bar"></div></div><ol id="stage-nav" class="stage-nav"></ol><div class="rail-actions"><button id="new-call" type="button" class="text-button">Start a new call · clear progress</button><button id="print-guide" type="button" class="button secondary">Print guide</button></div></div></aside>
<main class="main"><section class="setup" aria-labelledby="setup-title"><div class="setup-header"><h3 id="setup-title">Names for this call</h3><span class="eyebrow">Kept on this page only</span></div><p class="setup-note">Enter these as your friend confirms them. They are used only when preparing a message or prompt. Progress checkmarks may be saved in this browser; these names are never saved.</p><div class="fields"><div class="field"><label for="handle">GitHub handle</label><input id="handle" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="friend-handle" aria-describedby="handle-error"><p class="error" id="handle-error"></p></div><div class="field"><label for="vault-repo">Vault repository name</label><input id="vault-repo" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="name-second-brain" aria-describedby="vault-repo-error"><p class="error" id="vault-repo-error"></p></div></div><p id="validation" class="validation" aria-live="polite"></p></section><div id="stages"></div><section class="foot-card" aria-labelledby="sources-title"><h3 id="sources-title">Reference links</h3><ul id="sources" class="source-list"></ul><p class="print-note">Printed from the offline guide. Prompts are included in full; replace any remaining brace placeholders with the names from your call.</p></section></main>
</div>
<div id="status" class="status" role="status" aria-live="polite"></div>
<div id="fallback" class="fallback" hidden><div class="fallback-panel" role="dialog" aria-modal="true" aria-labelledby="fallback-title"><h3 id="fallback-title">Copy this text manually</h3><p>Clipboard access is unavailable here. The text is selected; press Copy on your keyboard.</p><textarea id="fallback-text" readonly></textarea><button id="fallback-close" type="button" class="button secondary">Close</button></div></div>
<script id="guide-data" type="application/json">{payload}</script>
<script>{JS}</script>
</body></html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, default=HERE / "content.json")
    parser.add_argument("--output", type=Path, default=HERE / "meet.html")
    args = parser.parse_args()
    data = read_content(args.content.resolve())
    args.output.write_text(render(data), encoding="utf-8")
    print(f"Built {args.output} from {args.content}")


if __name__ == "__main__":
    main()
