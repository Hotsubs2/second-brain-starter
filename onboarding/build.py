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
        live = stage.get("live")
        if not isinstance(live, dict):
            raise ValueError(f"{where}.live must be an object")
        for key in ("purpose", "transition"):
            if not require_text(live.get(key), f"{where}.live.{key}").strip():
                raise ValueError(f"{where}.live.{key} must not be empty")
        steps = require_list(live.get("steps"), f"{where}.live.steps")
        if not 2 <= len(steps) <= 6:
            raise ValueError(f"{where}.live.steps must contain 2–6 steps")
        for step_index, step in enumerate(steps):
            if not isinstance(step, dict):
                raise ValueError(f"{where}.live.steps[{step_index}] must be an object")
            for key in ("say", "action", "see"):
                if not require_text(step.get(key), f"{where}.live.steps[{step_index}].{key}").strip():
                    raise ValueError(f"{where}.live.steps[{step_index}].{key} must not be empty")
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
CSS += r"""
.masthead{padding:.85rem clamp(1rem,3vw,2.4rem)}.masthead-inner{align-items:center}.masthead h1{font-size:clamp(1.45rem,2.4vw,2.15rem);max-width:none;letter-spacing:-.025em;margin:.06em 0}.masthead .subtitle{font-size:.85rem;margin:.12rem 0 0}.masthead .meta{font-size:.74rem}.masthead .meta p{margin:.08rem 0}.layout{padding:1rem clamp(1rem,3vw,2.4rem) 4rem;gap:clamp(1rem,2.4vw,2rem)}.setup{padding:0;margin-bottom:.85rem}.setup summary{cursor:pointer;padding:.8rem 1rem;color:var(--green);font-weight:750}.setup-content{padding:0 1rem 1rem}.setup-note{margin:.1rem 0 .8rem}.stage{padding:clamp(1rem,2.2vw,1.8rem)}.stage-top{padding-bottom:.75rem}.stage-top h2{font-size:clamp(1.7rem,2.8vw,2.35rem)}.stage-purpose{margin:1rem 0;color:#405b4b;font-size:1rem}.call-orientation{background:#edf3e9;border-left:4px solid var(--green);padding:.75rem 1rem;margin:1rem 0;border-radius:0 9px 9px 0}.call-orientation p{margin:.25rem 0}.live-card{background:#f7faf5;border:1px solid #cbdcc9;border-radius:14px;padding:clamp(1rem,2vw,1.6rem);margin:1rem 0}.live-card .eyebrow{margin-bottom:.25rem}.microstep[hidden]{display:none}.microstep-title{font-size:1.25rem;font-family:Georgia,"Times New Roman",serif;margin:0 0 1rem}.live-row{padding:.8rem 0;border-top:1px solid var(--line)}.live-row:first-of-type{border-top:0}.live-row h4{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;color:var(--green);margin:0 0 .3rem}.live-row p{font-size:1.02rem;line-height:1.5;white-space:pre-wrap;margin:0}.live-row.say-row p{font:1.19rem/1.5 Georgia,"Times New Roman",serif}.live-row.see-row{background:#e9f1e7;border-radius:9px;border:0;padding:.75rem;margin-top:.7rem}.transition{border-top:1px solid var(--line);margin-top:1rem;padding-top:.8rem}.transition strong{color:var(--green);font-size:.75rem;letter-spacing:.1em;text-transform:uppercase}.transition p{margin:.25rem 0 0}.micro-controls{display:flex;justify-content:space-between;gap:.6rem;margin-top:1.15rem}.micro-controls .button:last-child{margin-left:auto}.utility-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin-top:1rem}.utility-card,.full-notes{border:1px solid var(--line);border-radius:12px;background:#fafbf6;padding:.75rem 1rem}.utility-card>summary,.full-notes>summary{cursor:pointer;color:var(--green);font-weight:750}.utility-card[open],.full-notes[open]{background:var(--card)}.full-notes{margin-top:.75rem}.full-notes .stage-grid{display:block;margin:.8rem 0 0}.full-notes .block{margin:.8rem 0}.full-notes .block-label{margin-bottom:.35rem}.full-notes .say{font-size:1rem}.full-notes .action-list{font-size:.9rem}.full-notes .see{font-size:.9rem}.send-list{margin-top:.75rem}.send-card{grid-template-columns:minmax(0,1fr) auto}.send-card details{grid-column:1/-1}.send-card details summary{color:var(--green);cursor:pointer;font-size:.8rem}.send-text{max-height:11rem;overflow:auto}.prompt-card{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.4rem .6rem;align-items:start;margin:.65rem 0}.prompt-card details{min-width:0}.prompt-card .prompt-hint{margin:.25rem 0}.prompt-card .prompt-body{max-height:16rem}.prompt-card .prompt-actions{grid-column:1/-1}.prompt-card .button{padding:.4rem .6rem;min-height:2rem}.stage-bottom{margin-top:1rem;padding-top:.8rem}.complete{font-size:.8rem}.stage-intro{font-size:.85rem}.foot-card{margin-top:.85rem}
@media(max-width:1000px){.utility-grid{grid-template-columns:1fr}}
@media(max-width:850px){.masthead{padding:.8rem 1rem}.masthead .meta{display:none}.rail-card{padding:.65rem .9rem}.rail-head,.progress-track,.rail-actions{display:none}.stage-nav li{min-width:9rem}.layout{gap:.7rem}.stage{padding:1rem}}
@media(max-width:600px){.masthead .subtitle{display:none}.micro-controls .button{white-space:normal}.live-row p{font-size:.96rem}.live-row.say-row p{font-size:1.08rem}}
.layout,.rail,.rail-card,.main,.setup,.stage,.live-card,.microstep,.utility-card,.full-notes{min-width:0;max-width:100%}.stage-purpose,.microstep-title,.live-row p,.transition p,.action-list li,.recovery p{overflow-wrap:anywhere}.stage-nav{max-width:100%}.stage-top>div{min-width:0}.micro-controls{min-width:0;flex-wrap:wrap}.micro-controls .button{max-width:100%}.prompt-card,.send-card{min-width:0}.prompt-card details,.send-card details{min-width:0;max-width:100%}.prompt-body,.send-text{max-width:100%;overflow-wrap:anywhere;white-space:pre-wrap}
@media(max-width:850px){.layout{grid-template-columns:minmax(0,1fr)}.rail{width:100%;overflow:hidden}.rail-card{width:100%;overflow:hidden}.stage-nav{width:100%;overflow-x:auto;overscroll-behavior-inline:contain}.stage-nav li{flex:0 0 9rem}.rail-actions{display:flex;margin-top:.35rem}.rail-actions .button{min-height:2rem;padding:.3rem .6rem}.main{width:100%}.masthead .meta{display:block;min-width:0;white-space:nowrap}.masthead .meta .pill,.masthead .meta #version,.masthead .meta #base-sha{display:none}}
@media(max-width:600px){.masthead .meta{text-align:left;margin:.2rem 0 0}}
@media print{.masthead .meta,.masthead .meta .pill,.masthead .meta #version,.masthead .meta #base-sha{display:block}.setup{display:none!important}.stage{display:block!important}.microstep[hidden]{display:block!important}.live-card{border:0;padding:0;margin:.4rem 0}.microstep{break-inside:avoid;border-top:1px solid #aaa;padding:.6rem 0}.micro-controls{display:none}.utility-grid{display:block}.utility-card,.full-notes{break-inside:auto;border:0;padding:0}.utility-card>summary,.full-notes>summary{font-size:12pt}.utility-card details>*{display:block}.send-card details .send-text{max-height:none;overflow:visible}.prompt-card{display:block}.prompt-card details .prompt-body{max-height:none;overflow:visible}.prompt-actions{display:none}.call-orientation{border:1px solid #aaa;background:white}.transition{break-inside:avoid}.live-row.see-row{background:white;border:1px solid #aaa}}
"""

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
  const state = { index: 0, micro: 0, done: {}, storage: false };
  const key = 'itsadoor-facilitator-progress-v2';
  const fields = { HANDLE: byId('handle'), VAULT_REPO: byId('vault-repo') };
  const labels = { HANDLE: 'GitHub handle', VAULT_REPO: 'vault repository name' };
  const tokenRe = /\{\{(HANDLE|VAULT_REPO)\}\}/g;
  let statusTimer;
  let fallbackReturnFocus = null;
  try {
    const saved = JSON.parse(localStorage.getItem(key) || '{}');
    if (saved && typeof saved === 'object' && !Array.isArray(saved)) {
      if (saved.done && typeof saved.done === 'object' && !Array.isArray(saved.done)) state.done = saved.done;
      if (Number.isInteger(saved.index) && saved.index >= 0 && saved.index < data.stages.length) state.index = saved.index;
      if (Number.isInteger(saved.micro) && saved.micro >= 0 && saved.micro < data.stages[state.index].live.steps.length) state.micro = saved.micro;
    }
    state.storage = true;
  } catch (_) { state.done = {}; }
  function persist() { if (state.storage) { try { localStorage.setItem(key, JSON.stringify({ index: state.index, micro: state.micro, done: state.done })); } catch (_) { state.storage = false; } } }
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
  function askForFields(text, message) {
    byId('setup-title').parentElement.open = true;
    const first = required(text).find(name => validate(name));
    if (first) fields[first].focus();
    announce(message);
  }
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
      if (!button.dataset.readyLabel) button.dataset.readyLabel = button.textContent;
      button.textContent = missing.length ? 'Add notebook details' : button.dataset.readyLabel;
      button.title = missing.length ? 'Open Names for this call to add ' + missing.map(name => labels[name]).join(', ') : '';
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
    if (result.error) { askForFields(text, result.error); return; }
    try { if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard API unavailable'); await navigator.clipboard.writeText(result.text); announce(label + ' copied.'); return; } catch (_) {}
    const area = document.createElement('textarea'); area.value = result.text; area.style.position = 'fixed'; area.style.opacity = '0'; document.body.append(area); area.select();
    let worked = false; try { worked = document.execCommand('copy'); } catch (_) {} area.remove();
    if (worked) announce(label + ' copied.'); else { showFallback(result.text); announce('Clipboard access failed. Select and copy the text shown.'); }
  }
  function download(text, filename) {
    const result = resolved(text);
    if (result.error) { askForFields(text, result.error); return; }
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
    article.append(el('p', 'stage-purpose', stage.live.purpose));
    if (index === 0) {
      const orientation = el('aside', 'call-orientation');
      orientation.append(el('strong', '', 'Before you begin'), el('p', '', 'Have Google Meet, this guide, the participant guide, the starter repository, and their chosen AI ready. Your friend controls their own screen. Keep the final 25 minutes for project work, the contribution, and a clear handoff; switch to the browser route if one setup issue takes five minutes.'));
      article.append(orientation);
    }
    const live = el('section', 'live-card'); live.setAttribute('aria-label', 'Live guide for ' + stage.title);
    stage.live.steps.forEach((step, stepIndex) => {
      const panel = el('div', 'microstep'); panel.dataset.micro = stepIndex;
      panel.append(el('div', 'eyebrow', 'Live guide · ' + (stepIndex + 1) + ' of ' + stage.live.steps.length));
      const heading = el('h3', 'microstep-title', stage.title + ' · ' + (stepIndex + 1)); heading.tabIndex = -1; panel.append(heading);
      for (const [label, key, cls] of [['Say this', 'say', 'say-row'], ['Guide this action', 'action', 'action-row'], ['Wait until you see', 'see', 'see-row']]) {
        const row = el('div', 'live-row ' + cls); row.append(el('h4', '', label), el('p', '', step[key])); panel.append(row);
      }
      if (stepIndex === stage.live.steps.length - 1) { const transition = el('div', 'transition'); transition.append(el('strong', '', 'Before the next stage'), el('p', '', stage.live.transition)); panel.append(transition); }
      const controls = el('div', 'micro-controls');
      const back = button('← Back', 'button secondary', () => stepIndex ? select(index, stepIndex - 1) : select(index - 1, data.stages[index - 1].live.steps.length - 1)); back.disabled = index === 0 && stepIndex === 0;
      const last = stepIndex === stage.live.steps.length - 1;
      const next = button(last ? (index === data.stages.length - 1 ? 'Finish guide' : 'Next stage →') : 'Next →', 'button', () => { if (last) { if (index < data.stages.length - 1) select(index + 1, 0); else announce('You reached the final step. Check the handoff and mark this stage complete when it is done.'); } else select(index, stepIndex + 1); });
      controls.append(back, next); panel.append(controls); live.append(panel);
    });
    article.append(live);
    const utilities = el('div', 'utility-grid');
    if (stage.recovery.length) {
      const stuck = el('details', 'utility-card recovery'); stuck.append(el('summary', '', 'Stuck? Open recovery options'));
      stage.recovery.forEach(item => { const details = el('details'); details.append(el('summary', '', item.symptom), el('p', '', item.action)); stuck.append(details); }); utilities.append(stuck);
    }
    if (stage.send.length) {
      const send = el('details', 'utility-card'); send.open = true; send.append(el('summary', '', 'Send or copy')); const cards = el('div', 'send-list');
      stage.send.forEach(item => { const card = el('div', 'send-card'); const strong = el('strong', '', item.label); const copyButton = button('Copy', 'button secondary', () => copy(item.text, item.label)); copyButton.dataset.copy = item.text; const details = el('details'); details.append(el('summary', '', 'View full text')); const printText = el('pre', 'send-text', item.text); printText.dataset.preview = item.text; details.append(printText); card.append(strong, copyButton, details); cards.append(card); });
      send.append(cards); utilities.append(send);
    }
    if (stage.prompt_ids.length) {
      const prompts = el('details', 'utility-card'); prompts.open = true; prompts.append(el('summary', '', 'Prompts for this stage'));
      stage.prompt_ids.forEach(id => {
        const prompt = data.prompts.find(item => item.id === id); const card = el('div', 'prompt-card'); const details = el('details');
        const summary = el('summary'); summary.append(el('strong', '', prompt.title)); details.append(summary);
        if (prompt.hint) details.append(el('p', 'prompt-hint', prompt.hint));
        const body = el('pre', 'prompt-body'); body.dataset.preview = prompt.body; body.textContent = preview(prompt.body); details.append(body);
        const copyButton = button('Copy prompt', 'button', () => copy(prompt.body, prompt.title)); copyButton.dataset.copy = prompt.body;
        const filename = prompt.file.split('/').pop() || 'prompt.md'; const downloadButton = button('Download .md', 'button secondary', () => download(prompt.body, filename)); downloadButton.dataset.copy = prompt.body;
        const actions = el('div', 'prompt-actions'); actions.append(downloadButton); card.append(details, copyButton, actions); prompts.append(card);
      }); utilities.append(prompts);
    }
    article.append(utilities);
    const notes = el('details', 'full-notes'); notes.append(el('summary', '', 'Full stage notes'));
    const grid = el('div', 'stage-grid');
    const say = block('Stage opener'); say.append(el('p', 'say', stage.say)); grid.append(say);
    const acts = block('Full action list'); const list = el('ol', 'action-list'); stage.actions.forEach(action => list.append(el('li', '', action))); acts.append(list); grid.append(acts);
    const see = block('Stage result'); see.append(el('p', 'see', stage.see)); grid.append(see); notes.append(grid); article.append(notes);
    const bottom = el('div', 'stage-bottom'); const complete = el('label', 'complete'); const checkbox = el('input'); checkbox.type = 'checkbox'; checkbox.checked = !!state.done[stage.id]; checkbox.addEventListener('change', () => { state.done[stage.id] = checkbox.checked; persist(); updateProgress(); }); complete.append(checkbox, document.createTextNode('Mark stage complete after you verify it')); bottom.append(complete); article.append(bottom);
    return article;
  }
  function updateProgress() {
    const count = data.stages.filter(stage => !!state.done[stage.id]).length;
    byId('progress-count').textContent = count + ' / ' + data.stages.length;
    byId('progress-bar').style.width = (count / data.stages.length * 100) + '%';
    document.querySelectorAll('.nav-done').forEach((node, index) => { node.textContent = state.done[data.stages[index].id] ? '✓' : ''; });
  }
  function select(index, micro = 0, scroll = true, save = true) {
    if (index < 0 || index >= data.stages.length) return;
    if (micro < 0 || micro >= data.stages[index].live.steps.length) return;
    state.index = index; state.micro = micro;
    document.querySelectorAll('.stage').forEach((node, i) => { const active = i === index; node.classList.toggle('active', active); node.setAttribute('aria-hidden', active ? 'false' : 'true'); });
    document.querySelectorAll('.nav-button').forEach((node, i) => { if (i === index) node.setAttribute('aria-current', 'step'); else node.removeAttribute('aria-current'); });
    document.querySelectorAll('.microstep').forEach(node => { node.hidden = Number(node.dataset.micro) !== micro || !node.closest('.stage').classList.contains('active'); });
    updateFields();
    if (save) persist();
    if (scroll) {
      document.querySelectorAll('.nav-button')[index].scrollIntoView({ block: 'nearest', inline: 'nearest' });
      byId('stage-' + index).scrollIntoView({ block: 'start', behavior: 'smooth' });
      const heading = byId('stage-' + index).querySelector('.microstep:not([hidden]) .microstep-title'); heading.focus({ preventScroll: true });
    }
  }
  data.stages.forEach((stage, index) => {
    const li = el('li'); const nav = button('', 'nav-button', () => select(index)); nav.append(el('span', 'nav-number', String(index + 1).padStart(2, '0')));
    const copy = el('span', 'nav-copy'); copy.append(el('strong', '', stage.title), el('small', '', stage.time)); nav.append(copy, el('span', 'nav-done')); li.append(nav); byId('stage-nav').append(li);
    byId('stages').append(stageNode(stage, index));
  });
  data.sources.forEach(source => { const li = el('li'); const link = el('a', '', source.label); link.href = source.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; li.append(link); byId('sources').append(li); });
  for (const input of Object.values(fields)) input.addEventListener('input', updateFields);
  byId('print-guide').addEventListener('click', () => window.print());
  byId('new-call').addEventListener('click', () => { for (const input of Object.values(fields)) input.value = ''; state.done = {}; state.index = 0; state.micro = 0; if (state.storage) { try { localStorage.removeItem(key); } catch (_) {} } document.querySelectorAll('.complete input').forEach(node => { node.checked = false; }); updateFields(); updateProgress(); select(0, 0, true, false); announce('New call started. Progress, place, and fields cleared.'); });
  byId('fallback-close').addEventListener('click', closeFallback);
  byId('fallback').addEventListener('click', event => { if (event.target === byId('fallback')) closeFallback(); });
  document.addEventListener('keydown', event => {
    if (byId('fallback').hidden) return;
    if (event.key === 'Escape') { closeFallback(); return; }
    if (event.key === 'Tab') { event.preventDefault(); (document.activeElement === byId('fallback-text') ? byId('fallback-close') : byId('fallback-text')).focus(); }
  });
  let printOpen = [];
  window.addEventListener('beforeprint', () => { printOpen = [...document.querySelectorAll('details:not([open])')]; printOpen.forEach(node => { node.open = true; }); });
  window.addEventListener('afterprint', () => { printOpen.forEach(node => { node.open = false; }); printOpen = []; });
  updateFields(); updateProgress(); select(state.index, state.micro, false);
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
<header class="masthead"><div class="masthead-inner"><div><div class="eyebrow">A calm, practical walkthrough</div><h1 id="guide-title"></h1><p class="subtitle" id="guide-subtitle"></p></div><div class="meta"><span class="pill">Offline ready</span><p id="version"></p><p id="base-sha"></p><p><a id="share-link" target="_blank" rel="noopener noreferrer">Open participant guide ↗</a></p></div></div></header>
<div class="layout">
<aside class="rail" aria-label="Guide steps"><div class="rail-card"><div class="rail-head"><span class="eyebrow">The call</span><strong id="progress-count">0 / 0</strong></div><div class="progress-track" role="presentation"><div id="progress-bar" class="progress-bar"></div></div><ol id="stage-nav" class="stage-nav"></ol><div class="rail-actions"><button id="new-call" type="button" class="text-button">Start a new call · clear progress</button><button id="print-guide" type="button" class="button secondary">Print guide</button></div></div></aside>
<main class="main"><details class="setup"><summary id="setup-title">Names for this call · open when confirmed</summary><div class="setup-content"><p class="setup-note">Enter these as your friend confirms them. They are used only when preparing a message or prompt. Your place and checkmarks may be saved in this browser; these names are never saved.</p><div class="fields"><div class="field"><label for="handle">GitHub handle</label><input id="handle" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="friend-handle" aria-describedby="handle-error"><p class="error" id="handle-error"></p></div><div class="field"><label for="vault-repo">Vault repository name</label><input id="vault-repo" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="name-second-brain" aria-describedby="vault-repo-error"><p class="error" id="vault-repo-error"></p></div></div><p id="validation" class="validation" aria-live="polite"></p></div></details><div id="stages"></div><section class="foot-card" aria-labelledby="sources-title"><h3 id="sources-title">Reference links</h3><ul id="sources" class="source-list"></ul><p class="print-note">Printed from the offline guide. Prompts are included in full; replace any remaining brace placeholders with the names from your call.</p></section></main>
</div>
<div id="status" class="status" role="status" aria-live="polite"></div>
<div id="fallback" class="fallback" hidden><div class="fallback-panel" role="dialog" aria-modal="true" aria-labelledby="fallback-title"><h3 id="fallback-title">Copy this text manually</h3><p>Clipboard access is unavailable here. The text is selected; press Copy on your keyboard.</p><textarea id="fallback-text" readonly></textarea><button id="fallback-close" type="button" class="button secondary">Close</button></div></div>
<script id="guide-data" type="application/json">{payload}</script>
<script>{JS}</script>
</body></html>
"""


def render_script(data: dict) -> str:
    """Produce a complete, printable script from the same verified source as the page."""
    lines = [
        "---", "type: note", "---", "", f"# {data['title']} — facilitator script", "",
        data["subtitle"], "", f"Version {data['version']} · template {data['base_sha']}", "",
        "Use alongside the [participant guide](" + data["share_url"] + "). Your friend controls their own screen. Have Meet, this guide, the starter repository, and their AI ready. Keep the final 25 minutes for project work, contribution, and handoff. Switch to the browser route after five minutes stuck on one setup issue.", "",
        "Replace `{{HANDLE}}` and `{{VAULT_REPO}}` with values your friend confirms. Do not put credentials or private project material into this guide.", "",
    ]
    prompts = {prompt["id"]: prompt for prompt in data["prompts"]}
    for index, stage in enumerate(data["stages"], 1):
        lines += [f"## {index}. {stage['title']} ({stage['time']})", "", stage["live"]["purpose"], ""]
        for step_index, step in enumerate(stage["live"]["steps"], 1):
            lines += [f"### Live step {step_index} of {len(stage['live']['steps'])}", "", "**Say this**", "", step["say"], "", "**Guide this action**", "", step["action"], "", "**Wait until you see**", "", step["see"], ""]
        lines += ["**Before the next stage:** " + stage["live"]["transition"], "", "### Full stage notes", "", "**Stage opener:** " + stage["say"], ""]
        for number, action in enumerate(stage["actions"], 1):
            lines.append(f"{number}. {action}")
        lines += ["", "**Stage result:** " + stage["see"], ""]
        if stage["recovery"]:
            lines += ["### Stuck?", ""]
            for item in stage["recovery"]:
                lines += [f"**{item['symptom']}**", "", item["action"], ""]
        if stage["send"]:
            lines += ["### Send or copy", ""]
            for item in stage["send"]:
                lines += [f"**{item['label']}**", "", "``````text", item["text"], "``````", ""]
        for prompt_id in stage["prompt_ids"]:
            prompt = prompts[prompt_id]
            lines += [f"### Prompt: {prompt['title']}", "", prompt["hint"], "", "``````markdown", prompt["body"].rstrip(), "``````", ""]
    lines += ["## Reference links", ""]
    lines += [f"- [{source['label']}]({source['url']})" for source in data["sources"]]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", type=Path, default=HERE / "content.json")
    parser.add_argument("--output", type=Path, default=HERE / "meet.html")
    parser.add_argument("--script-output", type=Path, default=HERE / "FACILITATOR.md")
    args = parser.parse_args()
    data = read_content(args.content.resolve())
    args.output.write_text(render(data), encoding="utf-8")
    args.script_output.write_text(render_script(data), encoding="utf-8")
    print(f"Built {args.output} and {args.script_output} from {args.content}")


if __name__ == "__main__":
    main()
