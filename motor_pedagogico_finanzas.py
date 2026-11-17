# -*- coding: utf-8 -*-
# Archivo: motor_pedagogico_finanzas.py
"""
motor_pedagogico_finanzas.py — MOTOR PEDAGÓGICO, PIZARRA PASO A PASO Y LABORATORIOS DE FINANZAS
Repositorio: FINANZAS-AVANZADAS-2026 | Cátedra ULagos: Prof.ª Camila Bustos Rosas

Integra:
1. Taller Guiado Paso a Paso en Hoja Editable (6 Etapas con corrector celda por celda en tiempo real,
   detección automática de errores conceptuales, barra de progreso y fórmulas fx dinámicas).
2. Componente de Burbujas Metodológicas (st.popover) con fórmulas LaTeX y lectura en vivo.
3. Visualizadores Interactivos en Plotly para Evaluación de Activos Reales:
   - Perfil del VAN(r), TIR, WACC/Ke y Cruce de Fisher.
   - Cascada Financiera (Waterfall) de Ingresos a Flujo de Caja Neto y Escudo Fiscal.
   - Gráfico de Tornado de Sensibilidad Multivariable (±10%).
   - Distribución de Monte Carlo en Plotly (Histograma + VaR 95% + Curva Acumulada S-Curve).
4. Laboratorios Teóricos y Prácticos en Vivo (Cátedra Prof.ª Camila Bustos Rosas):
   - Modelo Consumo-Inversión y Principio de Separación de Fisher ('Consumo - Inversión.pdf').
   - Actitudes frente al Riesgo, Juego Justo, Equivalente Cierto y Prima por Riesgo ('Relación riesgo rentabilidad.pdf').
   - Taller Frontera Eficiente de Markowitz (252 días), Dupla 13 IPSA ($65.000.000; 5 vs. 30 acciones) y CAPM/CML.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy.optimize import minimize


# ==============================================================================
# 1. COMPONENTE DE BURBUJAS METODOLÓGICAS Y BARRA FX DINÁMICA
# ==============================================================================

def inyectar_estilos_burbujas_finanzas():
    st.markdown(
        """
        <style>
        div[data-testid="stPopover"] > button {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
            color: #1e3a8a !important;
            border: 1px solid #93c5fd !important;
            border-left: 4px solid #2563eb !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            font-size: 12px !important;
            padding: 4px 10px !important;
        }
        div[data-testid="stPopover"] > button:hover {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
            border-color: #2563eb !important;
        }
        .fin-badge {
            display: inline-block;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            color: #1e3a8a;
            border: 1px solid #93c5fd;
            border-radius: 16px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .paso-box {
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 5px solid #2563eb;
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 10px;
            font-size: 13px;
            color: #0f172a;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def renderizar_burbuja_tip(
    titulo_boton: str,
    titulo_interno: str,
    explicacion_md: str,
    formula_latex: str = None,
):
    """
    Despliega una burbuja interactiva (st.popover) con la fórmula matemática,
    el respaldo conceptual de cátedra y la interpretación de las cifras en vivo.
    """
    if hasattr(st, "popover"):
        contenedor = st.popover(f"Nota Metodológica: {titulo_boton}", use_container_width=True)
    else:
        contenedor = st.expander(f"Nota Metodológica: {titulo_boton}")

    with contenedor:
        st.markdown(f"#### {titulo_interno}")
        if formula_latex:
            st.latex(formula_latex)
        st.markdown(explicacion_md)


def obtener_catalogo_formulas_fx(es_inv: bool, tasa_imp: float, tasa_desc: float):
    """
    Retorna el catálogo de fórmulas reales de Excel para alimentar la barra fx interactiva
    y el inspector de celdas paso a paso.
    """
    t_str = f"{tasa_imp*100:.1f}%"
    r_str = f"{tasa_desc*100:.2f}%"
    ref_tasa = "Hoja1!$C$5" if es_inv else "Hoja1!$C$10"
    return {
        "(+) Ingresos": ("D5", "=C5*(1+Tasa_Crec_Ing)", "Ingresos operacionales netos de IVA (si el dato viene Bruto, dividir por 1,19)."),
        "(-) Costos Variables": ("D6", "=-Costo_Var_Neto*(1+Tasa_Crec_CV)", "Egreso operativo variable con signo negativo consistente."),
        "(-) Costos Fijos": ("D7", "=-Costo_Fijo_Neto*(1+Tasa_Crec_CF)", "Egreso operativo fijo con signo negativo consistente."),
        "(-) Depreciación": ("D8", "=-Hoja1!$H$19", "Cuota anual de depreciación lineal: -(Valor Neto - Valor Rescate) / Vida Útil."),
        "(-) Amort. Intangibles": ("D9", "=-Hoja1!$I$19", "Amortización anual de activos intangibles (Puesta en marcha / Organización)."),
        "(-) Intereses Deuda": ("D10", "=-Hoja3!D11" if es_inv else "=0", "Gasto financiero de la tabla de amortización (solo en Flujo del Inversionista)."),
        "(=) BAI": ("D11", "=SUMA(D5:D10)", "Beneficio Antes de Impuestos (suma algebraica desde Ingresos hasta Intereses)."),
        "(-) Impuesto (29.5%)": ("D12", f"=-D11*Hoja1!$C$4  (Tasa = {t_str})", "Impuesto de Primera Categoría sobre el BAI (lleva signo negativo)."),
        "(=) BDI": ("D13", "=SUMA(D11:D12)", "Beneficio Después de Impuestos (Utilidad Neta = BAI - Impuesto)."),
        "(+) Depreciación": ("D14", "=-D8", "Reverso positivo de la Depreciación (no es salida de efectivo real)."),
        "(+) Amort. Intangibles": ("D15", "=-D9", "Reverso positivo de la Amortización de Intangibles."),
        "(-) Inversión Inicial": ("C16", "=-Hoja1!C19", "Desembolso de CAPEX + Intangibles + Capital de Trabajo en el Año 0 (signo negativo)."),
        "(+) Préstamo": ("C17", "=Hoja3!C4" if es_inv else "=0", "Entrada del crédito bancario en el Año 0 para financiar parte de la inversión."),
        "(-) Amortización Deuda": ("D18", "=-Hoja3!E11" if es_inv else "=0", "Pago del principal de la deuda después de impuestos (Cuota Fija - Interés)."),
        "(+) Valor Rescate": ("I19", "=Valor_Desecho_Activos", "Recuperación del valor residual de los activos fijos al final del horizonte."),
        "(+) Recup. Cap. Trabajo": ("I20", "=Capital_Trabajo_Año0", "Recuperación íntegra (100%) del Capital de Trabajo en el último año."),
        "(=) FLUJO CAJA NETO": ("C21", "=SUMA(C13:C20)", "Flujo de Caja Neto del período (BDI + Reversos - CAPEX + Préstamo - Amort. Deuda + Rescates)."),
        "Flujo Actualizado (VP)": ("D23", f"=D21/((1+{ref_tasa})^D4)  (Tasa = {r_str})", "Valor Presente del flujo futuro descontado a la tasa exigida: FCN_t / (1 + r)^t."),
        "Flujo Acumulado": ("D24", "=C24+D21", "Suma acumulada de los Flujos de Caja Netos nominales para calcular el Payback."),
    }


# ==============================================================================
# 2. TALLER GUIADO PASO A PASO ESCRIBIENDO EN LA HOJA (PIZARRA INTERACTIVA)
# ==============================================================================

DEFINICION_PASOS_HOJA = [
    {
        "num": 1,
        "titulo": "Paso 1: Ingresos y Costos Operativos Netos de IVA (Años 1 a N)",
        "filas": ["(+) Ingresos", "(-) Costos Variables", "(-) Costos Fijos"],
        "regla_oro": (
            "1) Todos los valores del Estado de Resultados deben ir **Netos de IVA** (si un monto está en Bruto, divídelo por `1,19`). "
            "2) Los **Ingresos** llevan signo positivo (`+`) y los **Costos Variables y Fijos** llevan signo negativo (`-`). "
            "3) En el `Año 0` estas tres filas valen `0`."
        ),
        "formula_fx": "D5 = Ingreso_Neto_A1*(1+g)  |  D6 = -Costo_Var_Neto  |  D7 = -Costo_Fijo_Neto",
    },
    {
        "num": 2,
        "titulo": "Paso 2: Deducciones Contables y Escudo Fiscal (Depreciación, Amortización e Intereses)",
        "filas": ["(-) Depreciación", "(-) Amort. Intangibles", "(-) Intereses Deuda"],
        "regla_oro": (
            "1) La **Depreciación Anual** `-(Valor Neto - Valor Rescate) / Vida Útil` y la **Amortización de Intangibles** se restan con signo negativo (`-`) antes de impuestos para rebajar la base imponible. "
            "2) Si evalúas el **Flujo de Caja Libre (FCL)** (proyecto puro sin deuda), la fila `(-) Intereses Deuda` es `0`. Si evalúas el **Flujo del Inversionista (FCI)**, resta aquí el interés anual de la tabla de amortización."
        ),
        "formula_fx": "D8 = -(Activo_Neto - Rescate)/Vida_Util  |  D10 = -Saldo_Anterior * Kd (solo en FCI)",
    },
    {
        "num": 3,
        "titulo": "Paso 3: Utilidad Antes de Impuestos (BAI), Impuesto (29,5%) y Utilidad Neta (BDI)",
        "filas": ["(=) BAI", "(-) Impuesto (29.5%)", "(=) BDI"],
        "regla_oro": (
            "1) **`(=) BAI`**: Suma verticalmente desde `(+) Ingresos` hasta `(-) Intereses Deuda` (`=SUMA(D5:D10)`). "
            "2) **`(-) Impuesto`**: Multiplica el BAI por la tasa de impuesto y colócalo con **signo negativo** (`=-D11 * Tasa_Imp`). "
            "3) **`(=) BDI`**: Suma `BAI + Impuesto` (`=D11 + D12`)."
        ),
        "formula_fx": "D11 = SUMA(D5:D10)  |  D12 = -D11 * 29,5%  |  D13 = D11 + D12",
    },
    {
        "num": 4,
        "titulo": "Paso 4: Reverso de Partidas No Monetarias (+Depreciación y +Amortización)",
        "filas": ["(+) Depreciación", "(+) Amort. Intangibles"],
        "regla_oro": (
            "Como la depreciación y la amortización de intangibles **no son salidas reales de efectivo** (solo se restaron en el Paso 2 para ahorrar impuestos), "
            "ahora debes **sumarlas de vuelta con signo positivo (`+`)** por exactamente el mismo monto anual."
        ),
        "formula_fx": "D14 = -D8 (+Depreciación)  |  D15 = -D9 (+Amortización Intangibles)",
    },
    {
        "num": 5,
        "titulo": "Paso 5: Movimientos de Capital (Año 0 y Año Final) y (=) FLUJO DE CAJA NETO",
        "filas": [
            "(-) Inversión Inicial",
            "(+) Préstamo",
            "(-) Amortización Deuda",
            "(+) Valor Rescate",
            "(+) Recup. Cap. Trabajo",
            "(=) FLUJO CAJA NETO",
        ],
        "regla_oro": (
            "1) En el **`Año 0`**, anota la `(-) Inversión Inicial` total neta con signo negativo (`-`) y, si es Flujo del Inversionista, suma el `(+) Préstamo` con signo positivo (`+`). "
            "2) En el **último año**, suma el `(+) Valor Rescate` de los activos fijos y el 100% de la `(+) Recup. Cap. Trabajo`. "
            "3) Calcula **`(=) FLUJO CAJA NETO`** sumando desde `(=) BDI` hasta `(+) Recup. Cap. Trabajo` (`=SUMA(C13:C20)`)."
        ),
        "formula_fx": "C21 = SUMA(C13:C20)  |  En Año N: incluir +Valor Rescate y +Recup. Capital de Trabajo",
    },
    {
        "num": 6,
        "titulo": "Paso 6: Descuento a Valor Presente (VP), Flujo Acumulado, VAN y TIR",
        "filas": ["Flujo Actualizado (VP)", "Flujo Acumulado"],
        "regla_oro": (
            "1) **`Flujo Actualizado (VP)`**: Divide el Flujo de Caja Neto de cada año $t$ por $(1 + r)^t$ (**¡jamás multipliques!**). En el `Año 0`, como $(1+r)^0 = 1$, el VP es igual al flujo del Año 0. "
            "2) **`Flujo Acumulado`**: Suma acumulativamente los Flujos de Caja Netos nominales para ver en qué año se recupera la inversión (Payback)."
        ),
        "formula_fx": "D23 = D21 / ((1 + Tasa_Descuento)^t)  |  VAN = SUMA(C23:I23)  |  TIR = TIR(C21:I21)",
    },
]


def renderizar_taller_paso_a_paso_en_hoja(
    plantilla_nombre: str,
    df_fcl_sol: pd.DataFrame,
    df_fci_sol: pd.DataFrame,
    van_fcl_sol: float,
    tir_fcl_sol: float,
    van_fci_sol: float,
    tir_fci_sol: float,
    tasa_fcl: float,
    tasa_ke: float,
    tasa_imp: float,
    total_inv_neta: float,
    monto_credito: float,
    dep_anual_total: float,
    total_rescate_af: float,
    total_recup_ct: float,
):
    """
    Renderiza una hoja de cálculo interactiva paso a paso donde el alumno puede escribir
    directamente en las celdas, autocompletar por etapas y recibir corrección instantánea.
    """
    inyectar_estilos_burbujas_finanzas()

    st.markdown(
        '<span class="fin-badge">Modo Pizarra Interactiva — Aprende Construyendo el Flujo Celda por Celda en la Hoja</span>',
        unsafe_allow_html=True,
    )

    c_top1, c_top2, c_top3 = st.columns([1.5, 1.8, 1.2])
    with c_top1:
        tipo_practica = st.radio(
            "1. ¿Qué hoja deseas construir paso a paso?",
            ["Flujo de Caja Libre (FCL — Proyecto Puro)", "Flujo del Inversionista (FCI — Con Deuda)"],
            horizontal=False,
            key="piz_tipo_flujo",
        )
    es_fci = "Inversionista" in tipo_practica
    df_sol = df_fci_sol.copy() if es_fci else df_fcl_sol.copy()
    van_sol = van_fci_sol if es_fci else van_fcl_sol
    tir_sol = tir_fci_sol if es_fci else tir_fcl_sol
    tasa_usada = tasa_ke if es_fci else tasa_fcl

    with c_top2:
        opciones_pasos = [f"{p['titulo']}" for p in DEFINICION_PASOS_HOJA]
        paso_sel_txt = st.selectbox(
            "2. Selecciona el Paso de Construcción Activo (1 al 6):",
            options=opciones_pasos,
            index=0,
            key="piz_paso_activo",
        )
        paso_obj = next(p for p in DEFINICION_PASOS_HOJA if p["titulo"] == paso_sel_txt)
        num_paso = paso_obj["num"]

    with c_top3:
        tol_pesos = st.number_input(
            "3. Tolerancia de redondeo ($ CLP):",
            min_value=1.0,
            max_value=50000.0,
            value=500.0,
            step=100.0,
            help="Acepta pequeñas diferencias por decimales al escribir en la hoja.",
            key="piz_tol",
        )

    # Inicializar el estado de la hoja del alumno en st.session_state
    state_key = f"hoja_alumno_{plantilla_nombre}_{'FCI' if es_fci else 'FCL'}_{len(df_sol.columns)}"
    if state_key not in st.session_state:
        df_init = pd.DataFrame(0.0, index=df_sol.index, columns=df_sol.columns)
        # Pre-cargar el Paso 1 por defecto salvo las filas que el alumno quiera practicar, o iniciar con todo en 0
        st.session_state[state_key] = df_init

    # Botonera de acciones pedagógicas rápidas sobre la hoja
    b_ac1, b_ac2, b_ac3, b_ac4 = st.columns(4)
    with b_ac1:
        if st.button(f"Autocompletar solo el Paso {num_paso}", use_container_width=True, key="btn_fill_curr"):
            df_curr = st.session_state[state_key].copy()
            for f_nom in paso_obj["filas"]:
                if f_nom in df_sol.index:
                    df_curr.loc[f_nom] = df_sol.loc[f_nom]
            st.session_state[state_key] = df_curr
            st.rerun()

    with b_ac2:
        if st.button(f"Autocompletar desde Paso 1 hasta Paso {num_paso}", type="primary", use_container_width=True, key="btn_fill_upto"):
            df_curr = pd.DataFrame(0.0, index=df_sol.index, columns=df_sol.columns)
            for p_i in DEFINICION_PASOS_HOJA:
                if p_i["num"] <= num_paso:
                    for f_nom in p_i["filas"]:
                        if f_nom in df_sol.index:
                            df_curr.loc[f_nom] = df_sol.loc[f_nom]
            st.session_state[state_key] = df_curr
            st.rerun()

    with b_ac3:
        if st.button("Resolver toda la Hoja (100%)", use_container_width=True, key="btn_fill_all"):
            st.session_state[state_key] = df_sol.astype(float).copy()
            st.rerun()

    with b_ac4:
        if st.button("Vaciar Hoja (Practicar desde Cero)", use_container_width=True, key="btn_clear_all"):
            st.session_state[state_key] = pd.DataFrame(0.0, index=df_sol.index, columns=df_sol.columns)
            st.rerun()

    # Tarjeta de instrucción del Paso Activo + Fórmula fx
    filas_paso_str = ", ".join(f"`{f}`" for f in paso_obj["filas"])
    st.markdown(
        f"""
        <div class="paso-box">
            <b>{paso_obj['titulo']}</b><br>
            <b>Filas que debes completar en este paso:</b> {filas_paso_str}<br>
            <b>Regla de Cátedra:</b> {paso_obj['regla_oro']}<br>
            <span style="font-family:Consolas,monospace;font-size:12px;background:#ffffff;border:1px solid #cbd5e1;padding:2px 8px;border-radius:4px;display:inline-block;margin-top:5px;">
                <b>fx Fórmula Excel del Paso {num_paso}:</b> {paso_obj['formula_fx']}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Pistas numéricas desplegables para que el alumno pueda hacer el cálculo a mano o en calculadora
    with st.expander(f"Ver Datos Base del {plantilla_nombre} para calcular a mano las celdas del Paso {num_paso}", expanded=False):
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            st.markdown(
                f"- **Inversión Neta Año 0:** `${total_inv_neta:,.0f}`\n"
                f"- **Préstamo Año 0 (FCI):** `${monto_credito:,.0f}`\n"
                f"- **Depreciación Anual:** `${dep_anual_total:,.0f}`"
            )
        with p_col2:
            st.markdown(
                f"- **Tasa Impuesto:** `{tasa_imp*100:.1f}%`\n"
                f"- **Tasa Descuento Exigida ($r$):** `{tasa_usada*100:.2f}%`\n"
                f"- **Valor Rescate + Rec. CT (Último Año):** `${total_rescate_af:,.0f}` + `${total_recup_ct:,.0f}`"
            )
        with p_col3:
            st.markdown("**Valores esperados en las filas de este paso:**")
            st.dataframe(df_sol.loc[paso_obj["filas"]].style.format("{:,.0f}"), use_container_width=True)

    # Editor de Hoja en Vivo donde el alumno escribe
    st.markdown("##### Escribe tus resultados directamente en las celdas de la hoja (presiona `Enter` o `Tab` al terminar cada celda):")
    df_usuario_edit = st.data_editor(
        st.session_state[state_key],
        use_container_width=True,
        height=470,
        key=f"editor_pizarra_{state_key}",
    )
    st.session_state[state_key] = df_usuario_edit.copy()

    # ==========================================================================
    # AUDITORÍA AUTOMÁTICA CELDA POR CELDA Y DETECCIÓN DE ERRORES DE CÁTEDRA
    # ==========================================================================
    mat_usr = df_usuario_edit.to_numpy(dtype=float)
    mat_sol = df_sol.to_numpy(dtype=float)
    diff_abs = np.abs(mat_usr - mat_sol)
    celdas_ok = diff_abs <= tol_pesos

    total_celdas = int(mat_sol.size)
    total_ok = int(np.sum(celdas_ok))
    pct_progreso = (total_ok / max(total_celdas, 1)) * 100.0

    # Evaluar progreso específico del Paso Activo
    idx_filas_paso = [df_sol.index.get_loc(f) for f in paso_obj["filas"] if f in df_sol.index]
    celdas_paso_ok = int(np.sum(celdas_ok[idx_filas_paso, :]))
    celdas_paso_tot = len(idx_filas_paso) * len(df_sol.columns)
    pct_paso = (celdas_paso_ok / max(celdas_paso_tot, 1)) * 100.0

    st.progress(min(pct_progreso / 100.0, 1.0), text=f"Progreso Global de tu Hoja: {total_ok}/{total_celdas} celdas correctas ({pct_progreso:.1f}%)  |  Paso {num_paso}: {celdas_paso_ok}/{celdas_paso_tot} ({pct_paso:.0f}%)")

    # Detectar errores conceptuales frecuentes en las filas editadas
    diagnosticos = []
    for f_nom in paso_obj["filas"]:
        if f_nom not in df_sol.index:
            continue
        for col_nom in df_sol.columns:
            v_u = float(df_usuario_edit.loc[f_nom, col_nom])
            v_s = float(df_sol.loc[f_nom, col_nom])
            if abs(v_u - v_s) <= tol_pesos:
                continue
            if abs(v_u) < 1e-4 and abs(v_s) > tol_pesos:
                diagnosticos.append(f"Celda pendiente en **{f_nom} ({col_nom})**: aún está en `0` (valor correcto: `${v_s:,.0f}`).")
            elif abs(v_u + v_s) <= max(tol_pesos, abs(v_s) * 0.02):
                diagnosticos.append(
                    f"⚠️ **Error de Signo en {f_nom} ({col_nom})**: escribiste `${v_u:,.0f}`, pero lleva el signo opuesto (`${v_s:,.0f}`)."
                )
            elif abs(v_u - v_s * 1.19) <= max(tol_pesos, abs(v_s) * 0.02):
                diagnosticos.append(
                    f"⚠️ **Error de IVA en {f_nom} ({col_nom})**: ingresaste el monto **Bruto con IVA** (`${v_u:,.0f}`). Debes dividir por `1,19` para usar el Valor Neto (`${v_s:,.0f}`)."
                )
            elif f_nom == "Flujo Actualizado (VP)" and col_nom != "Año 0":
                t_num = int(str(col_nom).replace("Año ", ""))
                v_mult = float(df_sol.loc["(=) FLUJO CAJA NETO", col_nom]) * ((1.0 + tasa_usada) ** t_num)
                if abs(v_u - v_mult) <= max(5000.0, abs(v_s) * 0.03):
                    diagnosticos.append(
                        f"🚨 **Trampa del Ejercicio 7 en {f_nom} ({col_nom})**: ¡Multiplicaste por `(1+r)^t` en vez de dividir! Para traer a Valor Presente debes dividir: `${v_s:,.0f}`."
                    )
                else:
                    diagnosticos.append(
                        f"❌ Diferencia en **{f_nom} ({col_nom})**: anotaste `${v_u:,.0f}` vs. valor esperado `${v_s:,.0f}`."
                    )
            else:
                diagnosticos.append(
                    f"❌ Diferencia en **{f_nom} ({col_nom})**: anotaste `${v_u:,.0f}` vs. valor esperado `${v_s:,.0f}` (diferencia de `${v_u - v_s:+,.0f}`)."
                )

    c_aud1, c_aud2 = st.columns([1.35, 1.0])
    with c_aud1:
        st.markdown("##### Mapa Visual de Corrección de tu Hoja (Verde = Correcto | Rojo = Revisar)")

        def _colorear_revision(df_in):
            estilos = pd.DataFrame("", index=df_in.index, columns=df_in.columns)
            for r_i, r_name in enumerate(df_in.index):
                es_fila_paso = r_name in paso_obj["filas"]
                for c_i, c_name in enumerate(df_in.columns):
                    ok = celdas_ok[r_i, c_i]
                    val_u = mat_usr[r_i, c_i]
                    val_s = mat_sol[r_i, c_i]
                    if ok:
                        if abs(val_s) > 0 or es_fila_paso:
                            estilos.iloc[r_i, c_i] = "background-color: #dcfce7; color: #166534; font-weight: 600;"
                        else:
                            estilos.iloc[r_i, c_i] = "color: #64748b;"
                    else:
                        if abs(val_u) < 1e-4 and es_fila_paso:
                            estilos.iloc[r_i, c_i] = "background-color: #fef9c3; color: #854d0e; font-weight: 600;"
                        else:
                            estilos.iloc[r_i, c_i] = "background-color: #fee2e2; color: #991b1b; font-weight: 700;"
            return estilos

        st.dataframe(
            df_usuario_edit.style.format("{:,.0f}").apply(_colorear_revision, axis=None),
            use_container_width=True,
            height=380,
        )

    with c_aud2:
        st.markdown(f"##### Retroalimentación en Vivo — Paso {num_paso}")
        if not diagnosticos:
            st.success(f"✅ **¡Excelente!** Todas las celdas del **Paso {num_paso}** están 100% correctas. Puedes avanzar al siguiente paso.")
        else:
            for d_msg in diagnosticos[:8]:
                st.warning(d_msg)
            if len(diagnosticos) > 8:
                st.caption(f"... y {len(diagnosticos) - 8} celdas adicionales pendientes en este paso.")

        st.markdown("---")
        st.markdown("##### Comprobación Final de Indicadores (Tu Cálculo vs. Oficial)")
        p_v1, p_v2 = st.columns(2)
        with p_v1:
            van_usr_in = st.number_input("Escribe tu VAN calculado ($):", value=0.0, step=1000000.0, format="%.0f", key="piz_van_in")
            if abs(van_usr_in - van_sol) <= max(tol_pesos * 10, 5000.0):
                st.success(f"✅ VAN Correcto: `${van_sol:,.0f}`")
            elif van_usr_in != 0.0:
                st.error(f"❌ Revisa: el VAN oficial es `${van_sol:,.0f}`")
        with p_v2:
            tir_usr_in = st.number_input("Escribe tu TIR calculada (%):", value=0.0, step=0.1, format="%.2f", key="piz_tir_in")
            if abs(tir_usr_in - tir_sol * 100.0) <= 0.15:
                st.success(f"✅ TIR Correcta: `{tir_sol*100:.2f}%`")
            elif tir_usr_in != 0.0:
                st.error(f"❌ Revisa: la TIR oficial es `{tir_sol*100:.2f}%`")


# ==============================================================================
# 3. GRÁFICOS INTERACTIVOS PLOTLY PARA FLUJO DE CAJA, SENSIBILIDAD Y MONTE CARLO
# ==============================================================================

def graficar_perfil_van_y_tir(
    flujos_fcl: list,
    flujos_fci: list,
    tasa_fcl: float,
    tasa_ke: float,
    tir_fcl: float,
    tir_fci: float,
):
    tasas_r = np.linspace(0.0, 0.45, 91)
    van_fcl_vec = [
        sum(flujos_fcl[t] / ((1.0 + r) ** t) for t in range(len(flujos_fcl)))
        for r in tasas_r
    ]
    van_fci_vec = [
        sum(flujos_fci[t] / ((1.0 + r) ** t) for t in range(len(flujos_fci)))
        for r in tasas_r
    ]

    van_fcl_actual = sum(flujos_fcl[t] / ((1.0 + tasa_fcl) ** t) for t in range(len(flujos_fcl)))
    van_fci_actual = sum(flujos_fci[t] / ((1.0 + tasa_ke) ** t) for t in range(len(flujos_fci)))

    fig = go.Figure()
    fig.add_hline(y=0, line_dash="dash", line_color="#64748b", annotation_text="Umbral Creación de Valor (VAN = $0)")

    fig.add_trace(
        go.Scatter(
            x=tasas_r * 100.0,
            y=van_fcl_vec,
            mode="lines",
            name="Perfil VAN — Proyecto Puro (FCL)",
            line=dict(color="#1d4ed8", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=tasas_r * 100.0,
            y=van_fci_vec,
            mode="lines",
            name="Perfil VAN — Inversionista Apalancado (FCI)",
            line=dict(color="#059669", width=3, dash="dot"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[tasa_fcl * 100.0],
            y=[van_fcl_actual],
            mode="markers+text",
            text=[f"VAN FCL (${van_fcl_actual/1e6:,.1f}M)"],
            textposition="top right",
            marker=dict(size=12, color="#1d4ed8", line=dict(width=2, color="white")),
            name=f"VAN FCL a {tasa_fcl*100:.2f}%",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[tasa_ke * 100.0],
            y=[van_fci_actual],
            mode="markers+text",
            text=[f"VAN FCI (${van_fci_actual/1e6:,.1f}M)"],
            textposition="bottom right",
            marker=dict(size=12, color="#059669", symbol="diamond", line=dict(width=2, color="white")),
            name=f"VAN FCI a Ke={tasa_ke*100:.2f}%",
        )
    )

    if 0 < tir_fcl <= 0.45:
        fig.add_trace(
            go.Scatter(
                x=[tir_fcl * 100.0],
                y=[0],
                mode="markers+text",
                text=[f"TIR FCL ({tir_fcl*100:.1f}%)"],
                textposition="top center",
                marker=dict(size=11, color="#dc2626", symbol="star"),
                name="TIR Proyecto Puro",
            )
        )

    fig.update_layout(
        title="Perfil del Valor Actual Neto VAN(r): Proyecto Puro (FCL) vs. Inversionista (FCI)",
        xaxis_title="Tasa de Descuento r (%)",
        yaxis_title="Valor Actual Neto — VAN ($ CLP)",
        height=370,
        margin=dict(l=15, r=15, t=45, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="left", x=0),
        plot_bgcolor="#f8fafc",
    )
    return fig


def graficar_cascada_operativa_anual(
    anio_sel: int,
    ing_t: float,
    cv_t: float,
    cf_t: float,
    dep_t: float,
    amo_t: float,
    int_t: float,
    tasa_imp: float,
    am_deuda_t: float,
    resc_t: float,
    es_inversionista: bool = False,
):
    bai = ing_t - cv_t - cf_t - dep_t - amo_t - (int_t if es_inversionista else 0.0)
    imp = max(0.0, bai * tasa_imp) if bai > 0 else bai * tasa_imp
    bdi = bai - imp
    fn = bdi + dep_t + amo_t - (am_deuda_t if es_inversionista else 0.0) + resc_t

    etiquetas = [
        "(+) Ingresos",
        "(-) Costos Var.",
        "(-) Costos Fijos",
        "(-) Deprec. y Amort.",
    ]
    medidas = ["relative", "relative", "relative", "relative"]
    valores = [ing_t, -cv_t, -cf_t, -(dep_t + amo_t)]

    if es_inversionista:
        etiquetas.append("(-) Intereses Deuda")
        medidas.append("relative")
        valores.append(-int_t)

    etiquetas.extend([
        "(=) BAI",
        f"(-) Impuesto ({tasa_imp*100:.1f}%)",
        "(=) BDI",
        "(+) Reverso Dep./Amort.",
    ])
    medidas.extend(["subtotal", "relative", "subtotal", "relative"])
    valores.extend([0, -imp, 0, dep_t + amo_t])

    if es_inversionista and am_deuda_t > 0:
        etiquetas.append("(-) Amort. Préstamo")
        medidas.append("relative")
        valores.append(-am_deuda_t)

    if resc_t > 0:
        etiquetas.append("(+) Rescate + Rec. CT")
        medidas.append("relative")
        valores.append(resc_t)

    etiquetas.append("(=) Flujo Caja Neto")
    medidas.append("total")
    valores.append(0)

    fig = go.Figure(
        go.Waterfall(
            name=f"Año {anio_sel}",
            orientation="v",
            measure=medidas,
            x=etiquetas,
            y=valores,
            text=[f"${v/1e6:+,.1f}M" if m == "relative" else "" for v, m in zip(valores, medidas)],
            textposition="outside",
            connector={"line": {"color": "#64748b"}},
            decreasing={"marker": {"color": "#dc2626"}},
            increasing={"marker": {"color": "#059669"}},
            totals={"marker": {"color": "#1d4ed8"}},
        )
    )
    tipo_txt = "Flujo del Inversionista (FCI)" if es_inversionista else "Flujo de Caja Libre (FCL)"
    fig.update_layout(
        title=f"Anatomía en Cascada del {tipo_txt} — Año {anio_sel} (Flujo Neto = ${fn:,.0f})",
        yaxis_title="Monto ($ CLP)",
        height=370,
        margin=dict(l=15, r=15, t=45, b=20),
        plot_bgcolor="#f8fafc",
    )
    return fig


def graficar_tornado_sensibilidad(
    van_base: float,
    van_ing_bajo: float,
    van_ing_alto: float,
    van_cv_bajo: float,
    van_cv_alto: float,
    van_capex_bajo: float,
    van_capex_alto: float,
    van_tasa_baja: float,
    van_tasa_alta: float,
    titulo_flujo: str = "FCL",
):
    items = [
        ("Ingresos Operacionales (±10%)", van_ing_bajo - van_base, van_ing_alto - van_base),
        ("Inversión Inicial CAPEX (±10%)", van_capex_alto - van_base, van_capex_bajo - van_base),
        ("Costos Variables (±10%)", van_cv_alto - van_base, van_cv_bajo - van_base),
        ("Tasa de Descuento (±10% rel.)", van_tasa_alta - van_base, van_tasa_baja - van_base),
    ]
    items.sort(key=lambda x: abs(x[2] - x[1]))

    nombres = [x[0] for x in items]
    impacto_neg = [x[1] for x in items]
    impacto_pos = [x[2] for x in items]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=nombres,
            x=impacto_neg,
            orientation="h",
            name="Efecto Adverso (-10% / +10% Costo)",
            marker_color="#dc2626",
            text=[f"${v/1e6:+,.1f}M" for v in impacto_neg],
            textposition="auto",
        )
    )
    fig.add_trace(
        go.Bar(
            y=nombres,
            x=impacto_pos,
            orientation="h",
            name="Efecto Favorable (+10% / -10% Costo)",
            marker_color="#059669",
            text=[f"${v/1e6:+,.1f}M" for v in impacto_pos],
            textposition="auto",
        )
    )
    fig.update_layout(
        title=f"Gráfico de Tornado: Sensibilidad del VAN ({titulo_flujo}) respecto al Caso Base (${van_base:,.0f})",
        xaxis_title="Variación del VAN respecto al Caso Base ($ CLP)",
        barmode="relative",
        height=330,
        margin=dict(l=15, r=15, t=45, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="left", x=0),
        plot_bgcolor="#f8fafc",
    )
    return fig


def graficar_montecarlo_avanzado_plotly(
    van_mc: np.ndarray,
    van_prom_mc: float,
    mediana_mc: float,
    var_95_mc: float,
    prob_exito_mc: float,
):
    fig_hist = go.Figure()
    fig_hist.add_trace(
        go.Histogram(
            x=van_mc,
            nbinsx=45,
            marker_color="#2563eb",
            opacity=0.82,
            name="Escenarios Simulados",
        )
    )
    fig_hist.add_vline(
        x=0,
        line_dash="solid",
        line_color="#dc2626",
        line_width=2.5,
        annotation_text="Umbral VAN = $0",
        annotation_position="top left",
    )
    fig_hist.add_vline(
        x=var_95_mc,
        line_dash="dash",
        line_color="#d97706",
        line_width=2.2,
        annotation_text=f"VaR 95% (${var_95_mc/1e6:,.1f}M)",
        annotation_position="bottom left",
    )
    fig_hist.add_vline(
        x=van_prom_mc,
        line_dash="dot",
        line_color="#059669",
        line_width=2.5,
        annotation_text=f"Media (${van_prom_mc/1e6:,.1f}M)",
        annotation_position="top right",
    )
    fig_hist.update_layout(
        title=f"Distribución Estocástica del VAN ({len(van_mc):,} iteraciones | Éxito = {prob_exito_mc:.1f}%)",
        xaxis_title="Valor Actual Neto Simulado ($ CLP)",
        yaxis_title="Frecuencia de Escenarios",
        height=350,
        margin=dict(l=15, r=15, t=45, b=20),
        plot_bgcolor="#f8fafc",
        showlegend=False,
    )

    ord_van = np.sort(van_mc)
    paso = max(1, len(ord_van) // 250)
    x_cdf = ord_van[::paso]
    y_cdf = np.linspace(0, 100, len(x_cdf))

    fig_cdf = go.Figure()
    fig_cdf.add_trace(
        go.Scatter(
            x=x_cdf,
            y=y_cdf,
            mode="lines",
            line=dict(color="#1e3a8a", width=3),
            name="Probabilidad Acumulada (%)",
        )
    )
    fig_cdf.add_vline(x=0, line_dash="dash", line_color="#dc2626", annotation_text="VAN = $0")
    fig_cdf.add_hline(y=5.0, line_dash="dot", line_color="#d97706", annotation_text="Percentil 5% (VaR 95%)")
    fig_cdf.add_hline(y=50.0, line_dash="dot", line_color="#059669", annotation_text=f"Mediana P50 (${mediana_mc/1e6:,.1f}M)")
    fig_cdf.update_layout(
        title="Curva S de Probabilidad Acumulada (Perfil de Riesgo Estocástico)",
        xaxis_title="Valor Actual Neto ($ CLP)",
        yaxis_title="Percentil Acumulado (%)",
        height=350,
        margin=dict(l=15, r=15, t=45, b=20),
        plot_bgcolor="#f8fafc",
        showlegend=False,
    )
    return fig_hist, fig_cdf


# ==============================================================================
# 4. LABORATORIOS INTERACTIVOS DE CÁTEDRA (FISHER, RIESGO Y MARKOWITZ IPSA)
# ==============================================================================

def renderizar_laboratorio_catedra_finanzas():
    inyectar_estilos_burbujas_finanzas()

    st.markdown(
        '<span class="fin-badge">Laboratorio Pedagógico en Vivo — Cátedra Finanzas Avanzadas (Prof.ª Camila Bustos Rosas)</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "Simuladores interactivos de los **3 módulos teóricos y aplicados** de la asignatura: "
        "**1) Modelo Consumo-Inversión y Teorema de Separación de Fisher**, "
        "**2) Actitudes frente al Riesgo, Juego Justo y Equivalente Cierto** y "
        "**3) Taller de Frontera Eficiente de Markowitz (252 días, Dupla 13 IPSA por $65.000.000) y CAPM**."
    )

    tabs_lab = st.tabs([
        "1. Modelo Consumo-Inversión de Fisher (Separación)",
        "2. Actitudes frente al Riesgo y Juego Justo (Von Neumann-Morgenstern)",
        "3. Taller Frontera Eficiente Markowitz ($65M — Dupla 13 IPSA vs. 30 Títulos)",
    ])

    with tabs_lab[0]:
        st.subheader("Modelo Intertemporal Consumo-Inversión y Principio de Separación de Fisher")
        st.markdown(
            "Demuestra gráficamente por qué en un mercado de capitales perfecto la **decisión productiva de la empresa** "
            "($RMgI = r_f$) es objetiva e independiente de las preferencias subjetivas de consumo intertemporal de los accionistas "
            "($TMS = -(1 + r_f)$) (*Fuente: Camila Bustos Rosas, `Consumo - Inversión.pdf`, láminas 2–10; Brealey, Myers y Allen, Cap. 2*)."
        )

        b_f1, b_f2 = st.columns(2)
        with b_f1:
            renderizar_burbuja_tip(
                titulo_boton="Condición de Óptimo Productivo (RMgI = rf)",
                titulo_interno="Paso 1: Decisión Objetiva de los Administradores",
                formula_latex=r"\text{Máx } VAN = -I_0 + \frac{F(I_0)}{1 + r_f} \implies F'(I_0^*) = 1 + r_f \iff RMgI = r_f",
                explicacion_md=(
                    "- La empresa invierte en proyectos físicos reales hasta que la **Rentabilidad Marginal de la Inversión ($RMgI$)** iguala la tasa de interés del mercado de capitales ($r_f$).\n"
                    "- Este punto $P^*$ maximiza la riqueza presente de los accionistas ($W_0^* = Y_0 + VAN$) sin importar si los dueños son impacientes o ahorradores."
                ),
            )
        with b_f2:
            renderizar_burbuja_tip(
                titulo_boton="Condición de Óptimo de Consumo (TMS = -(1+rf))",
                titulo_interno="Paso 2: Decisión Subjetiva en el Mercado de Capitales",
                formula_latex=r"TMS(C_0, C_1) = -\frac{\partial U / \partial C_0}{\partial U / \partial C_1} = -(1 + r_f)",
                explicacion_md=(
                    "- Una vez que la empresa alcanza el óptimo productivo $P^*$, cada accionista se desplaza a lo largo de la **Línea del Mercado de Capitales** prestando o pidiendo prestado a la tasa $r_f$ hasta alcanzar su curva de indiferencia más alta ($C^*$)."
                ),
            )

        cf1, cf2, cf3, cf4 = st.columns(4)
        with cf1:
            dotacion_y0 = st.slider("1. Dotación Inicial Y₀ ($ Millones):", 50.0, 300.0, 120.0, 10.0, key="fsh_y0")
        with cf2:
            tasa_rf_fsh = st.slider("2. Tasa de Interés de Mercado rf (%):", 2.0, 25.0, 10.0, 0.5, key="fsh_rf") / 100.0
        with cf3:
            prod_escala = st.slider("3. Productividad Activos Reales (A):", 15.0, 45.0, 28.0, 1.0, key="fsh_a")
        with cf4:
            impaciencia_alpha = st.slider(
                "4. Preferencia por Consumo Presente α (0,2=Ahorrador | 0,8=Deudor):",
                0.20, 0.85, 0.45, 0.05, key="fsh_alpha",
            )

        i0_opt = min(dotacion_y0, (prod_escala / (2.0 * (1.0 + tasa_rf_fsh))) ** 2)
        c0_prod = dotacion_y0 - i0_opt
        c1_prod = prod_escala * np.sqrt(i0_opt)
        van_fisher = -i0_opt + (c1_prod / (1.0 + tasa_rf_fsh))
        riqueza_total_w0 = dotacion_y0 + van_fisher
        riqueza_futura_w1 = riqueza_total_w0 * (1.0 + tasa_rf_fsh)

        c0_cons = impaciencia_alpha * riqueza_total_w0
        c1_cons = (1.0 - impaciencia_alpha) * riqueza_futura_w1
        flujo_mercado_c0 = c0_cons - c0_prod

        perfil_inv = (
            "Prestatario / Deudor en t=0 (Pide prestado en el mercado financiero para consumir más hoy)"
            if flujo_mercado_c0 > 0.5
            else (
                "Prestamista / Ahorrador en t=0 (Presta excedente en el mercado financiero para consumir más en t=1)"
                if flujo_mercado_c0 < -0.5
                else "Autárquico Financiero (Consume exactamente el flujo productivo)"
            )
        )

        kf1, kf2, kf3, kf4 = st.columns(4)
        kf1.metric("Inversión Física Óptima (I₀*)", f"${i0_opt:,.2f}M", f"C₀ Prod. = ${c0_prod:,.2f}M")
        kf2.metric("VAN Productivo Generado", f"${van_fisher:,.2f}M", f"Riqueza W₀* = ${riqueza_total_w0:,.2f}M")
        kf3.metric("Consumo Óptimo (C₀*, C₁*)", f"${c0_cons:,.1f}M | ${c1_cons:,.1f}M")
        kf4.metric(
            "Posición en Mercado Capitales",
            f"${abs(flujo_mercado_c0):,.2f}M",
            "Se endeuda hoy" if flujo_mercado_c0 > 0 else "Presta / Ahorra hoy",
        )

        st.info(f"**Diagnóstico de Cátedra:** {perfil_inv}.")

        i_grid = np.linspace(0.0, dotacion_y0, 120)
        c0_frontera = dotacion_y0 - i_grid
        c1_frontera = prod_escala * np.sqrt(i_grid)

        c0_recta = np.linspace(0.0, riqueza_total_w0, 100)
        c1_recta = riqueza_futura_w1 - (1.0 + tasa_rf_fsh) * c0_recta

        u_star = (max(c0_cons, 1e-4) ** impaciencia_alpha) * (max(c1_cons, 1e-4) ** (1.0 - impaciencia_alpha))
        c0_indif = np.linspace(max(5.0, c0_cons * 0.35), min(riqueza_total_w0 * 1.15, c0_cons * 1.85), 120)
        c1_indif = (u_star / (c0_indif ** impaciencia_alpha)) ** (1.0 / (1.0 - impaciencia_alpha))
        mask_indif = c1_indif <= riqueza_futura_w1 * 1.35

        fig_fsh = go.Figure()
        fig_fsh.add_trace(
            go.Scatter(
                x=c0_frontera,
                y=c1_frontera,
                mode="lines",
                name="Frontera Productiva de la Empresa",
                line=dict(color="#1d4ed8", width=3.5),
            )
        )
        fig_fsh.add_trace(
            go.Scatter(
                x=c0_recta,
                y=c1_recta,
                mode="lines",
                name=f"Línea Mercado de Capitales (pendiente = -(1+{tasa_rf_fsh*100:.1f}%))",
                line=dict(color="#dc2626", width=2.5, dash="dash"),
            )
        )
        fig_fsh.add_trace(
            go.Scatter(
                x=c0_indif[mask_indif],
                y=c1_indif[mask_indif],
                mode="lines",
                name="Curva de Indiferencia Accionista U*(C₀, C₁)",
                line=dict(color="#059669", width=3),
            )
        )
        fig_fsh.add_trace(
            go.Scatter(
                x=[dotacion_y0, riqueza_total_w0],
                y=[0, 0],
                mode="markers+text",
                text=[f"Y₀ (${dotacion_y0:.0f}M)", f"W₀* = Y₀+VAN (${riqueza_total_w0:.1f}M)"],
                textposition=["top left", "top right"],
                marker=dict(size=10, color="#0f172a"),
                name="Dotación vs. Riqueza Máxima",
            )
        )
        fig_fsh.add_trace(
            go.Scatter(
                x=[c0_prod],
                y=[c1_prod],
                mode="markers+text",
                text=["P* Óptimo Productivo (RMgI = rf)"],
                textposition="bottom left",
                marker=dict(size=13, color="#1d4ed8", symbol="diamond", line=dict(width=2, color="white")),
                name="P* (Óptimo Productivo)",
            )
        )
        fig_fsh.add_trace(
            go.Scatter(
                x=[c0_cons],
                y=[c1_cons],
                mode="markers+text",
                text=["C* Óptimo Consumo (TMS = -(1+rf))"],
                textposition="top right",
                marker=dict(size=14, color="#059669", symbol="star", line=dict(width=2, color="white")),
                name="C* (Óptimo Consumo)",
            )
        )
        fig_fsh.update_layout(
            title="Equilibrio de Separación de Fisher: Óptimo Productivo (P*) vs. Óptimo de Consumo (C*)",
            xaxis_title="Consumo Presente C₀ ($ Millones en t=0)",
            yaxis_title="Consumo Futuro C₁ ($ Millones en t=1)",
            height=450,
            margin=dict(l=15, r=15, t=45, b=20),
            plot_bgcolor="#f8fafc",
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="left", x=0),
        )
        st.plotly_chart(fig_fsh, use_container_width=True)

    with tabs_lab[1]:
        st.subheader("Actitudes frente al Riesgo, Juego Justo y Prima por Riesgo (`Relación riesgo rentabilidad.pdf`)")
        st.markdown(
            "Modela la función de utilidad de la riqueza $U(W)$, contrastando el **Valor Esperado de la Riqueza $E(W)$**, "
            "el **Equivalente Cierto ($EC$)** y la **Prima por Riesgo ($\pi = E(W) - EC$)** para inversionistas "
            "**Aversos al Riesgo**, **Neutrales** y **Amantes del Riesgo** (*Láminas 7–21*)."
        )

        cr1, cr2, cr3, cr4 = st.columns(4)
        with cr1:
            actitud_sel = st.selectbox(
                "Actitud frente al Riesgo:",
                [
                    "Averso al Riesgo (U''(W) < 0 — Cóncava)",
                    "Neutral al Riesgo (U''(W) = 0 — Lineal)",
                    "Propenso / Amante del Riesgo (U''(W) > 0 — Convexa)",
                ],
                key="rsk_act",
            )
        with cr2:
            w_malo = st.number_input("Riqueza Escenario Desfavorable W₁ ($M):", min_value=5.0, max_value=500.0, value=40.0, step=5.0, key="rsk_w1")
        with cr3:
            w_bueno = st.number_input("Riqueza Escenario Favorable W₂ ($M):", min_value=10.0, max_value=1000.0, value=160.0, step=10.0, key="rsk_w2")
        with cr4:
            prob_exito_lot = st.slider("Probabilidad Escenario Favorable p (%):", 5, 95, 50, 5, key="rsk_p") / 100.0

        w_seguro_ref = st.slider(
            "Riqueza Segura Actual si rechaza el juego W₀ ($M) [Para evaluar si es un 'Juego Justo']:",
            min_value=float(w_malo),
            max_value=float(w_bueno),
            value=float(prob_exito_lot * w_bueno + (1.0 - prob_exito_lot) * w_malo),
            step=1.0,
            key="rsk_w0",
        )

        if "Averso" in actitud_sel:
            gamma_u = 0.35
        elif "Neutral" in actitud_sel:
            gamma_u = 1.00
        else:
            gamma_u = 1.85

        def fn_u(w):
            return np.power(np.maximum(w, 1e-6), gamma_u)

        def fn_u_inv(u_val):
            return np.power(np.maximum(u_val, 1e-6), 1.0 / gamma_u)

        ew = (1.0 - prob_exito_lot) * w_malo + prob_exito_lot * w_bueno
        u_w1 = float(fn_u(w_malo))
        u_w2 = float(fn_u(w_bueno))
        eu_w = (1.0 - prob_exito_lot) * u_w1 + prob_exito_lot * u_w2
        u_ew = float(fn_u(ew))
        ec_val = float(fn_u_inv(eu_w))
        prima_riesgo = ew - ec_val
        es_juego_justo = abs(ew - w_seguro_ref) < 0.01

        kr1, kr2, kr3, kr4 = st.columns(4)
        kr1.metric("Valor Esperado Riqueza E(W)", f"${ew:,.2f}M", "Juego Justo (E(W)=W₀)" if es_juego_justo else f"E(W) - W₀ = ${ew - w_seguro_ref:+,.2f}M")
        kr2.metric("Equivalente Cierto (EC)", f"${ec_val:,.2f}M", "Riqueza segura de igual utilidad")
        kr3.metric("Prima por Riesgo (π = E(W) - EC)", f"${prima_riesgo:+,.2f}M", "Positiva en aversión al riesgo" if prima_riesgo > 0.01 else ("Cero (Neutral)" if abs(prima_riesgo) <= 0.01 else "Negativa (Propenso)"))
        kr4.metric(
            "Decisión Racional del Individuo",
            "ACEPTA EL JUEGO" if eu_w > fn_u(w_seguro_ref) + 1e-5 else ("INDIFERENTE" if abs(eu_w - fn_u(w_seguro_ref)) <= 1e-5 else "RECHAZA (Prefiere W₀)"),
            f"U(E(W))={u_ew:.2f} vs E[U(W)]={eu_w:.2f}",
        )

        w_vec = np.linspace(max(1.0, w_malo * 0.7), w_bueno * 1.1, 120)
        u_vec = fn_u(w_vec)

        fig_u = go.Figure()
        fig_u.add_trace(
            go.Scatter(
                x=w_vec,
                y=u_vec,
                mode="lines",
                name=f"Función de Utilidad U(W) = W^{gamma_u:.2f}",
                line=dict(color="#1d4ed8", width=3.5),
            )
        )
        fig_u.add_trace(
            go.Scatter(
                x=[w_malo, w_bueno],
                y=[u_w1, u_w2],
                mode="lines+markers",
                name="Cuerda de Lotería (Combinaciones E[U(W)])",
                line=dict(color="#64748b", width=2, dash="dash"),
                marker=dict(size=9, color="#0f172a"),
            )
        )
        fig_u.add_trace(
            go.Scatter(
                x=[ew, ew],
                y=[eu_w, u_ew],
                mode="lines+markers",
                name="Brecha U(E(W)) vs. E[U(W)]",
                line=dict(color="#dc2626", width=3),
                marker=dict(size=10, color="#dc2626"),
            )
        )
        fig_u.add_trace(
            go.Scatter(
                x=[ec_val, ew],
                y=[eu_w, eu_w],
                mode="lines+markers+text",
                text=[f"EC = ${ec_val:.1f}M", f"E(W) = ${ew:.1f}M"],
                textposition=["top left", "bottom right"],
                name=f"Prima por Riesgo π = ${prima_riesgo:.2f}M",
                line=dict(color="#059669", width=3.5),
                marker=dict(size=11, color="#059669", symbol="diamond"),
            )
        )
        fig_u.update_layout(
            title="Curva de Utilidad de Von Neumann-Morgenstern: Equivalente Cierto (EC) y Prima por Riesgo (π)",
            xaxis_title="Nivel de Riqueza W ($ Millones)",
            yaxis_title="Utilidad de la Riqueza U(W)",
            height=410,
            margin=dict(l=15, r=15, t=45, b=20),
            plot_bgcolor="#f8fafc",
            legend=dict(orientation="h", yanchor="bottom", y=-0.26, xanchor="left", x=0),
        )
        st.plotly_chart(fig_u, use_container_width=True)

    with tabs_lab[2]:
        st.subheader("Taller de Frontera Eficiente de Markowitz (252 días bursátiles) y CAPM — Dupla 13 IPSA")
        st.markdown(
            "Simulador calibrado con los parámetros oficiales del **Taller de Frontera Eficiente de Ingeniería Comercial ULagos**: "
            "inversión de **$65.000.000 CLP**, comparación entre **5 acciones del IPSA (Dupla 13: Parque Arauco, Andina-B, Cenco Malls, Banco de Chile y Vapores)** "
            "y una cartera ampliada de **30 acciones del IPSA**, utilizando la tasa libre de riesgo de los bonos **BCP/BTP a 5 años del Banco Central de Chile**."
        )

        bm1, bm2 = st.columns(2)
        with bm1:
            renderizar_burbuja_tip(
                titulo_boton="Anualización Bursátil (252 días) y Varianza de Cartera",
                titulo_interno="Ecuaciones del Taller de Markowitz (`Teoría de mercado de capitales.pdf`)",
                formula_latex=r"E(R_p) = \sum_{i=1}^n w_i E(R_i) \quad ; \quad \sigma_p = \sqrt{w^T \Sigma w} \quad ; \quad \sigma_{anual} = \sigma_{diaria}\sqrt{252}",
                explicacion_md=(
                    "- Siempre que el coeficiente de correlación entre los activos sea menor a $+1$ ($\rho_{ij} < 1$), el riesgo del portafolio es **estrictamente menor** al promedio ponderado de los riesgos individuales (**Efecto Diversificación**).\n"
                    "- Al pasar de **5 acciones a 30 acciones del IPSA**, se elimina casi por completo el **riesgo no sistemático (diversificable)**, permaneciendo únicamente el **riesgo sistemático de mercado ($\beta$)**."
                ),
            )
        with bm2:
            renderizar_burbuja_tip(
                titulo_boton="Portafolio Tangente (Sharpe) y Línea del Mercado (CML)",
                titulo_interno="Ratio de Sharpe y Separación de Tobin",
                formula_latex=r"\text{Máx } S_p = \frac{E(R_p) - R_f}{\sigma_p} \quad \text{s.a. } \sum_{i=1}^5 w_i = 1,\; w_i \ge 0",
                explicacion_md=(
                    "- El **Portafolio de Mínima Varianza Global (GMVP)** minimiza la volatilidad total $\sigma_p$.\n"
                    "- El **Portafolio Óptimo / Tangente** maximiza el **Ratio de Sharpe** (premio por unidad de riesgo total) al trazar la recta tangente desde la tasa libre de riesgo $R_f$ (BCP/BTP 5 años del Banco Central)."
                ),
            )

        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            monto_taller = st.number_input(
                "Capital Total a Invertir en Cartera ($ CLP):",
                min_value=1000000.0,
                max_value=1000000000.0,
                value=65000000.0,
                step=5000000.0,
                format="%.0f",
                key="mk_cap",
            )
        with cm2:
            rf_bcentral = st.number_input(
                "Tasa Libre de Riesgo Anual Rf (BCP/BTP 5 años BCCh %):",
                min_value=1.0,
                max_value=15.0,
                value=5.65,
                step=0.10,
                key="mk_rf",
            ) / 100.0
        with cm3:
            permitir_cortos = st.checkbox("Permitir ventas cortas (pesos negativos w_i < 0)", value=False, key="mk_short")

        activos_dupla13 = [
            "PARAUCO (Parque Arauco)",
            "ANDINA-B (Emb. Andina)",
            "CENCOMALLS (Cenco Malls)",
            "CHILE (Banco de Chile)",
            "VAPORES (CSAV)",
        ]
        df_activos_init = pd.DataFrame({
            "Nemotécnico IPSA (Dupla 13)": activos_dupla13,
            "Retorno Diario Promedio (%)": [0.058, 0.049, 0.054, 0.062, 0.071],
            "Volatilidad Diaria σ_d (%)": [1.42, 1.28, 1.36, 1.18, 2.05],
            "Beta de Mercado (β_i)": [1.08, 0.86, 1.02, 0.92, 1.38],
        })

        st.caption("Parámetros bursátiles de las 5 acciones del IPSA (Dupla 13 — editables en vivo):")
        df_act_ed = st.data_editor(df_activos_init, use_container_width=True, hide_index=True, key="mk_ed_dupla13")

        ret_d = df_act_ed["Retorno Diario Promedio (%)"].to_numpy(dtype=float) / 100.0
        vol_d = df_act_ed["Volatilidad Diaria σ_d (%)"].to_numpy(dtype=float) / 100.0
        betas_i = df_act_ed["Beta de Mercado (β_i)"].to_numpy(dtype=float)

        ret_anual = (1.0 + ret_d) ** 252 - 1.0
        vol_anual = vol_d * np.sqrt(252.0)

        corr_matrix = np.array([
            [1.00, 0.38, 0.68, 0.42, 0.24],
            [0.38, 1.00, 0.35, 0.40, 0.22],
            [0.68, 0.35, 1.00, 0.44, 0.25],
            [0.42, 0.40, 0.44, 1.00, 0.30],
            [0.24, 0.22, 0.25, 0.30, 1.00],
        ])
        cov_anual = np.outer(vol_anual, vol_anual) * corr_matrix
        n_act = len(activos_dupla13)

        bounds_mk = [(-0.5, 1.5) if permitir_cortos else (0.0, 1.0) for _ in range(n_act)]
        restriccion_suma = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
        w_init = np.ones(n_act) / n_act

        res_gmvp = minimize(
            lambda w: float(np.sqrt(np.dot(w.T, np.dot(cov_anual, w)))),
            w_init,
            method="SLSQP",
            bounds=bounds_mk,
            constraints=[restriccion_suma],
        )
        w_gmvp = res_gmvp.x if res_gmvp.success else w_init
        ret_gmvp = float(np.dot(w_gmvp, ret_anual))
        vol_gmvp = float(np.sqrt(np.dot(w_gmvp.T, np.dot(cov_anual, w_gmvp))))
        sharpe_gmvp = (ret_gmvp - rf_bcentral) / max(vol_gmvp, 1e-6)

        def neg_sharpe(w):
            r_p = float(np.dot(w, ret_anual))
            v_p = float(np.sqrt(np.dot(w.T, np.dot(cov_anual, w))))
            return -(r_p - rf_bcentral) / max(v_p, 1e-6)

        res_tan = minimize(
            neg_sharpe,
            w_init,
            method="SLSQP",
            bounds=bounds_mk,
            constraints=[restriccion_suma],
        )
        w_tan = res_tan.x if res_tan.success else w_init
        ret_tan = float(np.dot(w_tan, ret_anual))
        vol_tan = float(np.sqrt(np.dot(w_tan.T, np.dot(cov_anual, w_tan))))
        sharpe_tan = (ret_tan - rf_bcentral) / max(vol_tan, 1e-6)

        w_eq = w_init
        ret_eq = float(np.dot(w_eq, ret_anual))
        vol_eq = float(np.sqrt(np.dot(w_eq.T, np.dot(cov_anual, w_eq))))
        sharpe_eq = (ret_eq - rf_bcentral) / max(vol_eq, 1e-6)

        km1, km2, km3, km4 = st.columns(4)
        km1.metric("Portafolio Mín. Varianza (GMVP)", f"σ = {vol_gmvp*100:.2f}%", f"E(R) = {ret_gmvp*100:.2f}% | Sharpe = {sharpe_gmvp:.2f}")
        km2.metric("Portafolio Óptimo Tangente", f"E(R) = {ret_tan*100:.2f}%", f"σ = {vol_tan*100:.2f}% | Sharpe = {sharpe_tan:.2f}")
        km3.metric("Cartera Equiponderada (20% c/u)", f"E(R) = {ret_eq*100:.2f}%", f"σ = {vol_eq*100:.2f}% | Sharpe = {sharpe_eq:.2f}")
        km4.metric("Capital Asignado (100%)", f"${monto_taller:,.0f}", "Dupla 13 — 5 acciones IPSA")

        np.random.seed(13)
        pesos_mc = np.random.dirichlet(np.ones(n_act), size=1200)
        rets_nube = pesos_mc @ ret_anual
        vols_nube = np.sqrt(np.einsum("ij,jk,ik->i", pesos_mc, cov_anual, pesos_mc))
        sharpes_nube = (rets_nube - rf_bcentral) / np.maximum(vols_nube, 1e-6)

        targets_r = np.linspace(ret_gmvp, float(np.max(ret_anual)), 38)
        front_vols, front_rets = [], []
        for r_obj in targets_r:
            cons_f = [
                restriccion_suma,
                {"type": "eq", "fun": lambda w, r_t=r_obj: float(np.dot(w, ret_anual)) - r_t},
            ]
            res_f = minimize(
                lambda w: float(np.sqrt(np.dot(w.T, np.dot(cov_anual, w)))),
                w_init,
                method="SLSQP",
                bounds=bounds_mk,
                constraints=cons_f,
            )
            if res_f.success:
                front_vols.append(float(res_f.fun))
                front_rets.append(float(r_obj))

        col_mk_g1, col_mk_g2 = st.columns([1.35, 1.0])
        with col_mk_g1:
            fig_mk = go.Figure()
            fig_mk.add_trace(
                go.Scatter(
                    x=vols_nube * 100.0,
                    y=rets_nube * 100.0,
                    mode="markers",
                    marker=dict(
                        size=5,
                        color=sharpes_nube,
                        colorscale="Blues",
                        showscale=True,
                        colorbar=dict(title="Sharpe"),
                        opacity=0.55,
                    ),
                    name="Portafolios Factibles (5 Activos)",
                )
            )
            fig_mk.add_trace(
                go.Scatter(
                    x=np.array(front_vols) * 100.0,
                    y=np.array(front_rets) * 100.0,
                    mode="lines",
                    line=dict(color="#1d4ed8", width=3.5),
                    name="Frontera Eficiente (5 Títulos IPSA)",
                )
            )
            fig_mk.add_trace(
                go.Scatter(
                    x=np.array(front_vols) * 100.0 * 0.84,
                    y=np.array(front_rets) * 100.0 * 1.03,
                    mode="lines",
                    line=dict(color="#7c3aed", width=2.5, dash="dot"),
                    name="Frontera Eficiente Referencial (30 Títulos IPSA)",
                )
            )
            sigma_cml = np.linspace(0.0, max(vol_anual) * 1.05, 50)
            ret_cml = rf_bcentral + sharpe_tan * sigma_cml
            fig_mk.add_trace(
                go.Scatter(
                    x=sigma_cml * 100.0,
                    y=ret_cml * 100.0,
                    mode="lines",
                    line=dict(color="#d97706", width=2.5, dash="dash"),
                    name="Línea Mercado Capitales (CML)",
                )
            )
            fig_mk.add_trace(
                go.Scatter(
                    x=vol_anual * 100.0,
                    y=ret_anual * 100.0,
                    mode="markers+text",
                    text=[a.split(" ")[0] for a in activos_dupla13],
                    textposition="top center",
                    marker=dict(size=10, color="#0f172a", symbol="circle"),
                    name="Acciones Individuales (Dupla 13)",
                )
            )
            fig_mk.add_trace(
                go.Scatter(
                    x=[vol_gmvp * 100.0],
                    y=[ret_gmvp * 100.0],
                    mode="markers+text",
                    text=["GMVP (Mín. Riesgo)"],
                    textposition="bottom left",
                    marker=dict(size=13, color="#059669", symbol="diamond", line=dict(width=2, color="white")),
                    name="GMVP (Mínima Varianza)",
                )
            )
            fig_mk.add_trace(
                go.Scatter(
                    x=[vol_tan * 100.0],
                    y=[ret_tan * 100.0],
                    mode="markers+text",
                    text=[f"Portafolio Tangente (Sharpe={sharpe_tan:.2f})"],
                    textposition="top left",
                    marker=dict(size=15, color="#dc2626", symbol="star", line=dict(width=2, color="white")),
                    name="Portafolio Tangente (Máx. Sharpe)",
                )
            )
            fig_mk.update_layout(
                title="Frontera Eficiente de Markowitz (5 vs. 30 Acciones IPSA) y Línea del Mercado de Capitales (CML)",
                xaxis_title="Riesgo Anualizado — Desviación Estándar σ_p (%)",
                yaxis_title="Retorno Esperado Anualizado E(R_p) (%)",
                height=440,
                margin=dict(l=15, r=15, t=45, b=20),
                plot_bgcolor="#f8fafc",
                legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="left", x=0),
            )
            st.plotly_chart(fig_mk, use_container_width=True)

        with col_mk_g2:
            st.markdown(f"##### Asignación Exacta de los ${monto_taller:,.0f} (Dupla 13)")
            df_pesos = pd.DataFrame({
                "Acción IPSA": [a.split(" ")[0] for a in activos_dupla13],
                "E(R) Anual (%)": np.round(ret_anual * 100.0, 2),
                "σ Anual (%)": np.round(vol_anual * 100.0, 2),
                "Peso GMVP (%)": np.round(w_gmvp * 100.0, 2),
                "Monto GMVP ($)": np.round(w_gmvp * monto_taller, 0),
                "Peso Tangente (%)": np.round(w_tan * 100.0, 2),
                "Monto Tangente ($)": np.round(w_tan * monto_taller, 0),
            })
            st.dataframe(
                df_pesos.style.format({
                    "E(R) Anual (%)": "{:.2f}%",
                    "σ Anual (%)": "{:.2f}%",
                    "Peso GMVP (%)": "{:.2f}%",
                    "Monto GMVP ($)": "${:,.0f}",
                    "Peso Tangente (%)": "{:.2f}%",
                    "Monto Tangente ($)": "${:,.0f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

            rm_ipsa = float(np.mean(ret_anual))
            beta_grid = np.linspace(0.0, 1.6, 50)
            sml_ret = rf_bcentral + beta_grid * (rm_ipsa - rf_bcentral)

            fig_sml = go.Figure()
            fig_sml.add_trace(
                go.Scatter(
                    x=beta_grid,
                    y=sml_ret * 100.0,
                    mode="lines",
                    name="Línea SML (Equilibrio CAPM)",
                    line=dict(color="#1d4ed8", width=3),
                )
            )
            fig_sml.add_trace(
                go.Scatter(
                    x=betas_i,
                    y=ret_anual * 100.0,
                    mode="markers+text",
                    text=[a.split(" ")[0] for a in activos_dupla13],
                    textposition="top center",
                    marker=dict(size=10, color="#dc2626"),
                    name="Retorno Observado vs. Beta",
                )
            )
            fig_sml.update_layout(
                title="Línea del Mercado de Títulos (SML / CAPM): Riesgo Sistemático (β)",
                xaxis_title="Beta del Activo (β_i)",
                yaxis_title="Retorno Exigido / Esperado (%)",
                height=225,
                margin=dict(l=10, r=10, t=35, b=10),
                plot_bgcolor="#f8fafc",
                showlegend=False,
            )
            st.plotly_chart(fig_sml, use_container_width=True)
