# -*- coding: utf-8 -*-
"""
motor_fluidez_finanzas_60fps.py — ESTUDIO FINANCIERO INTEGRAL A 60 FPS (8 MÓDULOS + GUÍAS RESUELTAS + LECTURA VIVA)
Asignatura: Finanzas Avanzadas — Universidad de Los Lagos (Prof.ª Camila Bustos Rosas)
Renderiza en el navegador (HTML5 SVG + JavaScript sin recarga de servidor):
  1) Separación de Fisher: Frontera Productiva, Línea del Mercado de Capitales (RMgI = rf) y Consumo (TMS).
  2) Actitudes frente al Riesgo: Curva de Utilidad U(W), Juego Justo, Equivalente Cierto (EC) y Prima por Riesgo.
  3) Frontera Eficiente de Markowitz (252 días) y CAPM: Diversificación (ρ < 1), GMVP, Tangente (Sharpe), CML y SML.
  4) Estructura de Capital: Ecuación de Hamada (βU ↔ βL), WACC, Escudo Fiscal y Puente APV (Modigliani-Miller).
  5) Conflicto VAN vs. TIR (Tasa de Fisher) y Poder Generador de Utilidades (PGU / Identidad DuPont).
  6) Hoja de Entrenamiento Mecánico: 16 Fórmulas Puras + 6 Esqueletos SVG + Modo Ciego + Impresión Carta.
  7) Mapa Teórico Causal (5 Pilares) + Fichas de Lectura en 3 Capas + Control de Lectura Cruzado (10 Preguntas).
"""

import streamlit.components.v1 as components


HTML_FINANZAS_60FPS = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  body { margin: 0; padding: 0; background: #F8FAFC; color: #0F172A; }
  .wrap { max-width: 1240px; margin: 0 auto; padding: 4px 4px 14px 4px; }
  .top-tabs {
    display: flex; gap: 6px; margin-bottom: 11px; flex-wrap: wrap;
    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px;
  }
  .tab-btn {
    border: 1px solid #CBD5E1; background: #F8FAFC; color: #334155;
    padding: 6px 11px; border-radius: 6px; font-weight: 700; font-size: 12px;
    cursor: pointer; transition: all 0.14s ease;
  }
  .tab-btn:hover { border-color: #1D4ED8; color: #1D4ED8; background: #EFF6FF; }
  .tab-btn.active { background: #0F172A; color: #FFFFFF; border-color: #0F172A; }
  .panel { display: none; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px 16px; }
  .panel.active { display: block; }
  .sec-title {
    font-size: 13px; font-weight: 700; color: #1E3A8A;
    background: #DBEAFE; border-left: 4px solid #1D4ED8;
    padding: 7px 12px; border-radius: 4px; margin-bottom: 10px;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
  }
  .btn-bar { display: flex; gap: 6px; flex-wrap: wrap; }
  .act-btn {
    border: 1px solid #94A3B8; background: #FFFFFF; color: #0F172A;
    padding: 5px 10px; border-radius: 5px; font-size: 11.5px; font-weight: 700; cursor: pointer;
  }
  .act-btn:hover { background: #EFF6FF; border-color: #1D4ED8; color: #1D4ED8; }
  .act-btn.primary { background: #1D4ED8; color: #FFFFFF; border-color: #1D4ED8; }
  .act-btn.primary:hover { background: #1E40AF; }
  .sliders-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(185px, 1fr)); gap: 10px; margin-bottom: 11px; }
  .sl-card { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 8px 10px; }
  .sl-head { display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 700; color: #1E293B; margin-bottom: 4px; gap: 4px; }
  .sl-val { color: #1D4ED8; font-family: Consolas, monospace; white-space: nowrap; }
  .sl-delta { font-size: 10.5px; font-weight: 700; margin-left: 4px; }
  .d-up { color: #15803D; }
  .d-down { color: #DC2626; }
  .d-eq { color: #64748B; }
  input[type="range"] { width: 100%; accent-color: #1D4ED8; cursor: pointer; margin: 2px 0; }
  .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 8px; margin-bottom: 10px; }
  .kpi { background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #0F172A; border-radius: 5px; padding: 7px 10px; }
  .kpi-lbl { font-size: 11px; color: #475569; font-weight: 600; }
  .kpi-val { font-size: 14.5px; font-weight: 800; color: #0F172A; font-family: Consolas, monospace; margin-top: 2px; }
  .kpi-sub { font-size: 11px; color: #334155; margin-top: 1px; }
  .svg-box { width: 100%; border: 1px solid #E2E8F0; border-radius: 6px; background: #FFFFFF; overflow: hidden; }
  svg { width: 100%; height: auto; display: block; }
  .enun-box {
    background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 4px solid #0F172A;
    border-radius: 6px; padding: 9px 13px; margin-bottom: 10px; font-size: 12.1px; line-height: 1.46; color: #1E293B;
  }
  .enun-box summary {
    cursor: pointer; font-weight: 800; color: #0F172A; font-size: 12.3px; list-style: none;
    display: flex; justify-content: space-between; align-items: center;
  }
  .enun-box summary::-webkit-details-marker { display: none; }
  .enun-badge { font-size: 10.5px; font-weight: 700; color: #1E3A8A; background: #DBEAFE; padding: 2px 8px; border-radius: 10px; }
  .enun-body { margin-top: 7px; border-top: 1px dashed #CBD5E1; padding-top: 7px; }
  .sol-box {
    margin-top: 8px; background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 4px solid #15803D;
    border-radius: 6px; padding: 9px 12px; font-size: 12px; line-height: 1.48; color: #0F172A;
    font-family: Consolas, monospace;
  }
  .sol-box b { color: #1E3A8A; }

  /* === HOJA MECÁNICA === */
  .mec-toolbar {
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
    background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px 12px; margin-bottom: 10px;
  }
  .mec-filters { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }
  .flt-btn {
    border: 1px solid #CBD5E1; background: #FFFFFF; color: #334155;
    padding: 4px 10px; border-radius: 14px; font-size: 11.5px; font-weight: 700; cursor: pointer;
  }
  .flt-btn.active { background: #1E293B; color: #FFFFFF; border-color: #1E293B; }
  .pill-score {
    background: #0F172A; color: #FFFFFF; padding: 5px 11px; border-radius: 14px;
    font-size: 12px; font-weight: 700; font-family: Consolas, monospace;
  }
  .mec-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 9px; margin-bottom: 14px; }
  @media (max-width: 780px) { .mec-grid { grid-template-columns: 1fr; } }
  .f-card {
    border: 1px solid #CBD5E1; border-left: 3.5px solid #1E293B; border-radius: 6px;
    background: #FFFFFF; padding: 9px 11px; transition: border-color 0.15s ease;
  }
  .f-card.mastered { border-left-color: #15803D; background: #F0FDF4; }
  .f-head { display: flex; justify-content: space-between; align-items: center; gap: 6px; margin-bottom: 5px; }
  .f-title { font-size: 12px; font-weight: 800; color: #0F172A; }
  .f-cat { font-size: 10px; font-weight: 700; color: #475569; background: #E2E8F0; padding: 2px 6px; border-radius: 4px; }
  .chk-btn {
    border: 1px solid #94A3B8; background: #FFFFFF; color: #475569; width: 22px; height: 22px;
    border-radius: 4px; font-size: 12px; font-weight: 800; cursor: pointer; line-height: 1; padding: 0;
  }
  .f-card.mastered .chk-btn { background: #15803D; color: #FFFFFF; border-color: #15803D; }
  .f-body {
    background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 4px; padding: 7px 9px;
    cursor: pointer; min-height: 44px; display: flex; flex-direction: column; justify-content: center;
  }
  .f-eq {
    font-family: "Cambria Math", "Times New Roman", Georgia, serif;
    font-size: 14.5px; font-weight: 700; color: #0F172A; letter-spacing: 0.2px;
    display: flex; align-items: center; flex-wrap: wrap; gap: 4px;
  }
  .f-rule { font-size: 11px; color: #334155; margin-top: 5px; line-height: 1.32; }
  .frac { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 2px; font-size: 0.88em; line-height: 1.1; }
  .frac .num { border-bottom: 1.4px solid #0F172A; padding: 0 3px 1px 3px; text-align: center; }
  .frac .den { padding: 1px 3px 0 3px; text-align: center; }
  .blind-cover { display: none; font-size: 11.5px; font-weight: 700; color: #1D4ED8; text-align: center; padding: 4px 0; }
  .blind-mode .f-card:not(.revealed) .f-eq,
  .blind-mode .f-card:not(.revealed) .f-rule { display: none; }
  .blind-mode .f-card:not(.revealed) .blind-cover { display: block; }
  .skel-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
  @media (max-width: 860px) { .skel-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 560px) { .skel-grid { grid-template-columns: 1fr; } }
  .s-card { border: 1px solid #CBD5E1; border-radius: 6px; background: #FFFFFF; padding: 8px 9px; cursor: pointer; }
  .s-title { font-size: 11.5px; font-weight: 800; color: #0F172A; margin-bottom: 4px; }
  .s-sub { font-size: 10.5px; color: #475569; margin-top: 4px; line-height: 1.3; }
  .blind-mode .s-card:not(.revealed) .sk-lbl { opacity: 0; }
  .blind-mode .s-card:not(.revealed) .s-sub { visibility: hidden; }

  /* === MAPA TEÓRICO Y LECTURA VIVA === */
  .map-detail-card {
    margin-top: 9px; background: #F8FAFC; border: 1px solid #CBD5E1; border-left: 4px solid #1D4ED8;
    border-radius: 6px; padding: 10px 13px; font-size: 12.2px; line-height: 1.48; color: #0F172A;
  }
  .map-detail-head {
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
    margin-bottom: 6px; padding-bottom: 6px; border-bottom: 1px dashed #CBD5E1;
  }
  .map-detail-title { font-size: 13px; font-weight: 800; color: #1E3A8A; }
  .jump-btn {
    border: 1px solid #1D4ED8; background: #EFF6FF; color: #1E3A8A;
    padding: 4px 9px; border-radius: 5px; font-size: 11px; font-weight: 700; cursor: pointer;
  }
  .jump-btn:hover { background: #1D4ED8; color: #FFFFFF; }
  .lec-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-bottom: 12px; }
  @media (max-width: 820px) { .lec-grid { grid-template-columns: 1fr; } }
  .lec-card {
    border: 1px solid #CBD5E1; border-top: 3.5px solid #1E3A8A; border-radius: 6px;
    background: #FFFFFF; padding: 10px 12px; display: flex; flex-direction: column; gap: 6px;
  }
  .lec-meta { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 4px; }
  .lec-unit { font-size: 10px; font-weight: 800; color: #FFFFFF; background: #1E293B; padding: 2px 7px; border-radius: 4px; }
  .lec-src { font-size: 10.5px; font-weight: 600; color: #475569; font-family: Consolas, monospace; }
  .lec-title { font-size: 12.6px; font-weight: 800; color: #0F172A; }
  .lec-layer {
    font-size: 11.8px; line-height: 1.44; color: #1E293B; padding: 6px 9px; border-radius: 5px;
    background: #F8FAFC; border-left: 3px solid #94A3B8;
  }
  .lec-layer.l-core { border-left-color: #1D4ED8; background: #EFF6FF; }
  .lec-layer.l-bridge { border-left-color: #059669; background: #ECFDF5; }
  .lec-layer.l-trap { border-left-color: #DC2626; background: #FEF2F2; }
  .lec-layer b { color: #0F172A; }
  .qz-card {
    border: 1px solid #CBD5E1; border-left: 4px solid #334155; border-radius: 6px;
    background: #FFFFFF; padding: 9px 12px; margin-bottom: 8px;
  }
  .qz-card.ok { border-left-color: #15803D; background: #F0FDF4; }
  .qz-card.bad { border-left-color: #DC2626; background: #FEF2F2; }
  .qz-tag { font-size: 10px; font-weight: 800; color: #1E3A8A; background: #DBEAFE; padding: 2px 7px; border-radius: 4px; margin-right: 6px; }
  .qz-q { font-size: 12.2px; font-weight: 700; color: #0F172A; margin: 4px 0 7px 0; line-height: 1.42; }
  .qz-opts { display: flex; gap: 7px; flex-wrap: wrap; align-items: center; }
  .qz-btn {
    border: 1px solid #94A3B8; background: #FFFFFF; color: #0F172A;
    padding: 4px 10px; border-radius: 5px; font-size: 11.4px; font-weight: 700; cursor: pointer;
  }
  .qz-btn:hover { background: #EFF6FF; border-color: #1D4ED8; }
  .qz-btn.sel { background: #0F172A; color: #FFFFFF; border-color: #0F172A; }
  .qz-fb { font-size: 11.5px; color: #1E293B; margin-top: 7px; line-height: 1.42; display: none; border-top: 1px dashed #CBD5E1; padding-top: 6px; }
  .qz-card.answered .qz-fb { display: block; }
  .g-tbl { width: 100%; border-collapse: collapse; font-size: 11.5px; margin: 7px 0; }
  .g-tbl th { background: #1E293B; color: #FFFFFF; padding: 5px 7px; border: 1px solid #CBD5E1; text-align: center; font-weight: 700; }
  .g-tbl td { padding: 5px 7px; border: 1px solid #CBD5E1; text-align: right; font-family: Consolas, monospace; color: #0F172A; }
  .g-tbl td:first-child { text-align: left; font-family: inherit; font-weight: 700; background: #F8FAFC; }
  .g-subgrid { display: grid; grid-template-columns: 1.05fr 1fr; gap: 11px; align-items: start; }
  @media (max-width: 840px) { .g-subgrid { grid-template-columns: 1fr; } }

  @media print {
    body { background: #FFFFFF !important; }
    .top-tabs, .mec-toolbar, .mec-filters, .btn-bar, .chk-btn { display: none !important; }
    .panel { display: none !important; border: none !important; padding: 0 !important; }
    #panel-mecanica { display: block !important; }
    .sec-title { background: #F1F5F9 !important; color: #000000 !important; border-left: 3px solid #000 !important; padding: 4px 8px !important; font-size: 11px !important; }
    .mec-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 6px !important; }
    .f-card { break-inside: avoid; border: 1px solid #94A3B8 !important; padding: 5px 7px !important; }
    .blind-mode .f-card .f-eq, .blind-mode .f-card .f-rule { display: block !important; }
    .blind-mode .f-card .blind-cover { display: none !important; }
    .blind-mode .s-card .sk-lbl { opacity: 1 !important; }
    .blind-mode .s-card .s-sub { visibility: visible !important; }
    .skel-grid { grid-template-columns: repeat(3, 1fr) !important; gap: 6px !important; }
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="top-tabs">
    <button class="tab-btn active" onclick="openTab('fisher', this)">1. Separación de Fisher</button>
    <button class="tab-btn" onclick="openTab('riesgo', this)">2. Riesgo y Juego Justo</button>
    <button class="tab-btn" onclick="openTab('markowitz', this)">3. Markowitz (252d) y CAPM</button>
    <button class="tab-btn" onclick="openTab('hamada', this)">4. Hamada, WACC y APV</button>
    <button class="tab-btn" onclick="openTab('vantir', this)">5. VAN vs. TIR y PGU DuPont</button>
    <button class="tab-btn" onclick="openTab('mecanica', this)">6. Hoja Mecánica (Modo Ciego)</button>
    <button class="tab-btn" onclick="openTab('lectura', this)">7. Mapa Teórico y Lectura Viva</button>
    <button class="tab-btn" onclick="openTab('guias', this)">8. Guías Oficiales Resueltas</button>
  </div>

  <!-- ====================================================================== -->
  <!-- PANEL 1: MODELO CONSUMO-INVERSIÓN Y SEPARACIÓN DE FISHER (60 FPS)      -->
  <!-- ====================================================================== -->
  <div id="panel-fisher" class="panel active">
    <div class="sec-title">
      <span>Modelo Consumo-Inversión y Principio de Separación de Fisher (RMgI = rf · TMS = −(1 + rf))</span>
      <div class="btn-bar">
        <button class="act-btn primary" onclick="animarFisher()">Reproducir Baja de Tasa (rf: 20% → 6%)</button>
        <button class="act-btn" onclick="presetFisher(0.30)">Accionista Ahorrador (α=0,30)</button>
        <button class="act-btn" onclick="presetFisher(0.75)">Accionista Impaciente (α=0,75)</button>
        <button class="act-btn" onclick="fijarGhostFisher()">Fijar Fantasma</button>
      </div>
    </div>

    <details class="enun-box" open>
      <summary>
        <span>Planteamiento Oficial (Consumo - Inversión.pdf, láms. 2–10 · Brealey, Myers y Allen Cap. 2)</span>
        <span class="enun-badge">Enunciado y equilibrio sincronizados en vivo</span>
      </summary>
      <div class="enun-body" id="fs-enunciado"></div>
    </details>

    <div class="sliders-grid">
      <div class="sl-card"><div class="sl-head"><span>Dotación Inicial Y0 ($MM)</span><span id="fs-y0-v" class="sl-val">$120M</span></div><input id="fs-y0" type="range" min="60" max="260" step="5" value="120" oninput="drawFisher()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Tasa Mercado rf (%)</span><span><span id="fs-rf-v" class="sl-val">10,0%</span><span id="fs-rf-d" class="sl-delta d-eq"></span></span></div><input id="fs-rf" type="range" min="2.0" max="24.0" step="0.5" value="10.0" oninput="drawFisher()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Productividad Activos (A)</span><span id="fs-a-v" class="sl-val">20</span></div><input id="fs-a" type="range" min="14" max="36" step="1" value="20" oninput="drawFisher()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Impaciencia Consumo α</span><span id="fs-al-v" class="sl-val">0,45</span></div><input id="fs-al" type="range" min="0.20" max="0.85" step="0.05" value="0.45" oninput="drawFisher()" /></div>
    </div>

    <div class="kpis">
      <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">Inversión Física Óptima I0*</div><div id="fs-k-i0" class="kpi-val">$162M</div><div id="fs-k-p" class="kpi-sub">Punto P* (RMgI = rf)</div></div>
      <div class="kpi" style="border-left-color:#15803D;"><div class="kpi-lbl">VAN Productivo Generado</div><div id="fs-k-van" class="kpi-val">+$76,2M</div><div id="fs-k-w0" class="kpi-sub">Riqueza W0* = Y0 + VAN</div></div>
      <div class="kpi" style="border-left-color:#0F172A;"><div class="kpi-lbl">Consumo Óptimo (C0*, C1*)</div><div id="fs-k-c" class="kpi-val">$88M | $119M</div><div class="kpi-sub">TMS = -(1+rf)</div></div>
      <div class="kpi" style="border-left-color:#DC2626;"><div class="kpi-lbl">Mercado Financiero en t=0</div><div id="fs-k-pos" class="kpi-val">Pide prestado</div><div id="fs-k-pos2" class="kpi-sub">Separación objetiva</div></div>
    </div>

    <div class="svg-box"><svg id="svg-fisher" viewBox="0 0 980 395"></svg></div>
    <div id="fs-sol" class="sol-box"></div>
  </div>

  <!-- ====================================================================== -->
  <!-- PANEL 2: ACTITUDES FRENTE AL RIESGO Y JUEGO JUSTO (60 FPS)             -->
  <!-- ====================================================================== -->
  <div id="panel-riesgo" class="panel">
    <div class="sec-title">
      <span>Actitudes frente al Riesgo, Juego Justo y Prima por Riesgo (Von Neumann-Morgenstern)</span>
      <div class="btn-bar">
        <button class="act-btn primary" onclick="presetRiesgo(0.35)">Averso (U'' &lt; 0)</button>
        <button class="act-btn" onclick="presetRiesgo(1.00)">Neutral (U'' = 0)</button>
        <button class="act-btn" onclick="presetRiesgo(1.80)">Amante (U'' &gt; 0)</button>
        <button class="act-btn" onclick="hacerJuegoJusto()">Fijar Juego Justo (W0 = E[W])</button>
      </div>
    </div>

    <details class="enun-box" open>
      <summary>
        <span>Planteamiento Oficial (Relación riesgo rentabilidad.pdf, láms. 7–21)</span>
        <span class="enun-badge">Fórmula: Prima por Riesgo π = E(W) − EC</span>
      </summary>
      <div class="enun-body" id="rk-enunciado"></div>
    </details>

    <div class="sliders-grid">
      <div class="sl-card"><div class="sl-head"><span>Curvatura Utilidad γ (&lt;1 Averso)</span><span id="rk-g-v" class="sl-val">0,35</span></div><input id="rk-g" type="range" min="0.20" max="2.00" step="0.05" value="0.35" oninput="drawRiesgo()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Escenario Malo W1 ($M)</span><span id="rk-w1-v" class="sl-val">$40M</span></div><input id="rk-w1" type="range" min="10" max="120" step="5" value="40" oninput="drawRiesgo()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Escenario Bueno W2 ($M)</span><span id="rk-w2-v" class="sl-val">$160M</span></div><input id="rk-w2" type="range" min="130" max="320" step="5" value="160" oninput="drawRiesgo()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Prob. Escenario Bueno p (%)</span><span id="rk-p-v" class="sl-val">50%</span></div><input id="rk-p" type="range" min="10" max="90" step="5" value="50" oninput="drawRiesgo()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Riqueza Segura W0 ($M)</span><span id="rk-w0-v" class="sl-val">$100M</span></div><input id="rk-w0" type="range" min="20" max="260" step="2" value="100" oninput="drawRiesgo()" /></div>
    </div>

    <div class="kpis">
      <div class="kpi" style="border-left-color:#0F172A;"><div class="kpi-lbl">Valor Esperado E(W)</div><div id="rk-k-ew" class="kpi-val">$100,0M</div><div id="rk-k-jj" class="kpi-sub">Juego Justo</div></div>
      <div class="kpi" style="border-left-color:#15803D;"><div class="kpi-lbl">Equivalente Cierto (EC)</div><div id="rk-k-ec" class="kpi-val">$86,8M</div><div class="kpi-sub">Riqueza segura equivalente</div></div>
      <div class="kpi" style="border-left-color:#DC2626;"><div class="kpi-lbl">Prima por Riesgo (π)</div><div id="rk-k-pi" class="kpi-val">+$13,2M</div><div id="rk-k-act" class="kpi-sub">Averso al Riesgo</div></div>
      <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">Decisión Racional</div><div id="rk-k-dec" class="kpi-val">RECHAZA JUEGO</div><div id="rk-k-dec2" class="kpi-sub">Prefiere W0 seguro</div></div>
    </div>

    <div class="svg-box"><svg id="svg-riesgo" viewBox="0 0 980 385"></svg></div>
  </div>

  <!-- ====================================================================== -->
  <!-- PANEL 3: MARKOWITZ (252 DÍAS), CORRELACIÓN ρ Y CAPM / SML (60 FPS)     -->
  <!-- ====================================================================== -->
  <div id="panel-markowitz" class="panel">
    <div class="sec-title">
      <span>Frontera Eficiente de Markowitz (252 días), Diversificación (ρ &lt; 1), CML y CAPM / SML</span>
      <div class="btn-bar">
        <button class="act-btn primary" onclick="animarMarkowitz()">Reproducir Diversificación (ρ: +1 → −0,6)</button>
        <button class="act-btn" onclick="presetMarkowitz(1.0)">ρ = +1 (Sin Diversif.)</button>
        <button class="act-btn" onclick="presetMarkowitz(0.25)">ρ = +0,25 (IPSA Real)</button>
        <button class="act-btn" onclick="presetMarkowitz(-0.8)">ρ = −0,80 (Cobertura)</button>
        <button class="act-btn" onclick="fijarGhostMarkowitz()">Fijar Fantasma</button>
      </div>
    </div>

    <details class="enun-box" open>
      <summary>
        <span>Planteamiento Oficial (Teoría de mercado de capitales.pdf · Taller $65M Dupla 13 IPSA · 252 días)</span>
        <span class="enun-badge">Fórmulas: σ_anual = σ_d·√252 · Sharpe = (Rp − Rf)/σp</span>
      </summary>
      <div class="enun-body" id="mk-enunciado"></div>
    </details>

    <div class="sliders-grid">
      <div class="sl-card"><div class="sl-head"><span>Correlación ρ(A,B)</span><span><span id="mk-rho-v" class="sl-val">0,25</span><span id="mk-rho-d" class="sl-delta d-eq"></span></span></div><input id="mk-rho" type="range" min="-0.95" max="1.00" step="0.05" value="0.25" oninput="drawMarkowitz()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Peso en Activo A (wA)</span><span id="mk-wa-v" class="sl-val">55%</span></div><input id="mk-wa" type="range" min="0" max="100" step="2" value="55" oninput="drawMarkowitz()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Volat. Diaria A (CHILE)</span><span id="mk-sa-v" class="sl-val">1,18%</span></div><input id="mk-sa" type="range" min="0.60" max="2.60" step="0.02" value="1.18" oninput="drawMarkowitz()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Volat. Diaria B (VAPORES)</span><span id="mk-sb-v" class="sl-val">2,05%</span></div><input id="mk-sb" type="range" min="0.80" max="3.20" step="0.05" value="2.05" oninput="drawMarkowitz()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Tasa Rf BCP/BTP 5a (%)</span><span id="mk-rf-v" class="sl-val">5,65%</span></div><input id="mk-rf" type="range" min="2.0" max="10.0" step="0.05" value="5.65" oninput="drawMarkowitz()" /></div>
    </div>

    <div class="kpis">
      <div class="kpi" style="border-left-color:#15803D;"><div class="kpi-lbl">Mínima Varianza (GMVP)</div><div id="mk-k-gmvp" class="kpi-val">σ=16,8%</div><div id="mk-k-gmvp2" class="kpi-sub">E(R) = 17,6%</div></div>
      <div class="kpi" style="border-left-color:#DC2626;"><div class="kpi-lbl">Portafolio Tangente (Sharpe)</div><div id="mk-k-tan" class="kpi-val">S = 0,72</div><div id="mk-k-tan2" class="kpi-sub">E(R) | σ óptimo</div></div>
      <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">Tu Cartera (wA / wB)</div><div id="mk-k-cur" class="kpi-val">E(R)=18,1%</div><div id="mk-k-cur2" class="kpi-sub">σ = 17,9% | $65M</div></div>
      <div class="kpi" style="border-left-color:#7C3AED;"><div class="kpi-lbl">Ahorro de Riesgo (Diversif.)</div><div id="mk-k-div" class="kpi-val">-6,2 pp</div><div class="kpi-sub">vs promedio lineal (ρ=1)</div></div>
    </div>

    <div class="svg-box"><svg id="svg-markowitz" viewBox="0 0 980 390"></svg></div>
  </div>

  <!-- ====================================================================== -->
  <!-- PANEL 4: HAMADA (βU ↔ βL), WACC Y APV (MODIGLIANI-MILLER A 60 FPS)     -->
  <!-- ====================================================================== -->
  <div id="panel-hamada" class="panel">
    <div class="sec-title">
      <span>Estructura de Capital: Ecuación de Hamada (βL), WACC, Escudo Fiscal y Método APV</span>
      <div class="btn-bar">
        <button class="act-btn primary" onclick="animarHamada()">Reproducir Apalancamiento (B/V: 0% → 65%)</button>
        <button class="act-btn" onclick="presetHamada(30)">Caso Cátedra (30% Deuda)</button>
        <button class="act-btn" onclick="presetHamada(0)">Sin Deuda (100% Patrimonio)</button>
        <button class="act-btn" onclick="fijarGhostHamada()">Fijar Fantasma</button>
      </div>
    </div>

    <details class="enun-box" open>
      <summary>
        <span>Planteamiento Oficial (Ecuación de Hamada, CAPM, WACC y Modigliani-Miller con Impuestos)</span>
        <span class="enun-badge">Fórmula: βL = βU · [1 + (1 − t)·(B/S)]</span>
      </summary>
      <div class="enun-body" id="hm-enunciado"></div>
    </details>

    <div class="sliders-grid">
      <div class="sl-card"><div class="sl-head"><span>Beta Operativo Puro (βU)</span><span id="hm-bu-v" class="sl-val">1,05</span></div><input id="hm-bu" type="range" min="0.40" max="1.80" step="0.05" value="1.05" oninput="drawHamada()" /></div>
      <div class="sl-card"><div class="sl-head"><span>% Deuda sobre Valor (B/V)</span><span><span id="hm-dv-v" class="sl-val">30%</span><span id="hm-dv-d" class="sl-delta d-eq"></span></span></div><input id="hm-dv" type="range" min="0" max="75" step="1" value="30" oninput="drawHamada()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Tasa Deuda Kd (%)</span><span id="hm-kd-v" class="sl-val">6,5%</span></div><input id="hm-kd" type="range" min="3.0" max="13.0" step="0.25" value="6.5" oninput="drawHamada()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Impuesto Corporativo t (%)</span><span id="hm-tc-v" class="sl-val">29,5%</span></div><input id="hm-tc" type="range" min="0.0" max="35.0" step="0.5" value="29.5" oninput="drawHamada()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Prima Mercado (Rm − Rf)</span><span id="hm-pm-v" class="sl-val">7,0%</span></div><input id="hm-pm" type="range" min="3.0" max="11.0" step="0.5" value="7.0" oninput="drawHamada()" /></div>
    </div>

    <div class="kpis">
      <div class="kpi" style="border-left-color:#DC2626;"><div class="kpi-lbl">Beta Apalancado (βL)</div><div id="hm-k-bl" class="kpi-val">1,37</div><div id="hm-k-bs" class="kpi-sub">Ratio B/S = 0,43</div></div>
      <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">Costo Patrimonial Ke (CAPM)</div><div id="hm-k-ke" class="kpi-val">15,1%</div><div id="hm-k-ku" class="kpi-sub">Ku puro = 12,85%</div></div>
      <div class="kpi" style="border-left-color:#15803D;"><div class="kpi-lbl">Costo de Capital (WACC)</div><div id="hm-k-wa" class="kpi-val">11,94%</div><div id="hm-k-kdt" class="kpi-sub">Kd(1-t) = 4,58%</div></div>
      <div class="kpi" style="border-left-color:#0F172A;"><div class="kpi-lbl">Valor Apalancado APV ($100M base)</div><div id="hm-k-apv" class="kpi-val">$108,9M</div><div id="hm-k-esc" class="kpi-sub">Escudo t·B = +$8,9M</div></div>
    </div>

    <div class="svg-box"><svg id="svg-hamada" viewBox="0 0 980 380"></svg></div>
    <div id="hm-sol" class="sol-box"></div>
  </div>

  <!-- ====================================================================== -->
  <!-- PANEL 5: PERFIL VAN VS. TIR (TASA DE FISHER) + PGU DUPONT (60 FPS)     -->
  <!-- ====================================================================== -->
  <div id="panel-vantir" class="panel">
    <div class="sec-title">
      <span>Conflicto VAN vs. TIR en Proyectos Mutuamente Excluyentes (Tasa de Fisher — Ejercicios 3 y 4)</span>
      <div class="btn-bar">
        <button class="act-btn primary" onclick="presetVanTir(14)">Tasa 14% (Conflicto: Gana A)</button>
        <button class="act-btn" onclick="presetVanTir(21)">Tasa 21% (Post-Fisher: Gana B)</button>
      </div>
    </div>

    <div class="sliders-grid">
      <div class="sl-card"><div class="sl-head"><span>Tasa de Descuento Exigida r (%)</span><span id="vt-r-v" class="sl-val">14,0%</span></div><input id="vt-r" type="range" min="2.0" max="28.0" step="0.5" value="14.0" oninput="drawVanTir()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Flujo Final Proyecto A (Largo Plazo)</span><span id="vt-fa-v" class="sl-val">$175M</span></div><input id="vt-fa" type="range" min="110" max="230" step="5" value="175" oninput="drawVanTir()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Flujo Año 1 Proyecto B (Rápido)</span><span id="vt-fb-v" class="sl-val">$95M</span></div><input id="vt-fb" type="range" min="50" max="135" step="5" value="95" oninput="drawVanTir()" /></div>
    </div>

    <div class="kpis">
      <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">Proyecto A (Escala / Largo Plazo)</div><div id="vt-k-a" class="kpi-val">VAN $35,2M</div><div id="vt-k-ta" class="kpi-sub">TIR = 21,5%</div></div>
      <div class="kpi" style="border-left-color:#EA580C;"><div class="kpi-lbl">Proyecto B (Recuperación Rápida)</div><div id="vt-k-b" class="kpi-val">VAN $24,1M</div><div id="vt-k-tb" class="kpi-sub">TIR = 26,8%</div></div>
      <div class="kpi" style="border-left-color:#7C3AED;"><div class="kpi-lbl">Tasa de Intersección de Fisher (r*)</div><div id="vt-k-fis" class="kpi-val">17,8%</div><div class="kpi-sub">Donde VAN(A) = VAN(B)</div></div>
      <div class="kpi" style="border-left-color:#15803D;"><div class="kpi-lbl">Decisión Óptima Accionista</div><div id="vt-k-win" class="kpi-val">ELEGIR A</div><div id="vt-k-win2" class="kpi-sub">Mayor creación de valor</div></div>
    </div>

    <div class="svg-box"><svg id="svg-vantir" viewBox="0 0 980 285"></svg></div>

    <div class="sec-title" style="margin-top:12px;">
      <span>Poder Generador de Utilidades (PGU / Identidad DuPont — Ross, Westerfield y Jordan, Cap. 3)</span>
      <div class="btn-bar">
        <button class="act-btn" onclick="presetPGU(24, 0.7)">Estrategia Diferenciación (Alto Margen)</button>
        <button class="act-btn primary" onclick="presetPGU(6, 2.8)">Estrategia Supermercado (Alta Rotación)</button>
      </div>
    </div>
    <div class="sliders-grid" style="grid-template-columns: 1fr 1fr 1.6fr;">
      <div class="sl-card"><div class="sl-head"><span>Margen Operacional (EBIT/Ventas)</span><span id="pg-m-v" class="sl-val">18,0%</span></div><input id="pg-m" type="range" min="2" max="40" step="0.5" value="18.0" oninput="drawVanTir()" /></div>
      <div class="sl-card"><div class="sl-head"><span>Rotación Activos (Ventas/Act.Op.)</span><span id="pg-r-v" class="sl-val">1,20x</span></div><input id="pg-r" type="range" min="0.2" max="4.0" step="0.1" value="1.2" oninput="drawVanTir()" /></div>
      <div id="pg-box" class="sol-box" style="margin-top:0;"></div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PANEL 6: HOJA DE ENTRENAMIENTO MECÁNICO (16 FÓRMULAS + 6 ESQUELETOS)   -->
  <!-- ====================================================================== -->
  <div id="panel-mecanica" class="panel">
    <div class="sec-title">
      <span>Formulario y Entrenamiento Mecánico — Finanzas Avanzadas (ULagos 2026)</span>
      <div class="btn-bar">
        <button id="btn-modo-copia" class="act-btn primary" onclick="setModoMec(false)">Modo Copia (Todo Visible)</button>
        <button id="btn-modo-ciego" class="act-btn" onclick="setModoMec(true)">Modo Ciego (Autoevaluación)</button>
        <button class="act-btn" onclick="resetDominadas()">Reiniciar ✓</button>
        <button class="act-btn" onclick="window.print()">Imprimir / Guardar PDF (Carta)</button>
      </div>
    </div>

    <div class="mec-toolbar">
      <div style="font-size:12px;color:#334155;">
        <b>Método de cuaderno:</b> copia las 16 fórmulas y los 6 esqueletos; luego activa <b>Modo Ciego</b>, escríbelos de memoria y haz clic en cada tarjeta para comprobar y marcar <b>✓</b>.
      </div>
      <span id="mec-score" class="pill-score">Dominadas: 0 / 18</span>
    </div>

    <div class="mec-filters">
      <button class="flt-btn active" onclick="filtrarMec('all', this)">Todas (18)</button>
      <button class="flt-btn" onclick="filtrarMec('fsh', this)">I. Fisher, Riesgo y PGU (4)</button>
      <button class="flt-btn" onclick="filtrarMec('mk', this)">II. Markowitz, Estadística y CAPM (6)</button>
      <button class="flt-btn" onclick="filtrarMec('cap', this)">III. Hamada, WACC y APV (4)</button>
      <button class="flt-btn" onclick="filtrarMec('flj', this)">IV. Flujos FCL / FCI y Criterios (4)</button>
    </div>

    <div id="mec-container">
      <div class="mec-grid" id="mec-formulas-grid"></div>
      <div class="sec-title" style="margin-top:6px;">
        <span>Esqueletos de Gráficos Clave para Repaso en Cuaderno (6 diagramas)</span>
        <span style="font-size:11px;font-weight:600;color:#334155;">En Modo Ciego, haz clic en cada gráfico para revelar las etiquetas</span>
      </div>
      <div class="skel-grid" id="mec-skel-grid"></div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PANEL 7: MAPA TEÓRICO CAUSAL, LECTURA EN 3 CAPAS Y CONTROL CRUZADO     -->
  <!-- ====================================================================== -->
  <div id="panel-lectura" class="panel">
    <div class="sec-title">
      <span>Mapa Conceptual Integrado — Finanzas Avanzadas (Conexión entre los 5 Pilares del Curso)</span>
      <div class="btn-bar">
        <button class="act-btn primary" onclick="activarEscenarioFin('wacc')">Cadena A: De Markowitz/CAPM a WACC</button>
        <button class="act-btn" onclick="activarEscenarioFin('deuda')">Cadena B: Apalancamiento (Hamada → FCI)</button>
        <button class="act-btn" onclick="activarEscenarioFin('riesgo')">Cadena C: Aversión al Riesgo → Monte Carlo</button>
        <button class="act-btn" onclick="selectPilarFin('F1')">Ver Todo Libre</button>
      </div>
    </div>

    <div class="svg-box"><svg id="svg-mapa-fin" viewBox="0 0 980 320"></svg></div>
    <div id="mapa-fin-detail" class="map-detail-card"></div>

    <div class="sec-title" style="margin-top:14px;">
      <span>Síntesis Teórica en 3 Capas por Bibliografía Oficial (Prof.ª Camila Bustos · Brealey · Ross)</span>
      <div class="btn-bar">
        <button id="cap-btn-core" class="act-btn primary" onclick="setCapaFin('core')">Capa 1: Idea Central</button>
        <button id="cap-btn-bridge" class="act-btn" onclick="setCapaFin('bridge')">Capa 2: Puentes entre Pilares</button>
        <button id="cap-btn-trap" class="act-btn" onclick="setCapaFin('trap')">Capa 3: Trampas de Prueba</button>
        <button id="cap-btn-all" class="act-btn" onclick="setCapaFin('all')">Ver las 3 Capas</button>
      </div>
    </div>

    <div class="mec-filters">
      <button class="flt-btn active" onclick="filtrarLecturaFin('all', this)">Toda la Bibliografía (8)</button>
      <button class="flt-btn" onclick="filtrarLecturaFin('F1', this)">F1: Fisher (1)</button>
      <button class="flt-btn" onclick="filtrarLecturaFin('F2', this)">F2: Riesgo / PGU (1)</button>
      <button class="flt-btn" onclick="filtrarLecturaFin('F3', this)">F3: Markowitz / Estadística (2)</button>
      <button class="flt-btn" onclick="filtrarLecturaFin('F4', this)">F4: Hamada / WACC / APV (1)</button>
      <button class="flt-btn" onclick="filtrarLecturaFin('F5', this)">F5: FCL / FCI / Guías (3)</button>
    </div>

    <div class="lec-grid" id="lec-fin-grid"></div>

    <div class="sec-title" style="margin-top:14px;">
      <span>Control de Lectura y Aplicación Cruzada (14 preguntas integradas)</span>
      <div class="btn-bar">
        <span id="qz-fin-score" class="pill-score">Aciertos: 0 / 14</span>
        <button class="act-btn" onclick="toggleSoloErradasFin(this)">Ver Solo Pendientes / Erradas</button>
        <button class="act-btn" onclick="resetQuizFin()">Reiniciar Control</button>
      </div>
    </div>
    <div id="qz-fin-list"></div>
  </div>

  <!-- ====================================================================== -->
  <!-- PANEL 8: GUÍAS OFICIALES RESUELTAS A 60 FPS (CPA CARTERA + FLUJOS XX)  -->
  <!-- ====================================================================== -->
  <div id="panel-guias" class="panel">
    <div class="sec-title">
      <span>Guías Oficiales Resueltas — Teoría de la Cartera (CPA) y Flujos de Caja bajo Incertidumbre</span>
      <div class="btn-bar">
        <button class="act-btn primary" onclick="selGuiaBloque('ej1', this)">Ej. 1: Normal (68-95-99,7%)</button>
        <button class="act-btn" onclick="selGuiaBloque('ej2', this)">Ej. 2–3: 4 Estados + Cartera</button>
        <button class="act-btn" onclick="selGuiaBloque('ej4', this)">Ej. 4: Probabilidades X e Y</button>
        <button class="act-btn" onclick="selGuiaBloque('ej56', this)">Ej. 5–6: MSFT y Home Depot (12m)</button>
        <button class="act-btn" onclick="selGuiaBloque('ejxx', this)">Guía Flujos: Empresa XX + Planta ±6%</button>
      </div>
    </div>

    <!-- BLOQUE EJ 1: DISTRIBUCIÓN NORMAL -->
    <div id="gb-ej1" class="gb-sec">
      <details class="enun-box" open>
        <summary>
          <span>Guía 2 CPA — Ejercicio 1 (Distribución Normal y Regla Empírica de Rentabilidad Histórica 50 Años)</span>
          <span class="enun-badge">Fórmula: [μ − k·σ , μ + k·σ]</span>
        </summary>
        <div class="enun-body" id="g1-enun"></div>
      </details>
      <div class="sliders-grid" style="grid-template-columns: 1fr 1fr;">
        <div class="sl-card"><div class="sl-head"><span>Rentabilidad Promedio Anual μ (%)</span><span id="g1-mu-v" class="sl-val">14,3%</span></div><input id="g1-mu" type="range" min="2.0" max="30.0" step="0.1" value="14.3" oninput="drawGuiaEj1()" /></div>
        <div class="sl-card"><div class="sl-head"><span>Desviación Estándar Anual σ (%)</span><span id="g1-sd-v" class="sl-val">24,5%</span></div><input id="g1-sd" type="range" min="5.0" max="45.0" step="0.1" value="24.5" oninput="drawGuiaEj1()" /></div>
      </div>
      <div class="kpis">
        <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">Rango ±1σ (68,26%)</div><div id="g1-k1" class="kpi-val">[-10,2% ; 38,8%]</div><div class="kpi-sub">μ ± 1·σ</div></div>
        <div class="kpi" style="border-left-color:#059669;"><div class="kpi-lbl">Rango ±2σ (95,44%)</div><div id="g1-k2" class="kpi-val">[-34,7% ; 63,3%]</div><div class="kpi-sub">μ ± 2·σ</div></div>
        <div class="kpi" style="border-left-color:#EA580C;"><div class="kpi-lbl">Rango ±3σ (99,74%)</div><div id="g1-k3" class="kpi-val">[-59,2% ; 87,8%]</div><div class="kpi-sub">μ ± 3·σ</div></div>
      </div>
      <div class="svg-box"><svg id="svg-g1-gauss" viewBox="0 0 980 320"></svg></div>
    </div>

    <!-- BLOQUE EJ 2 Y 3: 4 ESTADOS EQUIPROBABLES + CARTERA 30/70 + RENDIMIENTO SIMPLE -->
    <div id="gb-ej2" class="gb-sec" style="display:none;">
      <details class="enun-box" open>
        <summary>
          <span>Guía 2 CPA — Ejercicio 2 (4 Estados Económicos Equiprobables + Cartera 30% A / 70% B) y Ejercicio 3</span>
          <span class="enun-badge">p = 0,25 cada estado · Var(p) = wA²σA² + wB²σB² + 2wAwB·Cov</span>
        </summary>
        <div class="enun-body">
          Estados equiprobables (25% c/u): <b>Depresión</b> (A: -20%, B: 5%), <b>Recesión</b> (A: 10%, B: 20%), <b>Normalidad</b> (A: 30%, B: -12%) y <b>Prosperidad</b> (A: 50%, B: 9%).
          Mueve el peso <b>w<sub>A</sub></b> (por defecto <b>30% A / 70% B</b>) para ver cómo cambia el riesgo y el retorno de la cartera gracias a la correlación negativa (<b>ρ = -0,1639</b>).
        </div>
      </details>
      <div class="sliders-grid" style="grid-template-columns: 1.5fr 1fr 1fr;">
        <div class="sl-card">
          <div class="sl-head"><span>Peso Activo A (wA) / B (wB = 1 − wA)</span><span id="g2-wa-v" class="sl-val">30% A / 70% B</span></div>
          <input id="g2-wa" type="range" min="0" max="100" step="1" value="30" oninput="drawGuiaEj2()" />
          <div class="btn-bar" style="margin-top:6px;">
            <button class="act-btn primary" onclick="setG2Peso(30)">Caso Guía (30% A / 70% B)</button>
            <button class="act-btn" onclick="setG2Peso(21)">Mínima Varianza (21% A)</button>
          </div>
        </div>
        <div class="sl-card"><div class="sl-head"><span>Ej. 3 — Inversión Inicial ($)</span><span id="g3-i0-v" class="sl-val">$600</span></div><input id="g3-i0" type="range" min="100" max="2000" step="50" value="600" oninput="drawGuiaEj2()" /></div>
        <div class="sl-card"><div class="sl-head"><span>Ej. 3 — Ingreso Efectivo Año 1 ($)</span><span id="g3-f1-v" class="sl-val">$1.400</span></div><input id="g3-f1" type="range" min="200" max="3000" step="50" value="1400" oninput="drawGuiaEj2()" /></div>
      </div>
      <div class="kpis">
        <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">Activo A (Esperado / σ)</div><div class="kpi-val">17,50% | 25,86%</div><div class="kpi-sub">Var(A) = 0,066875</div></div>
        <div class="kpi" style="border-left-color:#059669;"><div class="kpi-lbl">Activo B (Esperado / σ)</div><div class="kpi-val">5,50% | 11,50%</div><div class="kpi-sub">Var(B) = 0,013225</div></div>
        <div class="kpi" style="border-left-color:#7C3AED;"><div class="kpi-lbl">Covarianza y Correlación</div><div class="kpi-val">ρ = −0,1639</div><div class="kpi-sub">Cov(A,B) = −0,004875</div></div>
        <div class="kpi" style="border-left-color:#DC2626;"><div class="kpi-lbl">Cartera Activa (Rp / σp)</div><div id="g2-k-p" class="kpi-val">9,10% | 10,22%</div><div id="g2-k-vp" class="kpi-sub">Var(p) = 0,010451</div></div>
      </div>
      <div class="g-subgrid">
        <div id="g2-tbl-box"></div>
        <div class="svg-box"><svg id="svg-g2-port" viewBox="0 0 460 280"></svg></div>
      </div>
      <div id="g2-sol" class="sol-box"></div>
    </div>

    <!-- BLOQUE EJ 4: DISTRIBUCIÓN DE PROBABILIDADES ACCIÓN X E Y -->
    <div id="gb-ej4" class="gb-sec" style="display:none;">
      <details class="enun-box" open>
        <summary>
          <span>Guía 2 CPA — Ejercicio 4 (Distribución de Probabilidades Acción X e Acción Y)</span>
          <span class="enun-badge">E(R) = ∑ pi·Ri · Cov = ∑ pi·(Rx − E[Rx])(Ry − E[Ry])</span>
        </summary>
        <div class="enun-body">
          Distribución discreta de 5 escenarios con probabilidades <b>p = [0,1 ; 0,3 ; 0,3 ; 0,2 ; 0,1]</b>. Observa que la correlación resultante es casi nula (<b>ρ = +0,0034</b>), lo que evidencia independencia lineal casi total entre X e Y (ideal para diversificación).
        </div>
      </details>
      <div class="kpis">
        <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">a. Rendimientos Esperados</div><div class="kpi-val">Rx=4,80% | Ry=3,30%</div><div class="kpi-sub">∑ pi · Ri</div></div>
        <div class="kpi" style="border-left-color:#059669;"><div class="kpi-lbl">b. Varianzas y Desviación</div><div class="kpi-val">σX=7,60% | σY=6,12%</div><div class="kpi-sub">VarX=0,005776 | VarY=0,003741</div></div>
        <div class="kpi" style="border-left-color:#7C3AED;"><div class="kpi-lbl">c. Covarianza Cov(X,Y)</div><div class="kpi-val">+0,000016</div><div class="kpi-sub">Casi cero (0,0016%²)</div></div>
        <div class="kpi" style="border-left-color:#DC2626;"><div class="kpi-lbl">d. Correlación ρ(X,Y)</div><div class="kpi-val">+0,0034</div><div class="kpi-sub">Activos casi incorrelacionados</div></div>
      </div>
      <div id="g4-tbl-box"></div>
      <div class="sol-box">
        <b>Desarrollo exacto:</b> E(R<sub>X</sub>) = 0,1(−10%)+0,3(0%)+0,3(6%)+0,2(10%)+0,1(20%) = <b>4,80%</b> | E(R<sub>Y</sub>) = 0,1(4%)+0,3(8%)+0,3(0%)+0,2(−5%)+0,1(15%) = <b>3,30%</b>.<br/>
        <b>Cov(X,Y)</b> = +0,000016 &nbsp;⇒&nbsp; <b>ρ(X,Y)</b> = 0,000016 / (0,07600 × 0,06116) = <b>+0,0034</b> (al ser cercano a 0, combinar X e Y reduce drásticamente el riesgo de cartera).
      </div>
    </div>

    <!-- BLOQUE EJ 5 Y 6: SERIES 12 MESES MSFT Y HOME DEPOT VS S&P 500 -->
    <div id="gb-ej56" class="gb-sec" style="display:none;">
      <div class="mec-filters" style="margin-bottom:8px;">
        <button id="g56-btn-msft" class="flt-btn active" onclick="setCaso56('msft')">Ejercicio 5: Microsoft (MSFT) vs. S&amp;P 500 (12 meses)</button>
        <button id="g56-btn-hd" class="flt-btn" onclick="setCaso56('hd')">Ejercicio 6: Home Depot (HD) vs. S&amp;P 500 (1995, 12 meses)</button>
        <button id="g56-btn-mues" class="flt-btn active" onclick="setDdof56(1)">Convención Muestral (n − 1 = 11)</button>
        <button id="g56-btn-pob" class="flt-btn" onclick="setDdof56(0)">Convención Poblacional (n = 12)</button>
      </div>
      <div class="kpis">
        <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">a. Promedio Mensual (M / Acción)</div><div id="g56-k-med" class="kpi-val">-0,09% | 3,76%</div><div class="kpi-sub">Media aritmética 12 meses</div></div>
        <div class="kpi" style="border-left-color:#059669;"><div class="kpi-lbl">b. Varianza y σ Mensual</div><div id="g56-k-var" class="kpi-val">σM=3,06% | σA=7,24%</div><div id="g56-k-var2" class="kpi-sub">Var_M | Var_Acción</div></div>
        <div class="kpi" style="border-left-color:#7C3AED;"><div class="kpi-lbl">c. Covarianza Cov(M, Acción)</div><div id="g56-k-cov" class="kpi-val">+0,001270</div><div id="g56-k-div" class="kpi-sub">Divisor n−1 = 11</div></div>
        <div class="kpi" style="border-left-color:#DC2626;"><div class="kpi-lbl">d. Correlación ρ y Beta (β)</div><div id="g56-k-rho" class="kpi-val">ρ=0,573 | β=1,35</div><div class="kpi-sub">β = Cov(i,M) / Var(M)</div></div>
      </div>
      <div class="g-subgrid">
        <div id="g56-tbl-box"></div>
        <div class="svg-box"><svg id="svg-g56-scat" viewBox="0 0 470 330"></svg></div>
      </div>
      <div id="g56-sol" class="sol-box"></div>
    </div>

    <!-- BLOQUE GUÍA FLUJOS: EJ 1 EMPRESA XX + EJ 2 PLANTA PILOTO ULAGOS ±6% -->
    <div id="gb-ejxx" class="gb-sec" style="display:none;">
      <details class="enun-box" open>
        <summary>
          <span>Guía Flujos de Caja — Ej. 1 (Empresa XX Farmacéutico Probabilístico) y Ej. 2 (Planta Piloto ULagos $130M)</span>
          <span class="enun-badge">Tasa Ajustada por Riesgo: k = Rf + Prima = 8% + 2% = 10%</span>
        </summary>
        <div class="enun-body" id="gxx-enun"></div>
      </details>
      <div class="sliders-grid" style="grid-template-columns: 1fr 1fr 1fr;">
        <div class="sl-card"><div class="sl-head"><span>Inversión Inicial I0 ($)</span><span id="gxx-i0-v" class="sl-val">$1.000.000</span></div><input id="gxx-i0" type="range" min="600000" max="1500000" step="25000" value="1000000" oninput="drawGuiaXX()" /></div>
        <div class="sl-card"><div class="sl-head"><span>Tasa Libre de Riesgo Rf (%)</span><span id="gxx-rf-v" class="sl-val">8,0%</span></div><input id="gxx-rf" type="range" min="2.0" max="14.0" step="0.5" value="8.0" oninput="drawGuiaXX()" /></div>
        <div class="sl-card"><div class="sl-head"><span>Ajuste por Riesgo / Prima (%)</span><span id="gxx-pr-v" class="sl-val">2,0%</span></div><input id="gxx-pr" type="range" min="0.0" max="12.0" step="0.5" value="2.0" oninput="drawGuiaXX()" /></div>
      </div>
      <div class="kpis">
        <div class="kpi" style="border-left-color:#1D4ED8;"><div class="kpi-lbl">Flujos Esperados E(F1, F2, F3)</div><div class="kpi-val">$400k | $700k | $300k</div><div class="kpi-sub">∑ pi · Fi (guion '-' = $0)</div></div>
        <div class="kpi" style="border-left-color:#15803D;"><div class="kpi-lbl">VAN del Proyecto (a k = Rf+Prima)</div><div id="gxx-k-van" class="kpi-val">+$167.543</div><div id="gxx-k-k" class="kpi-sub">Tasa k = 10,0%</div></div>
        <div class="kpi" style="border-left-color:#DC2626;"><div class="kpi-lbl">TIR del Proyecto</div><div id="gxx-k-tir" class="kpi-val">19,55%</div><div id="gxx-k-dec" class="kpi-sub">ACEPTAR (TIR &gt; k)</div></div>
      </div>
      <div class="svg-box"><svg id="svg-gxx" viewBox="0 0 980 265"></svg></div>
      <div id="gxx-sol" class="sol-box"></div>
      <div class="sol-box" style="border-left-color:#1D4ED8;">
        <b>Guía Flujos de Caja — Ejercicio 2 (Planta Piloto ULagos $130M):</b> Para resolver automáticamente los 5 incisos completos (FCL, Tabla Amortización 7,5% a 5 años, FCI, <b>Sensibilidad +6% ingresos</b> y <b>VAN Esperado 55% original / 45% ingreso −6%</b>), abre la <b>Vista 3 (Evaluador Corporativo)</b> en el menú lateral, selecciona <b>Caso 2 — Guía P2 (130M)</b> y revisa la <b>Hoja5 (Sensibilidad)</b> donde ya viene calibrado el preset exacto <b>±6% y 55% / 45%</b>.
      </div>
    </div>
  </div>
</div>

<script>
const NS = "http://www.w3.org/2000/svg";
function fmtInt(n) { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "."); }
function fmtDec(n, d=1) {
  const s = Number(n).toFixed(d).split(".");
  return s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (d > 0 ? "," + s[1] : "");
}
function el(tag, attrs, parent) {
  const node = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v);
  if (parent) parent.appendChild(node);
  return node;
}
function addDefs(svg) {
  const defs = el("defs", {}, svg);
  for (const [id, col] of [["arr-red","#DC2626"],["arr-blue","#1D4ED8"],["arr-green","#15803D"],["arr-orange","#EA580C"],["arr-dark","#0F172A"]]) {
    const m = el("marker", { id, viewBox: "0 0 10 10", refX: "8", refY: "5", markerWidth: "7", markerHeight: "7", orient: "auto-start-reverse" }, defs);
    el("path", { d: "M 0 1 L 10 5 L 0 9 z", fill: col }, m);
  }
}
function drawArrow(svg, x1, y1, x2, y2, color, markerId, label, lx, ly, anchor="middle") {
  if (Math.hypot(x2 - x1, y2 - y1) < 6) return;
  el("line", { x1, y1, x2, y2, stroke: color, "stroke-width": "2.6", "marker-end": `url(#${markerId})` }, svg);
  if (label) {
    const bgW = Math.max(54, label.length * 6.5 + 10);
    const rx = anchor === "middle" ? lx - bgW / 2 : (anchor === "start" ? lx - 4 : lx - bgW + 4);
    el("rect", { x: rx, y: ly - 12, width: bgW, height: 17, rx: 4, fill: "rgba(255,255,255,0.94)", stroke: color, "stroke-width": "1" }, svg);
    const t = el("text", { x: lx, y: ly, fill: color, "font-size": "10.8", "font-weight": "700", "text-anchor": anchor }, svg);
    t.textContent = label;
  }
}
function setDelta(id, diff, dec=1, suf="") {
  const node = document.getElementById(id);
  if (!node) return;
  if (Math.abs(diff) < 1e-4) { node.textContent = ""; node.className = "sl-delta d-eq"; return; }
  node.textContent = `(${diff > 0 ? "↑ +" : "↓ -"}${fmtDec(Math.abs(diff), dec)}${suf})`;
  node.className = "sl-delta " + (diff > 0 ? "d-up" : "d-down");
}
function openTab(name, btn) {
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.getElementById("panel-" + name).classList.add("active");
  btn.classList.add("active");
  if (name === "fisher") drawFisher();
  if (name === "riesgo") drawRiesgo();
  if (name === "markowitz") drawMarkowitz();
  if (name === "hamada") drawHamada();
  if (name === "vantir") drawVanTir();
  if (name === "mecanica") renderMecanica();
  if (name === "lectura") { drawMapaFin(); renderLecturaFin(); renderQuizFin(); }
  if (name === "guias") { drawGuiaEj1(); drawGuiaEj2(); renderGuiaEj4(); drawGuia56(); drawGuiaXX(); }
}
function jumpToTab(name) {
  const btns = Array.from(document.querySelectorAll(".top-tabs .tab-btn"));
  const target = btns.find(b => (b.getAttribute("onclick") || "").includes("'" + name + "'"));
  if (target) {
    openTab(name, target);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

// ============================================================================
// 1. SEPARACIÓN DE FISHER (60 FPS)
// ============================================================================
let ghostFs = { y0: 120, rf: 10.0, a: 20, al: 0.45 };
let animFsId = null;

function solveFisher(y0, rfPct, A, al) {
  const rf = rfPct / 100;
  const i0 = Math.min(y0, Math.pow(A / (2 * (1 + rf)), 2));
  const c0p = y0 - i0;
  const c1p = A * Math.sqrt(i0);
  const van = -i0 + c1p / (1 + rf);
  const w0 = y0 + van;
  const w1 = w0 * (1 + rf);
  const c0c = al * w0;
  const c1c = (1 - al) * w1;
  return { i0, c0p, c1p, van, w0, w1, c0c, c1c, prestamo: c0c - c0p, rf };
}
function fijarGhostFisher() {
  ghostFs = { y0: +document.getElementById("fs-y0").value, rf: +document.getElementById("fs-rf").value, a: +document.getElementById("fs-a").value, al: +document.getElementById("fs-al").value };
  drawFisher();
}
function presetFisher(al) {
  fijarGhostFisher();
  document.getElementById("fs-al").value = al;
  drawFisher();
}
function animarFisher() {
  if (animFsId) cancelAnimationFrame(animFsId);
  document.getElementById("fs-rf").value = 20.0;
  fijarGhostFisher();
  const t0 = performance.now(), dur = 1800;
  function step(now) {
    const u = Math.min(1, (now - t0) / dur);
    const ease = 1 - Math.pow(1 - u, 3);
    document.getElementById("fs-rf").value = (20.0 - 14.0 * ease).toFixed(1);
    drawFisher();
    if (u < 1) animFsId = requestAnimationFrame(step);
  }
  animFsId = requestAnimationFrame(step);
}
function drawFisher() {
  const y0 = +document.getElementById("fs-y0").value, rf = +document.getElementById("fs-rf").value;
  const a = +document.getElementById("fs-a").value, al = +document.getElementById("fs-al").value;
  document.getElementById("fs-y0-v").textContent = "$" + fmtInt(y0) + "M";
  document.getElementById("fs-rf-v").textContent = fmtDec(rf, 1) + "%";
  document.getElementById("fs-a-v").textContent = fmtInt(a);
  document.getElementById("fs-al-v").textContent = fmtDec(al, 2);
  setDelta("fs-rf-d", rf - ghostFs.rf, 1, "%");

  const cur = solveFisher(y0, rf, a, al), gho = solveFisher(ghostFs.y0, ghostFs.rf, ghostFs.a, ghostFs.al);
  const posTxt = cur.prestamo > 0.5 ? `Pide prestado $${fmtDec(cur.prestamo,1)}M en t=0` : (cur.prestamo < -0.5 ? `Presta/ahorra $${fmtDec(Math.abs(cur.prestamo),1)}M en t=0` : "Autarquía financiera");

  document.getElementById("fs-enunciado").innerHTML =
    `Un accionista dispone de una dotación inicial <b>Y<sub>0</sub> = $${fmtInt(y0)}M</b> y acceso a proyectos físicos con curva de transformación <b>C<sub>1</sub> = ${a}·√I<sub>0</sub></b>, en un mercado de capitales perfecto con tasa <b>r<sub>f</sub> = ${fmtDec(rf,1)}%</b>. ` +
    `<b>Paso 1 (Objetivo):</b> el gerente invierte <b>I<sub>0</sub>* = $${fmtDec(cur.i0,1)}M</b> hasta que RMgI = r<sub>f</sub>, maximizando la riqueza en <b>W<sub>0</sub>* = $${fmtDec(cur.w0,1)}M</b> (VAN = +$${fmtDec(cur.van,1)}M). ` +
    `<b>Paso 2 (Subjetivo):</b> con preferencia α = <b>${fmtDec(al,2)}</b>, el dueño alcanza C* operando en el mercado financiero (<b>${posTxt}</b>).`;

  document.getElementById("fs-k-i0").textContent = `$${fmtDec(cur.i0, 1)}M`;
  document.getElementById("fs-k-p").textContent = `C0(P*) = $${fmtDec(cur.c0p, 1)}M`;
  document.getElementById("fs-k-van").textContent = `+$${fmtDec(cur.van, 1)}M`;
  document.getElementById("fs-k-w0").textContent = `W0* = $${fmtDec(cur.w0, 1)}M`;
  document.getElementById("fs-k-c").textContent = `$${fmtDec(cur.c0c, 1)}M | $${fmtDec(cur.c1c, 1)}M`;
  document.getElementById("fs-k-pos").textContent = cur.prestamo > 0.5 ? "DEUDOR t=0" : (cur.prestamo < -0.5 ? "AHORRADOR t=0" : "NEUTRO");
  document.getElementById("fs-k-pos2").textContent = posTxt;

  document.getElementById("fs-sol").innerHTML =
    `<b>Separación de Fisher:</b> Cambia α (impaciencia) y verifica que <b>P* (I<sub>0</sub>*=$${fmtDec(cur.i0,1)}M; VAN=$${fmtDec(cur.van,1)}M) NO se mueve</b>: ` +
    `la decisión de inversión es delegable al administrador, mientras C* se desliza sobre la recta de pendiente −(1+r<sub>f</sub>) = −${fmtDec(1 + cur.rf, 3)}.`;

  const svg = document.getElementById("svg-fisher");
  svg.innerHTML = "";
  addDefs(svg);
  const M = { l: 64, r: 30, t: 26, b: 46 }, W = 980, H = 395;
  const maxX = Math.max(cur.w0, gho.w0, y0) * 1.15;
  const maxY = Math.max(cur.w1, gho.w1, a * Math.sqrt(y0)) * 1.15;
  const sx = x => M.l + (x / maxX) * (W - M.l - M.r);
  const sy = y => H - M.b - (y / maxY) * (H - M.t - M.b);

  for (let i = 0; i <= 5; i++) {
    const xv = (maxX / 5) * i, yv = (maxY / 5) * i;
    el("line", { x1: M.l, y1: sy(yv), x2: W - M.r, y2: sy(yv), stroke: "#E2E8F0" }, svg);
    el("line", { x1: sx(xv), y1: M.t, x2: sx(xv), y2: H - M.b, stroke: "#F1F5F9" }, svg);
    const ty = el("text", { x: M.l - 8, y: sy(yv) + 4, fill: "#475569", "font-size": "11", "text-anchor": "end" }, svg);
    ty.textContent = "$" + fmtInt(yv) + "M";
    const tx = el("text", { x: sx(xv), y: H - M.b + 16, fill: "#475569", "font-size": "11", "text-anchor": "middle" }, svg);
    tx.textContent = "$" + fmtInt(xv) + "M";
  }
  el("line", { x1: M.l, y1: H - M.b, x2: W - M.r, y2: H - M.b, stroke: "#334155", "stroke-width": "1.6" }, svg);
  el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, stroke: "#334155", "stroke-width": "1.6" }, svg);

  // Fantasma recta de mercado si cambió
  if (Math.abs(cur.w0 - gho.w0) > 1.5 || Math.abs(cur.rf - gho.rf) > 0.005) {
    el("line", { x1: sx(0), y1: sy(gho.w1), x2: sx(gho.w0), y2: sy(0), stroke: "#94A3B8", "stroke-width": "1.6", "stroke-dasharray": "5,4" }, svg);
    el("circle", { cx: sx(gho.c0p), cy: sy(gho.c1p), r: 5, fill: "#94A3B8" }, svg);
  }

  // Frontera productiva
  const fpPts = [];
  for (let k = 0; k <= 80; k++) {
    const iv = (y0 / 80) * k;
    fpPts.push(`${sx(y0 - iv).toFixed(1)},${sy(a * Math.sqrt(iv)).toFixed(1)}`);
  }
  el("polyline", { points: fpPts.join(" "), fill: "none", stroke: "#1D4ED8", "stroke-width": "3.2" }, svg);

  // Recta mercado de capitales actual
  el("line", { x1: sx(0), y1: sy(cur.w1), x2: sx(cur.w0), y2: sy(0), stroke: "#DC2626", "stroke-width": "2.4", "stroke-dasharray": "7,4" }, svg);

  // Curva de indiferencia tangente en C*
  const uStar = Math.pow(Math.max(cur.c0c, 1), al) * Math.pow(Math.max(cur.c1c, 1), 1 - al);
  const indPts = [];
  for (let k = 0; k <= 70; k++) {
    const cx = Math.max(cur.c0c * 0.35, 3) + (cur.w0 * 0.95) * (k / 70);
    const cy = Math.pow(uStar / Math.pow(cx, al), 1 / (1 - al));
    if (cx <= maxX && cy <= maxY) indPts.push(`${sx(cx).toFixed(1)},${sy(cy).toFixed(1)}`);
  }
  if (indPts.length > 2) el("polyline", { points: indPts.join(" "), fill: "none", stroke: "#059669", "stroke-width": "2.8" }, svg);

  // Flecha VAN en eje X (Y0 -> W0*)
  drawArrow(svg, sx(y0), sy(0) - 10, sx(cur.w0), sy(0) - 10, "#15803D", "arr-green", `VAN +$${fmtDec(cur.van,1)}M`, (sx(y0) + sx(cur.w0)) / 2, sy(0) - 20);
  // Flecha financiera P* -> C*
  if (Math.hypot(sx(cur.c0c) - sx(cur.c0p), sy(cur.c1c) - sy(cur.c1p)) > 16) {
    drawArrow(svg, sx(cur.c0p), sy(cur.c1p), sx(cur.c0c), sy(cur.c1c), "#EA580C", "arr-orange", cur.prestamo > 0 ? "Se endeuda →" : "← Presta", (sx(cur.c0p) + sx(cur.c0c)) / 2, (sy(cur.c1p) + sy(cur.c1c)) / 2 - 12);
  }

  el("circle", { cx: sx(cur.c0p), cy: sy(cur.c1p), r: 7, fill: "#1D4ED8", stroke: "#FFFFFF", "stroke-width": "2" }, svg);
  const pNearLeft = sx(cur.c0p) < 230;
  const tP = el("text", { x: pNearLeft ? sx(cur.c0p) + 12 : sx(cur.c0p) - 10, y: pNearLeft ? sy(cur.c1p) - 8 : sy(cur.c1p) - 10, fill: "#1E3A8A", "font-size": "11.5", "font-weight": "800", "text-anchor": pNearLeft ? "start" : "end" }, svg);
  tP.textContent = "P* (Óptimo Productivo)";
  el("circle", { cx: sx(cur.c0c), cy: sy(cur.c1c), r: 7.5, fill: "#059669", stroke: "#FFFFFF", "stroke-width": "2" }, svg);
  const tC = el("text", { x: sx(cur.c0c) + 10, y: sy(cur.c1c) - 8, fill: "#065F46", "font-size": "11.5", "font-weight": "800", "text-anchor": "start" }, svg);
  tC.textContent = "C* (Óptimo Consumo)";
}

// ============================================================================
// 2. ACTITUDES FRENTE AL RIESGO Y JUEGO JUSTO (60 FPS)
// ============================================================================
function presetRiesgo(g) { document.getElementById("rk-g").value = g; drawRiesgo(); }
function hacerJuegoJusto() {
  const w1 = +document.getElementById("rk-w1").value, w2 = +document.getElementById("rk-w2").value, p = +document.getElementById("rk-p").value / 100;
  document.getElementById("rk-w0").value = Math.round((1 - p) * w1 + p * w2);
  drawRiesgo();
}
function drawRiesgo() {
  const g = +document.getElementById("rk-g").value;
  const w1 = +document.getElementById("rk-w1").value, w2 = +document.getElementById("rk-w2").value;
  const p = +document.getElementById("rk-p").value / 100;
  const w0 = +document.getElementById("rk-w0").value;

  document.getElementById("rk-g-v").textContent = fmtDec(g, 2);
  document.getElementById("rk-w1-v").textContent = "$" + fmtInt(w1) + "M";
  document.getElementById("rk-w2-v").textContent = "$" + fmtInt(w2) + "M";
  document.getElementById("rk-p-v").textContent = Math.round(p * 100) + "%";
  document.getElementById("rk-w0-v").textContent = "$" + fmtInt(w0) + "M";

  const fnU = w => Math.pow(Math.max(w, 1e-4), g);
  const fnInv = u => Math.pow(Math.max(u, 1e-4), 1 / g);

  const ew = (1 - p) * w1 + p * w2;
  const u1 = fnU(w1), u2 = fnU(w2);
  const eu = (1 - p) * u1 + p * u2;
  const uEw = fnU(ew);
  const ec = fnInv(eu);
  const pi = ew - ec;
  const esJJ = Math.abs(ew - w0) < 0.8;
  const actLbl = g < 0.96 ? "Averso al Riesgo (U'' < 0)" : (g > 1.04 ? "Amante del Riesgo (U'' > 0)" : "Neutral al Riesgo (U'' = 0)");
  const uW0 = fnU(w0);
  const dec = eu > uW0 + 1e-4 ? "ACEPTA EL JUEGO" : (Math.abs(eu - uW0) <= 1e-4 ? "INDIFERENTE" : "RECHAZA (Prefiere W0)");

  document.getElementById("rk-enunciado").innerHTML =
    `Un inversionista con perfil <b>${actLbl}</b> enfrenta una lotería que paga <b>W<sub>1</sub> = $${w1}M</b> (prob. ${Math.round((1-p)*100)}%) o <b>W<sub>2</sub> = $${w2}M</b> (prob. ${Math.round(p*100)}%), ` +
    `con valor esperado <b>E(W) = $${fmtDec(ew,1)}M</b> frente a una riqueza segura alternativa <b>W<sub>0</sub> = $${w0}M</b> (${esJJ ? "<b>Juego Justo</b>" : "Juego no justo"}). ` +
    `Su <b>Equivalente Cierto</b> es <b>EC = $${fmtDec(ec,1)}M</b> y su <b>Prima por Riesgo</b> es <b>π = ${pi >= 0 ? "+" : "-"}$${fmtDec(Math.abs(pi),1)}M</b>.`;

  document.getElementById("rk-k-ew").textContent = `$${fmtDec(ew, 1)}M`;
  document.getElementById("rk-k-jj").textContent = esJJ ? "Juego Justo (E[W]=W0)" : `Dif vs W0: ${ew - w0 >= 0 ? "+" : ""}$${fmtDec(ew - w0, 1)}M`;
  document.getElementById("rk-k-ec").textContent = `$${fmtDec(ec, 1)}M`;
  document.getElementById("rk-k-pi").textContent = `${pi >= 0 ? "+" : "-"}$${fmtDec(Math.abs(pi), 1)}M`;
  document.getElementById("rk-k-act").textContent = actLbl;
  document.getElementById("rk-k-dec").textContent = dec;
  document.getElementById("rk-k-dec2").textContent = `E[U(W)]=${fmtDec(eu,2)} vs U(W0)=${fmtDec(uW0,2)}`;

  const svg = document.getElementById("svg-riesgo");
  svg.innerHTML = "";
  addDefs(svg);
  const M = { l: 64, r: 30, t: 26, b: 46 }, W = 980, H = 385;
  const maxX = w2 * 1.12, maxY = fnU(maxX) * 1.08;
  const sx = x => M.l + (x / maxX) * (W - M.l - M.r);
  const sy = y => H - M.b - (y / maxY) * (H - M.t - M.b);

  for (let i = 0; i <= 5; i++) {
    const xv = (maxX / 5) * i, yv = (maxY / 5) * i;
    el("line", { x1: M.l, y1: sy(yv), x2: W - M.r, y2: sy(yv), stroke: "#E2E8F0" }, svg);
    const tx = el("text", { x: sx(xv), y: H - M.b + 16, fill: "#475569", "font-size": "11", "text-anchor": "middle" }, svg);
    tx.textContent = "$" + fmtInt(xv) + "M";
  }
  el("line", { x1: M.l, y1: H - M.b, x2: W - M.r, y2: H - M.b, stroke: "#334155", "stroke-width": "1.6" }, svg);
  el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, stroke: "#334155", "stroke-width": "1.6" }, svg);

  const uPts = [];
  for (let k = 1; k <= 90; k++) {
    const wx = (maxX / 90) * k;
    uPts.push(`${sx(wx).toFixed(1)},${sy(fnU(wx)).toFixed(1)}`);
  }
  el("polyline", { points: uPts.join(" "), fill: "none", stroke: "#1D4ED8", "stroke-width": "3.2" }, svg);
  // Cuerda entre W1 y W2
  el("line", { x1: sx(w1), y1: sy(u1), x2: sx(w2), y2: sy(u2), stroke: "#64748B", "stroke-width": "2", "stroke-dasharray": "6,4" }, svg);
  // Verticales a E(W) y EC
  el("line", { x1: sx(ew), y1: sy(0), x2: sx(ew), y2: sy(Math.max(uEw, eu)), stroke: "#94A3B8", "stroke-dasharray": "3,3" }, svg);
  el("line", { x1: sx(ec), y1: sy(0), x2: sx(ec), y2: sy(eu), stroke: "#15803D", "stroke-dasharray": "3,3" }, svg);

  // Flecha horizontal Prima por Riesgo π (EC <-> E(W))
  if (Math.abs(ew - ec) > 2) {
    drawArrow(svg, sx(ec), sy(eu), sx(ew), sy(eu), pi > 0 ? "#DC2626" : "#15803D", pi > 0 ? "arr-red" : "arr-green",
      `Prima π = ${pi >= 0 ? "+" : "-"}$${fmtDec(Math.abs(pi), 1)}M`, (sx(ec) + sx(ew)) / 2, sy(eu) + 22);
  }
  el("circle", { cx: sx(w1), cy: sy(u1), r: 5.5, fill: "#0F172A" }, svg);
  el("circle", { cx: sx(w2), cy: sy(u2), r: 5.5, fill: "#0F172A" }, svg);
  el("circle", { cx: sx(ec), cy: sy(eu), r: 7, fill: "#15803D", stroke: "#FFFFFF", "stroke-width": "2" }, svg);
  el("circle", { cx: sx(ew), cy: sy(eu), r: 6.5, fill: "#DC2626", stroke: "#FFFFFF", "stroke-width": "2" }, svg);
  el("circle", { cx: sx(ew), cy: sy(uEw), r: 6, fill: "#1D4ED8", stroke: "#FFFFFF", "stroke-width": "2" }, svg);
  const tEc = el("text", { x: sx(ec) - 8, y: sy(eu) - 10, fill: "#15803D", "font-size": "11.5", "font-weight": "800", "text-anchor": "end" }, svg);
  tEc.textContent = `EC = $${fmtDec(ec, 1)}M`;
  const tEw = el("text", { x: sx(ew) + 8, y: sy(uEw) - 8, fill: "#1E3A8A", "font-size": "11.5", "font-weight": "800", "text-anchor": "start" }, svg);
  tEw.textContent = `U(E[W])`;
}

// ============================================================================
// 3. MARKOWITZ (252 DÍAS), CORRELACIÓN ρ Y CAPM / SML (60 FPS)
// ============================================================================
let ghostMk = { rho: 0.25, sa: 1.18, sb: 2.05, rf: 5.65 };
let animMkId = null;
const DUPLA13_SML = [
  { nm: "ANDINA-B", b: 0.86, r: 13.1 }, { nm: "CHILE", b: 0.92, r: 16.9 },
  { nm: "CENCOMALLS", b: 1.02, r: 14.6 }, { nm: "PARAUCO", b: 1.08, r: 15.7 }, { nm: "VAPORES", b: 1.38, r: 19.6 }
];

function fijarGhostMarkowitz() {
  ghostMk = { rho: +document.getElementById("mk-rho").value, sa: +document.getElementById("mk-sa").value, sb: +document.getElementById("mk-sb").value, rf: +document.getElementById("mk-rf").value };
  drawMarkowitz();
}
function presetMarkowitz(rho) { fijarGhostMarkowitz(); document.getElementById("mk-rho").value = rho; drawMarkowitz(); }
function animarMarkowitz() {
  if (animMkId) cancelAnimationFrame(animMkId);
  document.getElementById("mk-rho").value = 1.00;
  fijarGhostMarkowitz();
  const t0 = performance.now(), dur = 2000;
  function step(now) {
    const u = Math.min(1, (now - t0) / dur);
    const ease = 1 - Math.pow(1 - u, 2.5);
    document.getElementById("mk-rho").value = (1.00 - 1.60 * ease).toFixed(2);
    drawMarkowitz();
    if (u < 1) animMkId = requestAnimationFrame(step);
  }
  animMkId = requestAnimationFrame(step);
}
function drawMarkowitz() {
  const rho = +document.getElementById("mk-rho").value;
  const wa = +document.getElementById("mk-wa").value / 100, wb = 1 - wa;
  const saD = +document.getElementById("mk-sa").value / 100, sbD = +document.getElementById("mk-sb").value / 100;
  const rf = +document.getElementById("mk-rf").value / 100;

  document.getElementById("mk-rho-v").textContent = fmtDec(rho, 2);
  document.getElementById("mk-wa-v").textContent = Math.round(wa * 100) + "%";
  document.getElementById("mk-sa-v").textContent = fmtDec(saD * 100, 2) + "%";
  document.getElementById("mk-sb-v").textContent = fmtDec(sbD * 100, 2) + "%";
  document.getElementById("mk-rf-v").textContent = fmtDec(rf * 100, 2) + "%";
  setDelta("mk-rho-d", rho - ghostMk.rho, 2);

  const sq252 = Math.sqrt(252);
  const sA = saD * sq252, sB = sbD * sq252;
  const rA = 0.169, rB = 0.196; // Retornos anualizados ref. CHILE vs VAPORES
  const port = (w, rh) => {
    const er = w * rA + (1 - w) * rB;
    const vr = Math.max(1e-8, w * w * sA * sA + (1 - w) * (1 - w) * sB * sB + 2 * w * (1 - w) * sA * sB * rh);
    return { er, sd: Math.sqrt(vr) };
  };

  let bestG = { sd: 99, w: 0.5 }, bestT = { sh: -99, w: 0.5 };
  const curve = [], ghostCurve = [];
  for (let k = 0; k <= 100; k++) {
    const w = k / 100;
    const p = port(w, rho);
    const sh = (p.er - rf) / p.sd;
    if (p.sd < bestG.sd) bestG = { ...p, w };
    if (sh > bestT.sh) bestT = { ...p, w, sh };
    curve.push(p);
    ghostCurve.push(port(w, ghostMk.rho));
  }
  const curP = port(wa, rho);
  const linSd = wa * sA + wb * sB;
  const ahorroRiesgo = (curP.sd - linSd) * 100;

  document.getElementById("mk-enunciado").innerHTML =
    `Anualizando a <b>252 días bursátiles</b> (σ<sub>anual</sub> = σ<sub>d</sub>·√252): <b>CHILE</b> tiene σ<sub>A</sub> = <b>${fmtDec(sA*100,1)}%</b> y <b>VAPORES</b> tiene σ<sub>B</sub> = <b>${fmtDec(sB*100,1)}%</b>. ` +
    `Con correlación <b>ρ = ${fmtDec(rho,2)}</b> y capital del Taller <b>$65.000.000</b> (BCP/BTP 5 años R<sub>f</sub> = ${fmtDec(rf*100,2)}%), el efecto diversificación reduce el riesgo de tu cartera en <b>${fmtDec(Math.abs(ahorroRiesgo),1)} pp</b> respecto a la línea recta (ρ = +1).`;

  document.getElementById("mk-k-gmvp").textContent = `σ = ${fmtDec(bestG.sd * 100, 1)}%`;
  document.getElementById("mk-k-gmvp2").textContent = `E(R)=${fmtDec(bestG.er * 100, 1)}% (wA=${Math.round(bestG.w * 100)}%)`;
  document.getElementById("mk-k-tan").textContent = `Sharpe = ${fmtDec(bestT.sh, 2)}`;
  document.getElementById("mk-k-tan2").textContent = `E(R)=${fmtDec(bestT.er * 100, 1)}% | σ=${fmtDec(bestT.sd * 100, 1)}%`;
  document.getElementById("mk-k-cur").textContent = `E(R) = ${fmtDec(curP.er * 100, 1)}%`;
  document.getElementById("mk-k-cur2").textContent = `σ=${fmtDec(curP.sd * 100, 1)}% ($${fmtDec(wa*65,1)}M / $${fmtDec(wb*65,1)}M)`;
  document.getElementById("mk-k-div").textContent = `${fmtDec(ahorroRiesgo, 1)} pp`;

  const svg = document.getElementById("svg-markowitz");
  svg.innerHTML = "";
  addDefs(svg);

  // Izquierda: Frontera Eficiente + CML
  const M = { l: 55, r: 445, t: 28, b: 46 }, W = 980, H = 390;
  const maxS = Math.max(sA, sB, 0.35) * 1.18, maxR = 0.25;
  const sx = s => M.l + (s / maxS) * (W - M.l - M.r);
  const sy = r => H - M.b - (r / maxR) * (H - M.t - M.b);

  for (let i = 0; i <= 5; i++) {
    const rv = (maxR / 5) * i, sv = (maxS / 5) * i;
    el("line", { x1: M.l, y1: sy(rv), x2: W - M.r, y2: sy(rv), stroke: "#E2E8F0" }, svg);
    const ty = el("text", { x: M.l - 7, y: sy(rv) + 4, fill: "#475569", "font-size": "10.5", "text-anchor": "end" }, svg);
    ty.textContent = fmtDec(rv * 100, 0) + "%";
    const tx = el("text", { x: sx(sv), y: H - M.b + 16, fill: "#475569", "font-size": "10.5", "text-anchor": "middle" }, svg);
    tx.textContent = fmtDec(sv * 100, 0) + "%";
  }
  el("line", { x1: M.l, y1: H - M.b, x2: W - M.r, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);
  el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);

  // Fantasma frontera anterior
  if (Math.abs(rho - ghostMk.rho) > 0.02) {
    el("polyline", { points: ghostCurve.map(p => `${sx(p.sd).toFixed(1)},${sy(p.er).toFixed(1)}`).join(" "), fill: "none", stroke: "#94A3B8", "stroke-width": "1.8", "stroke-dasharray": "5,4" }, svg);
  }
  // Línea CML tangente desde Rf
  const sCmlEnd = Math.min(maxS, (maxR - rf) / Math.max(bestT.sh, 0.05));
  el("line", { x1: sx(0), y1: sy(rf), x2: sx(sCmlEnd), y2: sy(rf + bestT.sh * sCmlEnd), stroke: "#D97706", "stroke-width": "2.2", "stroke-dasharray": "6,4" }, svg);
  // Frontera actual
  el("polyline", { points: curve.map(p => `${sx(p.sd).toFixed(1)},${sy(p.er).toFixed(1)}`).join(" "), fill: "none", stroke: "#1D4ED8", "stroke-width": "3.2" }, svg);

  // Flecha efecto diversificación desde recta ρ=1 hacia cartera actual
  if (linSd - curP.sd > 0.008) {
    drawArrow(svg, sx(linSd), sy(curP.er), sx(curP.sd), sy(curP.er), "#7C3AED", "arr-blue", `Diversif. ${fmtDec(ahorroRiesgo,1)}pp`, (sx(linSd) + sx(curP.sd)) / 2, sy(curP.er) - 12);
  }
  el("circle", { cx: sx(bestG.sd), cy: sy(bestG.er), r: 6.5, fill: "#15803D", stroke: "#FFF", "stroke-width": "1.8" }, svg);
  el("circle", { cx: sx(bestT.sd), cy: sy(bestT.er), r: 7.5, fill: "#DC2626", stroke: "#FFF", "stroke-width": "2" }, svg);
  el("circle", { cx: sx(curP.sd), cy: sy(curP.er), r: 6.5, fill: "#0F172A", stroke: "#FFF", "stroke-width": "1.8" }, svg);
  const tTan = el("text", { x: sx(bestT.sd) + 9, y: sy(bestT.er) - 6, fill: "#DC2626", "font-size": "11", "font-weight": "800" }, svg);
  tTan.textContent = "Tangente (CML)";

  // Derecha: Línea SML / CAPM (Dupla 13 IPSA)
  const bxL = 595, bxR = 955, byT = 36, byB = 344;
  const sbX = b => bxL + (b / 1.6) * (bxR - bxL);
  const srY = r => byB - (r / 24) * (byB - byT);
  const tSml = el("text", { x: (bxL + bxR) / 2, y: 22, fill: "#0F172A", "font-size": "12", "font-weight": "700", "text-anchor": "middle" }, svg);
  tSml.textContent = "Línea SML / CAPM (Dupla 13 IPSA)";
  el("line", { x1: bxL, y1: byB, x2: bxR, y2: byB, stroke: "#334155", "stroke-width": "1.5" }, svg);
  el("line", { x1: bxL, y1: byT, x2: bxL, y2: byB, stroke: "#334155", "stroke-width": "1.5" }, svg);
  const rmRef = 15.8, rfPct = rf * 100;
  el("line", { x1: sbX(0), y1: srY(rfPct), x2: sbX(1.55), y2: srY(rfPct + 1.55 * (rmRef - rfPct)), stroke: "#1D4ED8", "stroke-width": "2.6" }, svg);
  DUPLA13_SML.forEach(ac => {
    const rReq = rfPct + ac.b * (rmRef - rfPct);
    const subVal = ac.r >= rReq;
    el("circle", { cx: sbX(ac.b), cy: srY(ac.r), r: 5.5, fill: subVal ? "#15803D" : "#DC2626", stroke: "#FFF", "stroke-width": "1.5" }, svg);
    const tn = el("text", { x: sbX(ac.b), y: srY(ac.r) - 8, fill: subVal ? "#166534" : "#991B1B", "font-size": "9.8", "font-weight": "700", "text-anchor": "middle" }, svg);
    tn.textContent = ac.nm;
  });
}

// ============================================================================
// 4. HAMADA (βL), WACC Y APV (MODIGLIANI-MILLER A 60 FPS)
// ============================================================================
let ghostHm = { dv: 30 };
let animHmId = null;

function fijarGhostHamada() { ghostHm = { dv: +document.getElementById("hm-dv").value }; drawHamada(); }
function presetHamada(dv) { fijarGhostHamada(); document.getElementById("hm-dv").value = dv; drawHamada(); }
function animarHamada() {
  if (animHmId) cancelAnimationFrame(animHmId);
  document.getElementById("hm-dv").value = 0;
  fijarGhostHamada();
  const t0 = performance.now(), dur = 1900;
  function step(now) {
    const u = Math.min(1, (now - t0) / dur);
    const ease = 1 - Math.pow(1 - u, 2.5);
    document.getElementById("hm-dv").value = Math.round(65 * ease);
    drawHamada();
    if (u < 1) animHmId = requestAnimationFrame(step);
  }
  animHmId = requestAnimationFrame(step);
}
function drawHamada() {
  const bu = +document.getElementById("hm-bu").value;
  const dvPct = +document.getElementById("hm-dv").value, dv = dvPct / 100;
  const kd = +document.getElementById("hm-kd").value / 100;
  const tc = +document.getElementById("hm-tc").value / 100;
  const pm = +document.getElementById("hm-pm").value / 100;
  const rf = 0.055;

  document.getElementById("hm-bu-v").textContent = fmtDec(bu, 2);
  document.getElementById("hm-dv-v").textContent = dvPct + "%";
  document.getElementById("hm-kd-v").textContent = fmtDec(kd * 100, 2) + "%";
  document.getElementById("hm-tc-v").textContent = fmtDec(tc * 100, 1) + "%";
  document.getElementById("hm-pm-v").textContent = fmtDec(pm * 100, 1) + "%";
  setDelta("hm-dv-d", dvPct - ghostHm.dv, 0, "%");

  const calc = wD => {
    const wE = 1 - wD, bs = wD / Math.max(0.05, wE);
    const bl = bu * (1 + (1 - tc) * bs);
    const ku = rf + bu * pm;
    const ke = rf + bl * pm;
    const kdt = kd * (1 - tc);
    const wacc = wE * ke + wD * kdt;
    const escMM = tc * (wD * 100);
    return { bs, bl, ku, ke, kdt, wacc, apv: 100 + escMM, escMM };
  };
  const c = calc(dv);

  document.getElementById("hm-enunciado").innerHTML =
    `Partiendo de un riesgo operativo puro <b>β<sub>U</sub> = ${fmtDec(bu,2)}</b> (K<sub>u</sub> = ${fmtDec(c.ku*100,2)}%), al financiar <b>${dvPct}% con deuda</b> (B/S = ${fmtDec(c.bs,2)}) a K<sub>d</sub> = ${fmtDec(kd*100,2)}% con impuesto corporativo t = ${fmtDec(tc*100,1)}%, ` +
    `la <b>Ecuación de Hamada</b> eleva el beta accionario a <b>β<sub>L</sub> = ${fmtDec(c.bl,2)}</b> (K<sub>e</sub> = ${fmtDec(c.ke*100,2)}%), pero el escudo fiscal reduce el <b>WACC a ${fmtDec(c.wacc*100,2)}%</b>.`;

  document.getElementById("hm-k-bl").textContent = fmtDec(c.bl, 2);
  document.getElementById("hm-k-bs").textContent = `B/S = ${fmtDec(c.bs, 2)}`;
  document.getElementById("hm-k-ke").textContent = fmtDec(c.ke * 100, 2) + "%";
  document.getElementById("hm-k-ku").textContent = `Ku puro = ${fmtDec(c.ku * 100, 2)}%`;
  document.getElementById("hm-k-wa").textContent = fmtDec(c.wacc * 100, 2) + "%";
  document.getElementById("hm-k-kdt").textContent = `Kd(1-t) = ${fmtDec(c.kdt * 100, 2)}%`;
  document.getElementById("hm-k-apv").textContent = `$${fmtDec(c.apv, 1)}M`;
  document.getElementById("hm-k-esc").textContent = `Escudo t·B = +$${fmtDec(c.escMM, 1)}M`;
  document.getElementById("hm-sol").innerHTML =
    `<b>Hamada:</b> β<sub>L</sub> = ${fmtDec(bu,2)}·[1 + (1−${fmtDec(tc,3)})·${fmtDec(c.bs,2)}] = <b>${fmtDec(c.bl,2)}</b> | ` +
    `<b>WACC:</b> ${Math.round((1-dv)*100)}%·${fmtDec(c.ke*100,2)}% + ${dvPct}%·${fmtDec(c.kdt*100,2)}% = <b>${fmtDec(c.wacc*100,2)}%</b>`;

  const svg = document.getElementById("svg-hamada");
  svg.innerHTML = "";
  addDefs(svg);
  const M = { l: 55, r: 400, t: 28, b: 46 }, W = 980, H = 380;
  const maxR = 32;
  const sx = d => M.l + (d / 75) * (W - M.l - M.r);
  const sy = r => H - M.b - (Math.min(r, maxR) / maxR) * (H - M.t - M.b);

  for (let r = 0; r <= 30; r += 5) {
    el("line", { x1: M.l, y1: sy(r), x2: W - M.r, y2: sy(r), stroke: "#E2E8F0" }, svg);
    const ty = el("text", { x: M.l - 7, y: sy(r) + 4, fill: "#475569", "font-size": "10.5", "text-anchor": "end" }, svg);
    ty.textContent = r + "%";
  }
  for (let d = 0; d <= 75; d += 15) {
    const tx = el("text", { x: sx(d), y: H - M.b + 16, fill: "#475569", "font-size": "10.5", "text-anchor": "middle" }, svg);
    tx.textContent = d + "%";
  }
  el("line", { x1: M.l, y1: H - M.b, x2: W - M.r, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);
  el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);

  const pKe = [], pWa = [];
  for (let d = 0; d <= 75; d += 2) {
    const z = calc(d / 100);
    pKe.push(`${sx(d).toFixed(1)},${sy(z.ke * 100).toFixed(1)}`);
    pWa.push(`${sx(d).toFixed(1)},${sy(z.wacc * 100).toFixed(1)}`);
  }
  el("line", { x1: sx(0), y1: sy(c.kdt * 100), x2: sx(75), y2: sy(c.kdt * 100), stroke: "#0F766E", "stroke-width": "2", "stroke-dasharray": "5,4" }, svg);
  el("polyline", { points: pKe.join(" "), fill: "none", stroke: "#DC2626", "stroke-width": "2.8" }, svg);
  el("polyline", { points: pWa.join(" "), fill: "none", stroke: "#1D4ED8", "stroke-width": "3.2" }, svg);
  el("line", { x1: sx(dvPct), y1: M.t, x2: sx(dvPct), y2: H - M.b, stroke: "#64748B", "stroke-dasharray": "4,3" }, svg);
  el("circle", { cx: sx(dvPct), cy: sy(c.ke * 100), r: 6, fill: "#DC2626", stroke: "#FFF", "stroke-width": "1.5" }, svg);
  el("circle", { cx: sx(dvPct), cy: sy(c.wacc * 100), r: 6.5, fill: "#1D4ED8", stroke: "#FFF", "stroke-width": "1.8" }, svg);

  const lKe = el("text", { x: sx(dvPct) + 8, y: sy(c.ke * 100) - 4, fill: "#DC2626", "font-size": "10.8", "font-weight": "800" }, svg);
  lKe.textContent = `Ke ${fmtDec(c.ke*100,1)}%`;
  const lWa = el("text", { x: sx(dvPct) + 8, y: sy(c.wacc * 100) + 14, fill: "#1D4ED8", "font-size": "10.8", "font-weight": "800" }, svg);
  lWa.textContent = `WACC ${fmtDec(c.wacc*100,1)}%`;

  // Derecha: Puente Modigliani-Miller / APV
  const bx0 = 640, bw = 72, baseB = 315;
  const syV = v => baseB - (v / 140) * 240;
  const tApv = el("text", { x: 790, y: 26, fill: "#0F172A", "font-size": "12", "font-weight": "700", "text-anchor": "middle" }, svg);
  tApv.textContent = "Puente APV (Valor Empresa = Vu + t·B)";
  el("line", { x1: 620, y1: baseB, x2: 955, y2: baseB, stroke: "#334155", "stroke-width": "1.5" }, svg);

  const bars = [
    { x: bx0, y0: 0, y1: 100, col: "#1E293B", lbl: "Vu (Sin Deuda)", val: "$100M" },
    { x: bx0 + 105, y0: 100, y1: c.apv, col: "#15803D", lbl: "Escudo t·B", val: `+$${fmtDec(c.escMM,1)}M` },
    { x: bx0 + 210, y0: 0, y1: c.apv, col: "#1D4ED8", lbl: "VL (APV)", val: `$${fmtDec(c.apv,1)}M` }
  ];
  bars.forEach(b => {
    el("rect", { x: b.x, y: syV(b.y1), width: bw, height: Math.max(2, syV(b.y0) - syV(b.y1)), fill: b.col, rx: 4 }, svg);
    const tv = el("text", { x: b.x + bw / 2, y: syV(b.y1) - 6, fill: b.col, "font-size": "11", "font-weight": "800", "text-anchor": "middle" }, svg);
    tv.textContent = b.val;
    const tl = el("text", { x: b.x + bw / 2, y: baseB + 16, fill: "#1E293B", "font-size": "10.5", "font-weight": "700", "text-anchor": "middle" }, svg);
    tl.textContent = b.lbl;
  });
}

// ============================================================================
// 5. PERFIL VAN VS. TIR (TASA DE FISHER) + PGU DUPONT (60 FPS)
// ============================================================================
function presetVanTir(r) { document.getElementById("vt-r").value = r; drawVanTir(); }
function presetPGU(m, rot) { document.getElementById("pg-m").value = m; document.getElementById("pg-r").value = rot; drawVanTir(); }
function npvArr(fl, r) { return fl.reduce((s, v, t) => s + v / Math.pow(1 + r, t), 0); }
function calcIrr(fl) {
  let lo = -0.5, hi = 2.0;
  for (let i = 0; i < 40; i++) { const m = (lo + hi) / 2; if (npvArr(fl, m) > 0) lo = m; else hi = m; }
  return (lo + hi) / 2;
}
function drawVanTir() {
  const rPct = +document.getElementById("vt-r").value, r = rPct / 100;
  const fA3 = +document.getElementById("vt-fa").value, fB1 = +document.getElementById("vt-fb").value;
  document.getElementById("vt-r-v").textContent = fmtDec(rPct, 1) + "%";
  document.getElementById("vt-fa-v").textContent = "$" + fA3 + "M";
  document.getElementById("vt-fb-v").textContent = "$" + fB1 + "M";

  const flA = [-100, 15, 25, fA3];
  const flB = [-100, fB1, 45, 18];
  const vA = npvArr(flA, r), vB = npvArr(flB, r);
  const tA = calcIrr(flA) * 100, tB = calcIrr(flB) * 100;
  const flDif = flA.map((v, i) => v - flB[i]);
  const rFisher = calcIrr(flDif) * 100;

  document.getElementById("vt-k-a").textContent = `VAN $${fmtDec(vA, 1)}M`;
  document.getElementById("vt-k-ta").textContent = `TIR = ${fmtDec(tA, 1)}%`;
  document.getElementById("vt-k-b").textContent = `VAN $${fmtDec(vB, 1)}M`;
  document.getElementById("vt-k-tb").textContent = `TIR = ${fmtDec(tB, 1)}%`;
  document.getElementById("vt-k-fis").textContent = fmtDec(rFisher, 1) + "%";
  const ganaA = vA >= vB;
  document.getElementById("vt-k-win").textContent = (Math.max(vA, vB) < 0) ? "RECHAZAR AMBOS" : (ganaA ? "ELEGIR A" : "ELEGIR B");
  document.getElementById("vt-k-win2").textContent = `Ventaja: +$${fmtDec(Math.abs(vA - vB), 1)}M`;

  const svg = document.getElementById("svg-vantir");
  svg.innerHTML = "";
  const M = { l: 60, r: 30, t: 22, b: 38 }, W = 980, H = 285;
  const sx = rp => M.l + (rp / 32) * (W - M.l - M.r);
  const sy = v => H - M.b - ((v + 40) / 160) * (H - M.t - M.b);

  el("line", { x1: M.l, y1: sy(0), x2: W - M.r, y2: sy(0), stroke: "#334155", "stroke-width": "1.6" }, svg);
  el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);
  const ptsA = [], ptsB = [];
  for (let rp = 0; rp <= 32; rp += 0.5) {
    ptsA.push(`${sx(rp).toFixed(1)},${sy(npvArr(flA, rp / 100)).toFixed(1)}`);
    ptsB.push(`${sx(rp).toFixed(1)},${sy(npvArr(flB, rp / 100)).toFixed(1)}`);
  }
  el("polyline", { points: ptsA.join(" "), fill: "none", stroke: "#1D4ED8", "stroke-width": "3" }, svg);
  el("polyline", { points: ptsB.join(" "), fill: "none", stroke: "#EA580C", "stroke-width": "3" }, svg);
  if (rFisher > 0 && rFisher < 32) {
    el("line", { x1: sx(rFisher), y1: M.t, x2: sx(rFisher), y2: H - M.b, stroke: "#7C3AED", "stroke-width": "1.8", "stroke-dasharray": "5,3" }, svg);
    const tf = el("text", { x: sx(rFisher) + 5, y: M.t + 14, fill: "#6D28D9", "font-size": "11", "font-weight": "800" }, svg);
    tf.textContent = `Tasa Fisher r* = ${fmtDec(rFisher, 1)}%`;
  }
  el("line", { x1: sx(rPct), y1: M.t, x2: sx(rPct), y2: H - M.b, stroke: "#0F172A", "stroke-dasharray": "3,3" }, svg);
  el("circle", { cx: sx(rPct), cy: sy(vA), r: 6.5, fill: "#1D4ED8", stroke: "#FFF", "stroke-width": "1.8" }, svg);
  el("circle", { cx: sx(rPct), cy: sy(vB), r: 6.5, fill: "#EA580C", stroke: "#FFF", "stroke-width": "1.8" }, svg);

  // PGU DuPont
  const mOp = +document.getElementById("pg-m").value, rot = +document.getElementById("pg-r").value;
  document.getElementById("pg-m-v").textContent = fmtDec(mOp, 1) + "%";
  document.getElementById("pg-r-v").textContent = fmtDec(rot, 2) + "x";
  const pgu = mOp * rot;
  document.getElementById("pg-box").innerHTML =
    `<b>PGU (DuPont Operacional):</b> Margen (${fmtDec(mOp,1)}%) × Rotación (${fmtDec(rot,2)}x) = <b>${fmtDec(pgu, 2)}%</b> de rentabilidad sobre activos operacionales.`;
}

// ============================================================================
// 6. HOJA MECÁNICA FINANZAS AVANZADAS (16 FÓRMULAS + 6 ESQUELETOS SVG)
// ============================================================================
const FORMULAS_FIN = [
  { id: 1, cat: "fsh", tag: "Fisher", title: "1. Separación de Fisher (Inversión y Consumo)",
    eq: `RMgI = r<sub>f</sub> &nbsp;|&nbsp; TMS(C<sub>0</sub>, C<sub>1</sub>) = −(1 + r<sub>f</sub>)`,
    rule: "En mercado perfecto la decisión productiva (P*) es objetiva y delegable; el dueño elige C* prestando o endeudándose a rf." },
  { id: 2, cat: "fsh", tag: "Riesgo", title: "2. Valor Esperado y Juego Justo",
    eq: `E(W) = ∑ p<sub>i</sub>·W<sub>i</sub> &nbsp;|&nbsp; Juego Justo ⇔ E(W) = W<sub>0</sub>`,
    rule: "El individuo averso al riesgo rechaza todo juego justo porque U(E[W]) > E[U(W)] (utilidad marginal decreciente)." },
  { id: 3, cat: "fsh", tag: "Riesgo", title: "3. Equivalente Cierto (EC) y Prima por Riesgo",
    eq: `U(EC) = E[U(W)] &nbsp;|&nbsp; π = E(W) − EC`,
    rule: "Averso: π > 0 (U'' < 0). Neutral: π = 0 (U'' = 0). Propenso/Amante: π < 0 (U'' > 0)." },
  { id: 4, cat: "fsh", tag: "DuPont", title: "4. Poder Generador de Utilidades (PGU)",
    eq: `PGU = <span class="frac"><span class="num">EBIT</span><span class="den">Ventas</span></span> × <span class="frac"><span class="num">Ventas</span><span class="den">Activos Op.</span></span>`,
    rule: "Combina Margen Operacional × Rotación de Activos Operacionales (Ross, Westerfield & Jordan Cap. 3)." },

  { id: 5, cat: "mk", tag: "Markowitz", title: "5. Anualización Bursátil (252 Días)",
    eq: `σ<sub>anual</sub> = σ<sub>diaria</sub> · √252 &nbsp;|&nbsp; R<sub>anual</sub> = (1 + R<sub>d</sub>)<sup>252</sup> − 1`,
    rule: "Regla oficial del Taller de Frontera Eficiente IPSA ($65M; 5 vs. 30 acciones)." },
  { id: 6, cat: "mk", tag: "Markowitz", title: "6. Retorno y Riesgo de Portafolio (Diversificación)",
    eq: `E(R<sub>p</sub>) = ∑ w<sub>i</sub> E(R<sub>i</sub>) &nbsp;|&nbsp; σ<sub>p</sub> = √(w<sup>T</sup> Σ w)`,
    rule: "Para 2 activos: σp² = wA²σA² + wB²σB² + 2wAwB·ρ·σAσB. Hay efecto diversificación siempre que ρ < +1." },
  { id: 7, cat: "mk", tag: "Tobin", title: "7. Ratio de Sharpe y Línea CML",
    eq: `S<sub>p</sub> = <span class="frac"><span class="num">E(R<sub>p</sub>) − R<sub>f</sub></span><span class="den">σ<sub>p</sub></span></span> &nbsp;|&nbsp; E(R<sub>p</sub>) = R<sub>f</sub> + S<sub>T</sub>·σ<sub>p</sub>`,
    rule: "El Portafolio Tangente maximiza Sharpe usando Rf de bonos BCP/BTP 5 años del Banco Central." },
  { id: 8, cat: "mk", tag: "CAPM", title: "8. CAPM, Beta y Línea SML",
    eq: `R<sub>e</sub> = R<sub>f</sub> + β<sub>i</sub>(R<sub>m</sub> − R<sub>f</sub>) &nbsp;|&nbsp; β<sub>i</sub> = <span class="frac"><span class="num">Cov(R<sub>i</sub>, R<sub>m</sub>)</span><span class="den">Var(R<sub>m</sub>)</span></span>`,
    rule: "Solo se remunera el riesgo sistemático (β). El riesgo no sistemático se elimina diversificando (5 → 30 títulos IPSA)." },
  { id: 17, cat: "mk", tag: "Normal", title: "17. Distribución Normal (Regla Empírica 68-95-99,7%)",
    eq: `68,26%: μ ± 1σ &nbsp;|&nbsp; 95,44%: μ ± 2σ &nbsp;|&nbsp; 99,74%: μ ± 3σ`,
    rule: "Guía 2 CPA Ej. 1 (μ=14,3%, σ=24,5%): ±1σ [-10,2%; 38,8%], ±2σ [-34,7%; 63,3%], ±3σ [-59,2%; 87,8%]." },
  { id: 18, cat: "mk", tag: "Estadística", title: "18. Covarianza y Correlación (Ex-Ante vs. Histórica)",
    eq: `Cov = ∑ p<sub>s</sub>(R<sub>A,s</sub>−R̄<sub>A</sub>)(R<sub>B,s</sub>−R̄<sub>B</sub>) &nbsp;|&nbsp; ρ = <span class="frac"><span class="num">Cov(A,B)</span><span class="den">σ<sub>A</sub>·σ<sub>B</sub></span></span>`,
    rule: "Con probabilidades (Ej. 2 y 4) se pondera por p_s; en series históricas (Ej. 5 MSFT y Ej. 6 HD) se divide por n−1 (muestral) o n (poblacional). ρ siempre ∈ [−1, +1]." },

  { id: 9, cat: "cap", tag: "Hamada", title: "9. Ecuación de Hamada (βU ↔ βL)",
    eq: `β<sub>L</sub> = β<sub>U</sub> [1 + (1 − t)<span class="frac"><span class="num">B</span><span class="den">S</span></span>] &nbsp;|&nbsp; β<sub>U</sub> = <span class="frac"><span class="num">β<sub>L</sub></span><span class="den">1 + (1 − t)(B/S)</span></span>`,
    rule: "Desapalanca el beta de empresas comparables para obtener riesgo operativo puro (βU) y reapalanca con el B/S propio." },
  { id: 10, cat: "cap", tag: "WACC", title: "10. Costo Promedio Ponderado de Capital (WACC)",
    eq: `WACC = K<sub>e</sub><span class="frac"><span class="num">S</span><span class="den">V</span></span> + K<sub>d</sub>(1 − t)<span class="frac"><span class="num">B</span><span class="den">V</span></span>`,
    rule: "Tasa de descuento del Flujo de Caja Libre (FCL); incorpora el escudo fiscal de los intereses vía (1 − t)." },
  { id: 11, cat: "cap", tag: "Deuda", title: "11. Cuota Francesa (PAGO) y Escudo Fiscal",
    eq: `Cuota = P·<span class="frac"><span class="num">K<sub>d</sub>(1+K<sub>d</sub>)<sup>n</sup></span><span class="den">(1+K<sub>d</sub>)<sup>n</sup> − 1</span></span> &nbsp;|&nbsp; EF<sub>t</sub> = I<sub>t</sub>·t`,
    rule: "Intereses (It) se restan ANTES de impuestos (generan escudo fiscal); Amortización de capital va DESPUÉS de impuestos." },
  { id: 12, cat: "cap", tag: "MM / APV", title: "12. Valor Presente Ajustado (APV)",
    eq: `APV = VAN(FCL a K<sub>u</sub>) + ∑ <span class="frac"><span class="num">I<sub>t</sub> · t</span><span class="den">(1 + K<sub>d</sub>)<sup>t</sup></span></span>`,
    rule: "Separa el valor operativo puro del negocio (100% patrimonio a Ku) del valor creado por el financiamiento (escudo a Kd)." },

  { id: 13, cat: "flj", tag: "CAPEX", title: "13. Separación IVA (19%) y Depreciación Lineal",
    eq: `Neto = <span class="frac"><span class="num">Bruto</span><span class="den">1,19</span></span> &nbsp;|&nbsp; Dep = <span class="frac"><span class="num">Neto − Rescate</span><span class="den">Vida Útil</span></span>`,
    rule: "Terrenos y Capital de Trabajo NO se deprecian. La depreciación se resta antes de impuestos y se reversa (+) debajo del BDI." },
  { id: 14, cat: "flj", tag: "Flujos", title: "14. Relación Flujo Libre (FCL) vs. Inversionista (FCI)",
    eq: `FCI<sub>t</sub> = FCL<sub>t</sub> − I<sub>t</sub>(1 − t) − Amort<sub>t</sub>`,
    rule: "FCL se descuenta a WACC (o Ke si no hay deuda); FCI descuenta en Año 0 el préstamo recibido y se descuenta a Ke." },
  { id: 15, cat: "flj", tag: "Criterios", title: "15. VAN, TIR y Regla de Conflictos",
    eq: `VAN = −I<sub>0</sub> + ∑ <span class="frac"><span class="num">FCN<sub>t</sub></span><span class="den">(1 + r)<sup>t</sup></span></span> &nbsp;|&nbsp; VP = <span class="frac"><span class="num">FCN<sub>t</sub></span><span class="den">(1+r)<sup>t</sup></span></span>`,
    rule: "Nunca multiplicar por (1+r)^t (Error Ej. 7). En proyectos mutuamente excluyentes manda siempre el MAYOR VAN." },
  { id: 16, cat: "flj", tag: "Riesgo", title: "16. VAN Esperado, Desviación, CV y VaR 95%",
    eq: `E(VAN) = ∑ p<sub>i</sub>·VAN<sub>i</sub> &nbsp;|&nbsp; CV = <span class="frac"><span class="num">σ(VAN)</span><span class="den">|E(VAN)|</span></span>`,
    rule: "En Monte Carlo el VaR 95% corresponde al Percentil 5% de la distribución simulada del VAN." }
];

const ESQUELETOS_FIN = [
  {
    title: "1. Separación de Fisher (P* vs. C*)",
    sub: "Frontera cóncava + recta -(1+rf) tangente en P*; curva U* tangente en C*.",
    svg: `<svg viewBox="0 0 260 150">
      <line x1="24" y1="128" x2="240" y2="128" stroke="#0F172A" stroke-width="1.5"/><line x1="24" y1="16" x2="24" y2="128" stroke="#0F172A" stroke-width="1.5"/>
      <path d="M 24 38 Q 128 40 164 128" fill="none" stroke="#1D4ED8" stroke-width="2.2"/>
      <line x1="24" y1="22" x2="212" y2="128" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="4,3"/>
      <path d="M 90 22 Q 125 84 226 112" fill="none" stroke="#059669" stroke-width="2"/>
      <circle cx="98" cy="64" r="4.5" fill="#1D4ED8"/><circle cx="144" cy="90" r="4.5" fill="#059669"/>
      <g class="sk-lbl" font-size="9" font-weight="700">
        <text x="8" y="24">C1</text><text x="232" y="142">C0</text><text x="74" y="60" fill="#1D4ED8">P*</text><text x="150" y="88" fill="#059669">C*</text>
        <text x="154" y="142">Y0</text><text x="202" y="142" fill="#DC2626">W0*</text>
      </g>
    </svg>`
  },
  {
    title: "2. Utilidad U(W): Averso vs. Prima π",
    sub: "Curva cóncava por encima de la cuerda; distancia horizontal EC → E(W) = π.",
    svg: `<svg viewBox="0 0 260 150">
      <line x1="26" y1="128" x2="240" y2="128" stroke="#0F172A" stroke-width="1.5"/><line x1="26" y1="16" x2="26" y2="128" stroke="#0F172A" stroke-width="1.5"/>
      <path d="M 26 128 Q 92 38 232 24" fill="none" stroke="#1D4ED8" stroke-width="2.4"/>
      <line x1="60" y1="86" x2="216" y2="28" stroke="#64748B" stroke-width="1.6" stroke-dasharray="4,3"/>
      <line x1="100" y1="57" x2="138" y2="57" stroke="#DC2626" stroke-width="2.4"/>
      <circle cx="100" cy="57" r="4" fill="#15803D"/><circle cx="138" cy="57" r="4" fill="#DC2626"/>
      <g class="sk-lbl" font-size="9" font-weight="700">
        <text x="6" y="24">U(W)</text><text x="226" y="142">W</text><text x="84" y="50" fill="#15803D">EC</text><text x="142" y="72" fill="#DC2626">E(W)</text><text x="114" y="48" fill="#DC2626">π</text>
      </g>
    </svg>`
  },
  {
    title: "3. Markowitz (ρ < 1) + CML Tangente",
    sub: "Hipérbola de frontera eficiente + recta desde Rf tangente en Máx. Sharpe.",
    svg: `<svg viewBox="0 0 260 150">
      <line x1="26" y1="128" x2="240" y2="128" stroke="#0F172A" stroke-width="1.5"/><line x1="26" y1="16" x2="26" y2="128" stroke="#0F172A" stroke-width="1.5"/>
      <path d="M 192 114 Q 68 88 196 30" fill="none" stroke="#1D4ED8" stroke-width="2.4"/>
      <line x1="26" y1="96" x2="218" y2="22" stroke="#D97706" stroke-width="2" stroke-dasharray="5,3"/>
      <circle cx="129" cy="79" r="4.5" fill="#15803D"/><circle cx="152" cy="48" r="5" fill="#DC2626"/>
      <g class="sk-lbl" font-size="9" font-weight="700">
        <text x="6" y="99" fill="#D97706">Rf</text><text x="100" y="94" fill="#15803D">GMVP</text><text x="148" y="38" fill="#DC2626">Tangente</text><text x="226" y="142">σp</text>
      </g>
    </svg>`
  },
  {
    title: "4. Línea SML / CAPM (α > 0 vs. α < 0)",
    sub: "Sobre SML = subvalorado (comprar); bajo SML = sobrevalorado (vender).",
    svg: `<svg viewBox="0 0 260 150">
      <line x1="26" y1="128" x2="240" y2="128" stroke="#0F172A" stroke-width="1.5"/><line x1="26" y1="16" x2="26" y2="128" stroke="#0F172A" stroke-width="1.5"/>
      <line x1="26" y1="98" x2="232" y2="24" stroke="#1D4ED8" stroke-width="2.4"/>
      <circle cx="115" cy="42" r="4.5" fill="#15803D"/><circle cx="168" cy="86" r="4.5" fill="#DC2626"/>
      <g class="sk-lbl" font-size="9" font-weight="700">
        <text x="6" y="100">Rf</text><text x="122" y="42" fill="#15803D">α &gt; 0 (Comprar)</text><text x="148" y="100" fill="#DC2626">α &lt; 0 (Vender)</text><text x="224" y="142">β</text>
      </g>
    </svg>`
  },
  {
    title: "5. Hamada y WACC según Deuda (B/V)",
    sub: "Ke sube con el apalancamiento; WACC cae por el escudo fiscal Kd(1−t).",
    svg: `<svg viewBox="0 0 260 150">
      <line x1="26" y1="128" x2="240" y2="128" stroke="#0F172A" stroke-width="1.5"/><line x1="26" y1="16" x2="26" y2="128" stroke="#0F172A" stroke-width="1.5"/>
      <path d="M 26 74 Q 150 62 232 22" fill="none" stroke="#DC2626" stroke-width="2.2"/>
      <path d="M 26 74 Q 140 82 232 94" fill="none" stroke="#1D4ED8" stroke-width="2.4"/>
      <line x1="26" y1="112" x2="232" y2="112" stroke="#0F766E" stroke-width="1.8" stroke-dasharray="4,3"/>
      <g class="sk-lbl" font-size="9" font-weight="700">
        <text x="195" y="34" fill="#DC2626">Ke (↑)</text><text x="180" y="88" fill="#1D4ED8">WACC</text><text x="176" y="108" fill="#0F766E">Kd(1-t)</text><text x="215" y="142">B/V</text>
      </g>
    </svg>`
  },
  {
    title: "6. Perfil VAN(r) y Tasa de Fisher (r*)",
    sub: "A la izquierda de r* gana A (mayor VAN) aunque B tenga mayor TIR.",
    svg: `<svg viewBox="0 0 260 150">
      <line x1="26" y1="110" x2="240" y2="110" stroke="#0F172A" stroke-width="1.5"/><line x1="26" y1="16" x2="26" y2="134" stroke="#0F172A" stroke-width="1.5"/>
      <path d="M 26 24 Q 112 72 194 128" fill="none" stroke="#1D4ED8" stroke-width="2.2"/>
      <path d="M 26 54 Q 134 80 232 124" fill="none" stroke="#EA580C" stroke-width="2.2"/>
      <line x1="116" y1="22" x2="116" y2="110" stroke="#7C3AED" stroke-width="1.5" stroke-dasharray="4,3"/>
      <g class="sk-lbl" font-size="9" font-weight="700">
        <text x="34" y="28" fill="#1D4ED8">VAN A</text><text x="34" y="54" fill="#EA580C">VAN B</text><text x="120" y="34" fill="#6D28D9">r* Fisher</text>
        <text x="155" y="124" fill="#1D4ED8">TIR A</text><text x="200" y="124" fill="#EA580C">TIR B</text>
      </g>
    </svg>`
  }
];

let mecBlind = false, mecFilter = "all", mecMastered = new Set(), mecBuilt = false;
function renderMecanica() {
  const fGrid = document.getElementById("mec-formulas-grid"), sGrid = document.getElementById("mec-skel-grid");
  if (!fGrid || !sGrid) return;
  fGrid.innerHTML = "";
  FORMULAS_FIN.filter(f => mecFilter === "all" || f.cat === mecFilter).forEach(item => {
    const card = document.createElement("div");
    card.className = "f-card" + (mecMastered.has(item.id) ? " mastered" : "");
    card.innerHTML = `
      <div class="f-head">
        <div><span class="f-cat">${item.tag}</span> <span class="f-title">${item.title}</span></div>
        <button class="chk-btn" title="Marcar dominada" onclick="toggleMastered(${item.id}, event)">✓</button>
      </div>
      <div class="f-body" onclick="this.parentElement.classList.toggle('revealed')">
        <div class="blind-cover">Haz clic para revelar y comprobar tu cuaderno</div>
        <div class="f-eq">${item.eq}</div>
        <div class="f-rule">${item.rule}</div>
      </div>`;
    fGrid.appendChild(card);
  });
  if (!mecBuilt) {
    sGrid.innerHTML = "";
    ESQUELETOS_FIN.forEach(sk => {
      const sc = document.createElement("div");
      sc.className = "s-card";
      sc.onclick = function() { this.classList.toggle("revealed"); };
      sc.innerHTML = `<div class="s-title">${sk.title}</div>${sk.svg}<div class="s-sub">${sk.sub}</div>`;
      sGrid.appendChild(sc);
    });
    mecBuilt = true;
  }
  document.getElementById("mec-score").textContent = `Dominadas: ${mecMastered.size} / ${FORMULAS_FIN.length}`;
}
function setModoMec(isBlind) {
  mecBlind = isBlind;
  const cont = document.getElementById("mec-container");
  cont.classList.toggle("blind-mode", isBlind);
  document.getElementById("btn-modo-copia").classList.toggle("primary", !isBlind);
  document.getElementById("btn-modo-ciego").classList.toggle("primary", isBlind);
  cont.querySelectorAll(".f-card, .s-card").forEach(n => n.classList.remove("revealed"));
}
function filtrarMec(cat, btn) {
  mecFilter = cat;
  btn.parentElement.querySelectorAll(".flt-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  renderMecanica();
}
function toggleMastered(id, ev) { ev.stopPropagation(); if (mecMastered.has(id)) mecMastered.delete(id); else mecMastered.add(id); renderMecanica(); }
function resetDominadas() { mecMastered.clear(); renderMecanica(); }

// ============================================================================
// 7. MAPA CAUSAL, LECTURA EN 3 CAPAS Y CONTROL CRUZADO (FINANZAS AVANZADAS)
// ============================================================================
const MAPA_FIN_PILARES = {
  F1: {
    id: "F1", x: 135, y: 95, w: 215, h: 76, col: "#1D4ED8",
    lbl: "F1. CONSUMO-INVERSIÓN",
    sub: "Principio Separación de Fisher\nRMgI = rf · TMS = -(1+rf) · VAN",
    explica: "Demuestra el principio rector de las finanzas corporativas: en mercados de capitales sin fricciones, el objetivo único del administrador es maximizar el VAN de los proyectos físicos (RMgI = rf), delegando el patrón temporal de consumo al mercado financiero.",
    puentes: "<b>→ Hacia F5 (Activos Reales):</b> justifica por qué el VAN es el criterio supremo frente a TIR y Payback. <b>→ Hacia F3 (Markowitz/CAPM):</b> al levantar el supuesto de certidumbre, la tasa única rf se reemplaza por tasas ajustadas por riesgo (Ke y WACC).",
    jumps: [["fisher", "Abrir Separación de Fisher"], ["vantir", "Abrir VAN vs. TIR"]]
  },
  F2: {
    id: "F2", x: 490, y: 78, w: 220, h: 76, col: "#0F766E",
    lbl: "F2. RIESGO, UTILIDAD Y PGU",
    sub: "Von Neumann-Morgenstern · EC\nJuego Justo · Prima π · DuPont",
    explica: "Introduce la incertidumbre: los inversionistas aversos al riesgo (U'' < 0) rechazan juegos justos y exigen una Prima por Riesgo positiva (π = E[W] − EC). A nivel operacional de empresa, el PGU (Margen × Rotación) mide la capacidad de los activos para generar EBIT.",
    puentes: "<b>→ Hacia F3 (Markowitz):</b> la aversión al riesgo explica por qué los inversionistas buscan maximizar retorno para un riesgo mínimo (Frontera Eficiente). <b>→ Hacia F5 (Monte Carlo):</b> fundamenta medir el riesgo del VAN con σ, CV y VaR 95%.",
    jumps: [["riesgo", "Abrir Riesgo y Juego Justo"], ["vantir", "Abrir PGU DuPont"]]
  },
  F3: {
    id: "F3", x: 845, y: 95, w: 215, h: 76, col: "#B91C1C",
    lbl: "F3. MARKOWITZ Y CAPM",
    sub: "252 días · Diversificación (ρ<1)\nGMVP · Sharpe · CML · SML (β)",
    explica: "Formaliza la gestión de carteras (Taller IPSA $65M: 5 vs. 30 acciones): diversificar con ρ < 1 elimina el riesgo específico y deja solo el riesgo sistemático (β), cuyo precio de equilibrio en el mercado está dado por el CAPM (Re = Rf + β[Rm − Rf]).",
    puentes: "<b>← Desde F2:</b> operacionaliza la prima por riesgo en mercados reales (BCP/BTP 5 años). <b>→ Hacia F4 (Hamada/WACC):</b> entrega el costo patrimonial Ke que alimenta la estructura de capital corporativa.",
    jumps: [["markowitz", "Abrir Markowitz y CAPM"]]
  },
  F4: {
    id: "F4", x: 300, y: 248, w: 235, h: 76, col: "#7C3AED",
    lbl: "F4. HAMADA, WACC Y APV",
    sub: "βU ↔ βL · Escudo Fiscal (1-t)\nAmortización Francesa · MM",
    explica: "Conecta el riesgo de mercado con el endeudamiento de la firma: la Ecuación de Hamada ajusta el beta por el apalancamiento B/S, permitiendo calcular Ke, WACC y el Valor Presente Ajustado (APV = VAN a Ku + VP del Escudo Fiscal de los intereses).",
    puentes: "<b>← Desde F3:</b> toma betas de empresas comparables y los adapta a la estructura de deuda propia. <b>→ Hacia F5 (FCL/FCI):</b> fija las tasas exactas para descontar FCL (WACC) y FCI (Ke), además de la tabla de amortización (PAGO).",
    jumps: [["hamada", "Abrir Hamada, WACC y APV"]]
  },
  F5: {
    id: "F5", x: 685, y: 248, w: 235, h: 76, col: "#15803D",
    lbl: "F5. ACTIVOS REALES (FCL/FCI)",
    sub: "IVA/Depreciación · FCL vs. FCI\nSensibilidad · Monte Carlo · Ej. 1–8",
    explica: "Aplica toda la teoría a proyectos corporativos reales: separa IVA y depreciaciones, excluye costos hundidos, reversa partidas no monetarias, proyecta FCL y FCI con deuda, audita errores clásicos (Ej. 7–8) y cuantifica la probabilidad de éxito mediante Monte Carlo.",
    puentes: "<b>← Desde F1 y F4:</b> descuenta los flujos al WACC/Ke y decide por VAN máximo. <b>← Desde F2:</b> evalúa la incertidumbre mediante E(VAN), desviación estándar y VaR 95%.",
    jumps: [["vantir", "Abrir Perfil VAN vs. TIR"], ["mecanica", "Abrir Hoja Mecánica"]]
  }
};

const MAPA_FIN_EDGES = [
  { a: "F1", b: "F5", lbl: "Criterio VAN Máx." },
  { a: "F1", b: "F2", lbl: "De Certeza a Riesgo" },
  { a: "F2", b: "F3", lbl: "Aversión → Sharpe" },
  { a: "F3", b: "F4", lbl: "CAPM → Ke / β" },
  { a: "F4", b: "F5", lbl: "WACC / Ke / Deuda" },
  { a: "F2", b: "F5", lbl: "PGU y VaR 95%" },
  { a: "F1", b: "F3", lbl: "rf → Línea CML" }
];

const ESCENARIOS_FIN = {
  wacc: {
    titulo: "Cadena A: De la Cartera de Mercado (Markowitz / CAPM) a la Tasa de Descuento Corporativa (WACC)",
    nodes: ["F3", "F4", "F5"],
    edges: [["F3", "F4"], ["F4", "F5"]],
    texto: "<b>1) En F3 (Markowitz/CAPM):</b> los retornos diarios del IPSA anualizados (252 días) y los bonos BCP/BTP 5 años definen Rf, Rm y el riesgo sistemático β. " +
           "<b>2) En F4 (Hamada/WACC):</b> se desapalanca βL de comparables para obtener βU, se reapalanca con el B/S del proyecto y se obtiene Ke y WACC. " +
           "<b>3) En F5 (Evaluación FCL):</b> el WACC descuenta los Flujos de Caja Libres (dividiendo siempre por (1+r)^t) para determinar el VAN.",
    jumps: [["markowitz", "Ver Markowitz y CAPM"], ["hamada", "Ver Hamada y WACC"]]
  },
  deuda: {
    titulo: "Cadena B: Efecto del Apalancamiento Financiero (De FCL Puro a FCI con Escudo Fiscal)",
    nodes: ["F4", "F5"],
    edges: [["F4", "F5"]],
    texto: "<b>1) En F4 (Hamada y Cuota PAGO):</b> endeudar el proyecto al 30% eleva βL y Ke por mayor riesgo financiero, pero los intereses rebajan la base tributaria (29,5%), generando un Escudo Fiscal = I_t × t_c. " +
           "<b>2) En F5 (FCI):</b> el préstamo reduce el aporte propio del Año 0 y, mientras Kd(1−t) sea menor que la TIR del FCL, el apalancamiento dispara la TIR del Inversionista.",
    jumps: [["hamada", "Probar Apalancamiento en Hamada"]]
  },
  riesgo: {
    titulo: "Cadena C: De la Aversión al Riesgo Individual a la Simulación de Monte Carlo",
    nodes: ["F2", "F3", "F5"],
    edges: [["F2", "F3"], ["F2", "F5"]],
    texto: "<b>1) En F2 (Utilidad):</b> como los accionistas son aversos al riesgo (π > 0), no basta conocer el VAN promedio; importa la dispersión de resultados. " +
           "<b>2) En F3 (Diversificación):</b> en mercados financieros el riesgo único se diversifica con ρ < 1. " +
           "<b>3) En F5 (Activos Reales):</b> en proyectos indivisibles (Ej. 5 y Hoja 6) el riesgo total se cuantifica con E(VAN), σ, CV y VaR 95% en Monte Carlo.",
    jumps: [["riesgo", "Ver Curva de Utilidad U(W)"]]
  }
};

let finPilarAct = "F1", finEscKey = null;
function selectPilarFin(k) { finEscKey = null; finPilarAct = k; drawMapaFin(); }
function activarEscenarioFin(k) { finEscKey = k; drawMapaFin(); }
function drawMapaFin() {
  const svg = document.getElementById("svg-mapa-fin"), box = document.getElementById("mapa-fin-detail");
  if (!svg || !box) return;
  svg.innerHTML = "";
  addDefs(svg);
  const esc = finEscKey ? ESCENARIOS_FIN[finEscKey] : null;
  const active = new Set(esc ? esc.nodes : [finPilarAct]);

  MAPA_FIN_EDGES.forEach(ed => {
    const na = MAPA_FIN_PILARES[ed.a], nb = MAPA_FIN_PILARES[ed.b];
    const isHot = esc ? esc.edges.some(([x, y]) => (x === ed.a && y === ed.b) || (x === ed.b && y === ed.a)) : (ed.a === finPilarAct || ed.b === finPilarAct);
    const dx = nb.x - na.x, dy = nb.y - na.y, dist = Math.hypot(dx, dy) || 1;
    const x1 = na.x + (dx / dist) * 60, y1 = na.y + (dy / dist) * 34;
    const x2 = nb.x - (dx / dist) * 64, y2 = nb.y - (dy / dist) * 36;
    el("line", { x1, y1, x2, y2, stroke: isHot ? "#DC2626" : "#CBD5E1", "stroke-width": isHot ? "2.8" : "1.5", "stroke-dasharray": isHot ? "" : "4,3", "marker-end": isHot ? "url(#arr-red)" : "" }, svg);
    if (isHot) {
      const mx = (x1 + x2) / 2, my = (y1 + y2) / 2, bw = Math.max(76, ed.lbl.length * 6.2 + 10);
      el("rect", { x: mx - bw / 2, y: my - 9, width: bw, height: 16, rx: 4, fill: "#FFFFFF", stroke: "#DC2626", "stroke-width": "1" }, svg);
      const tl = el("text", { x: mx, y: my + 3, fill: "#991B1B", "font-size": "9.8", "font-weight": "700", "text-anchor": "middle" }, svg);
      tl.textContent = ed.lbl;
    }
  });

  Object.values(MAPA_FIN_PILARES).forEach(nd => {
    const isSel = active.has(nd.id);
    const g = el("g", { style: "cursor:pointer;", onclick: `selectPilarFin('${nd.id}')` }, svg);
    el("rect", { x: nd.x - nd.w / 2, y: nd.y - nd.h / 2, width: nd.w, height: nd.h, rx: 9, fill: isSel ? nd.col : "#FFFFFF", stroke: isSel ? "#0F172A" : nd.col, "stroke-width": isSel ? "2.6" : "1.8", opacity: esc && !isSel ? "0.45" : "1" }, g);
    const t1 = el("text", { x: nd.x, y: nd.y - 13, fill: isSel ? "#FFFFFF" : nd.col, "font-size": "11.5", "font-weight": "800", "text-anchor": "middle" }, g);
    t1.textContent = nd.lbl;
    nd.sub.split("\n").forEach((ln, k) => {
      const ts = el("text", { x: nd.x, y: nd.y + 6 + k * 14, fill: isSel ? "#F1F5F9" : "#334155", "font-size": "10", "font-weight": "600", "text-anchor": "middle" }, g);
      ts.textContent = ln;
    });
  });

  if (esc) {
    const btns = esc.jumps.map(([tb, lb]) => `<button class="jump-btn" onclick="jumpToTab('${tb}')">${lb} →</button>`).join(" ");
    box.innerHTML = `<div class="map-detail-head"><span class="map-detail-title">${esc.titulo}</span><div class="btn-bar">${btns}</div></div><div>${esc.texto}</div>`;
  } else {
    const p = MAPA_FIN_PILARES[finPilarAct];
    const btns = p.jumps.map(([tb, lb]) => `<button class="jump-btn" onclick="jumpToTab('${tb}')">${lb} →</button>`).join(" ");
    box.innerHTML = `<div class="map-detail-head"><span class="map-detail-title">${p.lbl} (Haz clic en otro pilar para cambiar el foco)</span><div class="btn-bar">${btns}</div></div><div><b>Lógica central:</b> ${p.explica}</div><div style="margin-top:5px;"><b>Puentes con el ramo:</b> ${p.puentes}</div>`;
  }
}

const FICHAS_FIN = [
  {
    unit: "F1", src: "Consumo - Inversión.pdf (láms. 2–10) · Brealey, Myers y Allen Cap. 2",
    title: "1. Modelo Consumo-Inversión y Principio de Separación de Fisher",
    core: "<b>Idea central:</b> En un mercado de capitales perfecto (sin costos de transacción, impuestos ni brecha entre tasa activa y pasiva), la firma invierte en activos físicos hasta que RMgI = r<sub>f</sub> (maximizando el VAN), y cada accionista ajusta su consumo intertemporal C* prestando o pidiendo prestado a r<sub>f</sub> donde TMS = −(1 + r<sub>f</sub>).",
    bridge: "<b>Puente entre pilares:</b> Fundamenta teóricamente la delegación gerencial y la supremacía del criterio VAN (F5) sobre las preferencias subjetivas de los dueños.",
    trap: "<b>Trampas de prueba:</b> Si existen imperfecciones (tasa de endeudamiento distinta a la de ahorro, racionamiento de capital o costos de transacción), el Teorema de Separación de Fisher deja de cumplirse exactamente y los dueños podrían discrepar sobre qué proyectos ejecutar."
  },
  {
    unit: "F2", src: "Relación riesgo rentabilidad.pdf (láms. 7–21 y 26–35) · Ross Cap. 3",
    title: "2. Actitudes frente al Riesgo, Juego Justo y PGU (DuPont)",
    core: "<b>Idea central:</b> Un juego es 'justo' cuando E(W) = W<sub>0</sub>. El individuo averso al riesgo tiene función de utilidad cóncava (U'' &lt; 0), Equivalente Cierto EC &lt; E(W) y Prima por Riesgo positiva (π &gt; 0). En la empresa, el Poder Generador de Utilidades (PGU = Margen Operacional × Rotación de Activos) mide la eficiencia operativa.",
    bridge: "<b>Puente entre pilares:</b> La aversión al riesgo justifica diversificar en Markowitz (F3) y analizar distribuciones completas en Monte Carlo (F5).",
    trap: "<b>Trampas de prueba:</b> (1) Un individuo averso al riesgo NO evita todo riesgo: acepta proyectos riesgosos siempre que el retorno esperado compense su prima por riesgo (EC &gt; W<sub>0</sub>). (2) Confundir utilidad esperada E[U(W)] con utilidad del valor esperado U(E[W])."
  },
  {
    unit: "F3", src: "Teoría de mercado de capitales.pdf · Taller Frontera Eficiente IPSA ($65M)",
    title: "3. Frontera Eficiente de Markowitz (252 días), CML y CAPM / SML",
    core: "<b>Idea central:</b> Combinar activos con correlación ρ &lt; 1 reduce el riesgo del portafolio sin sacrificar retorno proporcionalmente. La anualización bursátil usa 252 días (σ<sub>anual</sub> = σ<sub>d</sub>·√252). La CML conecta R<sub>f</sub> (BCP/BTP 5 años BCCh) con el Portafolio Tangente (Máx. Sharpe). El CAPM (SML) valora activos individuales solo por su riesgo sistemático β.",
    bridge: "<b>Puente entre pilares:</b> Entrega la tasa exigida por el patrimonio K<sub>e</sub> y el beta β que entran a Hamada/WACC (F4) y a la evaluación de proyectos (F5).",
    trap: "<b>Trampas de prueba:</b> (1) Al pasar de 5 acciones (Dupla 13) a 30 acciones del IPSA, el riesgo NO cae a cero: se elimina el riesgo no sistemático, pero persiste el riesgo sistemático de mercado. (2) En la CML el eje X es riesgo total (σ<sub>p</sub>); en la SML el eje X es riesgo sistemático (β<sub>i</sub>)."
  },
  {
    unit: "F4", src: "Hamada · Modigliani-Miller · Brealey, Myers y Allen",
    title: "4. Estructura de Capital: Ecuación de Hamada, WACC y Método APV",
    core: "<b>Idea central:</b> El endeudamiento aumenta la variabilidad de las utilidades residuales del accionista (sube β<sub>L</sub> y K<sub>e</sub> según Hamada), pero genera un Escudo Fiscal sobre los intereses (I<sub>t</sub>·t<sub>c</sub>) que reduce el WACC y eleva el valor de la firma (APV = VAN a K<sub>u</sub> + VP Escudo a K<sub>d</sub>).",
    bridge: "<b>Puente entre pilares:</b> Conecta el mercado financiero (F3) con la estructura de financiamiento de los Casos 1, 2 y 3 (30% deuda, tabla PAGO) en el Evaluador Corporativo (F5).",
    trap: "<b>Trampas de prueba:</b> (1) Usar β<sub>L</sub> de una empresa comparable sin desapalancarlo primero con su propio B/S y tasa t. (2) Incluir intereses dentro del Flujo de Caja Libre (FCL): en el FCL el escudo fiscal ya está capturado en el WACC; poner intereses en el FCL contaría doble el beneficio tributario."
  },
  {
    unit: "F5", src: "Guía de Análisis — Inversión en Activos Reales (Ejercicios 1 al 6)",
    title: "5. Criterios de Decisión Corporativa: VAN vs. TIR vs. Payback e Incertidumbre",
    core: "<b>Idea central:</b> En proyectos mutuamente excluyentes (Ej. 3 y 4) o cuando existe conflicto con políticas internas de Payback (Ej. 6), manda siempre el <b>VAN</b> porque mide directamente la riqueza creada en pesos de hoy y asume reinversión al costo de capital. Bajo incertidumbre (Ej. 5), se calcula E(VAN), σ y CV.",
    bridge: "<b>Puente entre pilares:</b> Materializa el Teorema de Fisher (F1) y la gestión del riesgo (F2) en recomendaciones ejecutivas para directorios.",
    trap: "<b>Trampas de prueba:</b> (1) Elegir un proyecto solo por mayor TIR cuando tiene menor escala o menor VAN (conflicto antes de la Tasa de Fisher). (2) Rechazar un proyecto con VAN $150M y TIR 15% > WACC 10% solo porque su Payback (7 años) supera una política fija de 5 años."
  },
  {
    unit: "F5", src: "Guía de Análisis — Auditoría Ejercicio 7 y Caso 10 Años Ejercicio 8",
    title: "6. Arquitectura de Flujos FCL/FCI: Errores Clásicos, Hundidos y Valor Libro",
    core: "<b>Idea central:</b> Un flujo limpio exige: (1) valores netos de IVA, (2) consistencia de signos, (3) reverso positivo de depreciación y amortización bajo el BDI, (4) exclusión total de costos hundidos (ej. estudio de viabilidad previo de $800k en Ej. 8), (5) correcto tratamiento de venta de activos usados con Valor Libro, y (6) descuento dividiendo por (1 + r)<sup>t</sup>.",
    bridge: "<b>Puente entre pilares:</b> Todo error de flujo arruina el VAN aunque el CAPM y WACC (F3–F4) estén impecablemente calculados.",
    trap: "<b>Trampas de prueba (Ej. 7 y 8):</b> (1) Multiplicar por (1+r)<sup>t</sup> en vez de dividir al actualizar flujos (infló el VAN del asesor de $9M a $67,5M). (2) Olvidar reversar el Valor Libro (+VL) después de impuestos cuando se vende una máquina usada. (3) Depreciar terrenos o Capital de Trabajo."
  },
  {
    unit: "F3", src: "Guía de Ejercicios 2 — Teoría de la Cartera (CPA · Ejercicios 1 al 6)",
    title: "7. Estadística de Carteras: Distribución Normal, Covarianza, Correlación y Beta Histórico",
    core: "<b>Idea central:</b> La rentabilidad esperada y el riesgo se miden de dos formas: <b>Ex-Ante</b> (ponderando estados económicos por su probabilidad p<sub>s</sub>, Ej. 2 y 4) y <b>Ex-Post</b> (promediando retornos históricos observados como MSFT y Home Depot vs. S&amp;P 500, Ej. 5 y 6). Bajo normalidad, 68,26%, 95,44% y 99,74% de los retornos caen en μ ± 1σ, 2σ y 3σ.",
    bridge: "<b>Puente entre pilares:</b> La covarianza con el mercado dividida por la varianza del mercado (Cov(i,M)/Var(M)) es exactamente el <b>Beta (β)</b> que alimenta al CAPM (F3) y Hamada (F4).",
    trap: "<b>Trampas de prueba (Guía 2 CPA):</b> (1) En series históricas (12 meses) usar divisor muestral (n−1 = 11) para varianza y covarianza —aunque <b>ρ y β dan idéntico</b> con n−1 o n porque el divisor se cancela. (2) Confundir rendimiento simple (F<sub>1</sub>−I<sub>0</sub>)/I<sub>0</sub> = 133,33% (Ej. 3) con razón F<sub>1</sub>/I<sub>0</sub> = 233,33%."
  },
  {
    unit: "F5", src: "Guía Flujos de Caja — Empresa XX (Ej. 1) y Planta Piloto ULagos $130M (Ej. 2)",
    title: "8. Flujos Esperados bajo Incertidumbre, Tasa Ajustada por Riesgo y Sensibilidad ±6%",
    core: "<b>Idea central:</b> Cuando los flujos futuros son aleatorios (Ej. 1 Empresa XX), primero se obtiene el flujo esperado de cada año E(F<sub>t</sub>) = ∑ p<sub>i</sub>·F<sub>i</sub> y se descuenta a la <b>tasa ajustada por riesgo</b> k = R<sub>f</sub> + Prima (8% + 2% = 10%). En proyectos complejos (Planta Piloto $130M), se evalúa el impacto de variaciones porcentuales en ingresos (+6%) y el VAN esperado ponderado por probabilidades (55% Base / 45% Escenario −6%).",
    bridge: "<b>Puente entre pilares:</b> Une el cálculo de valor esperado de F2 con el motor FCL/FCI y Monte Carlo de F5.",
    trap: "<b>Trampas de prueba (Guía Flujos):</b> (1) En la tabla del Ej. 1, el guion '−' significa flujo $0 (nunca se omite su probabilidad; las probabilidades de cada periodo deben sumar 1,00). (2) En Planta Piloto ULagos ($130M), las pruebas de producción ($6M) y las ventas ($190M) vienen en <b>Bruto</b> (dividir por 1,19), mientras la máquina ($130M), egresos ($60,4M), capacitación ($7M) y CT ($35M) ya están en <b>Neto</b>."
  }
];

let capaFinAct = "core", filtroFinUnit = "all";
function setCapaFin(capa) {
  capaFinAct = capa;
  ["core", "bridge", "trap", "all"].forEach(k => { const b = document.getElementById("cap-btn-" + k); if (b) b.classList.toggle("primary", k === capa); });
  renderLecturaFin();
}
function filtrarLecturaFin(u, btn) {
  filtroFinUnit = u;
  btn.parentElement.querySelectorAll(".flt-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  renderLecturaFin();
}
function renderLecturaFin() {
  const g = document.getElementById("lec-fin-grid");
  if (!g) return;
  g.innerHTML = "";
  FICHAS_FIN.filter(f => filtroFinUnit === "all" || f.unit === filtroFinUnit).forEach(f => {
    const c = document.createElement("div");
    c.className = "lec-card";
    let h = "";
    if (capaFinAct === "core" || capaFinAct === "all") h += `<div class="lec-layer l-core">${f.core}</div>`;
    if (capaFinAct === "bridge" || capaFinAct === "all") h += `<div class="lec-layer l-bridge">${f.bridge}</div>`;
    if (capaFinAct === "trap" || capaFinAct === "all") h += `<div class="lec-layer l-trap">${f.trap}</div>`;
    c.innerHTML = `<div class="lec-meta"><span class="lec-unit">${f.unit}</span><span class="lec-src">${f.src}</span></div><div class="lec-title">${f.title}</div>${h}`;
    g.appendChild(c);
  });
}

const QUIZ_FIN_DATA = [
  {
    tag: "F1 Fisher",
    q: "Según el Principio de Separación de Fisher en un mercado de capitales perfecto, si cambia la impaciencia (preferencia subjetiva por consumo presente) de los accionistas:",
    opts: ["La empresa debe cambiar su nivel de inversión física I0* para producir más flujo hoy", "El óptimo productivo P* (RMgI = rf) permanece intacto y el accionista ajusta su consumo C* en el mercado financiero", "El VAN de los proyectos se vuelve negativo automáticamente"],
    ans: 1,
    why: "En mercados perfectos la decisión productiva depende solo de igualar RMgI = rf (objetiva y delegable). El accionista logra su consumo óptimo C* prestando o pidiendo prestado a rf (Consumo - Inversión.pdf)."
  },
  {
    tag: "F2 Riesgo",
    q: "Un inversionista averso al riesgo (U''(W) < 0) recibe la oferta de participar en un 'juego justo' donde el valor esperado E(W) es igual a su riqueza segura actual W0. ¿Cuál será su decisión racional?",
    opts: ["Rechaza el juego porque su Equivalente Cierto es menor que W0 (π > 0)", "Acepta el juego porque E(W) = W0 garantiza igual utilidad", "Es indiferente porque el valor esperado no cambia"],
    ans: 0,
    why: "Por utilidad marginal decreciente (concavidad), U(E[W]) > E[U(W)], lo que implica EC < E(W) = W0 y una prima por riesgo positiva; por tanto rechaza el juego justo (Relación riesgo rentabilidad.pdf)."
  },
  {
    tag: "F2 PGU DuPont",
    q: "Una cadena de retail opera con un Margen Operacional (EBIT/Ventas) bajo de 5%, pero alcanza una Rotación de Activos Operacionales de 3,2 veces al año. ¿Cuál es su Poder Generador de Utilidades (PGU)?",
    opts: ["8,2% (suma de margen y rotación)", "1,56% (división margen / rotación)", "16,0% (PGU = Margen × Rotación = 5% × 3,2)"],
    ans: 2,
    why: "El PGU se calcula multiplicando Margen Operacional (EBIT/Ventas) por Rotación de Activos Operacionales (Ventas/Activos Op.): 0,05 × 3,2 = 16,0% (Ross Cap. 3)."
  },
  {
    tag: "F3 Markowitz",
    q: "En el Taller de Frontera Eficiente ($65M; Dupla 13 IPSA), si la desviación estándar diaria de una acción es σ_d = 1,50%, ¿cuál es su volatilidad anualizada estándar (252 días bursátiles)?",
    opts: ["1,50% × 252 = 378,0%", "1,50% × √252 ≈ 23,81%", "1,50% / √252 ≈ 0,09%"],
    ans: 1,
    why: "La varianza escala linealmente con el tiempo (252 días), por lo que la desviación estándar se anualiza multiplicando por √252 ≈ 15,8745: 1,50% × 15,8745 = 23,81%."
  },
  {
    tag: "F3 CAPM / SML",
    q: "Al ampliar una cartera desde 5 acciones del IPSA a 30 acciones del IPSA diversificadas, ¿qué componente del riesgo se reduce drásticamente y cuál permanece?",
    opts: ["Se reduce el riesgo no sistemático (específico) y permanece el riesgo sistemático de mercado (β)", "Se elimina el riesgo sistemático (β = 0) y permanece el riesgo propio de cada empresa", "Ambos riesgos caen a cero siempre que ρ < +1"],
    ans: 0,
    why: "La diversificación elimina el riesgo idiosincrático/no sistemático de las compañías, pero no puede eliminar el riesgo sistemático común al mercado, medido por Beta."
  },
  {
    tag: "F4 Hamada",
    q: "Una empresa sin deuda tiene βU = 1,00. Si adopta una estructura con relación Deuda/Patrimonio B/S = 0,50 y tasa de impuesto corporativo t = 30%, ¿cuál será su Beta Apalancado βL según Hamada?",
    opts: ["βL = 1,50 (1,00 × [1 + 0,50])", "βL = 0,74 (desapalancado)", "βL = 1,35 (1,00 × [1 + (1 − 0,30) × 0,50])"],
    ans: 2,
    why: "Aplicando la Ecuación de Hamada: βL = βU·[1 + (1 − t)(B/S)] = 1,00 × [1 + 0,70 × 0,50] = 1,35."
  },
  {
    tag: "F4 ↔ F5 FCL vs FCI",
    q: "¿Por qué en el Flujo de Caja Libre (FCL — Proyecto Puro) NO se deben restar los intereses de la deuda bancaria antes de impuestos?",
    opts: ["Porque el ahorro tributario de los intereses ya está incorporado en el WACC vía Kd(1−t); restarlos en el FCL duplicaría el escudo fiscal", "Porque los intereses bancarios nunca son gasto deducible de impuestos en Chile", "Porque el FCL solo incluye el Año 0"],
    ans: 0,
    why: "El FCL evalúa el activo puro; el efecto financiero y el escudo tributario se capturan en el WACC (para FCL) o explícitamente en el Flujo del Inversionista (FCI, descontado a Ke)."
  },
  {
    tag: "F5 Guía Ej. 3-4",
    q: "Dos máquinas mutuamente excluyentes requieren igual inversión. Máquina A tiene VAN = $120M y TIR = 17%; Máquina B tiene VAN = $90M y TIR = 24% (tasa exigida 14%). ¿Cuál debe recomendarse al directorio?",
    opts: ["Máquina B porque ofrece 7 puntos porcentuales más de TIR", "Máquina A porque crea $30M más de riqueza neta en pesos de hoy (manda el VAN)", "Ambas son equivalentes porque superan el 14%"],
    ans: 1,
    why: "Ante conflicto entre VAN y TIR en alternativas mutuamente excluyentes (Ej. 3 y 4 de la Guía), siempre se privilegia el mayor VAN positivo porque mide creación directa de valor para los accionistas."
  },
  {
    tag: "F5 Guía Ej. 7",
    q: "En la auditoría del Ejercicio 7, el asesor omitió reversar la Depreciación (+$4.845.000/año) después de impuestos y además multiplicó cada flujo por (1+r)^t al actualizarlo. ¿Qué efecto tuvo ese segundo error?",
    opts: ["Subestimó el valor presente de los años futuros", "No alteró el resultado porque se canceló exactamente con la amortización", "Capitalizó los flujos hacia el futuro en lugar de descontarlos, inflando artificialmente el VAN"],
    ans: 2,
    why: "Actualizar flujos futuros exige dividir por (1+r)^t (o multiplicar por (1+r)^(-t)). Multiplicar por (1+r)^t capitalizó el dinero y generó un VAN falso de +$67,5M."
  },
  {
    tag: "F5 Guía Ej. 8",
    q: "En el Ejercicio 8 (10 años), al final del Año 8 se vende en $2.500.000 una máquina que tiene un Valor Libro remanente de $2.000.000 (impuesto 15%). ¿Cómo impacta correctamente el flujo de caja del Año 8?",
    opts: ["Se suma +$2.500.000 y se resta −$2.000.000 antes de impuestos (tributa 15% solo sobre la ganancia de $500.000), y luego se reversa +$2.000.000 debajo del BDI", "Se suma +$2.500.000 directamente después de impuestos sin considerar el Valor Libro", "El Valor Libro se resta antes de impuestos y no se reversa porque es pérdida de efectivo"],
    ans: 0,
    why: "La utilidad tributable por venta de activo es Precio de Venta − Valor Libro ($500.000 → impuesto $75.000). Como el Valor Libro no es salida de caja, se reversa (+$2.000.000) después de impuestos, dejando un ingreso neto de caja de $2.425.000."
  },
  {
    tag: "F3 Guía 2 CPA",
    q: "Si la rentabilidad media histórica de un mercado accionario es μ = 14,3% y su desviación estándar es σ = 24,5% (distribución normal), ¿entre qué valores se ubica el 68,26% de las rentabilidades anuales?",
    opts: ["Entre 0,0% y 38,8%", "Entre −10,2% y +38,8% (μ ± 1σ)", "Entre −34,7% y +63,3% (μ ± 2σ)"],
    ans: 1,
    why: "Por la regla empírica de la distribución normal, el 68,26% corresponde a μ ± 1σ: 14,3% − 24,5% = −10,2% y 14,3% + 24,5% = +38,8% (Guía 2 CPA, Ej. 1)."
  },
  {
    tag: "F3 Guía 2 CPA",
    q: "En el Ejercicio 2 (4 estados equiprobables), los activos A (σ=25,86%) y B (σ=11,50%) tienen correlación ρ = −0,1639. Al formar una cartera 30% A y 70% B, su desviación estándar es σp = 10,22%. ¿Por qué el riesgo de la cartera es MENOR incluso que el del activo B por sí solo?",
    opts: ["Porque el término de covarianza 2·wA·wB·Cov(A,B) es negativo y compensa parte de la varianza individual (efecto diversificación)", "Porque el promedio ponderado simple de 25,86% y 11,50% es 10,22%", "Porque al ser estados equiprobables la varianza se divide por 4 dos veces"],
    ans: 0,
    why: "Cuando ρ < 0 (como −0,1639), los activos tienden a moverse en direcciones opuestas entre estados económicos, logrando una volatilidad de cartera (10,22%) inferior incluso al activo menos riesgoso individual (B = 11,50%)."
  },
  {
    tag: "F3 Guía 2 CPA",
    q: "Al calcular la correlación (ρ) y el Beta (β = Cov/Var_M) de Microsoft o Home Depot frente al S&P 500 usando 12 retornos mensuales, ¿cambia el resultado de ρ o β si usas divisor muestral (n−1=11) vs. poblacional (n=12)?",
    opts: ["Sí, el Beta cambia en un 9,1% según el divisor usado", "No cambian ni ρ ni β, porque el factor (n−1) o (n) aparece tanto en el numerador como en el denominador y se cancela exactamente", "Solo cambia la correlación ρ, pero la varianza se mantiene igual"],
    ans: 1,
    why: "La varianza y la covarianza sí cambian de escala entre n−1 y n, pero en ρ = Cov/(σi·σM) y en β = Cov(i,M)/Var(M) el divisor se simplifica algebraicamente dando exactamente el mismo valor (MSFT: ρ=0,5730, β=1,3534)."
  },
  {
    tag: "F5 Guía Flujos",
    q: "En el Ejercicio 1 de la Guía de Flujos (Empresa XX, I0 = $1.000.000, flujos esperados $400k, $700k y $300k), se descuenta con una tasa ajustada por riesgo k = 8% + 2% = 10%, obteniendo VAN = +$167.543 y TIR = 19,55%. ¿Qué significa este resultado?",
    opts: ["Rechazar porque la suma nominal de flujos ($1.400k) apenas supera la inversión", "Aceptar el proyecto: los flujos esperados cubren el 8% libre de riesgo, el 2% de prima por riesgo y generan $167.543 de riqueza neta hoy", "Descontar nuevamente al 8% libre de riesgo para duplicar la prima"],
    ans: 1,
    why: "Como VAN(10%) = +$167.543 > 0 y TIR = 19,55% > k = 10%, el proyecto compensa sobradamente el riesgo exigido y crea valor económico para la empresa."
  }
];

let qzFinAns = {}, qzFinSoloPend = false;
function toggleSoloErradasFin(btn) { qzFinSoloPend = !qzFinSoloPend; btn.classList.toggle("primary", qzFinSoloPend); renderQuizFin(); }
function responderQuizFin(i, o) { qzFinAns[i] = o; renderQuizFin(); }
function resetQuizFin() { qzFinAns = {}; qzFinSoloPend = false; renderQuizFin(); }
function renderQuizFin() {
  const w = document.getElementById("qz-fin-list");
  if (!w) return;
  w.innerHTML = "";
  let ok = 0;
  QUIZ_FIN_DATA.forEach((it, idx) => {
    const u = qzFinAns[idx], isAns = u !== undefined, isOk = isAns && u === it.ans;
    if (isOk) ok++;
    if (qzFinSoloPend && isOk) return;
    const c = document.createElement("div");
    c.className = "qz-card" + (isAns ? (" answered " + (isOk ? "ok" : "bad")) : "");
    const btns = it.opts.map((op, oi) => `<button class="qz-btn ${u === oi ? "sel" : ""}" onclick="responderQuizFin(${idx}, ${oi})">${op}</button>`).join("");
    const bdg = isAns ? `<span style="font-size:11.5px;font-weight:800;color:${isOk ? "#15803D" : "#DC2626"};">${isOk ? "✓ Correcto" : "✗ Revisar"}</span>` : "";
    c.innerHTML = `<div><span class="qz-tag">${it.tag}</span> <span style="font-size:11px;color:#475569;font-weight:700;">Pregunta ${idx + 1}</span></div><div class="qz-q">${it.q}</div><div class="qz-opts">${btns}${bdg}</div><div class="qz-fb"><b>Fundamento oficial:</b> ${it.why}</div>`;
    w.appendChild(c);
  });
  document.getElementById("qz-fin-score").textContent = `Aciertos: ${ok} / ${QUIZ_FIN_DATA.length}`;
}

drawFisher();
drawRiesgo();
drawMarkowitz();
drawHamada();
drawVanTir();
renderMecanica();
drawMapaFin();

// ============================================================================
// 8. GUÍAS OFICIALES RESUELTAS A 60 FPS (GUÍA 2 CPA + GUÍA FLUJOS DE CAJA)
// ============================================================================
function selGuiaBloque(key, btn) {
  document.querySelectorAll(".gb-sec").forEach(d => d.style.display = "none");
  const target = document.getElementById("gb-" + key);
  if (target) target.style.display = "block";
  btn.parentElement.querySelectorAll(".act-btn").forEach(b => b.classList.remove("primary"));
  btn.classList.add("primary");
  if (key === "ej1") drawGuiaEj1();
  if (key === "ej2") drawGuiaEj2();
  if (key === "ej4") renderGuiaEj4();
  if (key === "ej56") drawGuia56();
  if (key === "ejxx") drawGuiaXX();
}

// --- Ej. 1: Campana Normal SVG (68,26% / 95,44% / 99,74%) ---
function drawGuiaEj1() {
  const mu = +document.getElementById("g1-mu").value;
  const sd = +document.getElementById("g1-sd").value;
  document.getElementById("g1-mu-v").textContent = fmtDec(mu, 1) + "%";
  document.getElementById("g1-sd-v").textContent = fmtDec(sd, 1) + "%";

  const r1a = mu - sd, r1b = mu + sd;
  const r2a = mu - 2 * sd, r2b = mu + 2 * sd;
  const r3a = mu - 3 * sd, r3b = mu + 3 * sd;

  document.getElementById("g1-enun").innerHTML =
    `La rentabilidad promedio anual histórica (50 años) es <b>μ = ${fmtDec(mu,1)}%</b> con desviación estándar <b>σ = ${fmtDec(sd,1)}%</b>. ` +
    `Bajo distribución normal: <b>68,26%</b> cae en <b>[${fmtDec(r1a,1)}% ; ${fmtDec(r1b,1)}%]</b>, ` +
    `<b>95,44%</b> en <b>[${fmtDec(r2a,1)}% ; ${fmtDec(r2b,1)}%]</b> y <b>99,74%</b> en <b>[${fmtDec(r3a,1)}% ; ${fmtDec(r3b,1)}%]</b>.`;

  document.getElementById("g1-k1").textContent = `[${fmtDec(r1a, 1)}% ; ${fmtDec(r1b, 1)}%]`;
  document.getElementById("g1-k2").textContent = `[${fmtDec(r2a, 1)}% ; ${fmtDec(r2b, 1)}%]`;
  document.getElementById("g1-k3").textContent = `[${fmtDec(r3a, 1)}% ; ${fmtDec(r3b, 1)}%]`;

  const svg = document.getElementById("svg-g1-gauss");
  if (!svg) return;
  svg.innerHTML = "";
  const M = { l: 44, r: 44, t: 26, b: 48 }, W = 980, H = 320;
  const sx = z => M.l + ((z + 3.6) / 7.2) * (W - M.l - M.r);
  const pdf = z => Math.exp(-0.5 * z * z);
  const sy = p => H - M.b - p * (H - M.t - M.b);

  const areaBand = (za, zb, col) => {
    const pts = [`${sx(za).toFixed(1)},${sy(0).toFixed(1)}`];
    for (let k = 0; k <= 40; k++) {
      const z = za + (zb - za) * (k / 40);
      pts.push(`${sx(z).toFixed(1)},${sy(pdf(z)).toFixed(1)}`);
    }
    pts.push(`${sx(zb).toFixed(1)},${sy(0).toFixed(1)}`);
    el("polygon", { points: pts.join(" "), fill: col }, svg);
  };
  areaBand(-3, 3, "rgba(234,88,12,0.16)");
  areaBand(-2, 2, "rgba(5,150,105,0.20)");
  areaBand(-1, 1, "rgba(29,78,216,0.28)");

  const curvePts = [];
  for (let k = 0; k <= 120; k++) {
    const z = -3.6 + 7.2 * (k / 120);
    curvePts.push(`${sx(z).toFixed(1)},${sy(pdf(z)).toFixed(1)}`);
  }
  el("polyline", { points: curvePts.join(" "), fill: "none", stroke: "#0F172A", "stroke-width": "2.6" }, svg);
  el("line", { x1: M.l, y1: sy(0), x2: W - M.r, y2: sy(0), stroke: "#334155", "stroke-width": "1.6" }, svg);

  for (const z of [-3, -2, -1, 0, 1, 2, 3]) {
    const val = mu + z * sd;
    el("line", { x1: sx(z), y1: sy(0), x2: sx(z), y2: sy(pdf(z)), stroke: z === 0 ? "#0F172A" : "#64748B", "stroke-dasharray": z === 0 ? "" : "4,3" }, svg);
    const t1 = el("text", { x: sx(z), y: sy(0) + 17, fill: "#0F172A", "font-size": "11", "font-weight": "800", "text-anchor": "middle" }, svg);
    t1.textContent = fmtDec(val, 1) + "%";
    const t2 = el("text", { x: sx(z), y: sy(0) + 32, fill: "#475569", "font-size": "10", "font-weight": "700", "text-anchor": "middle" }, svg);
    t2.textContent = z === 0 ? "μ" : (z > 0 ? `+${z}σ` : `${z}σ`);
  }
  const tMid = el("text", { x: sx(0), y: sy(0.48), fill: "#1E3A8A", "font-size": "13", "font-weight": "800", "text-anchor": "middle" }, svg);
  tMid.textContent = "68,26% (±1σ)";
  const t2 = el("text", { x: sx(1.5), y: sy(0.18), fill: "#065F46", "font-size": "11", "font-weight": "800", "text-anchor": "middle" }, svg);
  t2.textContent = "95,44%";
  const t3 = el("text", { x: sx(2.5), y: sy(0.06), fill: "#9A3412", "font-size": "10.5", "font-weight": "800", "text-anchor": "middle" }, svg);
  t3.textContent = "99,74%";
}

// --- Ej. 2 y 3: 4 Estados Equiprobables + Cartera 30/70 + Rendimiento ---
function setG2Peso(w) { document.getElementById("g2-wa").value = w; drawGuiaEj2(); }
function drawGuiaEj2() {
  const waPct = +document.getElementById("g2-wa").value, wa = waPct / 100, wb = 1 - wa;
  const i0 = +document.getElementById("g3-i0").value, f1 = +document.getElementById("g3-f1").value;
  document.getElementById("g2-wa-v").textContent = `${waPct}% A / ${100 - waPct}% B`;
  document.getElementById("g3-i0-v").textContent = "$" + fmtInt(i0);
  document.getElementById("g3-f1-v").textContent = "$" + fmtInt(f1);

  const era = 0.175, erb = 0.055, va = 0.066875, vb = 0.013225, cov = -0.004875;
  const erp = wa * era + wb * erb;
  const vp = wa * wa * va + wb * wb * vb + 2 * wa * wb * cov;
  const sp = Math.sqrt(Math.max(1e-9, vp));
  const r3 = ((f1 - i0) / i0) * 100;

  document.getElementById("g2-k-p").textContent = `${fmtDec(erp * 100, 2)}% | ${fmtDec(sp * 100, 2)}%`;
  document.getElementById("g2-k-vp").textContent = `Var(p) = ${vp.toFixed(6)}`;

  const states = [
    ["Depresión", 0.25, -20, 5], ["Recesión", 0.25, 10, 20], ["Normalidad", 0.25, 30, -12], ["Prosperidad", 0.25, 50, 9]
  ];
  let tbl = `<table class="g-tbl"><thead><tr><th>Estado</th><th>Prob.</th><th>Rent. A</th><th>Rent. B</th><th>Cartera (${waPct}/${100-waPct})</th></tr></thead><tbody>`;
  states.forEach(([nm, p, ra, rb]) => {
    const rp = wa * ra + wb * rb;
    tbl += `<tr><td>${nm}</td><td>${fmtDec(p*100,0)}%</td><td>${fmtDec(ra,1)}%</td><td>${fmtDec(rb,1)}%</td><td><b>${fmtDec(rp,2)}%</b></td></tr>`;
  });
  tbl += `<tr><td><b>Esperado / σ</b></td><td>100%</td><td>17,5% (25,9%)</td><td>5,5% (11,5%)</td><td><b>${fmtDec(erp*100,2)}% (${fmtDec(sp*100,2)}%)</b></td></tr></tbody></table>`;
  document.getElementById("g2-tbl-box").innerHTML = tbl;

  document.getElementById("g2-sol").innerHTML =
    `<b>Ej. 2 (${waPct}% A / ${100-waPct}% B):</b> E(R<sub>p</sub>) = ${fmtDec(wa,2)}(17,5%)+${fmtDec(wb,2)}(5,5%) = <b>${fmtDec(erp*100,2)}%</b> | ` +
    `Var(p) = ${fmtDec(wa,2)}²(0,066875)+${fmtDec(wb,2)}²(0,013225)+2(${fmtDec(wa,2)})(${fmtDec(wb,2)})(−0,004875) = <b>${vp.toFixed(6)}</b> ⇒ σ<sub>p</sub> = <b>${fmtDec(sp*100,2)}%</b><br/>` +
    `<b>Ej. 3 (Rendimiento Simple):</b> R = ($${fmtInt(f1)} − $${fmtInt(i0)}) / $${fmtInt(i0)} = <b>${fmtDec(r3, 2)}%</b>`;

  const svg = document.getElementById("svg-g2-port");
  if (!svg) return;
  svg.innerHTML = "";
  const M = { l: 46, r: 22, t: 20, b: 36 }, W = 460, H = 280;
  const sx = s => M.l + (s / 30) * (W - M.l - M.r);
  const sy = r => H - M.b - (r / 20) * (H - M.t - M.b);
  el("line", { x1: M.l, y1: H - M.b, x2: W - M.r, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);
  el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);
  const pts = [];
  for (let k = 0; k <= 100; k++) {
    const w = k / 100;
    const er = (w * era + (1 - w) * erb) * 100;
    const sd = Math.sqrt(w * w * va + (1 - w) * (1 - w) * vb + 2 * w * (1 - w) * cov) * 100;
    pts.push(`${sx(sd).toFixed(1)},${sy(er).toFixed(1)}`);
  }
  el("polyline", { points: pts.join(" "), fill: "none", stroke: "#1D4ED8", "stroke-width": "2.8" }, svg);
  el("circle", { cx: sx(25.86), cy: sy(17.5), r: 5, fill: "#0F172A" }, svg);
  el("circle", { cx: sx(11.50), cy: sy(5.5), r: 5, fill: "#059669" }, svg);
  el("circle", { cx: sx(sp * 100), cy: sy(erp * 100), r: 7, fill: "#DC2626", stroke: "#FFF", "stroke-width": "2" }, svg);
  const t1 = el("text", { x: sx(sp * 100) + 10, y: sy(erp * 100) + 4, fill: "#DC2626", "font-size": "11", "font-weight": "800" }, svg);
  t1.textContent = `Cartera (${waPct}/${100-waPct})`;
  const tx = el("text", { x: W - M.r, y: H - 8, fill: "#475569", "font-size": "10.5", "text-anchor": "end" }, svg);
  tx.textContent = "Riesgo σp (%)";
}

// --- Ej. 4: Tabla Probabilidades X e Y ---
function renderGuiaEj4() {
  const box = document.getElementById("g4-tbl-box");
  if (!box) return;
  const rows = [
    [0.1, -10, 4], [0.3, 0, 8], [0.3, 6, 0], [0.2, 10, -5], [0.1, 20, 15]
  ];
  const ex = 0.048, ey = 0.033;
  let h = `<table class="g-tbl"><thead><tr><th>Escenario</th><th>Prob. (p)</th><th>Rx</th><th>Ry</th><th>p·(Rx−E[Rx])²</th><th>p·(Ry−E[Ry])²</th><th>p·(Rx−E[Rx])(Ry−E[Ry])</th></tr></thead><tbody>`;
  rows.forEach(([p, rx, ry], i) => {
    const dx = rx / 100 - ex, dy = ry / 100 - ey;
    h += `<tr><td>Esc. ${i+1}</td><td>${fmtDec(p,1)}</td><td>${rx}%</td><td>${ry}%</td><td>${(p*dx*dx).toFixed(6)}</td><td>${(p*dy*dy).toFixed(6)}</td><td>${(p*dx*dy).toFixed(6)}</td></tr>`;
  });
  h += `<tr><td><b>Suma / Total</b></td><td><b>1,0</b></td><td><b>E=4,80%</b></td><td><b>E=3,30%</b></td><td><b>0,005776</b></td><td><b>0,003741</b></td><td><b>+0,000016</b></td></tr></tbody></table>`;
  box.innerHTML = h;
}

// --- Ej. 5 y 6: MSFT y Home Depot (12 meses vs S&P 500) ---
const MESES_12 = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"];
const DATA_56 = {
  msft: {
    lbl: "MSFT (Microsoft)",
    m: [3.25, -3.00, -4.58, 1.16, 1.24, -2.68, 3.15, 3.76, -2.69, 2.08, -3.95, 1.23],
    a: [5.58, -3.08, 2.73, 9.14, 16.22, -3.95, -0.24, 12.86, -3.44, 12.25, -0.20, -2.78]
  },
  hd: {
    lbl: "HD (Home Depot 1995)",
    m: [2.43, 3.61, 2.73, 2.80, 3.63, 2.13, 3.18, -0.03, 4.01, -0.50, 4.10, 1.74],
    a: [1.63, -4.01, -1.39, -5.65, -0.30, -2.10, 7.98, -9.09, -0.31, -6.58, 19.13, 7.61]
  }
};
let caso56 = "msft", ddof56 = 1;
function setCaso56(k) {
  caso56 = k;
  document.getElementById("g56-btn-msft").classList.toggle("active", k === "msft");
  document.getElementById("g56-btn-hd").classList.toggle("active", k === "hd");
  drawGuia56();
}
function setDdof56(d) {
  ddof56 = d;
  document.getElementById("g56-btn-mues").classList.toggle("active", d === 1);
  document.getElementById("g56-btn-pob").classList.toggle("active", d === 0);
  drawGuia56();
}
function drawGuia56() {
  const ds = DATA_56[caso56];
  const n = 12, div = n - ddof56;
  const rm = ds.m.map(v => v / 100), ra = ds.a.map(v => v / 100);
  const mm = rm.reduce((s, v) => s + v, 0) / n;
  const ma = ra.reduce((s, v) => s + v, 0) / n;
  const vm = rm.reduce((s, v) => s + Math.pow(v - mm, 2), 0) / div;
  const va = ra.reduce((s, v) => s + Math.pow(v - ma, 2), 0) / div;
  const cov = rm.reduce((s, v, i) => s + (v - mm) * (ra[i] - ma), 0) / div;
  const sm = Math.sqrt(vm), sa = Math.sqrt(va);
  const rho = cov / (sm * sa), beta = cov / vm, alpha = ma - beta * mm;

  document.getElementById("g56-k-med").textContent = `${fmtDec(mm*100,2)}% | ${fmtDec(ma*100,2)}%`;
  document.getElementById("g56-k-var").textContent = `σM=${fmtDec(sm*100,2)}% | σA=${fmtDec(sa*100,2)}%`;
  document.getElementById("g56-k-var2").textContent = `VarM=${vm.toFixed(6)} | VarA=${va.toFixed(6)}`;
  document.getElementById("g56-k-cov").textContent = `${cov >= 0 ? "+" : ""}${cov.toFixed(6)}`;
  document.getElementById("g56-k-div").textContent = ddof56 === 1 ? "Divisor muestral (n−1 = 11)" : "Divisor poblacional (n = 12)";
  document.getElementById("g56-k-rho").textContent = `ρ=${fmtDec(rho,4)} | β=${fmtDec(beta,2)}`;

  let tbl = `<table class="g-tbl"><thead><tr><th>Mes</th><th>S&amp;P 500</th><th>${ds.lbl.split(" ")[0]}</th><th>Mes</th><th>S&amp;P 500</th><th>${ds.lbl.split(" ")[0]}</th></tr></thead><tbody>`;
  for (let i = 0; i < 6; i++) {
    tbl += `<tr><td>${MESES_12[i]}</td><td>${fmtDec(ds.m[i],2)}%</td><td>${fmtDec(ds.a[i],2)}%</td><td>${MESES_12[i+6]}</td><td>${fmtDec(ds.m[i+6],2)}%</td><td>${fmtDec(ds.a[i+6],2)}%</td></tr>`;
  }
  tbl += `</tbody></table>`;
  document.getElementById("g56-tbl-box").innerHTML = tbl;

  document.getElementById("g56-sol").innerHTML =
    `<b>${ds.lbl} (${ddof56===1 ? "Muestral n−1=11" : "Poblacional n=12"}):</b> ` +
    `Media S&amp;P500 = <b>${fmtDec(mm*100,4)}%</b> | Media Acción = <b>${fmtDec(ma*100,4)}%</b> | ` +
    `Var(M) = <b>${vm.toFixed(6)}</b> | Var(Acc) = <b>${va.toFixed(6)}</b> | Cov = <b>${cov.toFixed(6)}</b> | ` +
    `<b>ρ = ${fmtDec(rho,4)}</b> | <b>β = ${fmtDec(beta,4)}</b> (idénticos bajo n−1 o n).`;

  const svg = document.getElementById("svg-g56-scat");
  if (!svg) return;
  svg.innerHTML = "";
  const M = { l: 48, r: 22, t: 26, b: 36 }, W = 470, H = 330;
  const minX = -6, maxX = 6, minY = -12, maxY = 22;
  const sx = x => M.l + ((x - minX) / (maxX - minX)) * (W - M.l - M.r);
  const sy = y => H - M.b - ((y - minY) / (maxY - minY)) * (H - M.t - M.b);

  el("line", { x1: M.l, y1: sy(0), x2: W - M.r, y2: sy(0), stroke: "#94A3B8", "stroke-dasharray": "4,3" }, svg);
  el("line", { x1: sx(0), y1: M.t, x2: sx(0), y2: H - M.b, stroke: "#94A3B8", "stroke-dasharray": "4,3" }, svg);
  el("line", { x1: M.l, y1: H - M.b, x2: W - M.r, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);
  el("line", { x1: M.l, y1: M.t, x2: M.l, y2: H - M.b, stroke: "#334155", "stroke-width": "1.5" }, svg);

  // Recta característica Ri = alpha + beta * Rm
  const yL = (alpha + beta * (minX / 100)) * 100, yR = (alpha + beta * (maxX / 100)) * 100;
  el("line", { x1: sx(minX), y1: sy(Math.max(minY, Math.min(maxY, yL))), x2: sx(maxX), y2: sy(Math.max(minY, Math.min(maxY, yR))), stroke: "#DC2626", "stroke-width": "2.4" }, svg);

  ds.m.forEach((xm, i) => {
    el("circle", { cx: sx(xm), cy: sy(ds.a[i]), r: 4.8, fill: "#1D4ED8", stroke: "#FFF", "stroke-width": "1.3" }, svg);
  });
  const tt = el("text", { x: W / 2, y: 16, fill: "#0F172A", "font-size": "11.5", "font-weight": "700", "text-anchor": "middle" }, svg);
  tt.textContent = `Recta Característica ${ds.lbl.split(" ")[0]} vs. S&P 500 (β = ${fmtDec(beta, 2)})`;
}

// --- Guía Flujos Ej. 1: Empresa XX Farmacéutico ---
function drawGuiaXX() {
  const i0 = +document.getElementById("gxx-i0").value;
  const rf = +document.getElementById("gxx-rf").value;
  const pr = +document.getElementById("gxx-pr").value;
  document.getElementById("gxx-i0-v").textContent = "$" + fmtInt(i0);
  document.getElementById("gxx-rf-v").textContent = fmtDec(rf, 1) + "%";
  document.getElementById("gxx-pr-v").textContent = fmtDec(pr, 1) + "%";

  const k = (rf + pr) / 100;
  const fl = [-i0, 400000, 700000, 300000];
  const vps = fl.map((v, t) => v / Math.pow(1 + k, t));
  const van = vps.reduce((s, v) => s + v, 0);
  const tir = calcIrr(fl) * 100;

  document.getElementById("gxx-enun").innerHTML =
    `La empresa XX evalúa un producto farmacéutico a 3 años con inversión <b>I<sub>0</sub> = $${fmtInt(i0)}</b> y tasa ajustada por riesgo <b>k = ${fmtDec(rf,1)}% + ${fmtDec(pr,1)}% = ${fmtDec(rf+pr,1)}%</b>. ` +
    `Los flujos esperados ponderando las probabilidades oficiales (donde '−' equivale a $0) son: <b>E(F<sub>1</sub>) = $400.000</b>, <b>E(F<sub>2</sub>) = $700.000</b> y <b>E(F<sub>3</sub>) = $300.000</b>.`;

  document.getElementById("gxx-k-van").textContent = `${van >= 0 ? "+" : "-"}$${fmtInt(Math.abs(van))}`;
  document.getElementById("gxx-k-k").textContent = `Tasa k = ${fmtDec(rf + pr, 1)}%`;
  document.getElementById("gxx-k-tir").textContent = fmtDec(tir, 2) + "%";
  document.getElementById("gxx-k-dec").textContent = van >= 0 ? "ACEPTAR (VAN > 0 y TIR > k)" : "RECHAZAR (VAN < 0)";

  document.getElementById("gxx-sol").innerHTML =
    `<b>VAN(${fmtDec(rf+pr,1)}%):</b> −$${fmtInt(i0)} + $400.000/${fmtDec(1+k,3)} + $700.000/${fmtDec(Math.pow(1+k,2),4)} + $300.000/${fmtDec(Math.pow(1+k,3),4)} ` +
    `= −$${fmtInt(i0)} + $${fmtInt(vps[1])} + $${fmtInt(vps[2])} + $${fmtInt(vps[3])} = <b>${van >= 0 ? "+" : "-"}$${fmtInt(Math.abs(van))}</b> | <b>TIR = ${fmtDec(tir,2)}%</b>`;

  const svg = document.getElementById("svg-gxx");
  if (!svg) return;
  svg.innerHTML = "";
  const M = { l: 74, r: 30, t: 24, b: 40 }, W = 980, H = 265;
  const maxV = 850000, minV = -1600000;
  const sy = v => H - M.b - ((v - minV) / (maxV - minV)) * (H - M.t - M.b);
  el("line", { x1: M.l, y1: sy(0), x2: W - M.r, y2: sy(0), stroke: "#0F172A", "stroke-width": "1.6" }, svg);
  const slot = (W - M.l - M.r) / 4, bw = 62;
  ["Año 0 (I0)", "Año 1 (E[F1])", "Año 2 (E[F2])", "Año 3 (E[F3])"].forEach((lb, t) => {
    const cx = M.l + t * slot + slot / 2;
    const drawB = (x, val, col) => {
      const yT = sy(Math.max(0, val)), yB = sy(Math.min(0, val));
      el("rect", { x, y: yT, width: bw, height: Math.max(2, yB - yT), fill: col, rx: 3 }, svg);
    };
    drawB(cx - bw - 3, fl[t], t === 0 ? "#DC2626" : "#94A3B8");
    drawB(cx + 3, vps[t], t === 0 ? "#991B1B" : "#1D4ED8");
    const tv = el("text", { x: cx, y: fl[t] >= 0 ? sy(fl[t]) - 6 : sy(fl[t]) + 14, fill: "#0F172A", "font-size": "10.5", "font-weight": "800", "text-anchor": "middle" }, svg);
    tv.textContent = `VP: ${vps[t] >= 0 ? "" : "-"}$${fmtInt(Math.abs(vps[t]))}`;
    const tl = el("text", { x: cx, y: H - 10, fill: "#334155", "font-size": "11", "font-weight": "700", "text-anchor": "middle" }, svg);
    tl.textContent = lb;
  });
}

renderLecturaFin();
renderQuizFin();
drawGuiaEj1();
drawGuiaEj2();
renderGuiaEj4();
drawGuia56();
drawGuiaXX();
</script>
</body>
</html>
"""


def renderizar_estudio_fluido_finanzas_60fps():
    """Renderiza el Estudio Financiero Integral a 60 FPS (8 módulos) sin recarga de servidor."""
    components.html(HTML_FINANZAS_60FPS, height=1180, scrolling=True)
