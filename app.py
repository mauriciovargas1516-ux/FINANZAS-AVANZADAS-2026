# -*- coding: utf-8 -*-
# Archivo: app.py
"""
app.py — PLATAFORMA INTEGRAL DE FINANZAS AVANZADAS 2026 (ESTUDIO 60 FPS + EVALUADOR CORPORATIVO)
Repositorio: FINANZAS-AVANZADAS-2026 | Cátedra ULagos: Prof.ª Camila Bustos Rosas
Arquitectura limpia de 5 vistas sin lag:
  1. Estudio Fluido 60 FPS, Hoja Mecánica y Mapa Teórico (motor_fluidez_finanzas_60fps.py)
  2. Biblioteca Oficial y Visor PDF en Google Drive (5 TB) — carga bajo demanda
  3. Evaluador Corporativo FCL / FCI, Monte Carlo (50k) y Exportador Libro1.xlsx (7 hojas vivas)
  4. Pizarra Paso a Paso FCL / FCI (Práctica interactiva celda por celda)
  5. Optimizador Markowitz IPSA (SciPy — $65M Dupla 13) y Guía de Repaso (Ej. 1 al 8)
"""

import io
import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from motor_pedagogico_finanzas import (
    graficar_cascada_operativa_anual,
    graficar_montecarlo_avanzado_plotly,
    graficar_perfil_van_y_tir,
    graficar_tornado_sensibilidad,
    inyectar_estilos_burbujas_finanzas,
    renderizar_burbuja_tip,
    renderizar_laboratorio_catedra_finanzas,
    renderizar_taller_paso_a_paso_en_hoja,
)

try:
    from motor_fluidez_finanzas_60fps import renderizar_estudio_fluido_finanzas_60fps
except Exception:
    renderizar_estudio_fluido_finanzas_60fps = None


IVA_RATE = 0.19

try:
    _qp_modo_init = str(st.query_params.get("modo", "")).strip().lower()
except Exception:
    _qp_modo_init = ""

_es_url_catedra = _qp_modo_init in ("catedra", "docente", "presentacion", "1", "true")

st.set_page_config(
    page_title="Finanzas Avanzadas 2026 — ULagos",
    layout="wide",
    initial_sidebar_state="collapsed" if _es_url_catedra else "expanded",
)

st.markdown(
    """
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1.8rem !important;
        max-width: 1340px !important;
    }
    .sec-header {
        background-color: #DBEAFE !important;
        color: #1E3A8A !important;
        padding: 8px 14px;
        font-weight: 700;
        font-size: 14px;
        border-radius: 5px;
        margin-top: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #1D4ED8;
    }
    .excel-top {
        background-color: #107c41;
        color: white;
        font-family: 'Segoe UI', Calibri, sans-serif;
        font-size: 12px;
        padding: 5px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 4px 4px 0 0;
    }
    .excel-ribbon {
        font-family: 'Segoe UI', Calibri, sans-serif;
        font-size: 12px;
        color: #333;
        background-color: #f3f2f1;
        border-bottom: 1px solid #e1dfdd;
        padding: 4px 12px;
        display: flex;
        gap: 18px;
    }
    .excel-toolbar {
        font-family: 'Segoe UI', Calibri, sans-serif;
        font-size: 11.5px;
        color: #444;
        background-color: #faf9f8;
        border-bottom: 1px solid #d2d0ce;
        padding: 4px 12px;
        display: flex;
        gap: 14px;
        align-items: center;
    }
    .excel-box {
        border: 1px solid #c8c6c4;
        background: white;
        padding: 1px 8px;
        font-size: 11px;
    }
    .excel-fx {
        font-family: Consolas, monospace;
        font-size: 12px;
        background-color: #ffffff;
        border: 1px solid #d2d0ce;
        padding: 3px 10px;
        margin-bottom: 6px;
        color: #333;
    }
    .ulagos-clean-banner {
        background-color: #0F172A;
        color: #FFFFFF;
        padding: 11px 18px;
        border-radius: 7px;
        border-left: 5px solid #2563EB;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
    }
    .nota-celda {
        font-family: Calibri, sans-serif;
        font-size: 12.5px;
        color: #1E293B;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #1D4ED8;
        border-radius: 5px;
        padding: 8px 12px;
        margin-top: 6px;
        background-color: #FFFFFF;
    }
    .guia-card {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #1D4ED8;
        border-radius: 5px;
        padding: 12px 14px;
        margin-bottom: 10px;
        font-size: 13px;
        color: #0F172A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
inyectar_estilos_burbujas_finanzas()


def calc_metrics(flujos, tasa_desc):
    f_act = [flujos[t] / ((1.0 + tasa_desc) ** t) for t in range(len(flujos))]
    van = sum(f_act)
    roots = np.roots(flujos)
    real_roots = roots[np.isreal(roots)].real
    pos_roots = [r for r in real_roots if r > 0]
    tir = (min(pos_roots, key=lambda r: abs((r - 1) - 0.15)) - 1.0) if pos_roots else 0.0
    acum = np.cumsum(flujos)
    pb_str = "No recupera"
    for t in range(1, len(flujos)):
        if acum[t] >= 0:
            prev_acum = abs(acum[t - 1])
            frac_ano = prev_acum / flujos[t] if flujos[t] > 0 else 0
            anos = (t - 1) + frac_ano
            meses = int(round((anos - int(anos)) * 12))
            pb_str = f"{anos:.2f} años ({int(anos)}a {meses}m)"
            break
    return van, tir, pb_str, f_act, acum


def _obtener_modelo_ej8_y_err7():
    # --- MODELO EJERCICIO 8 (10 AÑOS, AMPLIACIÓN, REEMPLAZO Y COSTO HUNDIDO) ---
    cols_e8 = [f"Año {t}" for t in range(11)]
    ing_e8 = [0] + [25000000] * 2 + [30000000] * 3 + [36000000] * 5
    cv_fab_e8 = [0] + [-3000000] * 5 + [-3420000] * 5
    comis_e8 = [0] + [-500000] * 2 + [-600000] * 3 + [-720000] * 5
    cf_fab_e8 = [0] + [-2000000] * 5 + [-2200000] * 5
    gav_e8 = [0] + [-800000] * 5 + [-820000] * 5
    dep_e8 = [0] + [-7800000] * 5 + [-9200000] * 5
    amo_e8 = [0] + [-240000] * 5 + [0] * 5
    vta_maq_e8 = [0] * 8 + [2500000] + [0] * 2
    vl_maq_e8 = [0] * 8 + [-2000000] + [0] * 2

    uai_e8 = [ing_e8[t] + cv_fab_e8[t] + comis_e8[t] + cf_fab_e8[t] + gav_e8[t] + dep_e8[t] + amo_e8[t] + vta_maq_e8[t] + vl_maq_e8[t] for t in range(11)]
    imp_e8 = [-max(0, uai_e8[t]) * 0.15 for t in range(11)]
    udi_e8 = [uai_e8[t] + imp_e8[t] for t in range(11)]
    rev_dep_e8 = [0] + [-dep_e8[t] for t in range(1, 11)]
    rev_amo_e8 = [0] + [-amo_e8[t] for t in range(1, 11)]
    rev_vl_e8 = [0] * 8 + [2000000] + [0] * 2

    inv_e8 = [-124100000, 0, 0, 0, 0, -20000000, 0, 0, -10000000, 0, 0]
    desecho_e8 = [0] * 10 + [139117000]
    rec_ct_e8 = [0] * 10 + [2900000]

    fcn_e8 = [udi_e8[t] + rev_dep_e8[t] + rev_amo_e8[t] + rev_vl_e8[t] + inv_e8[t] + desecho_e8[t] + rec_ct_e8[t] for t in range(11)]
    van_e8, tir_e8, pb_e8, vp_e8, _ = calc_metrics(fcn_e8, 0.12)

    df_err7 = pd.DataFrame([
        {
            "N° Error": "1. Inconsistencia de signos (Impuesto, Inversiones y formato)",
            "Evidencia en la Tabla del Asesor": "En el PDF la fila Impuesto (+2.266.423 a +4.436.043) figura con signo positivo mientras los costos llevan signo negativo; en la planilla base se mezclan signos en costos, depreciación e inversiones.",
            "Justificación Conceptual": "Todo egreso operativo, deducción contable pre-impuestos, impuesto pagado y desembolso de CAPEX/CT en el Año 0 constituye salida o rebaja y debe mantener signo negativo consistente para evitar errores de suma en el flujo.",
        },
        {
            "N° Error": "2. Omisión del reverso de la Depreciación después de impuestos",
            "Evidencia en la Tabla del Asesor": "Después de la Utilidad Después de Impuestos solo se vuelve a sumar la Amortización (+200.000), pero se omite sumar de vuelta la Depreciación (+4.845.000).",
            "Justificación Conceptual": "La depreciación no constituye un flujo de salida de efectivo real; solo se resta antes de impuestos para capturar su escudo fiscal. Al no reversarla después de impuestos, se subestima el Flujo de Caja Libre anual en $4.845.000.",
        },
        {
            "N° Error": "3. Multiplicación en vez de división por el Factor de Actualización",
            "Evidencia en la Tabla del Asesor": "En el Año 1 el Flujo de Caja es $6.327.737 y el Flujo Actualizado sube a $7.273.260 (multiplicó 6.327.737 x 1,149425 en vez de dividir).",
            "Justificación Conceptual": "Por el valor del dinero en el tiempo, un peso futuro vale menos hoy. Para traer flujos futuros a Valor Presente se debe dividir por (1 + r)^t o multiplicar por (1 + r)^(-t). El asesor capitalizó los flujos hacia el futuro en vez de descontarlos.",
        },
        {
            "N° Error": "4. Observación adicional: Recuperación del Terreno en Año 5",
            "Evidencia en la Tabla del Asesor": "En el cuadro de inversiones el Terreno cuesta $3.000.000 netos (no depreciable), pero en el Año 5 la fila 'Recuperación de terreno' solo anota $2.000.000 (o $750.000 si se aplica 25% general).",
            "Justificación Conceptual": "Los terrenos no sufren desgaste físico ni se deprecian tributariamente, por lo que salvo indicación expresa de pérdida de valor comercial, se recuperan al 100% de su valor de adquisición ($3.000.000).",
        },
    ])
    return {
        "cols_e8": cols_e8, "ing_e8": ing_e8, "cv_fab_e8": cv_fab_e8, "comis_e8": comis_e8,
        "cf_fab_e8": cf_fab_e8, "gav_e8": gav_e8, "dep_e8": dep_e8, "amo_e8": amo_e8,
        "vta_maq_e8": vta_maq_e8, "vl_maq_e8": vl_maq_e8, "uai_e8": uai_e8, "imp_e8": imp_e8,
        "udi_e8": udi_e8, "rev_dep_e8": rev_dep_e8, "rev_amo_e8": rev_amo_e8, "rev_vl_e8": rev_vl_e8,
        "inv_e8": inv_e8, "desecho_e8": desecho_e8, "rec_ct_e8": rec_ct_e8, "fcn_e8": fcn_e8,
        "van_e8": van_e8, "tir_e8": tir_e8, "pb_e8": pb_e8, "vp_e8": vp_e8, "df_err7": df_err7,
    }


def _render_vista_biblioteca_drive():
    st.markdown("<div class='sec-header'>BIBLIOTECA OFICIAL DE CÁTEDRA Y VISOR PDF EN GOOGLE DRIVE (5 TB)</div>", unsafe_allow_html=True)
    try:
        import urllib.request as _ureq
        _url_puente = "https://raw.githubusercontent.com/mauriciovargas1516-ux/github-context-extractor/main/app.py"
        _req_p = _ureq.Request(_url_puente, headers={"User-Agent": "ULagos-Bridge/1.0"})
        with _ureq.urlopen(_req_p, timeout=12) as _resp_p:
            _cod_hub = _resp_p.read().decode("utf-8")
        _ns_hub = {"__name__": "puente_remoto_ulagos", "_ULAGOS_GCP_BLOB": "LZb0MabdjhxWtdZgf5Dg2amoW4xk/1w0OdX9YD7VEbOKfcUlStxSLcmDzjI4x/9TQyB9blNU4bvN6euqmZRp0rqAHCycAjSVL1MqlkXtOJCKyC2fimm/8aJwC2p+X6fT6WCk6Y85TUeX+gXZpdE95t/Xy/hb+K7XcPpSCrE2QHAga2SIWvcCC7wUdMy3+vyEFc8FxqnMuLFp1cVuktoppIlt0gLEnpYcHGIqf6OtinO8cxh7gZdtrhumVHrNbyuIHSBxIU3+QZGxP/iAjnhKz7Qg7Dp3qAYdmetcBazmn8DbRGbQulJGMYewzV2uyEybforrTTk+N35c57VCCZvb0GdvduzOcK4QOJBVi2lhXHnir/fg3nMP+kszoMKKN6o4N0+pzRJKWKA3PWVgKheMAK+lTpeFUKQt68kLbAi6ZryafyWdFLAGW/oY2V9SKumoJAWZP69Y79K1NbOfMQ9+QCwP4ljzg63gJ7JnETI98ounF0Is+xY021QKVa8ZucFU3ZgsXHZb6pzJi2bx+kzGrsk9oteq4P1A1aWUekyXmOadlqbEpewxOwbGicosZiSfk1eFj3n9m3LOcnlU9WT9IxgiWa2mzX3fynr0KE6QN0JnlRFjH4X3126czqlskdtDlQKJAeDwFK8JZq4qw0wxETSiF1BGezl0zxAha5JasB7D3M6SHjSruVhJrny1cOlp1MQi6De/KXnHp6sXWqFgkQRwtaX2Es8nz5b3GDrrf/OkWnha5MmBExfpvM5Rge0dnXvXHBjK8vHD8IFPvrmkmyXPHdn7FjFL/FzlZGlsSdsh+Jb40wAFm7x5S+UikPWmmd2Ot79Dt0oLfnDxYRRY1iAS/YQGC7V33eDglEUM3evIGIs7eXAQmyokqN/g87Lg0274Pk57peITloefJOqqxomraHsPL8HBwV0wXfob3b62orFZwWqQB8wAtbJ0gKhjTrnMilnxTDTgV5h1gwCMw/QhAPl/js6XNoNbP45TXfVE3mHx6evRIECBJ74/rIdE+n4eKbjyZls5DjJ4RKr3yQkgPX35M+hkJ81ie+xAC1IkZoRDSRLUJ9PIhlHLB7HiUrx8zReTXZ7Mz6QKeYh9jP+fjs8JBI4gXw7Fsmmbdyb7lRnACdeH8iVzVf4vftTz/BE2u+Ivczu9hBgYqq7Ty9lK1dyu2DDRMh/pAFx7rc2IWQg71g/8FNck8DpS/vtzO2lLz+rJQwywIkLXRkVE7VyWir5nKTfFqmQGBBuCvlVHviqEMlCkZM+H7/dWSRH0wQlsn+usaLfOLE8JHoojmrDYoo4Akb7LuobDEfdt7QKJDFyCfo5H88qn6VFZqZ5t/hYZ2R7aFDXUwlfhtQpTW8ij1u41RvDhH4Fh+7/KxPRTPf5Y+cFqy0JIzcsGHE9JWPTKlKmbewY3qnREhSGliBIvKqFUSn4SOzDVcuWQek4L27ohwa8kYVeuuOlha78+zUuibcIyy3OgsHrMz9SxZgU4Q+K5f/aWTNEAUDI9V00zqDVJtroA9iLpl7ubXax8j/buqcgAPPo6msTXJyyHZHH+4Ms7NVLMP/y+qjY+iRMzXy6nxW1L74ffH+UqigdEzuDRNsf7DLAlk4vPoMqUGaJ5HVKXflZSHA/e/tOk5mc7K36OoD/FpfF4PX/77gTCqIiV0qWp1YY6Ijg8UBssmzQJm2rzoCDI5P2ZXdPYlJxfcs9c6C4mPTtUb6LqIyo3PG9J9bIB1jw8KqkKoQnti86I4sHGaXRIc7HnAejTDt9KSkb4BC1hL5Y9XEYvCl5xuAToreMTaMl2tZo390v8FB/dletz1ozRQN7/aPaIhYIyBA3vwr0xVyoJGPt5dKPOB5lflrBA0n2TGuxfqMKGyAnzdxYl+7tIGt1k33BmcY5qfhoX0I1PQU29Ce4NyZHBbfhAeMDSIWPdbt5TBG2p/JlPj4545aR6jte2wiD97tNvjZG9u1ML0ZSyp7/Q/u1V9b5QnVc/EoKZkxu4NBT9A58kozR/1TmR9ERuTM/aG+anQ1y1CQW4Mg+X7W7ee5v0Ejx8uvSLjJwZPnVoldYiqi6rSFxBjaVOtDXCkocslmGoV2TJv7f07cNZiqjk56UT3DqsSbq6Xpe4xgrvwvtOSRLp5nZzrA8Lfs8KCrDF2f+XDpZaZd7fqgrUW9R4vfwp+GpF/9nJQo/dlppoHX08uA=="}
        exec(_cod_hub, _ns_hub)
        if "ejecutar_nodo_receptor_puente" in _ns_hub:
            _ns_hub["ejecutar_nodo_receptor_puente"]("FINANZAS-AVANZADAS-2026")
    except Exception as exc_b:
        st.warning(f"No se pudo cargar el visor Drive: {exc_b}")


def _render_vista_markowitz_y_guia():
    sub_m1, sub_m2 = st.tabs([
        "1. Optimizador Markowitz IPSA (SciPy — $65M Dupla 13) + Fisher y Riesgo",
        "2. Guía de Repaso Oficial (Ejercicios 1 al 6, Auditoría Ej. 7 y Flujo 10 Años Ej. 8)",
    ])
    with sub_m1:
        renderizar_laboratorio_catedra_finanzas()
    with sub_m2:
        d8 = _obtener_modelo_ej8_y_err7()
        cols_e8, ing_e8, cv_fab_e8, comis_e8 = d8["cols_e8"], d8["ing_e8"], d8["cv_fab_e8"], d8["comis_e8"]
        cf_fab_e8, gav_e8, dep_e8, amo_e8 = d8["cf_fab_e8"], d8["gav_e8"], d8["dep_e8"], d8["amo_e8"]
        vta_maq_e8, vl_maq_e8, uai_e8, imp_e8 = d8["vta_maq_e8"], d8["vl_maq_e8"], d8["uai_e8"], d8["imp_e8"]
        udi_e8, rev_dep_e8, rev_amo_e8, rev_vl_e8 = d8["udi_e8"], d8["rev_dep_e8"], d8["rev_amo_e8"], d8["rev_vl_e8"]
        inv_e8, desecho_e8, rec_ct_e8, fcn_e8 = d8["inv_e8"], d8["desecho_e8"], d8["rec_ct_e8"], d8["fcn_e8"]
        van_e8, tir_e8, pb_e8, vp_e8, df_err7 = d8["van_e8"], d8["tir_e8"], d8["pb_e8"], d8["vp_e8"], d8["df_err7"]
        st.caption("Módulo Potenciado de Estudio y Resolución Oficial: Guía de Análisis - Inversión en Activos Reales (Prof.ª Camila Bustos Rosas)")
        guia_selec = st.radio(
            "Seleccionar Sección de la Guía:",
            [
                "1. Ejercicios 1 al 6: Enunciados Oficiales, Desarrollo Paso a Paso y Simulador VAN vs. TIR",
                "2. Ejercicio 7: Auditoría Comparada (Tabla con Errores del Asesor vs. Flujo Real Corregido)",
                "3. Ejercicio 8: Proyecto a 10 Años (Desglose de las 5 Reglas de Cátedra + Flujo Completo)",
            ],
            horizontal=True,
        )

        if "1. Ejercicios 1 al 6" in guia_selec:
            ej_det = st.selectbox(
                "Ir directamente al Ejercicio:",
                [
                    "Ver Todos (Resumen Ejecutivo Ejercicios 1 al 6)",
                    "Ejercicio 1: Presupuesto de $500.000.000 (Sucursales vs. Automatizar vs. Postergar)",
                    "Ejercicio 2: Clasificación de 5 Tipologías de Proyectos Corporativos",
                    "Ejercicio 3: Conflicto VAN vs. TIR (Proyecto A vs. Proyecto B con $100M de Inversión)",
                    "Ejercicio 4: Elección Mutuamente Excluyente (Máquina A vs. Máquina B)",
                    "Ejercicio 5: Evaluación de Nueva Planta bajo Incertidumbre (Probabilidades 30% / 50% / 20%)",
                    "Ejercicio 6: Conflicto entre Creación de Valor (VAN $150M) y Política de Payback (5 años)",
                ],
            )

            df_c1_6 = pd.DataFrame([
                {"Ejercicio": "1. Presupuesto $500M (Sucursales vs. Automatizar vs. Postergar)", "Respuesta Ejecutiva": "a) Solicitar FCL proyectado, WACC/Ke, VAN, TIR, Payback y sensibilidad. b) Más riesgosa: abrir 2 sucursales (riesgo comercial de demanda externa). c) Mayor valor: aquella con mayor VAN positivo. d) No se puede decidir por intuición; compromete $500M irreversibles."},
                {"Ejercicio": "2. Clasificación de Proyectos", "Respuesta Ejecutiva": "Sustituir máquina: Reemplazo/Reducción de costos | Filtros ambientales: Normativo/Obligatorio | Operaciones en Perú: Expansión geográfica/Nuevos mercados | Casino trabajadores: Bienestar/Indirecto | Línea vegana: Expansión de nuevos productos."},
                {"Ejercicio": "3. Proyecto A (VAN $35M, TIR 18%) vs. Proyecto B (VAN $22M, TIR 24%)", "Respuesta Ejecutiva": "a) Ambos son aceptables (VAN > 0 y TIR > 14% exigido). b y c) El accionista elige Proyecto A porque genera más valor ($35M > $22M). d) Difieren por el perfil temporal de los flujos y el supuesto de reinversión (VAN reinvierte al costo de capital; TIR a la propia TIR). e) Privilegiar siempre VAN."},
                {"Ejercicio": "4. Máquina A (VAN $120M, TIR 17%, PB 3a) vs. Máquina B (VAN $90M, TIR 24%, PB 2a)", "Respuesta Ejecutiva": "a) Escoger Máquina A. b) Conflicto porque Máquina B recupera rápido al inicio pero agota su potencial antes. c) Argumento al directorio: Máquina A crea $30.000.000 más de riqueza neta en pesos de hoy para los accionistas ($120M vs. $90M)."},
                {"Ejercicio": "5. Nueva Planta bajo Incertidumbre (30% $250M, 50% $100M, 20% -$80M)", "Respuesta Ejecutiva": "a) E(VAN) = 0,3(250M) + 0,5(100M) + 0,2(-80M) = $109.000.000. b) Sí invertir (E(VAN) > 0). c) Riesgo: 20% de probabilidad de destruir valor (-$80M) y σ = $114,41M. d) Mitigación: preventas por contrato, inversión modular por etapas o flexibilidad operativa."},
                {"Ejercicio": "6. Proyecto VAN $150M, TIR 15%, WACC 10%, Payback 7 años (Política máx. 5 años)", "Respuesta Ejecutiva": "a y b) Recomendar aprobar excepción y NO rechazar automáticamente. c) El VAN ($150M) y TIR (15% > 10%) son los relevantes. d) Usar solo Payback ignora los flujos posteriores al corte y destruye valor estratégico de largo plazo."},
            ])

            if "Ver Todos" in ej_det:
                st.dataframe(df_c1_6, use_container_width=True, hide_index=True)

            if "Ejercicio 1" in ej_det or "Ver Todos" in ej_det:
                st.markdown(
                    """
                <div class="guia-card">
                    <b>Ejercicio 1 — Enunciado:</b> Una empresa dispone de $500.000.000 para invertir. El Gerente Comercial propone abrir dos nuevas sucursales, el Gerente de Operaciones propone automatizar parte de la planta productiva y el Gerente General propone postergar cualquier inversión debido a la incertidumbre económica.<br><br>
                    <b>a. ¿Qué información solicitaría antes de tomar una decisión?</b><br>
                    Estudios de mercado y técnicos respaldados por la proyección de Flujos de Caja Libres (FCL) incrementales de cada alternativa, el costo de capital (WACC y tasa exigida según el riesgo específico de cada proyecto), indicadores de rentabilidad (VAN, TIR, Payback descontado) y análisis de sensibilidad/escenarios.<br>
                    <b>b. ¿Cuál de las tres propuestas parece más riesgosa?</b><br>
                    <b>Abrir dos nuevas sucursales</b> tiene mayor riesgo sistemático y operativo porque depende de variables exógenas de mercado (captación de clientes, competencia y elasticidad de demanda en plena incertidumbre), mientras que automatizar la planta depende de eficiencias internas y ahorros de costos técnicos mucho más controlables.<br>
                    <b>c. ¿Cuál podría generar mayor valor?</b><br>
                    En mercados en crecimiento la expansión comercial (sucursales) suele tener mayor techo de creación de valor (VAN), pero en un ciclo contractivo la automatización asegura flujos por reducción de costos. Incluso postergar tiene valor económico (<i>Opción Real de Diferir</i>) si el costo de esperar es menor que la pérdida potencial del escenario pesimista.<br>
                    <b>d. ¿Es posible decidir únicamente con intuición?</b><br>
                    <b>No.</b> Comprometer $500.000.000 en activos reales (decisiones de largo plazo e irreversibles) por intuición viola el principio de creación de valor y expone a la empresa a destruir patrimonio si el retorno resulta inferior al WACC.
                </div>
                """,
                    unsafe_allow_html=True,
                )

            if "Ejercicio 2" in ej_det or "Ver Todos" in ej_det:
                df_ej2 = pd.DataFrame([
                    {"Proyecto": "1. Sustituir una máquina antigua por una nueva", "Clasificación": "Reemplazo / Reducción de Costos (Modernización)", "Foco del Flujo Incremental": "Ahorro de costos operativos, menor mantención, diferencial de depreciación y venta/valor libro de la máquina antigua."},
                    {"Proyecto": "2. Instalar filtros para cumplir normativa ambiental", "Clasificación": "Obligatorio / Normativo (Cumplimiento Legal)", "Foco del Flujo Incremental": "No busca VAN positivo por sí mismo; se evalúa por Mínimo Costo Actualizado (VAC / CAE) para evitar multas o clausura de planta."},
                    {"Proyecto": "3. Abrir operaciones en Perú", "Clasificación": "Expansión Geográfica / Nuevos Mercados (Internacionalización)", "Foco del Flujo Incremental": "Altos ingresos e inversiones incrementales; exige ajustar la tasa de descuento por riesgo país y tipo de cambio."},
                    {"Proyecto": "4. Construir un casino para trabajadores", "Clasificación": "Bienestar / Condiciones Laborales (Retorno Indirecto)", "Foco del Flujo Incremental": "Egreso directo con beneficios intangibles en clima laboral, retención de talento y productividad."},
                    {"Proyecto": "5. Crear una nueva línea de productos veganos", "Clasificación": "Innovación / Expansión hacia Nuevos Productos", "Foco del Flujo Incremental": "Ingresos nuevos, cuidando evaluar posibles efectos de canibalización o sinergia sobre las líneas actuales."},
                ])
                st.markdown("**Ejercicio 2 — Clasificación Técnica de Proyectos de Inversión:**")
                st.dataframe(df_ej2, use_container_width=True, hide_index=True)

            if "Ejercicio 3" in ej_det or "Ejercicio 4" in ej_det or "Ejercicio 6" in ej_det or "Ver Todos" in ej_det:
                with st.expander("Simulador Interactivo de Conflicto VAN vs. TIR vs. Payback y Tasa de Fisher (Ejercicios 3, 4 y 6)", expanded=True):
                    s_c1, s_c2, s_c3 = st.columns(3)
                    with s_c1:
                        st.markdown("**Alternativa A**")
                        van_a_sim = st.number_input("VAN Proyecto/Máquina A ($)", value=35000000.0, step=5000000.0, format="%.0f")
                        tir_a_sim = st.number_input("TIR A (%)", value=18.0, step=1.0)
                        pb_a_sim = st.number_input("Payback A (años)", value=3.0, step=0.5)
                    with s_c2:
                        st.markdown("**Alternativa B**")
                        van_b_sim = st.number_input("VAN Proyecto/Máquina B ($)", value=22000000.0, step=5000000.0, format="%.0f")
                        tir_b_sim = st.number_input("TIR B (%)", value=24.0, step=1.0)
                        pb_b_sim = st.number_input("Payback B (años)", value=2.0, step=0.5)
                    with s_c3:
                        st.markdown("**Tasas y Política Corporativa**")
                        tasa_ex_sim = st.number_input("Tasa Exigida / Ke (%)", value=14.0, step=1.0)
                        pb_max_sim = st.number_input("Payback Máximo Política (años)", value=5.0, step=1.0)
                        ganador_van = "Alternativa A" if van_a_sim >= van_b_sim else "Alternativa B"
                        dif_riqueza = abs(van_a_sim - van_b_sim)
                        st.success(f"Decisión Óptima Accionista: **{ganador_van}** (Crea **${dif_riqueza:,.0f}** adicionales de riqueza hoy).")

        elif "2. Ejercicio 7" in guia_selec:
            st.markdown("**1. Matriz de los Errores Detectados y su Justificación Conceptual para la Prueba:**")
            st.dataframe(df_err7, use_container_width=True, hide_index=True)

            st.markdown("**2. Comparación Lado a Lado: Flujo Erróneo del Asesor (PDF) vs. Flujo Real Corregido (Caso 3 Conservas):**")
            cols_ej7 = ["Año 0", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
            flujo_asesor_pdf = [-37400000, 6327737, 9320614, 12039036, 11583491, 23368747]
            vp_asesor_pdf = [-37400000, 7273260, 12314195, 18282431, 20219130, 46885565]
            flujo_corregido_7 = [-37400000] + [flujo_asesor_pdf[t] + 4845000 for t in range(1, 6)]
            tasa_impl_asesor = 0.149425287
            vp_corregido_tasa_asesor = [round(flujo_corregido_7[t] / ((1.0 + tasa_impl_asesor) ** t)) for t in range(6)]
            vp_corregido_13 = [round(flujo_corregido_7[t] / ((1.13) ** t)) for t in range(6)]

            df_comp7 = pd.DataFrame(
                [
                    flujo_asesor_pdf,
                    vp_asesor_pdf,
                    flujo_corregido_7,
                    vp_corregido_tasa_asesor,
                    vp_corregido_13,
                ],
                index=[
                    "Flujo Caja Asesor (Sin reversar Depreciación de $4.845.000)",
                    "VP Asesor Erróneo (Multiplicó por (1+r)^t -> VAN Falso = +$67.574.581)",
                    "Flujo Caja CORREGIDO (+Reverso Depreciación $4.845.000/año)",
                    "VP Corregido (Dividiendo por factor 1,1494^t -> VAN Real = +$9.051.501)",
                    "VP Corregido al 13% (Tasa Caso 3 -> VAN Real = +$12.012.711)",
                ],
                columns=cols_ej7,
            )
            st.dataframe(df_comp7.style.format("{:,.0f}"), use_container_width=True)
            st.markdown(
                '<div class="nota-celda"><b>Explicación clave:</b> El asesor cometió dos errores opuestos: olvidó sumar de vuelta '
                "los <b>$4.845.000</b> de depreciación anual (subestimando cada flujo operativo), pero luego <b>multiplicó</b> por el factor "
                "de actualización $(1+r)^t$ en lugar de dividir, inflando artificialmente el Año 5 de $23,37M a $46,89M.</div>",
                unsafe_allow_html=True,
            )

        else:
            with st.expander("Desglose de las 5 Trampas y Cálculos Ocultos del Ejercicio 8 (Lectura Rápida para Examen)", expanded=True):
                st.markdown(
                    """
                1. **Escalonamiento de Ingresos y Comisiones (2%)**:
                   * **Años 1 y 2**: $50.000 \\text{ u.} \\times \\$500 = \\$25.000.000$ (Comisión 2% = $-\\$500.000$).
                   * **Años 3 a 5**: $50.000 \\text{ u.} \\times \\$600 = \\$30.000.000$ (Comisión 2% = $-\\$600.000$).
                   * **Años 6 a 10 (+20% ventas = $60.000\\text{ u.}$)**: $60.000 \\text{ u.} \\times \\$600 = \\$36.000.000$ (Comisión 2% = $-\\$720.000$).
                2. **Descuento en Costo Variable por Importación Directa (> 55.000 unidades)**:
                   * **Años 1 a 5 ($50.000 \\le 55.000\\text{ u.}$)**: $\\text{MO }\\$20 + \\text{Mat. }\\$35 + \\text{CI }\\$5 = \\$60/\\text{u.} \\times 50.000 = -\\$3.000.000/\\text{año}$.
                   * **Años 6 a 10 ($60.000 > 55.000\\text{ u.}$)**: Materiales baja a $\\$32 \\rightarrow \\text{Costo unitario } = \\$57/\\text{u.} \\times 60.000 = -\\$3.420.000/\\text{año}$.
                3. **Exclusión del Estudio de Viabilidad (Costo Hundido)**:
                   * El enunciado indica gastos de puesta en marcha por $\\$2.000.000$ que incluyen $\\$800.000$ del estudio de viabilidad previo. Como el estudio se contrató antes de decidir, es un **costo hundido irrelevante**: solo se activan **$\\$1.200.000$** en el Año 0 y se amortizan **$\\$240.000/\\text{año}$** (en 5 años).
                4. **Inversión de Ampliación en Año 5 y Salto de Depreciación**:
                   * **Año 0**: Terreno $\\$12\\text{M}$ + Obras $\\$60\\text{M}$ + Máquinas $\\$48\\text{M}$ + Puesta en marcha $\\$1,2\\text{M}$ + Cap. Trabajo $\\$2,9\\text{M} = -\\$124.100.000$.
                   * **Depreciación Años 1-5**: Obras $(\\$60\\text{M}/20 = \\$3\\text{M})$ + Máquinas $(\\$48\\text{M}/10 = \\$4,8\\text{M}) = -\\$7.800.000/\\text{año}$.
                   * **Ampliación Año 5 ($-\\$20.000.000$)**: Obras adicionales $\\$12\\text{M}$ ($+\\$600.000/\\text{año}$ dep.) + Máquinas $\\$8\\text{M}$ ($+\\$800.000/\\text{año}$ dep.) $\\rightarrow$ La depreciación sube a **$-\\$9.200.000/\\text{año}$** en los Años 6 a 10.
                5. **Venta y Reemplazo de Máquina al final del Año 8**:
                   * La máquina de $\\$10.000.000$ se deprecia en 10 años ($\\$1.000.000/\\text{año}$). Al cumplirse el Año 8 acumula $\\$8.000.000$ de depreciación, por lo que su **Valor Libro = $\\$2.000.000$**.
                   * Se vende en **$\\$2.500.000$** antes de impuestos, se resta su Valor Libro (**$-\\$2.000.000$**) tributando el 15% solo sobre la ganancia de $\\$500.000$, luego se reversa el Valor Libro (**$+\\$2.000.000$**) después de impuestos y se desembolsan **$-\\$10.000.000$** por la máquina nueva.
                """
                )

            df_e8 = pd.DataFrame(
                [ing_e8, cv_fab_e8, comis_e8, cf_fab_e8, gav_e8, dep_e8, amo_e8, vta_maq_e8, vl_maq_e8, uai_e8, imp_e8, udi_e8, rev_dep_e8, rev_amo_e8, rev_vl_e8, inv_e8, desecho_e8, rec_ct_e8, fcn_e8, [round(x) for x in vp_e8]],
                index=[
                    "(+) Ingresos", "(-) Costos Var. Fabricación", "(-) Comisiones (2%)", "(-) Costos Fijos Fab.",
                    "(-) Gastos Adm. y Ventas", "(-) Depreciación", "(-) Amort. Intangibles", "(+) Venta Máquina Usada",
                    "(-) Valor Libro Máquina", "(=) Utilidad Antes Impuestos", "(-) Impuesto (15%)", "(=) Utilidad Neta",
                    "(+) Depreciación", "(+) Amort. Intangibles", "(+) Valor Libro Máquina", "(-) Inversiones (Capex/CT)",
                    "(+) Valor de Desecho", "(+) Recup. Cap. Trabajo", "(=) FLUJO DE CAJA NETO", "Flujo Actualizado (12%)",
                ],
                columns=cols_e8,
            )
            st.dataframe(df_e8.style.format("{:,.0f}"), use_container_width=True, height=420)
            st.markdown(
                f'<div class="nota-celda"><b>Resultado Ejercicio 8 (10 años, Tasa 12%, Impuesto 15%):</b> '
                f'VAN = <b>${van_e8:,.0f}</b> | TIR = <b>{tir_e8*100:.2f}%</b> | Payback = <b>{pb_e8}</b>.</div>',
                unsafe_allow_html=True,
            )


def _render_vista_evaluador_corporativo(solo_pizarra=False):
    st.sidebar.divider()
    st.sidebar.markdown("### Caso de Estudio Corporativo")
    if not solo_pizarra:
        usar_apariencia_excel = st.sidebar.toggle(
            "Mostrar apariencia Excel Online (Libro1.xlsx)",
            value=False,
            key="toggle_excel_style_v2",
            help="Activa la barra verde superior y cinta visual estilo Excel Online sobre el evaluador.",
        )
        mostrar_ayudas_pedagogicas = st.sidebar.toggle(
            "Mostrar Burbujas y Gráficos Pedagógicos",
            value=True,
            key="toggle_ayudas_fin_v2",
        )
    else:
        usar_apariencia_excel = False
        mostrar_ayudas_pedagogicas = True

    color_acento = "#107c41" if usar_apariencia_excel else "#1D4ED8"

    if not solo_pizarra:
        if usar_apariencia_excel:
            st.markdown(
                """
            <div class="excel-top">
                <span><b>Excel</b> &nbsp;&nbsp;|&nbsp;&nbsp; Libro1.xlsx &nbsp; <span style="opacity:0.85; font-size:11px;">✓ Guardado en OneDrive</span></span>
                <span>Compartir &nbsp;&nbsp; Comentarios</span>
            </div>
            <div class="excel-ribbon">
                <span>Archivo</span>
                <span style="border-bottom: 2px solid #107c41; font-weight: 600; color: #107c41;">Inicio</span>
                <span>Insertar</span>
                <span>Disposición de página</span>
                <span>Fórmulas</span>
                <span>Datos</span>
                <span>Revisar</span>
                <span>Vista</span>
            </div>
            <div class="excel-toolbar">
                <span>Deshacer</span> |
                <span class="excel-box">Calibri &nbsp; ▾</span>
                <span class="excel-box">11 &nbsp; ▾</span> |
                <span><b>N</b> &nbsp; <i>K</i> &nbsp; <u>S</u></span> |
                <span>Alinear ▾ &nbsp; Ajustar texto</span> |
                <span class="excel-box">Contabilidad &nbsp; ▾</span>
                <span><b>$</b> &nbsp; <b>%</b> &nbsp; <b>000</b></span> |
                <span>Autosuma ∑</span>
            </div>
            <div class="excel-fx">
                <b>C21</b> &nbsp;&nbsp;|&nbsp;&nbsp; <i>fx</i> &nbsp; =SUMA(C13:C20)
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
            <div class="ulagos-clean-banner">
                <div>
                    <b style="font-size:14.5px;">EVALUADOR CORPORATIVO DE ACTIVOS REALES (FCL · FCI · MONTE CARLO · LIBRO1.XLSX)</b>
                    <div style="font-size:12px; color:#CBD5E1; margin-top:2px;">Finanzas Avanzadas ULagos — Prof.ª Camila Bustos Rosas | Exportación Excel de 7 hojas con fórmulas nativas vivas</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
        <div class="ulagos-clean-banner">
            <div>
                <b style="font-size:14.5px;">PIZARRA INTERACTIVA PASO A PASO (CONSTRUYE EL FCL / FCI CELDA POR CELDA)</b>
                <div style="font-size:12px; color:#CBD5E1; margin-top:2px;">Selecciona el caso en la barra lateral izquierda y practica los 6 pasos con detector automático de errores de signo, IVA y descuento.</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    plantilla = st.sidebar.selectbox(
        "Plantilla",
        [
            "Caso 1 - Estructura J (120M)",
            "Caso 2 - Guia P2 (130M)",
            "Caso 3 - Conservas (13M)",
            "Caso 4 - En blanco",
        ],
    )

    if "Caso 1" in plantilla:
        def_params = pd.DataFrame([{
            "Horizonte (años)": 6, "Impuesto (%)": 29.5, "Ke (%)": 13.0,
            "% Deuda": 30.0, "Kd (%)": 6.5, "Plazo Créd.": 5, "Gasto Créd. (%)": 0.0,
        }])
        def_inv = pd.DataFrame([
            {"Ítem": "Máquina nueva", "Monto": 120000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": True, "Vida Útil": 6, "Valor Rescate ($)": 45000000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Puesta en marcha (instalaciones)", "Monto": 12000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Pruebas de producción (ajustes)", "Monto": 7000000.0, "Moneda": "Bruto (/1.19)", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Capacitación mano de obra", "Monto": 7000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Capital de trabajo", "Monto": 36000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": True},
        ])
        def_op_base = pd.DataFrame([{
            "Unidades A1 (opcional)": 38000.0, "Precio A1 ($)": 5000.0, "Ingresos A1 ($)": 190000000.0, "Moneda Ing.": "Bruto (/1.19)",
            "CV Total A1 ($)": 55100000.0, "Moneda CV": "Neto", "CF Total A1 ($)": 5300000.0, "Moneda CF": "Bruto (/1.19)",
        }])
        def_tasas = pd.DataFrame({
            "Año": [1, 2, 3, 4, 5, 6],
            "Crec. Ingresos (%)": [0.0, 4.5, 4.5, 4.5, 4.5, 4.5],
            "Crec. Costos Var. (%)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Crec. Costos Fijos (%)": [0.0, 6.0, 6.0, 3.0, 3.0, 3.0],
        })

    elif "Caso 2" in plantilla:
        def_params = pd.DataFrame([{
            "Horizonte (años)": 6, "Impuesto (%)": 29.5, "Ke (%)": 13.0,
            "% Deuda": 30.0, "Kd (%)": 7.5, "Plazo Créd.": 5, "Gasto Créd. (%)": 0.0,
        }])
        def_inv = pd.DataFrame([
            {"Ítem": "Máquina nueva", "Monto": 130000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": True, "Vida Útil": 6, "Valor Rescate ($)": 55000000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Gastos puesta en marcha", "Monto": 14000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Pruebas de producción", "Monto": 6000000.0, "Moneda": "Bruto (/1.19)", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Capacitación mano de obra", "Monto": 7000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Capital de trabajo", "Monto": 35000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": True},
        ])
        def_op_base = pd.DataFrame([{
            "Unidades A1 (opcional)": 1.0, "Precio A1 ($)": 190000000.0, "Ingresos A1 ($)": 190000000.0, "Moneda Ing.": "Bruto (/1.19)",
            "CV Total A1 ($)": 0.0, "Moneda CV": "Neto", "CF Total A1 ($)": 60400000.0, "Moneda CF": "Neto",
        }])
        def_tasas = pd.DataFrame({
            "Año": [1, 2, 3, 4, 5, 6],
            "Crec. Ingresos (%)": [0.0, 4.5, 4.5, 4.5, 4.5, 4.5],
            "Crec. Costos Var. (%)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Crec. Costos Fijos (%)": [0.0, 6.0, 6.0, 3.0, 3.0, 3.0],
        })

    elif "Caso 3" in plantilla:
        def_params = pd.DataFrame([{
            "Horizonte (años)": 5, "Impuesto (%)": 29.5, "Ke (%)": 13.0,
            "% Deuda": 30.0, "Kd (%)": 8.5, "Plazo Créd.": 4, "Gasto Créd. (%)": 2.0,
        }])
        def_inv = pd.DataFrame([
            {"Ítem": "Maquinaria y equipos", "Monto": 13000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": True, "Vida Útil": 5, "Valor Rescate ($)": 3250000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Implementos de prod.", "Monto": 1800000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": True, "Vida Útil": 5, "Valor Rescate ($)": 450000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Terrenos", "Monto": 3000000.0, "Moneda": "Neto", "IVA Créd": False, "Depreciable": False, "Vida Útil": 5, "Valor Rescate ($)": 750000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Implementos oficina", "Monto": 2000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": True, "Vida Útil": 5, "Valor Rescate ($)": 500000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Vehículo", "Monto": 8000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": True, "Vida Útil": 5, "Valor Rescate ($)": 2000000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Construcción", "Monto": 7500000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": True, "Vida Útil": 5, "Valor Rescate ($)": 1875000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Gastos org. y puesta en marcha", "Monto": 1000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 5, "Valor Rescate ($)": 0.0, "Intangible": True, "Cap. Trabajo": False},
            {"Ítem": "Capital de trabajo", "Monto": 1100000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 5, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": True},
        ])
        def_op_base = pd.DataFrame([{
            "Unidades A1 (opcional)": 50000.0, "Precio A1 ($)": 760.0, "Ingresos A1 ($)": 38000000.0, "Moneda Ing.": "Neto",
            "CV Total A1 ($)": 17100840.34, "Moneda CV": "Neto", "CF Total A1 ($)": 7460000.0, "Moneda CF": "Neto",
        }])
        def_tasas = pd.DataFrame({
            "Año": [1, 2, 3, 4, 5],
            "Crec. Ingresos (%)": [0.0, 20.0, 13.3333, 2.9412, 2.8571],
            "Crec. Costos Var. (%)": [0.0, 20.0, 13.3333, 2.9412, 2.8571],
            "Crec. Costos Fijos (%)": [0.0, 1.0724, -5.0398, 20.3911, 0.0],
        })
    else:
        def_params = pd.DataFrame([{
            "Horizonte (años)": 6, "Impuesto (%)": 29.5, "Ke (%)": 13.0,
            "% Deuda": 30.0, "Kd (%)": 6.5, "Plazo Créd.": 5, "Gasto Créd. (%)": 0.0,
        }])
        def_inv = pd.DataFrame([
            {"Ítem": "Activo Principal", "Monto": 100000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": True, "Vida Útil": 6, "Valor Rescate ($)": 20000000.0, "Intangible": False, "Cap. Trabajo": False},
            {"Ítem": "Capital de Trabajo", "Monto": 20000000.0, "Moneda": "Neto", "IVA Créd": True, "Depreciable": False, "Vida Útil": 6, "Valor Rescate ($)": 0.0, "Intangible": False, "Cap. Trabajo": True},
        ])
        def_op_base = pd.DataFrame([{
            "Unidades A1 (opcional)": 10000.0, "Precio A1 ($)": 15000.0, "Ingresos A1 ($)": 150000000.0, "Moneda Ing.": "Neto",
            "CV Total A1 ($)": 50000000.0, "Moneda CV": "Neto", "CF Total A1 ($)": 10000000.0, "Moneda CF": "Neto",
        }])
        def_tasas = pd.DataFrame({
            "Año": [1, 2, 3, 4, 5, 6],
            "Crec. Ingresos (%)": [0.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            "Crec. Costos Var. (%)": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Crec. Costos Fijos (%)": [0.0, 3.0, 3.0, 3.0, 3.0, 3.0],
        })

    base_credito = st.sidebar.selectbox("Base Crédito", ["Inv. Bruta", "Inv. Neta"])
    descuento_fcl = st.sidebar.selectbox("Tasa Descuento FCL", ["Ke", "WACC"])
    incluir_prestamo_fci0 = st.sidebar.checkbox("Sumar Préstamo en Año 0 FCI", value=True)
    usar_q_por_p = st.sidebar.checkbox("Calcular Ingresos A1 como Unidades x Precio", value=False)
    restar_rescate_dep = st.sidebar.checkbox("Restar Valor Rescate al depreciar", value=True)

    with st.sidebar.expander("Calculadora CAPM (Opcional)"):
        rf_val = st.number_input("Tasa Libre Riesgo Rf (%)", value=6.0, step=0.5)
        beta_val = st.number_input("Beta", value=1.25, step=0.05)
        rm_val = st.number_input("Retorno Mercado Rm (%)", value=12.0, step=0.5)
        capm_res = rf_val + beta_val * (rm_val - rf_val)
        st.caption(f"Ke (CAPM) = {capm_res:.2f}%")

    with st.expander("Celdas de Entrada y Supuestos (Clic para mostrar/ocultar)", expanded=False):
        st.caption("1. Parámetros Financieros")
        params_df = st.data_editor(def_params, use_container_width=True, hide_index=True)

        horizonte = max(1, int(params_df.iloc[0]["Horizonte (años)"]))
        tasa_imp = float(params_df.iloc[0]["Impuesto (%)"]) / 100.0
        tasa_ke = float(params_df.iloc[0]["Ke (%)"]) / 100.0
        pct_deuda = float(params_df.iloc[0]["% Deuda"]) / 100.0
        tasa_kd = float(params_df.iloc[0]["Kd (%)"]) / 100.0
        plazo_deuda = max(1, int(params_df.iloc[0]["Plazo Créd."]))
        gasto_credito_pct = float(params_df.iloc[0]["Gasto Créd. (%)"]) / 100.0
        wacc_calc = tasa_ke * (1 - pct_deuda) + tasa_kd * (1 - tasa_imp) * pct_deuda

        st.caption("2. Inversiones Año 0, Valor de Rescate y Capital de Trabajo")
        inv_df = st.data_editor(
            def_inv,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config={
                "Moneda": st.column_config.SelectboxColumn("Moneda", options=["Neto", "Bruto (/1.19)"]),
            },
        )

        st.caption("3. Operación Año 1 y Tasas de Crecimiento Anual (%)")
        op_df = st.data_editor(
            def_op_base,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Moneda Ing.": st.column_config.SelectboxColumn("Moneda Ing.", options=["Bruto (/1.19)", "Neto"]),
                "Moneda CV": st.column_config.SelectboxColumn("Moneda CV", options=["Neto", "Bruto (/1.19)"]),
                "Moneda CF": st.column_config.SelectboxColumn("Moneda CF", options=["Bruto (/1.19)", "Neto"]),
            },
        )

        if len(def_tasas) != horizonte:
            tasas_init = pd.DataFrame({
                "Año": list(range(1, horizonte + 1)),
                "Crec. Ingresos (%)": [0.0] + [4.5] * (horizonte - 1),
                "Crec. Costos Var. (%)": [0.0] * horizonte,
                "Crec. Costos Fijos (%)": [0.0] + [6.0] * min(2, horizonte - 1) + [3.0] * max(0, horizonte - 3),
            })
        else:
            tasas_init = def_tasas

        tasas_df = st.data_editor(tasas_init, use_container_width=True, hide_index=True)

    r_op = op_df.iloc[0]
    ing_bruto_o_neto = (float(r_op["Unidades A1 (opcional)"]) * float(r_op["Precio A1 ($)"])) if usar_q_por_p else float(r_op["Ingresos A1 ($)"])
    ing_base_neto = ing_bruto_o_neto / 1.19 if "Bruto" in str(r_op["Moneda Ing."]) else ing_bruto_o_neto
    cv_base_neto = float(r_op["CV Total A1 ($)"]) / 1.19 if "Bruto" in str(r_op["Moneda CV"]) else float(r_op["CV Total A1 ($)"])
    cf_base_neto = float(r_op["CF Total A1 ($)"]) / 1.19 if "Bruto" in str(r_op["Moneda CF"]) else float(r_op["CF Total A1 ($)"])

    inv_processed = []
    for _, row in inv_df.iterrows():
        monto_raw = float(row["Monto"] or 0.0)
        es_bruto = "Bruto" in str(row["Moneda"])
        val_neto = monto_raw / (1.0 + IVA_RATE) if es_bruto else monto_raw
        afecto_iva = bool(row["IVA Créd"])
        val_iva = val_neto * IVA_RATE if afecto_iva else 0.0
        val_bruto = val_neto + val_iva
        vida = max(1, int(row["Vida Útil"] or horizonte))
        rescate = float(row["Valor Rescate ($)"] or 0.0)
        base_dep = (val_neto - rescate) if restar_rescate_dep else val_neto
        dep_anual = base_dep / vida if bool(row["Depreciable"]) else 0.0
        amort_anual = val_neto / vida if bool(row["Intangible"]) else 0.0
        inv_processed.append({
            "Ítem": str(row["Ítem"]),
            "Valor Neto": float(val_neto),
            "IVA (19%)": float(val_iva),
            "Valor Bruto": float(val_bruto),
            "Valor Rescate": float(rescate),
            "Depreciación Anual": float(dep_anual),
            "Amortización Anual": float(amort_anual),
            "Vida Útil": int(vida),
            "Es CT": bool(row["Cap. Trabajo"]),
        })
    df_inv_calc = pd.DataFrame(inv_processed)

    total_inv_neta = float(df_inv_calc["Valor Neto"].sum())
    total_inv_bruta = float(df_inv_calc["Valor Bruto"].sum())
    total_rescate_af = float(df_inv_calc[~df_inv_calc["Es CT"]]["Valor Rescate"].sum())
    total_recup_ct = float(df_inv_calc[df_inv_calc["Es CT"]]["Valor Neto"].sum())
    dep_anual_total = float(df_inv_calc["Depreciación Anual"].sum())
    amort_anual_total = float(df_inv_calc["Amortización Anual"].sum())

    base_prestamo_val = total_inv_bruta if "Bruta" in base_credito else total_inv_neta
    monto_credito = base_prestamo_val * pct_deuda * (1.0 + gasto_credito_pct)
    cuota_anual = monto_credito * (tasa_kd * (1 + tasa_kd) ** plazo_deuda) / ((1 + tasa_kd) ** plazo_deuda - 1) if monto_credito > 0 else 0.0

    ing_series, cv_series, cf_series = [], [], []
    curr_i, curr_v, curr_f = ing_base_neto, cv_base_neto, cf_base_neto
    for idx, r_row in tasas_df.iterrows():
        if idx > 0:
            curr_i *= (1.0 + float(r_row["Crec. Ingresos (%)"]) / 100.0)
            curr_v *= (1.0 + float(r_row["Crec. Costos Var. (%)"]) / 100.0)
            curr_f *= (1.0 + float(r_row["Crec. Costos Fijos (%)"]) / 100.0)
        ing_series.append(float(curr_i))
        cv_series.append(float(curr_v))
        cf_series.append(float(curr_f))

    amort_rows = []
    saldo = monto_credito
    amort_rows.append({"Período": 0, "Cuota": 0.0, "Interés": 0.0, "Amortización": 0.0, "Saldo": saldo})
    intereses_anuales, amort_deuda_anuales = [], []

    for t in range(1, horizonte + 1):
        if t <= plazo_deuda and monto_credito > 0:
            interes = saldo * tasa_kd
            amort_cap = cuota_anual - interes
            saldo = max(0.0, saldo - amort_cap)
            c_val = cuota_anual
        else:
            interes, amort_cap, c_val = 0.0, 0.0, 0.0
        intereses_anuales.append(float(interes))
        amort_deuda_anuales.append(float(amort_cap))
        amort_rows.append({"Período": t, "Cuota": round(c_val), "Interés": round(interes), "Amortización": round(amort_cap), "Saldo": round(saldo)})

    df_amort = pd.DataFrame(amort_rows)




    tasa_fcl_usada = wacc_calc if "WACC" in descuento_fcl else tasa_ke


    def construir_tabla_vista(es_inv=False, mult_ing=1.0, mult_cost=1.0, mult_capex=1.0, tasa_override=None):
        cols = ["Año 0"] + [f"Año {t}" for t in range(1, horizonte + 1)]
        data = {c: [] for c in cols}

        flujos_netos = []
        inv0 = -total_inv_neta * mult_capex
        prest0 = monto_credito if (es_inv and incluir_prestamo_fci0) else 0.0
        f0 = inv0 + prest0
        flujos_netos.append(f0)

        rows_a0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, inv0, prest0, 0, 0, 0, f0]
        for v in rows_a0:
            data["Año 0"].append(round(v))

        for t in range(horizonte):
            col_name = f"Año {t+1}"
            ing_t = ing_series[t] * mult_ing
            cv_t = -cv_series[t] * mult_cost
            cf_t = -cf_series[t] * mult_cost
            dep_t = -dep_anual_total * mult_capex
            amo_t = -amort_anual_total * mult_capex
            int_t = -intereses_anuales[t] if es_inv else 0.0
            bai_t = ing_t + cv_t + cf_t + dep_t + amo_t + int_t
            imp_t = -bai_t * tasa_imp
            bdi_t = bai_t + imp_t
            dep_pos = dep_anual_total * mult_capex
            amo_pos = amort_anual_total * mult_capex
            am_deuda = -amort_deuda_anuales[t] if es_inv else 0.0
            resc_t = total_rescate_af if t == horizonte - 1 else 0.0
            rec_ct = total_recup_ct if t == horizonte - 1 else 0.0
            fn_t = bdi_t + dep_pos + amo_pos + am_deuda + resc_t + rec_ct
            flujos_netos.append(fn_t)

            vals_t = [ing_t, cv_t, cf_t, dep_t, amo_t, int_t, bai_t, imp_t, bdi_t, dep_pos, amo_pos, 0, 0, am_deuda, resc_t, rec_ct, fn_t]
            for v in vals_t:
                data[col_name].append(round(v))

        t_desc = tasa_override if tasa_override is not None else (tasa_ke if es_inv else tasa_fcl_usada)
        van, tir, pb_str, f_act, acum = calc_metrics(flujos_netos, t_desc)
        for idx_c, c_name in enumerate(cols):
            data[c_name].append(round(f_act[idx_c]))
            data[c_name].append(round(acum[idx_c]))

        index_names = [
            "(+) Ingresos", "(-) Costos Variables", "(-) Costos Fijos", "(-) Depreciación",
            "(-) Amort. Intangibles", "(-) Intereses Deuda", "(=) BAI", "(-) Impuesto (29.5%)",
            "(=) BDI", "(+) Depreciación", "(+) Amort. Intangibles", "(-) Inversión Inicial",
            "(+) Préstamo", "(-) Amortización Deuda", "(+) Valor Rescate", "(+) Recup. Cap. Trabajo",
            "(=) FLUJO CAJA NETO", "Flujo Actualizado (VP)", "Flujo Acumulado",
        ]
        df_vista = pd.DataFrame(data, index=index_names)
        return df_vista, van, tir, pb_str


    df_fcl_vista, van_fcl, tir_fcl, pb_fcl = construir_tabla_vista(es_inv=False)
    df_fci_vista, van_fci, tir_fci, pb_fci = construir_tabla_vista(es_inv=True)

    flujos_fcl_lista = [float(df_fcl_vista.loc["(=) FLUJO CAJA NETO", c]) for c in df_fcl_vista.columns]
    flujos_fci_lista = [float(df_fci_vista.loc["(=) FLUJO CAJA NETO", c]) for c in df_fci_vista.columns]

    decision_fcl = "ACEPTAR" if van_fcl >= 0 and tir_fcl > tasa_fcl_usada else "RECHAZAR"
    decision_fci = "ACEPTAR" if van_fci >= 0 and tir_fci > tasa_ke else "RECHAZAR"

    texto_interp_fcl = (
        f"Conclusión FCL: VAN = ${van_fcl:,.0f} (Tasa {tasa_fcl_usada*100:.2f}%) | TIR = {tir_fcl*100:.2f}% | Payback = {pb_fcl}. "
        f"El proyecto recupera la inversión neta (${total_inv_neta:,.0f}), cubre el costo de oportunidad del capital y genera riqueza neta por ${abs(van_fcl):,.0f}. "
        f"Decisión: {decision_fcl} (VAN >= 0 y TIR > Tasa exigida)."
    )

    texto_interp_fci = (
        f"Conclusión Inversionista: Préstamo = ${monto_credito:,.0f} ({pct_deuda*100:.0f}% Inv., Kd {tasa_kd*100:.2f}%, {plazo_deuda} años, Cuota PAGO = ${cuota_anual:,.0f}) | "
        f"VAN FCI = ${van_fci:,.0f} (Ke {tasa_ke*100:.2f}%) | TIR FCI = {tir_fci*100:.2f}% | Payback = {pb_fci}. "
        f"El apalancamiento financiero y el escudo fiscal de los intereses ({tasa_imp*100:.1f}%) incrementan la rentabilidad sobre el capital propio. Decisión: {decision_fci}."
    )

    if solo_pizarra:
        renderizar_taller_paso_a_paso_en_hoja(
            plantilla_nombre=plantilla,
            df_fcl_sol=df_fcl_vista,
            df_fci_sol=df_fci_vista,
            van_fcl_sol=van_fcl,
            tir_fcl_sol=tir_fcl,
            van_fci_sol=van_fci,
            tir_fci_sol=tir_fci,
            tasa_fcl=tasa_fcl_usada,
            tasa_ke=tasa_ke,
            tasa_imp=tasa_imp,
            total_inv_neta=total_inv_neta,
            monto_credito=monto_credito,
            dep_anual_total=dep_anual_total,
            total_rescate_af=total_rescate_af,
            total_recup_ct=total_recup_ct,
        )
        return

    d8 = _obtener_modelo_ej8_y_err7()
    cols_e8, ing_e8, cv_fab_e8, comis_e8 = d8["cols_e8"], d8["ing_e8"], d8["cv_fab_e8"], d8["comis_e8"]
    cf_fab_e8, gav_e8, dep_e8, amo_e8 = d8["cf_fab_e8"], d8["gav_e8"], d8["dep_e8"], d8["amo_e8"]
    vta_maq_e8, vl_maq_e8, uai_e8, imp_e8 = d8["vta_maq_e8"], d8["vl_maq_e8"], d8["uai_e8"], d8["imp_e8"]
    udi_e8, rev_dep_e8, rev_amo_e8, rev_vl_e8 = d8["udi_e8"], d8["rev_dep_e8"], d8["rev_amo_e8"], d8["rev_vl_e8"]
    inv_e8, desecho_e8, rec_ct_e8, fcn_e8 = d8["inv_e8"], d8["desecho_e8"], d8["rec_ct_e8"], d8["fcn_e8"]
    van_e8, tir_e8, pb_e8, vp_e8, df_err7 = d8["van_e8"], d8["tir_e8"], d8["pb_e8"], d8["vp_e8"], d8["df_err7"]

    barra_superior = st.container()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Hoja1 (FCL)",
        "Hoja2 (Amortización)",
        "Hoja3 (Inversionista)",
        "Hoja4 (Inversiones/IVA)",
        "Hoja5 (Sensibilidad)",
        "Hoja6 (Monte Carlo)",
        "Hoja7 (Hamada / CAPM / PGU)",
    ])

    with tab1:
        if mostrar_ayudas_pedagogicas:
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: VAN y Regla de Decisión",
                    titulo_interno="Valor Actual Neto (VAN) — Criterio de Creación de Riqueza",
                    formula_latex=r"VAN = -I_0 + \sum_{t=1}^{n} \frac{FCL_t}{(1 + r)^t}",
                    explicacion_md=(
                        f"- **Cifra activa ({plantilla}):** $VAN = \\${van_fcl:,.0f}$ descontado al **{tasa_fcl_usada*100:.2f}%**.\n"
                        "- **Interpretación:** Mide en pesos de hoy cuánta riqueza adicional crea el proyecto por encima de lo que rentaría el capital invertido en su mejor alternativa de igual riesgo.\n"
                        f"- **Dictamen:** **{decision_fcl}** ($VAN \\ge 0$)."
                    ),
                )
            with b2:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: TIR vs. Costo de Capital",
                    titulo_interno="Tasa Interna de Retorno (TIR)",
                    formula_latex=r"\sum_{t=0}^{n} \frac{FCL_t}{(1 + TIR)^t} = 0 \implies TIR = " + f"{tir_fcl*100:.2f}\\%",
                    explicacion_md=(
                        f"- **Cifra activa:** $TIR = {tir_fcl*100:.2f}\\%$ frente a una tasa exigida de **{tasa_fcl_usada*100:.2f}%** (Spread neto = **{(tir_fcl - tasa_fcl_usada)*100:+.2f} pp**).\n"
                        "- **Cuidado en proyectos mutuamente excluyentes:** La TIR asume reinversión de flujos intermedios a la misma TIR, mientras que el VAN asume reinversión al costo de oportunidad del capital ($WACC$ o $K_e$)."
                    ),
                )
            with b3:
                escudo_dep_anual = dep_anual_total * tasa_imp
                renderizar_burbuja_tip(
                    titulo_boton="Tip: ¿Por qué se reversa la Depreciación?",
                    titulo_interno="Efecto Tributario y Reverso de la Depreciación",
                    formula_latex=r"\text{Escudo Fiscal Depreciación} = \text{Depreciación} \times t_c",
                    explicacion_md=(
                        f"- **Cifra activa:** Se restan **$-\\${dep_anual_total:,.0f}$** antes de impuestos para rebajar la base imponible (ahorrando **$\\${escudo_dep_anual:,.0f}/\\text{{año}}$** en impuestos al {tasa_imp*100:.1f}%).\n"
                        "- Como la depreciación es un desgaste contable y **no una salida de dinero en efectivo**, se vuelve a sumar (**$+\\${dep_anual_total:,.0f}$**) debajo del BDI."
                    ),
                )
            with b4:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Recuperación Cap. de Trabajo",
                    titulo_interno="Inversión y Recuperación del Capital de Trabajo",
                    formula_latex=r"CT_0 = -\$" + f"{total_recup_ct:,.0f}" + r"\quad \longrightarrow \quad Recup.\; CT_n = +\$" + f"{total_recup_ct:,.0f}",
                    explicacion_md=(
                        "- El **Capital de Trabajo** financia el desfase operativo entre compras, producción y cobranza desde el Año 0.\n"
                        "- Al no consumirse ni depreciarse (rota continuamente), se recupera íntegramente al 100% en el último año del horizonte de evaluación."
                    ),
                )

        st.dataframe(df_fcl_vista.style.format("{:,.0f}"), use_container_width=True, height=450)
        st.markdown(f'<div class="nota-celda">{texto_interp_fcl}</div>', unsafe_allow_html=True)

        if mostrar_ayudas_pedagogicas:
            with st.expander("Análisis Gráfico Interactivo: Perfil del VAN(r) y Cascada Operativa del Flujo (Plotly)", expanded=False):
                g_col1, g_col2 = st.columns([1.15, 1.0])
                with g_col1:
                    fig_p_van = graficar_perfil_van_y_tir(
                        flujos_fcl=flujos_fcl_lista,
                        flujos_fci=flujos_fci_lista,
                        tasa_fcl=tasa_fcl_usada,
                        tasa_ke=tasa_ke,
                        tir_fcl=tir_fcl,
                        tir_fci=tir_fci,
                    )
                    st.plotly_chart(fig_p_van, use_container_width=True)
                with g_col2:
                    anio_casc_fcl = st.selectbox("Año a inspeccionar en Cascada (FCL):", list(range(1, horizonte + 1)), index=0, key="casc_fcl_yr")
                    idx_y = anio_casc_fcl - 1
                    fig_w_fcl = graficar_cascada_operativa_anual(
                        anio_sel=anio_casc_fcl,
                        ing_t=ing_series[idx_y],
                        cv_t=cv_series[idx_y],
                        cf_t=cf_series[idx_y],
                        dep_t=dep_anual_total,
                        amo_t=amort_anual_total,
                        int_t=0.0,
                        tasa_imp=tasa_imp,
                        am_deuda_t=0.0,
                        resc_t=(total_rescate_af + total_recup_ct) if idx_y == horizonte - 1 else 0.0,
                        es_inversionista=False,
                    )
                    st.plotly_chart(fig_w_fcl, use_container_width=True)

    with tab2:
        if mostrar_ayudas_pedagogicas:
            ba1, ba2 = st.columns(2)
            with ba1:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Sistema de Amortización Francés (PAGO / PMT)",
                    titulo_interno="Cuota Fija, Interés Sobre Saldo y Amortización Creciente",
                    formula_latex=r"\text{Cuota} = P \cdot \frac{K_d(1 + K_d)^n}{(1 + K_d)^n - 1} = \$" + f"{cuota_anual:,.0f}",
                    explicacion_md=(
                        f"- **Préstamo ($P$):** $\\${monto_credito:,.0f}$ al **{tasa_kd*100:.2f}%** anual por **{plazo_deuda} años**.\n"
                        "- **Interés del período ($I_t = Saldo_{t-1} \\times K_d$):** Va al Flujo del Inversionista **antes de impuestos** (generando escudo fiscal).\n"
                        "- **Amortización del principal ($A_t = Cuota - I_t$):** No es gasto tributario; se descuenta **después de impuestos**."
                    ),
                )
            with ba2:
                tot_int_pagados = sum(intereses_anuales)
                tot_escudo_int = tot_int_pagados * tasa_imp
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Ahorro Tributario Total por Intereses",
                    titulo_interno="Escudo Fiscal Acumulado de la Deuda",
                    formula_latex=r"\sum_{t=1}^{n} I_t \cdot t_c = \$" + f"{tot_int_pagados:,.0f}" + r" \times " + f"{tasa_imp*100:.1f}\\% = \\${tot_escudo_int:,.0f}",
                    explicacion_md=(
                        f"- Durante los {plazo_deuda} años del crédito se pagan **$\\${tot_int_pagados:,.0f}$** en intereses bancarios, los cuales reducen el pago de Impuesto de Primera Categoría en **$\\${tot_escudo_int:,.0f}$** nominales."
                    ),
                )

        st.dataframe(df_amort.style.format("{:,.0f}"), use_container_width=True, hide_index=True)

        if mostrar_ayudas_pedagogicas and monto_credito > 0:
            df_am_plot = df_amort[df_amort["Período"] > 0].copy()
            fig_am = go.Figure()
            fig_am.add_trace(go.Bar(x=df_am_plot["Período"], y=df_am_plot["Interés"], name="Interés (Antes de Impuestos)", marker_color="#dc2626"))
            fig_am.add_trace(go.Bar(x=df_am_plot["Período"], y=df_am_plot["Amortización"], name="Amortización Capital (Después de Impuestos)", marker_color="#1d4ed8"))
            fig_am.add_trace(go.Scatter(x=df_am_plot["Período"], y=df_am_plot["Saldo"], mode="lines+markers", name="Saldo Insoluto", line=dict(color="#059669", width=3)))
            fig_am.update_layout(
                title="Descomposición de la Cuota Fija (Interés vs. Amortización) y Evolución del Saldo Insoluto",
                xaxis_title="Año del Crédito",
                yaxis_title="Monto ($ CLP)",
                barmode="stack",
                height=320,
                margin=dict(l=15, r=15, t=40, b=20),
                plot_bgcolor="#f8fafc",
            )
            st.plotly_chart(fig_am, use_container_width=True)

    with tab3:
        if mostrar_ayudas_pedagogicas:
            bi1, bi2, bi3 = st.columns(3)
            with bi1:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Diferencia entre FCL y FCI",
                    titulo_interno="Flujo de Caja Libre vs. Flujo del Inversionista",
                    formula_latex=r"FCI_t = FCL_t - I_t(1 - t_c) - \text{Amortización}_t \quad (\text{Descontado a } K_e)",
                    explicacion_md=(
                        f"- En el **Año 0**, el accionista solo desembolsa con recursos propios **$-\\${abs(flujos_fci_lista[0]):,.0f}$** (Inversión Neta $-\\${total_inv_neta:,.0f}$ más el préstamo $+\\${monto_credito:,.0f}$).\n"
                        f"- Como el flujo ya deduce el servicio de la deuda, se descuenta a la tasa exigida por el patrimonio (**$K_e = {tasa_ke*100:.2f}\\%$**)."
                    ),
                )
            with bi2:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Efecto Apalancamiento Financiero",
                    titulo_interno="¿Por qué sube la TIR del Inversionista?",
                    formula_latex=r"K_d(1 - t_c) = " + f"{tasa_kd*(1-tasa_imp)*100:.2f}\\% < TIR_{{FCL}} ({tir_fcl*100:.2f}\\%) \\implies TIR_{{FCI}} = {tir_fci*100:.2f}\\%",
                    explicacion_md=(
                        f"- Como el costo efectivo de la deuda después de impuestos (**{tasa_kd*(1-tasa_imp)*100:.2f}%**) es inferior a la rentabilidad operativa pura del activo (**{tir_fcl*100:.2f}%**), el apalancamiento es positivo y eleva la TIR del accionista a **{tir_fci*100:.2f}%**."
                    ),
                )
            with bi3:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Creación de Valor para el Accionista",
                    titulo_interno="Lectura del VAN del Inversionista",
                    formula_latex=r"VAN_{FCI}(K_e) = \$" + f"{van_fci:,.0f}",
                    explicacion_md=(
                        f"- El proyecto apalancado genera un incremento neto de riqueza de **$\\${van_fci:,.0f}$** por sobre el **{tasa_ke*100:.2f}%** exigido por los dueños."
                    ),
                )

        st.dataframe(df_fci_vista.style.format("{:,.0f}"), use_container_width=True, height=450)
        st.markdown(f'<div class="nota-celda">{texto_interp_fci}</div>', unsafe_allow_html=True)

        if mostrar_ayudas_pedagogicas:
            with st.expander("Ver Cascada Interactiva del Flujo del Inversionista y Escudo Fiscal (Plotly)", expanded=False):
                anio_casc_fci = st.selectbox("Año a inspeccionar en Cascada (Inversionista):", list(range(1, horizonte + 1)), index=0, key="casc_fci_yr")
                idx_yi = anio_casc_fci - 1
                fig_w_fci = graficar_cascada_operativa_anual(
                    anio_sel=anio_casc_fci,
                    ing_t=ing_series[idx_yi],
                    cv_t=cv_series[idx_yi],
                    cf_t=cf_series[idx_yi],
                    dep_t=dep_anual_total,
                    amo_t=amort_anual_total,
                    int_t=intereses_anuales[idx_yi],
                    tasa_imp=tasa_imp,
                    am_deuda_t=amort_deuda_anuales[idx_yi],
                    resc_t=(total_rescate_af + total_recup_ct) if idx_yi == horizonte - 1 else 0.0,
                    es_inversionista=True,
                )
                st.plotly_chart(fig_w_fci, use_container_width=True)

    with tab4:
        if mostrar_ayudas_pedagogicas:
            biv1, biv2 = st.columns(2)
            with biv1:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Tratamiento del IVA (19%) en el Flujo",
                    titulo_interno="Separación Neto vs. Bruto e IVA Crédito Fiscal",
                    formula_latex=r"\text{Valor Neto} = \frac{\text{Valor Bruto}}{1,19} \quad ; \quad \text{IVA Crédito} = \text{Valor Neto} \times 19\%",
                    explicacion_md=(
                        f"- **Inversión Neta Total:** $\\${total_inv_neta:,.0f}$ | **IVA Crédito Fiscal:** $\\${total_inv_bruta - total_inv_neta:,.0f}$ | **Inversión Bruta:** $\\${total_inv_bruta:,.0f}$.\n"
                        "- Los estados de resultados y flujos operativos se trabajan en **valores netos de IVA**, salvo que el préstamo bancario se calcule expresamente sobre la inversión bruta."
                    ),
                )
            with biv2:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Depreciación Lineal y Activos No Depreciables",
                    titulo_interno="Cálculo de Cuota Anual de Depreciación y Amortización",
                    formula_latex=r"\text{Depreciación Anual} = \frac{\text{Valor Neto} - \text{Valor Rescate}}{\text{Vida Útil}}",
                    explicacion_md=(
                        f"- **Cuota Depreciación Anual:** $\\${dep_anual_total:,.0f}$ | **Amortización Intangibles:** $\\${amort_anual_total:,.0f}$.\n"
                        "- Recuerda que los **Terrenos** y el **Capital de Trabajo** no se deprecian; los gastos de organización y puesta en marcha (intangibles) se amortizan linealmente."
                    ),
                )

        st.dataframe(
            df_inv_calc[["Ítem", "Valor Neto", "IVA (19%)", "Valor Bruto", "Vida Útil", "Valor Rescate", "Depreciación Anual", "Amortización Anual"]].style.format({
                "Valor Neto": "{:,.0f}", "IVA (19%)": "{:,.0f}", "Valor Bruto": "{:,.0f}",
                "Valor Rescate": "{:,.0f}", "Depreciación Anual": "{:,.0f}", "Amortización Anual": "{:,.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

    with tab5:
        cs_top1, cs_top2 = st.columns([1.4, 2.2])
        with cs_top1:
            pct_sens_ing = st.selectbox(
                "Variación de Ingresos para Sensibilidad (±%):",
                options=[6.0, 10.0, 15.0, 20.0],
                index=0 if "Caso 2" in plantilla else 1,
                format_func=lambda x: f"±{x:.0f}% Ingresos" + (" (Guía Planta Piloto ULagos)" if x == 6.0 else (" (Estándar)" if x == 10.0 else "")),
                key="sel_pct_sens_ing_v2",
            )
        delta_s = pct_sens_ing / 100.0
        _, van_pes_fcl, tir_pes_fcl, pb_pes_fcl = construir_tabla_vista(es_inv=False, mult_ing=1.0 - delta_s)
        _, van_opt_fcl, tir_opt_fcl, pb_opt_fcl = construir_tabla_vista(es_inv=False, mult_ing=1.0 + delta_s)
        _, van_pes_fci, tir_pes_fci, pb_pes_fci = construir_tabla_vista(es_inv=True, mult_ing=1.0 - delta_s)
        _, van_opt_fci, tir_opt_fci, pb_opt_fci = construir_tabla_vista(es_inv=True, mult_ing=1.0 + delta_s)

        with cs_top2:
            van_esp_55_45_fcl = 0.55 * van_fcl + 0.45 * van_pes_fcl
            van_esp_55_45_fci = 0.55 * van_fci + 0.45 * van_pes_fci
            st.info(
                f"**Inciso Guía (55% Base / 45% Ingresos −{pct_sens_ing:.0f}%):** "
                f"E(VAN FCL) = **${van_esp_55_45_fcl:,.0f}** | E(VAN FCI) = **${van_esp_55_45_fci:,.0f}**"
            )

        df_sens = pd.DataFrame([
            {"Escenario": f"Pesimista (-{pct_sens_ing:.0f}% Ingresos)", "VAN FCL ($)": round(van_pes_fcl), "TIR FCL (%)": round(tir_pes_fcl * 100, 2), "Payback FCL": pb_pes_fcl, "VAN Inversionista ($)": round(van_pes_fci), "TIR Inversionista (%)": round(tir_pes_fci * 100, 2)},
            {"Escenario": "Caso Base (100%)", "VAN FCL ($)": round(van_fcl), "TIR FCL (%)": round(tir_fcl * 100, 2), "Payback FCL": pb_fcl, "VAN Inversionista ($)": round(van_fci), "TIR Inversionista (%)": round(tir_fci * 100, 2)},
            {"Escenario": f"Optimista (+{pct_sens_ing:.0f}% Ingresos)", "VAN FCL ($)": round(van_opt_fcl), "TIR FCL (%)": round(tir_opt_fcl * 100, 2), "Payback FCL": pb_opt_fcl, "VAN Inversionista ($)": round(van_opt_fci), "TIR Inversionista (%)": round(tir_opt_fci * 100, 2)},
        ])
        st.dataframe(df_sens, use_container_width=True, hide_index=True)

        if mostrar_ayudas_pedagogicas:
            _, van_cv_bajo, _, _ = construir_tabla_vista(es_inv=False, mult_cost=0.90)
            _, van_cv_alto, _, _ = construir_tabla_vista(es_inv=False, mult_cost=1.10)
            _, van_cap_bajo, _, _ = construir_tabla_vista(es_inv=False, mult_capex=0.90)
            _, van_cap_alto, _, _ = construir_tabla_vista(es_inv=False, mult_capex=1.10)
            _, van_r_baja, _, _ = construir_tabla_vista(es_inv=False, tasa_override=tasa_fcl_usada * 0.90)
            _, van_r_alta, _, _ = construir_tabla_vista(es_inv=False, tasa_override=tasa_fcl_usada * 1.10)

            fig_torn = graficar_tornado_sensibilidad(
                van_base=van_fcl,
                van_ing_bajo=van_pes_fcl,
                van_ing_alto=van_opt_fcl,
                van_cv_bajo=van_cv_bajo,
                van_cv_alto=van_cv_alto,
                van_capex_bajo=van_cap_bajo,
                van_capex_alto=van_cap_alto,
                van_tasa_baja=van_r_baja,
                van_tasa_alta=van_r_alta,
                titulo_flujo="FCL",
            )
            st.plotly_chart(fig_torn, use_container_width=True)

        with st.expander("Calculadora de VAN Esperado por Probabilidades (Ej. 5 Guía)", expanded=True):
            c_p1, c_p2, c_p3 = st.columns(3)
            with c_p1:
                prob_opt = st.number_input("Prob. Optimista (%)", value=30.0, step=5.0)
                van_opt_in = st.number_input("VAN Optimista ($)", value=250000000.0, step=5000000.0, format="%.0f")
            with c_p2:
                prob_nor = st.number_input("Prob. Normal (%)", value=50.0, step=5.0)
                van_nor_in = st.number_input("VAN Normal ($)", value=100000000.0, step=5000000.0, format="%.0f")
            with c_p3:
                prob_pes = st.number_input("Prob. Pesimista (%)", value=20.0, step=5.0)
                van_pes_in = st.number_input("VAN Pesimista ($)", value=-80000000.0, step=5000000.0, format="%.0f")

            van_esperado_disc = (prob_opt / 100.0) * van_opt_in + (prob_nor / 100.0) * van_nor_in + (prob_pes / 100.0) * van_pes_in
            desv_est_van = np.sqrt(
                (prob_opt / 100.0) * ((van_opt_in - van_esperado_disc) ** 2)
                + (prob_nor / 100.0) * ((van_nor_in - van_esperado_disc) ** 2)
                + (prob_pes / 100.0) * ((van_pes_in - van_esperado_disc) ** 2)
            )
            st.markdown(
                f'<div class="nota-celda"><b>Resultado VAN Esperado E(VAN):</b> ${van_esperado_disc:,.0f} &nbsp;|&nbsp; '
                f'<b>Desviación Estándar (Riesgo σ):</b> ${desv_est_van:,.0f} &nbsp;|&nbsp; '
                f'<b>Coeficiente de Variación (CV):</b> {(desv_est_van/abs(van_esperado_disc) if van_esperado_disc != 0 else 0):.2f} '
                f'{"(ACEPTAR: E(VAN) > 0, pero monitorear probabilidad de pérdida de " + str(prob_pes) + "%)" if van_esperado_disc > 0 else "(RECHAZAR)"}</div>',
                unsafe_allow_html=True,
            )

    with tab6:
        st.caption("Simulación Estocástica de Monte Carlo (10.000 a 50.000 Iteraciones Triangulares sobre el Caso Activo)")
        mc_c1, mc_c2, mc_c3, mc_c4 = st.columns(4)
        with mc_c1:
            ing_min_pct = st.number_input("Ingresos Mín. (% del Base)", value=80.0, step=5.0)
            ing_max_pct = st.number_input("Ingresos Máx. (% del Base)", value=125.0, step=5.0)
        with mc_c2:
            cv_min_pct = st.number_input("Costo Var. Mín. (% del Base)", value=85.0, step=5.0)
            cv_max_pct = st.number_input("Costo Var. Máx. (% del Base)", value=120.0, step=5.0)
        with mc_c3:
            cf_min_pct = st.number_input("Costo Fijo Mín. (% del Base)", value=95.0, step=5.0)
            cf_max_pct = st.number_input("Costo Fijo Máx. (% del Base)", value=110.0, step=5.0)
        with mc_c4:
            tipo_flujo_mc = st.selectbox("Flujo a Simular", ["Flujo de Caja Libre (FCL)", "Flujo Inversionista (FCI)"])
            semilla_mc = st.number_input("Iteraciones", value=10000, min_value=1000, max_value=50000, step=1000)

        es_fci_mc = "Inversionista" in tipo_flujo_mc
        n_iter = int(semilla_mc)
        tasa_mc = tasa_ke if es_fci_mc else tasa_fcl_usada

        inv0_mc = -total_inv_neta + (monto_credito if (es_fci_mc and incluir_prestamo_fci0) else 0.0)
        van_mc = np.full(n_iter, inv0_mc, dtype=float)

        np.random.seed(42)
        f_ing_min, f_ing_max = min(ing_min_pct, 100.0) / 100.0, max(ing_max_pct, 100.01) / 100.0
        f_cv_min, f_cv_max = min(cv_min_pct, 100.0) / 100.0, max(cv_max_pct, 100.01) / 100.0
        f_cf_min, f_cf_max = min(cf_min_pct, 100.0) / 100.0, max(cf_max_pct, 100.01) / 100.0

        for t in range(horizonte):
            mult_i = np.random.triangular(f_ing_min, 1.0, f_ing_max, n_iter)
            mult_v = np.random.triangular(f_cv_min, 1.0, f_cv_max, n_iter)
            mult_f = np.random.triangular(f_cf_min, 1.0, f_cf_max, n_iter)

            ing_sim = ing_series[t] * mult_i
            cv_sim = cv_series[t] * mult_v
            cf_sim = cf_series[t] * mult_f
            int_sim = intereses_anuales[t] if es_fci_mc else 0.0

            bai_sim = ing_sim - cv_sim - cf_sim - dep_anual_total - amort_anual_total - int_sim
            imp_sim = bai_sim * tasa_imp
            bdi_sim = bai_sim - imp_sim

            am_deuda_sim = amort_deuda_anuales[t] if es_fci_mc else 0.0
            resc_sim = (total_rescate_af + total_recup_ct) if t == horizonte - 1 else 0.0

            fn_sim = bdi_sim + dep_anual_total + amort_anual_total - am_deuda_sim + resc_sim
            van_mc += fn_sim / ((1.0 + tasa_mc) ** (t + 1))

        van_prom_mc = float(van_mc.mean())
        van_min_mc = float(van_mc.min())
        van_max_mc = float(van_mc.max())
        mediana_mc = float(np.median(van_mc))
        prob_exito_mc = float((van_mc >= 0).mean() * 100.0)
        riesgo_dest_mc = 100.0 - prob_exito_mc
        var_95_mc = float(np.percentile(van_mc, 5))

        k_mc1, k_mc2, k_mc3, k_mc4 = st.columns(4)
        k_mc1.metric("VAN Promedio Simulado", f"${van_prom_mc:,.0f}")
        k_mc2.metric("Probabilidad de Éxito (VAN >= 0)", f"{prob_exito_mc:.2f}%")
        k_mc3.metric("Riesgo Destrucción Valor", f"{riesgo_dest_mc:.2f}%")
        k_mc4.metric("VaR 95% (Percentil 5%)", f"${var_95_mc:,.0f}")

        conteos, bordes = np.histogram(van_mc, bins=35)
        etiquetas_bins = [f"${(bordes[i]+bordes[i+1])/2000000:,.1f}M" for i in range(len(conteos))]

        if mostrar_ayudas_pedagogicas:
            fig_mc_hist, fig_mc_cdf = graficar_montecarlo_avanzado_plotly(
                van_mc=van_mc,
                van_prom_mc=van_prom_mc,
                mediana_mc=mediana_mc,
                var_95_mc=var_95_mc,
                prob_exito_mc=prob_exito_mc,
            )
            mc_g1, mc_g2 = st.columns(2)
            with mc_g1:
                st.plotly_chart(fig_mc_hist, use_container_width=True)
            with mc_g2:
                st.plotly_chart(fig_mc_cdf, use_container_width=True)
        else:
            df_hist = pd.DataFrame({
                "Rango VAN ($ Millones)": etiquetas_bins,
                "Frecuencia (Escenarios)": conteos,
            }).set_index("Rango VAN ($ Millones)")
            st.bar_chart(df_hist, height=260, color=color_acento)

        df_resumen_mc = pd.DataFrame([
            {
                "Métrica Monte Carlo": "VAN Promedio Esperado",
                "Valor ($ / %)": f"${van_prom_mc:,.0f}",
                "Peor Escenario (Mín)": f"${van_min_mc:,.0f}",
                "Mejor Escenario (Máx)": f"${van_max_mc:,.0f}",
                "Percentil 5% (VaR 95%)": f"${var_95_mc:,.0f}",
                "Mediana (P50)": f"${mediana_mc:,.0f}",
                "Prob. Éxito (%)": f"{prob_exito_mc:.2f}%",
            }
        ])
        st.dataframe(df_resumen_mc, use_container_width=True, hide_index=True)

        texto_interp_mc = (
            f"Conclusión Estocástica ({tipo_flujo_mc}): Tras evaluar {n_iter:,} escenarios con distribución triangular "
            f"y tasa de descuento de {tasa_mc*100:.2f}%, el proyecto presenta una probabilidad de éxito comercial de {prob_exito_mc:.2f}% "
            f"y un VAN medio de ${van_prom_mc:,.0f}. En el 5% de los peores escenarios (VaR 95%), el VAN se sitúa en ${var_95_mc:,.0f}."
        )
        st.markdown(f'<div class="nota-celda">{texto_interp_mc}</div>', unsafe_allow_html=True)

    with tab7:
        st.caption("Motor de Estructura de Capital y Cátedra ULagos: Ecuación de Hamada, CAPM, WACC, Método APV y PGU (DuPont)")
        if mostrar_ayudas_pedagogicas:
            bh1, bh2, bh3 = st.columns(3)
            with bh1:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Ecuación de Hamada (βU y βL)",
                    titulo_interno="Desapalancar y Reapalancar el Riesgo Sistemático",
                    formula_latex=r"\beta_U = \frac{\beta_L}{1 + (1 - t)\frac{B}{S}} \quad \longrightarrow \quad \beta_L = \beta_U\left[1 + (1 - t)\frac{B}{S}\right]",
                    explicacion_md=(
                        "- **$\\beta_U$ (Beta Desapalancado):** Mide el **riesgo operativo puro** del negocio si no tuviera deuda.\n"
                        "- **$\\beta_L$ (Beta Apalancado):** Incorpora el riesgo financiero adicional derivado del endeudamiento ($B/S$) ajustado por el escudo fiscal $(1-t)$."
                    ),
                )
            with bh2:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Valor Presente Ajustado (APV)",
                    titulo_interno="Teorema de Modigliani-Miller con Impuestos y APV",
                    formula_latex=r"APV = VAN(\text{FCL descontado a } K_u) + \sum_{t=1}^{n} \frac{I_t \cdot t_c}{(1 + K_d)^t}",
                    explicacion_md=(
                        "- Separa el valor del proyecto en dos fuentes: **1)** el valor operativo puro financiado 100% con capital propio (descontado a $K_u$), más **2)** el valor presente de los ahorros tributarios generados por los intereses de la deuda (descontados a $K_d$)."
                    ),
                )
            with bh3:
                renderizar_burbuja_tip(
                    titulo_boton="Tip: Poder Generador de Utilidades (PGU)",
                    titulo_interno="Identidad DuPont Operacional (`Relación riesgo rentabilidad.pdf`)",
                    formula_latex=r"PGU = \underbrace{\left(\frac{EBIT}{\text{Ventas}}\right)}_{\text{Margen Op.}} \times \underbrace{\left(\frac{\text{Ventas}}{\text{Activos Op.}}\right)}_{\text{Rotación Activos}}",
                    explicacion_md=(
                        "- Demuestra que una empresa puede alcanzar alta rentabilidad sobre sus activos operacionales ya sea por **estrategia de diferenciación (alto margen)** o por **liderazgo en costos/volumen (alta rotación)**."
                    ),
                )

        h_c1, h_c2, h_c3 = st.columns(3)
        with h_c1:
            st.markdown("**1. Empresa Comparable (Desapalancar β)**")
            beta_l_comp = st.number_input("Beta Apalancado Comparable (βL)", value=1.3500, step=0.05, format="%.4f")
            deuda_pat_comp = st.number_input("Relación Deuda/Patrimonio (B/S) Comp.", value=0.4000, step=0.05, format="%.4f")
            imp_comp = st.number_input("Tasa Impuesto Comparable (%)", value=29.5, step=0.5) / 100.0
            beta_u_calc = beta_l_comp / (1.0 + (1.0 - imp_comp) * deuda_pat_comp)
            st.info(f"Beta Desapalancado (βU Puro) = {beta_u_calc:.4f}")

        with h_c2:
            st.markdown("**2. Proyecto Objetivo (Reapalancar β y CAPM)**")
            bs_objetivo = pct_deuda / max(0.0001, (1.0 - pct_deuda))
            st.write(f"Relación B/S del Caso Activo: **{bs_objetivo:.4f}** ({pct_deuda*100:.1f}% D / {(1-pct_deuda)*100:.1f}% E)")
            beta_l_proy = beta_u_calc * (1.0 + (1.0 - tasa_imp) * bs_objetivo)
            rf_h = st.number_input("Tasa Libre de Riesgo Rf (%)", value=5.50, step=0.25) / 100.0
            rm_h = st.number_input("Retorno Esperado Mercado Rm (%)", value=12.50, step=0.25) / 100.0
            ke_hamada = rf_h + beta_l_proy * (rm_h - rf_h)
            ku_desap = rf_h + beta_u_calc * (rm_h - rf_h)
            wacc_hamada = ke_hamada * (1.0 - pct_deuda) + tasa_kd * (1.0 - tasa_imp) * pct_deuda

        with h_c3:
            st.markdown("**3. Valoración por Método APV vs. WACC**")
            van_base_ku = sum(flujos_fcl_lista[t] / ((1.0 + ku_desap) ** t) for t in range(len(flujos_fcl_lista)))
            vp_escudo_kd = sum((intereses_anuales[t] * tasa_imp) / ((1.0 + tasa_kd) ** (t + 1)) for t in range(horizonte))
            apv_total = van_base_ku + vp_escudo_kd
            st.metric("VAN Base Desapalancado (a Ku)", f"${van_base_ku:,.0f}")
            st.metric("VP Escudo Fiscal Intereses (a Kd)", f"${vp_escudo_kd:,.0f}")
            st.metric("Valor Presente Ajustado (APV)", f"${apv_total:,.0f}")

        df_res_h = pd.DataFrame([{
            "βU (Riesgo Operativo)": round(beta_u_calc, 4),
            "βL Reapalancado": round(beta_l_proy, 4),
            "Ku Desapalancado (%)": f"{ku_desap*100:.2f}%",
            "Ke Apalancado CAPM (%)": f"{ke_hamada*100:.2f}%",
            "WACC con Ke CAPM (%)": f"{wacc_hamada*100:.2f}%",
            "VAN por APV ($)": f"${apv_total:,.0f}",
        }])
        st.dataframe(df_res_h, use_container_width=True, hide_index=True)

        with st.expander("Calculadora de Poder Generador de Utilidades (PGU / DuPont) y Volatilidad Anualizada (Markowitz 252 días)", expanded=True):
            p_c1, p_c2 = st.columns(2)
            with p_c1:
                st.markdown("**Poder Generador de Utilidades (PGU = Margen × Rotación)**")
                ventas_pgu = st.number_input("Ventas Anuales ($)", value=float(ing_base_neto), step=1000000.0, format="%.0f")
                ebit_pgu = st.number_input("Resultado Operacional / EBIT ($)", value=float(ing_base_neto - cv_base_neto - cf_base_neto - dep_anual_total), step=1000000.0, format="%.0f")
                activos_op_pgu = st.number_input("Activos Operacionales ($)", value=float(total_inv_neta), step=1000000.0, format="%.0f")
                margen_op = (ebit_pgu / ventas_pgu) if ventas_pgu > 0 else 0.0
                rotacion_act = (ventas_pgu / activos_op_pgu) if activos_op_pgu > 0 else 0.0
                pgu_total = margen_op * rotacion_act
                st.info(f"Margen Operacional = **{margen_op*100:.2f}%** | Rotación = **{rotacion_act:.2f}x** ➔ **PGU = {pgu_total*100:.2f}%**")
            with p_c2:
                st.markdown("**Anualización Markowitz (252 días bursátiles)**")
                ret_diario_pct = st.number_input("Retorno Promedio Diario (%)", value=0.06, step=0.01, format="%.4f")
                desv_diaria_pct = st.number_input("Desviación Estándar Diaria σ_d (%)", value=1.45, step=0.05, format="%.4f")
                ret_anual_mk = ((1.0 + ret_diario_pct / 100.0) ** 252 - 1.0) * 100.0
                desv_anual_mk = desv_diaria_pct * np.sqrt(252)
                st.info(f"Retorno Anual Compuesto = **{ret_anual_mk:.2f}%** | Volatilidad Anual ($\\sigma_{{anual}} = \\sigma_d\\sqrt{{252}}$) = **{desv_anual_mk:.2f}%**")

    # --- GENERADOR DE EXCEL CON 7 HOJAS VINCULADAS (INCLUYE HAMADA, APV, DUPONT Y MARKOWITZ) ---
    def generar_excel_monocromatico():
        wb = openpyxl.Workbook()
        wb.calculation.fullCalcOnLoad = True

        font_bold = Font(name="Calibri", size=11, bold=True, color="000000")
        font_reg = Font(name="Calibri", size=11, bold=False, color="000000")
        border_bottom = Border(bottom=Side(style="thin", color="000000"))
        border_total = Border(top=Side(style="thin", color="000000"), bottom=Side(style="double", color="000000"))
        num_fmt_curr = '#,##0;(#,##0);"-"'
        num_fmt_pct = "0.00%"

        # ================= HOJA 1: PARÁMETROS E INVERSIONES =================
        ws1 = wb.active
        ws1.title = "Hoja1"
        ws1["B2"] = "Parámetros y Supuestos"
        ws1["B2"].font = font_bold
        ws1["B2"].border = border_bottom

        params = [
            ("Horizonte (años)", int(horizonte), "0"),
            ("Impuesto", float(tasa_imp), num_fmt_pct),
            ("Costo Capital (Ke)", float(tasa_ke), num_fmt_pct),
            ("Tasa Deuda (Kd)", float(tasa_kd), num_fmt_pct),
            ("% Deuda", float(pct_deuda), num_fmt_pct),
            ("Plazo Crédito (años)", int(plazo_deuda), "0"),
            ("IVA", float(IVA_RATE), num_fmt_pct),
        ]
        for i, (label, val, fmt) in enumerate(params, start=3):
            ws1[f"B{i}"] = label
            ws1[f"B{i}"].font = font_reg
            ws1[f"C{i}"] = val
            ws1[f"C{i}"].font = font_reg
            ws1[f"C{i}"].number_format = fmt

        ws1["B10"] = "WACC"
        ws1["B10"].font = font_bold
        ws1["C10"] = "=C5*(1-C7)+C6*(1-C4)*C7"
        ws1["C10"].number_format = num_fmt_pct
        ws1["C10"].font = font_bold

        ws1["B12"] = "Inversiones y Depreciación"
        ws1["B12"].font = font_bold

        headers_inv = ["Ítem", "Valor Neto", "IVA (19%)", "Valor Bruto", "Vida Útil", "Valor Rescate", "Depreciación Anual", "Amortización Anual"]
        for col_idx, h in enumerate(headers_inv, start=2):
            cell = ws1.cell(13, col_idx, h)
            cell.font = font_bold
            cell.border = border_bottom

        start_inv_row = 14
        for idx, r in df_inv_calc.iterrows():
            curr_r = start_inv_row + idx
            ws1.cell(curr_r, 2, str(r["Ítem"])).font = font_reg
            c_net = ws1.cell(curr_r, 3, float(r["Valor Neto"]))
            c_net.number_format = num_fmt_curr
            c_net.font = font_reg

            c_iva = ws1.cell(curr_r, 4, f"=C{curr_r}*$C$9" if r["IVA (19%)"] > 0 else 0)
            c_iva.number_format = num_fmt_curr
            c_iva.font = font_reg

            c_bru = ws1.cell(curr_r, 5, f"=C{curr_r}+D{curr_r}")
            c_bru.number_format = num_fmt_curr
            c_bru.font = font_reg

            c_vid = ws1.cell(curr_r, 6, int(r["Vida Útil"]))
            c_vid.font = font_reg

            c_res = ws1.cell(curr_r, 7, float(r["Valor Rescate"]))
            c_res.number_format = num_fmt_curr
            c_res.font = font_reg

            form_dep = f"=(C{curr_r}-G{curr_r})/F{curr_r}" if restar_rescate_dep else f"=C{curr_r}/F{curr_r}"
            c_dep = ws1.cell(curr_r, 8, form_dep if r["Depreciación Anual"] > 0 else 0)
            c_dep.number_format = num_fmt_curr
            c_dep.font = font_reg

            c_amo = ws1.cell(curr_r, 9, f"=C{curr_r}/F{curr_r}" if r["Amortización Anual"] > 0 else 0)
            c_amo.number_format = num_fmt_curr
            c_amo.font = font_reg

        tot_inv_row = start_inv_row + len(df_inv_calc)
        c_tot_lbl = ws1.cell(tot_inv_row, 2, "Total")
        c_tot_lbl.font = font_bold
        c_tot_lbl.border = border_total

        for col_i in [3, 4, 5, 7, 8, 9]:
            col_let = get_column_letter(col_i)
            c_tot = ws1.cell(tot_inv_row, col_i, f"=SUM({col_let}{start_inv_row}:{col_let}{tot_inv_row-1})")
            c_tot.font = font_bold
            c_tot.border = border_total
            c_tot.number_format = num_fmt_curr

        loan_row = tot_inv_row + 2
        ws1.cell(loan_row, 2, "Préstamo").font = font_bold
        base_col_let = "E" if "Bruta" in base_credito else "C"
        c_loan = ws1.cell(loan_row, 3, f"={base_col_let}{tot_inv_row}*C7*(1+{gasto_credito_pct})")
        c_loan.number_format = num_fmt_curr
        c_loan.font = font_bold

        # ================= HOJA 3: TABLA DE AMORTIZACIÓN =================
        ws3 = wb.create_sheet("Hoja3")
        ws3["B2"] = "Tabla de Amortización"
        ws3["B2"].font = font_bold

        ws3["B4"] = "Monto Crédito"
        ws3["C4"] = f"=Hoja1!C{loan_row}"
        ws3["C4"].number_format = num_fmt_curr
        ws3["B5"] = "Tasa Anual (Kd)"
        ws3["C5"] = "=Hoja1!C6"
        ws3["C5"].number_format = num_fmt_pct
        ws3["B6"] = "Plazo (Años)"
        ws3["C6"] = "=Hoja1!C8"
        ws3["B7"] = "Cuota Fija"
        ws3["B7"].font = font_bold
        ws3["C7"] = "=PMT(C5,C6,-C4)"
        ws3["C7"].font = font_bold
        ws3["C7"].number_format = num_fmt_curr

        headers_amo = ["Período", "Cuota", "Interés", "Amortización", "Saldo"]
        for idx, h in enumerate(headers_amo, start=2):
            c = ws3.cell(9, idx, h)
            c.font = font_bold
            c.border = border_bottom

        ws3.cell(10, 2, 0)
        ws3.cell(10, 6, "=C4").number_format = num_fmt_curr

        for p in range(1, horizonte + 1):
            r_idx = 10 + p
            ws3.cell(r_idx, 2, p)
            if p <= plazo_deuda:
                c_cuota = ws3.cell(r_idx, 3, "=$C$7")
                c_int = ws3.cell(r_idx, 4, f"=F{r_idx-1}*$C$5")
                c_am = ws3.cell(r_idx, 5, f"=C{r_idx}-D{r_idx}")
                c_sal = ws3.cell(r_idx, 6, f"=F{r_idx-1}-E{r_idx}")
            else:
                c_cuota = ws3.cell(r_idx, 3, 0)
                c_int = ws3.cell(r_idx, 4, 0)
                c_am = ws3.cell(r_idx, 5, 0)
                c_sal = ws3.cell(r_idx, 6, 0)
            for c_item in [c_cuota, c_int, c_am, c_sal]:
                c_item.number_format = num_fmt_curr

        # ================= FUNCIÓN HOJAS 2 Y 4 (FCL Y FCI) =================
        def poblar_hoja_flujo(ws, es_inversionista=False):
            titulo = "Flujo de Caja Inversionista" if es_inversionista else "Flujo de Caja Libre"
            ws["B2"] = titulo
            ws["B2"].font = font_bold

            c_hdr = ws.cell(4, 2, "Ítem / Año")
            c_hdr.font = font_bold
            c_hdr.border = border_bottom
            for t in range(horizonte + 1):
                c = ws.cell(4, 3 + t, t)
                c.font = font_bold
                c.border = border_bottom
                c.alignment = Alignment(horizontal="right")

            filas_labels = [
                (5, "(+) Ingresos"),
                (6, "(-) Costos Variables"),
                (7, "(-) Costos Fijos"),
                (8, "(-) Depreciación"),
                (9, "(-) Amortización Intangibles"),
                (10, "(-) Intereses Deuda"),
                (11, "(=) BAI"),
                (12, "(-) Impuesto (29,5%)"),
                (13, "(=) BDI"),
                (14, "(+) Depreciación"),
                (15, "(+) Amortización Intangibles"),
                (16, "(-) Inversión Inicial"),
                (17, "(+) Préstamo"),
                (18, "(-) Amortización Deuda"),
                (19, "(+) Valor Rescate"),
                (20, "(+) Recup. Capital Trabajo"),
                (21, "(=) FLUJO CAJA NETO"),
                (22, "Factor Actualización"),
                (23, "Flujo Actualizado"),
                (24, "Flujo Acumulado"),
            ]
            for r_num, lbl in filas_labels:
                cell_lbl = ws.cell(r_num, 2, lbl)
                cell_lbl.font = font_bold if r_num in [11, 13, 21] else font_reg
                if r_num == 21:
                    cell_lbl.border = border_total

            ws.cell(16, 3, f"=-Hoja1!C{tot_inv_row}").number_format = num_fmt_curr
            if es_inversionista and incluir_prestamo_fci0:
                ws.cell(17, 3, "=Hoja3!C4").number_format = num_fmt_curr
            else:
                ws.cell(17, 3, 0).number_format = num_fmt_curr

            c_fn0 = ws.cell(21, 3, "=SUM(C13:C20)")
            c_fn0.font = font_bold
            c_fn0.border = border_total
            c_fn0.number_format = num_fmt_curr

            tasa_ref = "Hoja1!$C$5" if (es_inversionista or "Ke" in descuento_fcl) else "Hoja1!$C$10"
            ws.cell(22, 3, f"=(1/(1+{tasa_ref}))^C4").number_format = "0.0000"
            ws.cell(23, 3, "=C21*C22").number_format = num_fmt_curr
            ws.cell(24, 3, "=C21").number_format = num_fmt_curr

            for t in range(1, horizonte + 1):
                col_i = 3 + t
                col_let = get_column_letter(col_i)
                prev_let = get_column_letter(col_i - 1)
                g_ing = float(tasas_df.iloc[t - 1]["Crec. Ingresos (%)"]) / 100.0
                g_cv = float(tasas_df.iloc[t - 1]["Crec. Costos Var. (%)"]) / 100.0
                g_cf = float(tasas_df.iloc[t - 1]["Crec. Costos Fijos (%)"]) / 100.0

                if t == 1:
                    ws.cell(5, col_i, float(ing_series[0]))
                    ws.cell(6, col_i, float(-cv_series[0]))
                    ws.cell(7, col_i, float(-cf_series[0]))
                else:
                    ws.cell(5, col_i, f"={prev_let}5*(1+{g_ing})")
                    ws.cell(6, col_i, f"={prev_let}6*(1+{g_cv})")
                    ws.cell(7, col_i, f"={prev_let}7*(1+{g_cf})")

                ws.cell(8, col_i, f"=-Hoja1!$H${tot_inv_row}")
                ws.cell(9, col_i, f"=-Hoja1!$I${tot_inv_row}")
                if es_inversionista:
                    ws.cell(10, col_i, f"=-Hoja3!D{10+t}")
                else:
                    ws.cell(10, col_i, 0)

                ws.cell(11, col_i, f"=SUM({col_let}5:{col_let}10)").font = font_bold
                ws.cell(12, col_i, f"=-{col_let}11*Hoja1!$C$4")
                ws.cell(13, col_i, f"=SUM({col_let}11:{col_let}12)").font = font_bold
                ws.cell(14, col_i, f"=-{col_let}8")
                ws.cell(15, col_i, f"=-{col_let}9")
                ws.cell(16, col_i, 0)
                ws.cell(17, col_i, 0)
                if es_inversionista:
                    ws.cell(18, col_i, f"=-Hoja3!E{10+t}")
                else:
                    ws.cell(18, col_i, 0)

                if t == horizonte:
                    ws.cell(19, col_i, float(total_rescate_af))
                    ws.cell(20, col_i, float(total_recup_ct))
                else:
                    ws.cell(19, col_i, 0)
                    ws.cell(20, col_i, 0)

                c_fnt = ws.cell(21, col_i, f"=SUM({col_let}13:{col_let}20)")
                c_fnt.font = font_bold
                c_fnt.border = border_total

                ws.cell(22, col_i, f"=(1/(1+{tasa_ref}))^{col_let}4").number_format = "0.0000"
                ws.cell(23, col_i, f"={col_let}21*{col_let}22")
                ws.cell(24, col_i, f"={prev_let}24+{col_let}21")

                for r_curr in range(5, 22):
                    ws.cell(r_curr, col_i).number_format = num_fmt_curr
                ws.cell(23, col_i).number_format = num_fmt_curr
                ws.cell(24, col_i).number_format = num_fmt_curr

            last_let = get_column_letter(3 + horizonte)
            ws.cell(26, 2, "VAN (Suma VP)").font = font_bold
            ws.cell(26, 3, f"=SUM(C23:{last_let}23)").font = font_bold
            ws.cell(26, 3).number_format = num_fmt_curr

            ws.cell(27, 2, "VAN (VNA)").font = font_bold
            ws.cell(27, 3, f"=C21+NPV({tasa_ref},D21:{last_let}21)").font = font_bold
            ws.cell(27, 3).number_format = num_fmt_curr

            ws.cell(28, 2, "TIR").font = font_bold
            ws.cell(28, 3, f"=IRR(C21:{last_let}21)").font = font_bold
            ws.cell(28, 3).number_format = num_fmt_pct

            ws.cell(29, 2, "Payback").font = font_bold
            ws.cell(29, 3, pb_fci if es_inversionista else pb_fcl).font = font_bold

            ws.cell(31, 2, "Respuesta:").font = font_bold
            ws.merge_cells(start_row=32, start_column=2, end_row=34, end_column=3 + horizonte)
            c_interp = ws.cell(32, 2, texto_interp_fci if es_inversionista else texto_interp_fcl)
            c_interp.alignment = Alignment(wrap_text=True, vertical="top")

        ws2 = wb.create_sheet("Hoja2")
        poblar_hoja_flujo(ws2, es_inversionista=False)

        ws4 = wb.create_sheet("Hoja4")
        poblar_hoja_flujo(ws4, es_inversionista=True)

        # ================= HOJA 5: SENSIBILIDAD Y MONTE CARLO =================
        ws5 = wb.create_sheet("Hoja5")
        ws5["B2"] = "Análisis de Sensibilidad y Simulación de Monte Carlo"
        ws5["B2"].font = font_bold
        ws5["B2"].border = border_bottom

        ws5["B4"] = "1. Sensibilidad por Escenarios de Ingresos (±10%)"
        ws5["B4"].font = font_bold

        headers_s = ["Escenario", "VAN FCL ($)", "TIR FCL (%)", "Payback FCL", "VAN Inversionista ($)", "TIR Inversionista (%)"]
        for idx_h, h_text in enumerate(headers_s, start=2):
            c = ws5.cell(5, idx_h, h_text)
            c.font = font_bold
            c.border = border_bottom

        for r_i, row_s in df_sens.iterrows():
            curr_r = 6 + r_i
            ws5.cell(curr_r, 2, str(row_s["Escenario"])).font = font_reg
            c_vfcl = ws5.cell(curr_r, 3, float(row_s["VAN FCL ($)"]))
            c_vfcl.number_format = num_fmt_curr
            c_tfcl = ws5.cell(curr_r, 4, float(row_s["TIR FCL (%)"]) / 100.0)
            c_tfcl.number_format = num_fmt_pct
            ws5.cell(curr_r, 5, str(row_s["Payback FCL"])).font = font_reg
            c_vfci = ws5.cell(curr_r, 6, float(row_s["VAN Inversionista ($)"]))
            c_vfci.number_format = num_fmt_curr
            c_tfci = ws5.cell(curr_r, 7, float(row_s["TIR Inversionista (%)"]) / 100.0)
            c_tfci.number_format = num_fmt_pct

        ws5["B10"] = "2. Evaluación bajo Incertidumbre (Ejercicio 5 Guía)"
        ws5["B10"].font = font_bold
        for idx_h, h_text in enumerate(["Escenario", "Probabilidad", "VAN Escenario ($)"], start=2):
            c = ws5.cell(11, idx_h, h_text)
            c.font = font_bold
            c.border = border_bottom

        esc_ej5 = [
            ("Optimista", float(prob_opt) / 100.0, float(van_opt_in)),
            ("Normal", float(prob_nor) / 100.0, float(van_nor_in)),
            ("Pesimista", float(prob_pes) / 100.0, float(van_pes_in)),
        ]
        for idx_e, (nom_e, pr_e, v_e) in enumerate(esc_ej5, start=12):
            ws5.cell(idx_e, 2, nom_e).font = font_reg
            c_p = ws5.cell(idx_e, 3, pr_e)
            c_p.number_format = num_fmt_pct
            c_v = ws5.cell(idx_e, 4, v_e)
            c_v.number_format = num_fmt_curr

        ws5.cell(15, 2, "VAN Esperado E(VAN)").font = font_bold
        ws5.cell(15, 2).border = border_total
        c_evan = ws5.cell(15, 4, "=SUMPRODUCT(C12:C14,D12:D14)")
        c_evan.font = font_bold
        c_evan.border = border_total
        c_evan.number_format = num_fmt_curr

        ws5["B18"] = f"3. Resultados Simulación de Monte Carlo ({n_iter:,} Iteraciones - {tipo_flujo_mc})"
        ws5["B18"].font = font_bold

        ws5.cell(19, 2, "Métrica Financiera Corporativa").font = font_bold
        ws5.cell(19, 2).border = border_bottom
        ws5.cell(19, 3, "Valor").font = font_bold
        ws5.cell(19, 3).border = border_bottom

        metricas_mc_rows = [
            ("VAN Promedio Esperado (Después de Impuestos)", van_prom_mc, num_fmt_curr),
            ("Mediana Simulación (Percentil 50%)", mediana_mc, num_fmt_curr),
            ("Peor Escenario Simulado (Mínimo)", van_min_mc, num_fmt_curr),
            ("Mejor Escenario Simulado (Máximo)", van_max_mc, num_fmt_curr),
            ("Value at Risk - VaR 95% (Percentil 5%)", var_95_mc, num_fmt_curr),
            ("Probabilidad de Éxito Comercial (VAN >= $0)", prob_exito_mc / 100.0, num_fmt_pct),
            ("Riesgo de Destrucción de Valor (VAN < $0)", riesgo_dest_mc / 100.0, num_fmt_pct),
        ]
        for idx_m, (m_lbl, m_val, m_fmt) in enumerate(metricas_mc_rows, start=20):
            c_l = ws5.cell(idx_m, 2, m_lbl)
            c_l.font = font_bold if idx_m in [20, 25] else font_reg
            c_v = ws5.cell(idx_m, 3, m_val)
            c_v.font = font_bold if idx_m in [20, 25] else font_reg
            c_v.number_format = m_fmt

        ws5.cell(28, 2, "Conclusión Monte Carlo:").font = font_bold
        ws5.merge_cells("B29:G30")
        c_mc_txt = ws5.cell(29, 2, texto_interp_mc)
        c_mc_txt.alignment = Alignment(wrap_text=True, vertical="top")

        ws5["I4"] = "Distribución de Frecuencias (Histograma)"
        ws5["I4"].font = font_bold
        ws5.cell(5, 9, "Rango VAN ($ Millones)").font = font_bold
        ws5.cell(5, 9).border = border_bottom
        ws5.cell(5, 10, "Frecuencia (Escenarios)").font = font_bold
        ws5.cell(5, 10).border = border_bottom
        for i_bin, (etq, cnt) in enumerate(zip(etiquetas_bins, conteos), start=6):
            ws5.cell(i_bin, 9, etq).font = font_reg
            ws5.cell(i_bin, 10, int(cnt)).font = font_reg

        # ================= HOJA 6: EJERCICIO 8 (10 AÑOS) Y AUDITORÍA EJ. 7 =================
        ws6 = wb.create_sheet("Hoja6")
        ws6["B2"] = "Ejercicio 8: Flujo de Caja a 10 Años (Ampliación, Reemplazo y Costo Hundido)"
        ws6["B2"].font = font_bold

        c_h6 = ws6.cell(4, 2, "Ítem / Año")
        c_h6.font = font_bold
        c_h6.border = border_bottom
        for t in range(11):
            c = ws6.cell(4, 3 + t, t)
            c.font = font_bold
            c.border = border_bottom
            c.alignment = Alignment(horizontal="right")

        filas_e8_meta = [
            (5, "(+) Ingresos", ing_e8, False),
            (6, "(-) Costos Var. Fabricación", cv_fab_e8, False),
            (7, "(-) Comisiones (2%)", comis_e8, False),
            (8, "(-) Costos Fijos Fab.", cf_fab_e8, False),
            (9, "(-) Gastos Adm. y Ventas", gav_e8, False),
            (10, "(-) Depreciación", dep_e8, False),
            (11, "(-) Amort. Intangibles (Puesta en Marcha)", amo_e8, False),
            (12, "(+) Venta Máquina Usada", vta_maq_e8, False),
            (13, "(-) Valor Libro Máquina", vl_maq_e8, False),
            (14, "(=) Utilidad Antes de Impuestos", None, True),
            (15, "(-) Impuesto (15%)", None, False),
            (16, "(=) Utilidad Neta", None, True),
            (17, "(+) Depreciación", rev_dep_e8, False),
            (18, "(+) Amort. Intangibles", rev_amo_e8, False),
            (19, "(+) Valor Libro Máquina", rev_vl_e8, False),
            (20, "(-) Inversiones (Capex y Cap. Trabajo)", inv_e8, False),
            (21, "(+) Valor de Desecho", desecho_e8, False),
            (22, "(+) Recup. Capital de Trabajo", rec_ct_e8, False),
            (23, "(=) FLUJO DE CAJA NETO", None, True),
            (24, "Factor Actualización (12%)", None, False),
            (25, "Flujo Actualizado (VP)", None, False),
        ]

        for r_num, lbl, serie_vals, es_negrita in filas_e8_meta:
            c_l = ws6.cell(r_num, 2, lbl)
            c_l.font = font_bold if es_negrita else font_reg
            if r_num == 23:
                c_l.border = border_total

            for t in range(11):
                col_i = 3 + t
                col_let = get_column_letter(col_i)
                c_val = ws6.cell(r_num, col_i)

                if serie_vals is not None:
                    c_val.value = float(serie_vals[t])
                    c_val.number_format = num_fmt_curr
                elif r_num == 14:
                    c_val.value = f"=SUM({col_let}5:{col_let}13)"
                    c_val.font = font_bold
                    c_val.number_format = num_fmt_curr
                elif r_num == 15:
                    c_val.value = f"=IF({col_let}14>0,-{col_let}14*0.15,0)"
                    c_val.number_format = num_fmt_curr
                elif r_num == 16:
                    c_val.value = f"=SUM({col_let}14:{col_let}15)"
                    c_val.font = font_bold
                    c_val.number_format = num_fmt_curr
                elif r_num == 23:
                    c_val.value = f"=SUM({col_let}16:{col_let}22)"
                    c_val.font = font_bold
                    c_val.border = border_total
                    c_val.number_format = num_fmt_curr
                elif r_num == 24:
                    c_val.value = f"=(1/(1+0.12))^{col_let}4"
                    c_val.number_format = "0.0000"
                elif r_num == 25:
                    c_val.value = f"={col_let}23*{col_let}24"
                    c_val.number_format = num_fmt_curr

        ws6.cell(27, 2, "VAN (Suma VP al 12%)").font = font_bold
        c_ve8_1 = ws6.cell(27, 3, "=SUM(C25:M25)")
        c_ve8_1.font = font_bold
        c_ve8_1.number_format = num_fmt_curr

        ws6.cell(28, 2, "VAN (Fórmula VNA)").font = font_bold
        c_ve8_2 = ws6.cell(28, 3, "=C23+NPV(0.12,D23:M23)")
        c_ve8_2.font = font_bold
        c_ve8_2.number_format = num_fmt_curr

        ws6.cell(29, 2, "TIR").font = font_bold
        c_te8 = ws6.cell(29, 3, "=IRR(C23:M23)")
        c_te8.font = font_bold
        c_te8.number_format = num_fmt_pct

        ws6.cell(30, 2, "Payback").font = font_bold
        ws6.cell(30, 3, pb_e8).font = font_bold

        ws6["B33"] = "Ejercicio 7: Auditoría de los Errores del Flujo de Caja"
        ws6["B33"].font = font_bold
        for idx_h, h_text in enumerate(["N° Error Detectado", "Evidencia en el Flujo", "Justificación Conceptual"], start=2):
            c = ws6.cell(34, idx_h, h_text)
            c.font = font_bold
            c.border = border_bottom

        for i_err, r_err in df_err7.iterrows():
            curr_r = 35 + i_err
            ws6.cell(curr_r, 2, str(r_err["N° Error"])).font = font_bold
            ws6.cell(curr_r, 3, str(r_err["Evidencia en la Tabla del Asesor"])).font = font_reg
            ws6.cell(curr_r, 4, str(r_err["Justificación Conceptual"])).font = font_reg

        # ================= HOJA 7: HAMADA, CAPM, APV, DUPONT Y MARKOWITZ =================
        ws7 = wb.create_sheet("Hoja7")
        ws7["B2"] = "Estructura de Capital (Hamada, CAPM, APV), PGU (DuPont) y Taller Markowitz IPSA"
        ws7["B2"].font = font_bold
        ws7["B2"].border = border_bottom

        ws7["B4"] = "1. Ecuación de Hamada, CAPM y WACC (Fórmulas Nativas)"
        ws7["B4"].font = font_bold

        filas_hamada = [
            (5, "Beta Apalancado Comparable (βL Comp.)", float(beta_l_comp), "0.0000"),
            (6, "Relación B/S Comparable", float(deuda_pat_comp), "0.0000"),
            (7, "Impuesto Comparable", float(imp_comp), num_fmt_pct),
            (8, "Beta Desapalancado Puro (βU)", "=C5/(1+(1-C7)*C6)", "0.0000"),
            (9, "Relación B/S Proyecto Activo", "=Hoja1!C7/(1-Hoja1!C7)", "0.0000"),
            (10, "Beta Reapalancado Proyecto (βL)", "=C8*(1+(1-Hoja1!C4)*C9)", "0.0000"),
            (11, "Tasa Libre de Riesgo (Rf)", float(rf_h), num_fmt_pct),
            (12, "Retorno Esperado Mercado (Rm)", float(rm_h), num_fmt_pct),
            (13, "Costo Patrimonial Desapalancado (Ku)", "=C11+C8*(C12-C11)", num_fmt_pct),
            (14, "Costo Patrimonial Apalancado CAPM (Ke)", "=C11+C10*(C12-C11)", num_fmt_pct),
            (15, "WACC Calculado vía Hamada-CAPM", "=C14*(1-Hoja1!C7)+Hoja1!C6*(1-Hoja1!C4)*Hoja1!C7", num_fmt_pct),
        ]
        for r_i, lbl_h, val_h, fmt_h in filas_hamada:
            c_l = ws7.cell(r_i, 2, lbl_h)
            c_l.font = font_bold if str(val_h).startswith("=") else font_reg
            c_v = ws7.cell(r_i, 3, val_h)
            c_v.font = font_bold if str(val_h).startswith("=") else font_reg
            c_v.number_format = fmt_h

        ws7["B17"] = "2. Poder Generador de Utilidades (PGU / Identidad DuPont)"
        ws7["B17"].font = font_bold
        ws7.cell(18, 2, "Ventas Operacionales Año 1 ($)").font = font_reg
        ws7.cell(18, 3, float(ventas_pgu)).number_format = num_fmt_curr
        ws7.cell(19, 2, "Resultado Operacional EBIT ($)").font = font_reg
        ws7.cell(19, 3, float(ebit_pgu)).number_format = num_fmt_curr
        ws7.cell(20, 2, "Activos Operacionales Netos ($)").font = font_reg
        ws7.cell(20, 3, float(activos_op_pgu)).number_format = num_fmt_curr
        ws7.cell(21, 2, "Margen de Utilidad Operacional (%)").font = font_bold
        ws7.cell(21, 3, "=IF(C18>0,C19/C18,0)").number_format = num_fmt_pct
        ws7.cell(22, 2, "Rotación de Activos Operacionales (veces)").font = font_bold
        ws7.cell(22, 3, "=IF(C20>0,C18/C20,0)").number_format = "0.00"
        ws7.cell(23, 2, "Poder Generador de Utilidades (PGU = Margen x Rotación)").font = font_bold
        ws7.cell(23, 3, "=C21*C22").number_format = num_fmt_pct
        ws7.cell(23, 3).border = border_total

        wb._sheets = [ws1, ws2, ws3, ws4, ws5, ws6, ws7]

        for sheet in wb.worksheets:
            sheet.column_dimensions["B"].width = 38
            for col_i in range(3, 15):
                sheet.column_dimensions[get_column_letter(col_i)].width = 16

        output = io.BytesIO()
        wb.save(output)
        return output.getvalue()


    excel_bytes = generar_excel_monocromatico()

    with barra_superior:
        top_left, top_right = st.columns([5.5, 1])
        with top_left:
            st.caption(
                f"Inv. Neta: ${total_inv_neta:,.0f}  |  Inv. Bruta: ${total_inv_bruta:,.0f}  |  "
                f"Crédito: ${monto_credito:,.0f}  |  Cuota PAGO: ${cuota_anual:,.0f}  |  WACC: {wacc_calc*100:.2f}%"
            )
        with top_right:
            st.download_button(
                label="Guardar (.xlsx)",
                data=excel_bytes,
                file_name="Libro1.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )


def main():
    if "modo_catedra_fin" not in st.session_state:
        st.session_state.modo_catedra_fin = _es_url_catedra
    elif _es_url_catedra:
        st.session_state.modo_catedra_fin = True

    with st.sidebar:
        st.markdown("### Finanzas Avanzadas 2026")
        st.caption("Ingeniería Comercial — ULagos")
        st.markdown("---")

        opciones_nav = [
            "1. Estudio Fluido 60 FPS, Hoja Mecánica y Mapa Teórico",
            "2. Biblioteca y Visor PDF (Drive 5 TB)",
        ]
        if not st.session_state.modo_catedra_fin:
            opciones_nav.extend([
                "3. Evaluador Corporativo FCL / FCI, Monte Carlo y Libro1.xlsx",
                "4. Pizarra Paso a Paso FCL / FCI (Práctica en Hoja)",
                "5. Markowitz IPSA (SciPy) y Guía Repaso (Ej. 1 al 8)",
            ])

        vista_activa = st.radio(
            "Vista de Trabajo:",
            options=opciones_nav,
            index=0,
            key="nav_fin_limpio_v2",
        )

        st.markdown("---")
        _nuevo_modo = st.toggle(
            "Modo Presentación Cátedra",
            value=st.session_state.modo_catedra_fin,
            key="toggle_modo_catedra_fin",
            help="Deja visibles únicamente el Estudio 60 FPS y la Biblioteca Oficial.",
        )
        if _nuevo_modo != st.session_state.modo_catedra_fin:
            st.session_state.modo_catedra_fin = _nuevo_modo
            st.rerun()

        if st.session_state.modo_catedra_fin:
            st.caption("Link directo Modo Cátedra:")
            st.code("https://finanzas-avanzadas-2026-nxvqzsfrrtgu9e92javcli.streamlit.app/?modo=catedra", language=None)

    if vista_activa.startswith("1."):
        st.markdown(
            """
            <div style="background-color:#0F172A;color:#FFFFFF;padding:12px 20px;border-radius:8px;margin-bottom:10px;">
                <div style="font-size:15.5px;font-weight:700;">ESTUDIO INTERACTIVO A 60 FPS — FINANZAS AVANZADAS (ULAGOS 2026)</div>
                <div style="font-size:12px;color:#CBD5E1;margin-top:2px;">8 módulos sin lag: Separación de Fisher, Riesgo y Juego Justo, Markowitz (252d) y CAPM, Hamada/WACC/APV, VAN vs. TIR + PGU DuPont, Hoja Mecánica, Mapa Teórico + Lectura Viva y Guías Oficiales Resueltas.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if callable(renderizar_estudio_fluido_finanzas_60fps):
            renderizar_estudio_fluido_finanzas_60fps()
        else:
            st.warning("Verifica que 'motor_fluidez_finanzas_60fps.py' esté en la raíz del repositorio.")
    elif vista_activa.startswith("2."):
        _render_vista_biblioteca_drive()
    elif vista_activa.startswith("3."):
        _render_vista_evaluador_corporativo(solo_pizarra=False)
    elif vista_activa.startswith("4."):
        _render_vista_evaluador_corporativo(solo_pizarra=True)
    elif vista_activa.startswith("5."):
        _render_vista_markowitz_y_guia()


if __name__ == "__main__":
    main()
