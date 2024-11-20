import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Archivos de datos
file_path = "base_datos_productos.xlsx"
ventas_file = "ventas.xlsx"

# Función para cargar datos de productos
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        if 'Ventas' not in df.columns:
            df['Ventas'] = 0  # Inicializar columna de ventas acumuladas si no existe
        return df
    except FileNotFoundError:
        st.error("El archivo de base de datos no fue encontrado.")
        return pd.DataFrame()

# Función para guardar datos
def save_data(df, file_path):
    try:
        df.to_excel(file_path, index=False)
        st.success("Datos guardados correctamente.")
    except PermissionError:
        st.error("No se pudo guardar el archivo. Verifica que no esté abierto o revisa los permisos.")

# Función para cargar datos de ventas
def load_ventas():
    if os.path.exists(ventas_file):
        return pd.read_excel(ventas_file)
    else:
        return pd.DataFrame(columns=['Fecha', 'CODIGO', 'Cantidad', 'Canal'])

# Función para guardar ventas
def save_ventas(ventas_df):
    try:
        ventas_df.to_excel(ventas_file, index=False)
        st.success("Ventas guardadas correctamente en 'ventas.xlsx'.")
    except Exception as e:
        st.error(f"No se pudo guardar las ventas: {e}")

# Cargar datos iniciales
df = load_data(file_path)  # Datos de productos
ventas_acumuladas = load_ventas()  # Datos de ventas

# Verificar si la base de datos está vacía
if df.empty:
    st.warning("La base de datos de productos está vacía o no se pudo cargar.")

#pagina de incio
def pagina_inicio():
    # CSS para diseño visual
    st.markdown("""
    <style>
    .centered {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-top: 20px;
    }
    .brand-name {
        font-size: 3rem; /* Tamaño del nombre de la marca */
        font-weight: bold;
        color: #495057; /* Color del texto principal */
        margin-bottom: 10px;
    }
    .slogan {
        font-size: 1.8rem; /* Tamaño del slogan */
        font-weight: lighter;
        color: #6c757d;
        margin-bottom: 30px;
    }
    .gallery {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 30px;
    }
    .gallery img {
        width: 150px;
        height: 150px;
        object-fit: cover;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Marca y Slogan
    st.markdown("""
    <div class="centered">
        <div class="brand-name">MALA</div>
        <div class="slogan">Effortless Wear</div>
        <p style="font-size: 1.2rem; color: #6c757d;">"made and inspired by modern women"</p>
    </div>
    """, unsafe_allow_html=True)

    # Galería de Fotos
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("foto1.jpg", caption=None, use_column_width=True)
    with col2:
        st.image("foto2.jpg", caption=None, use_column_width=True)
    with col3:
        st.image("foto3.jpg", caption=None, use_column_width=True)

    # Separador visual
    st.markdown("---")

    # Texto motivador
    st.markdown("""
    <div class="centered">
        <h2 style="color: #495057;">Explora nuestras herramientas</h2>
        <p>Registra tus ventas, gestiona inventarios y analiza tus estadísticas con estilo.</p>
    </div>
    """, unsafe_allow_html=True)

def pagina_catalogo():
    st.title("📋 Catálogo de Productos")
    st.markdown("Aquí puedes visualizar y buscar tus productos.")
    if df.empty:
        st.error("La base de datos de productos está vacía.")
    else:
        st.dataframe(df)
        buscador = st.text_input("Buscar producto por código o descripción")
        if buscador:
            resultados = df[df['CODIGO'].str.contains(buscador, na=False, case=False) |
                            df['Familia'].str.contains(buscador, na=False, case=False)]
            st.dataframe(resultados)

# Página de gestión de inventario
def pagina_gestion_inventario():
    st.title("📦 Gestión de Inventario")
    st.markdown("Añade o quita inventario de tus productos.")
    if df.empty:
        st.error("La base de datos de productos está vacía.")
        return

    # Filtros y selección
    familia = st.selectbox("Selecciona Familia", options=["Todos"] + list(df['Familia'].unique()))
    color = st.selectbox("Selecciona Color", options=["Todos"] + list(df['Color'].unique()))
    talla = st.selectbox("Selecciona Talla", options=["Todos"] + list(df['Talla'].unique()))

    # Filtrar productos
    productos_filtrados = df.copy()
    if familia != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Familia'] == familia]
    if color != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Color'] == color]
    if talla != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Talla'] == talla]

    producto_seleccionado = st.selectbox("Selecciona Producto", options=productos_filtrados['CODIGO'])

    # Actualizar inventario
    with st.form("form_inventario"):
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        operacion = st.selectbox("Operación", ["Añadir", "Quitar"])
        submit = st.form_submit_button("Actualizar Inventario")

    if submit:
        if producto_seleccionado in df['CODIGO'].values:
            idx = df[df['CODIGO'] == producto_seleccionado].index[0]
            if operacion == "Añadir":
                df.loc[idx, 'Inventario'] += cantidad
                st.success(f"Se añadieron {cantidad} unidades a {producto_seleccionado}.")
            elif operacion == "Quitar" and df.loc[idx, 'Inventario'] >= cantidad:
                df.loc[idx, 'Inventario'] -= cantidad
                st.success(f"Se quitaron {cantidad} unidades de {producto_seleccionado}.")
            save_data(df, file_path)

# Página de registro de ventas
def pagina_registro_ventas():
    st.title("🛒 Registro de Ventas")
    st.markdown("Registra las ventas de tus productos aquí.")
    
    # Filtros
    familia = st.selectbox("Selecciona Familia", options=["Todos"] + list(df['Familia'].unique()))
    color = st.selectbox("Selecciona Color", options=["Todos"] + list(df['Color'].unique()))
    talla = st.selectbox("Selecciona Talla", options=["Todos"] + list(df['Talla'].unique()))

    # Filtrar productos
    productos_filtrados = df.copy()
    if familia != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Familia'] == familia]
    if color != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Color'] == color]
    if talla != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Talla'] == talla]

    producto_seleccionado = st.selectbox("Selecciona Producto", options=productos_filtrados['CODIGO'])

    # Mostrar detalles del producto seleccionado
    if not productos_filtrados.empty:
        producto_info = productos_filtrados[productos_filtrados['CODIGO'] == producto_seleccionado]
        st.write("Detalles del Producto:")
        st.table(producto_info[['CODIGO', 'Familia', 'Color', 'Talla', 'Inventario', 'Precio']])

    # Formulario para registrar venta
    with st.form("form_ventas"):
        cantidad = st.number_input("Cantidad Vendida", min_value=1, step=1)
        canal = st.selectbox("Canal de Venta", ["Whatsapp", "Instagram", "Showroom", "Shopify", "Puntos de Venta"])
        submit = st.form_submit_button("Registrar Venta")

        # Este bloque debe estar correctamente indentado
        if submit:
            if producto_seleccionado in df['CODIGO'].values:
                idx = df[df['CODIGO'] == producto_seleccionado].index[0]
                if df.loc[idx, 'Inventario'] >= cantidad:
                    # Actualizar inventario y registrar venta
                    df.loc[idx, 'Inventario'] -= cantidad
                    df.loc[idx, 'Ventas'] += cantidad

                    nueva_venta = pd.DataFrame({
                        'Fecha': [pd.Timestamp.now()],
                        'CODIGO': [producto_seleccionado],
                        'Cantidad': [cantidad],
                        'Canal': [canal]
                    })
                    ventas_acumuladas = pd.concat([ventas_acumuladas, nueva_venta], ignore_index=True)
                    save_data(df, file_path)
                    save_ventas(ventas_acumuladas)
                    st.success(f"Venta registrada: {cantidad} unidades de {producto_seleccionado} por {canal}.")
                else:
                    st.error(f"No hay suficiente inventario para vender {cantidad} unidades de {producto_seleccionado}.")
            else:
                st.error("El producto seleccionado no existe en la base de datos.")


# Página de estadísticas
def pagina_estadisticas():
    global ventas_acumuladas
    st.title("📊 Estadísticas")
    st.markdown("Analiza tus datos de forma **intuitiva y visual**.")

    if not ventas_acumuladas.empty:
        # Calcular métricas principales
        total_ventas = ventas_acumuladas['Cantidad'].sum()
        ventas_con_info = ventas_acumuladas.merge(df, on="CODIGO", how="left")

        # Calcular utilidad y margen
        ventas_con_info['Utilidad'] = (ventas_con_info['Precio'] - ventas_con_info['costo']) * ventas_con_info['Cantidad']
        total_utilidad = ventas_con_info['Utilidad'].sum()
        margen_utilidad = (total_utilidad / (ventas_con_info['Precio'] * ventas_con_info['Cantidad']).sum()) * 100

        # Producto más vendido
        producto_mas_vendido = ventas_con_info.groupby('Familia')['Cantidad'].sum().idxmax()

        # Talla más vendida
        talla_mas_vendida = ventas_con_info.groupby('Talla')['Cantidad'].sum().idxmax()

        # Color más vendido
        color_mas_vendido = ventas_con_info.groupby('Color')['Cantidad'].sum().idxmax()

        # CSS mejorado para cuadros métricos
        st.markdown("""
        <style>
        .metric-box {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 120px;
            margin-bottom: 20px;
        }
        .metric-box h4 {
            font-size: 1.2rem;
            margin: 0;
        }
        .metric-box h2 {
            font-size: 2.2rem;
            margin: 0;
            color: #495057;
            word-wrap: break-word;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

        # Crear cuadros métricos
        st.markdown("### **Resumen de Ventas**")
        col1, col2, col3 = st.columns([1, 1, 1], gap="large")
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <h4>Piezas Vendidas</h4>
                <h2>{total_ventas}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <h4>Utilidad Total</h4>
                <h2>${total_utilidad:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-box">
                <h4>Margen de Utilidad</h4>
                <h2>{margen_utilidad:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)

        col4, col5, col6 = st.columns([1, 1, 1], gap="large")
        with col4:
            st.markdown(f"""
            <div class="metric-box">
                <h4>Producto Más Vendido</h4>
                <h2>{producto_mas_vendido}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
            <div class="metric-box">
                <h4>Talla Más Vendida</h4>
                <h2>{talla_mas_vendida}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col6:
            st.markdown(f"""
            <div class="metric-box">
                <h4>Color Más Vendido</h4>
                <h2>{color_mas_vendido}</h2>
            </div>
            """, unsafe_allow_html=True)

        # Gráfico de ventas diarias
        st.markdown("### **Ventas Diarias**")
        ventas_acumuladas['Fecha'] = pd.to_datetime(ventas_acumuladas['Fecha'])
        ventas_diarias = ventas_acumuladas.groupby(ventas_acumuladas['Fecha'].dt.date)['Cantidad'].sum()
        
        if len(ventas_diarias) > 1:  # Más de un dato para graficar
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            ventas_diarias.plot(kind='line', ax=ax1, marker='o', color='#6c757d')
            ax1.set_title("Ventas Diarias", fontsize=16, weight='bold')
            ax1.set_xlabel("Fecha", fontsize=12)
            ax1.set_ylabel("Cantidad Vendida", fontsize=12)
            ax1.grid(visible=True, linestyle='--', alpha=0.5)
            st.pyplot(fig1)
        else:  # Si solo hay un dato
            st.warning("No hay suficientes datos para graficar las ventas diarias. Asegúrate de tener múltiples fechas registradas.")
            st.write("**Datos actuales de ventas diarias:**")
            st.dataframe(ventas_diarias)




        # Gráfico de ventas por hora
        st.markdown("### **Ventas por Hora**")
        ventas_acumuladas['Hora'] = ventas_acumuladas['Fecha'].dt.hour
        ventas_por_hora = ventas_acumuladas.groupby('Hora')['Cantidad'].sum()
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ventas_por_hora.plot(kind='bar', ax=ax2, color='#adb5bd', edgecolor='black')
        ax2.set_title("Ventas por Hora", fontsize=16, weight='bold')
        ax2.set_xlabel("Hora del Día", fontsize=12)
        ax2.set_ylabel("Cantidad Vendida", fontsize=12)
        ax2.grid(visible=False)
        st.pyplot(fig2)

        # Gráfico de pastel para ventas por canal
        st.markdown("### **Distribución por Canal**")
        ventas_por_canal = ventas_acumuladas.groupby('Canal')['Cantidad'].sum()
        fig3, ax3 = plt.subplots(figsize=(8, 8))
        ventas_por_canal.plot(kind='pie', ax=ax3, autopct='%1.1f%%', startangle=90, colors=['#adb5bd', '#dee2e6', '#ced4da', '#e9ecef'])
        ax3.set_ylabel("")  # Quitamos la etiqueta del eje Y
        ax3.set_title("Porcentaje de Ventas por Canal", fontsize=16, weight='bold')
        st.pyplot(fig3)
    else:
        st.warning("No se han registrado ventas todavía.")

# Navegación
secciones = {
    "Inicio": pagina_inicio,
    "Catálogo de Productos": pagina_catalogo,
    "Gestión de Inventario": pagina_gestion_inventario,
    "Registro de Ventas": pagina_registro_ventas,
    "Estadísticas": pagina_estadisticas,
}

st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a", list(secciones.keys()))
secciones[opcion]()









