/* Private Client Tax Digest — shared UI: language toggle + read-aloud (Web Speech API).
   No dependencies, no network. Works on GitHub Pages. */
(function () {
  function zhOn() { return document.documentElement.classList.contains('lang-zh'); }

  // ---------- Language toggle ----------
  window.setLangBtn = function () {
    var b = document.getElementById('langtoggle');
    if (b) b.textContent = zhOn() ? 'EN' : '繁中';
  };
  window.toggleLang = function () {
    var h = document.documentElement, zh = !zhOn();
    h.classList.toggle('lang-zh', zh);
    try { localStorage.setItem('pctd-lang', zh ? 'zh' : 'en'); } catch (e) {}
    window.setLangBtn();
    window.stopSpeak();      // stop any speech; language changed
    window.setTtsBtn();
  };

  // ---------- Read aloud ----------
  var synth = window.speechSynthesis;
  var speaking = false, queue = [], idx = 0;

  function ttsBtn() { return document.getElementById('ttsbtn'); }
  window.setTtsBtn = function () {
    var b = ttsBtn(); if (!b) return;
    if (speaking) b.textContent = zhOn() ? '⏹ 停止' : '⏹ Stop';
    else b.textContent = zhOn() ? '🔊 朗讀' : '🔊 Read';
  };

  function pickVoice(prefix) {
    var vs = (synth && synth.getVoices()) || [];
    var m = vs.filter(function (v) { return v.lang && v.lang.toLowerCase().indexOf(prefix) === 0; });
    return m[0] || null;
  }

  function articleText() {
    var sel = 'article div.' + (zhOn() ? 'zh' : 'en');
    var el = document.querySelector(sel) || document.querySelector('article') || document.body;
    var clone = el.cloneNode(true);
    // drop chips, buttons, back-link and scripts so they aren't read out
    clone.querySelectorAll('.tag,.badge,.back,.lang-btn,button,script,style').forEach(function (n) {
      if (n.parentNode) n.parentNode.removeChild(n);
    });
    return (clone.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function chunkText(t) {
    // split into ~200-char pieces at sentence boundaries (no lookbehind, for Safari)
    var out = [], buf = '';
    for (var i = 0; i < t.length; i++) {
      buf += t[i];
      if (buf.length >= 200 && /[.!?。！？；;]/.test(t[i])) { out.push(buf.trim()); buf = ''; }
    }
    if (buf.trim()) out.push(buf.trim());
    return out;
  }

  window.stopSpeak = function () {
    try { if (synth) synth.cancel(); } catch (e) {}
    speaking = false; queue = []; idx = 0;
    window.setTtsBtn();
  };

  function speakNext(lang, voice) {
    if (!speaking || idx >= queue.length) { speaking = false; window.setTtsBtn(); return; }
    var u = new SpeechSynthesisUtterance(queue[idx++]);
    u.lang = lang; if (voice) u.voice = voice; u.rate = 1; u.pitch = 1;
    u.onend = function () { if (speaking) speakNext(lang, voice); };
    u.onerror = function () { if (speaking) speakNext(lang, voice); };
    synth.speak(u);
  }

  window.readAloud = function () {
    if (!synth) { alert('Sorry — this browser does not support read-aloud (text-to-speech).'); return; }
    if (speaking) { window.stopSpeak(); return; }   // toggle off
    var zh = zhOn();
    var lang = zh ? 'zh-TW' : 'en-GB';
    queue = chunkText(articleText()); idx = 0;
    if (!queue.length) return;
    var voice = pickVoice(zh ? 'zh' : 'en');
    if (!voice && synth.getVoices().length === 0) {
      // voices load async on some browsers — grab them then start
      synth.onvoiceschanged = function () {
        if (speaking) { /* already started with default */ }
      };
    }
    speaking = true; window.setTtsBtn();
    speakNext(lang, voice);
  };

  window.addEventListener('beforeunload', function () { try { if (synth) synth.cancel(); } catch (e) {} });

  // init button labels on load
  try { window.setLangBtn(); } catch (e) {}
  try { window.setTtsBtn(); } catch (e) {}
})();
