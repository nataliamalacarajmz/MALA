import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns 

# Archivos de datos
file_path = "base_datos_productos.xlsx"
ventas_file = "ventas.xlsx"

# Función para cargar datos de productos

def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        if 'Ventas' not in df.columns:
            df['Ventas'] = 0  # Asegúrate de que tenga la columna Ventas
        return df
    except FileNotFoundError:
        st.error("El archivo de base de datos no fue encontrado.")
        return pd.DataFrame()


# Función para guardar datos
def save_data(df, file_path):
    try:
        df.to_excel(file_path, index=False)
        st.success("Datos guardados correctamente.")
        # Recargar datos después de guardar
        return load_data(file_path)
    except PermissionError:
        st.error("No se pudo guardar el archivo. Verifica que no esté abierto o revisa los permisos.")
        return df
    except Exception as e:
        st.error(f"Ocurrió un error al guardar el archivo: {e}")
        return df

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
        font-size: 3rem;
        font-weight: bold;
        color: #495057;
        margin-bottom: 10px;
        transition: color 0.3s ease-in-out;
    }
    .brand-name:hover {
        color: #007BFF;
    }
    .slogan {
        font-size: 1.8rem;
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
    .cta-button {
        display: inline-block;
        padding: 15px 30px;
        font-size: 1.2rem;
        color: #fff;
        background-color: #333333; /* Gris oscuro */
        text-decoration: none;
        border-radius: 30px;
        margin-top: 20px;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }
    .cta-button:hover {
        background-color: #555555; /* Gris más claro al pasar el cursor */
        box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-3px);
    }
    .testimonial {
        font-size: 1.5rem;
        font-style: italic;
        color: #6c757d;
        margin-top: 20px;
    }
    .testimonial-author {
        font-size: 1.2rem;
        color: #495057;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Marca y Slogan
    st.markdown("""
    <div class="centered">
        <div class="brand-name">MALA</div>
        <div class="slogan">Effortless Wear</div>
        <p style="font-size: 1.2rem; color: #6c757d;">"Made and inspired by modern women"</p>
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

    # Texto motivador con botón
    st.markdown("""
    <div class="centered">
        <p class="testimonial">"Vestir bien nunca fue tan fácil como con MALA."</p>
        <p class="testimonial-author">- Una clienta satisfecha</p>
        <a href="https://malaeffortlesswear.com/" target="_blank" class="cta-button">
            Ir a nuestra Página Web
        </a>
    </div>
    """, unsafe_allow_html=True)

#Catalogo

def pagina_catalogo():
    st.title("📋 Catálogo de Productos")
    st.markdown("Aquí puedes visualizar y buscar tus productos.")

    if df.empty:
        st.error("La base de datos de productos está vacía.")
        return

    # Buscador y filtros
    buscador = st.text_input("Buscar producto (código, descripción, color, etc.)")
    familia_filtro = st.selectbox("Filtrar por Familia", options=["Todos"] + list(df['Familia'].unique()))
    rango_precio = st.slider("Filtrar por Rango de Precio", min_value=int(df['Precio'].min()), 
                             max_value=int(df['Precio'].max()), value=(int(df['Precio'].min()), int(df['Precio'].max())))

    # Filtrar productos
    productos_filtrados = df.copy()
    if buscador:
        # Filtrar por múltiples columnas
        productos_filtrados = productos_filtrados[
            productos_filtrados['CODIGO'].str.contains(buscador, na=False, case=False) |
            productos_filtrados['Familia'].str.contains(buscador, na=False, case=False) |
            productos_filtrados['Color'].str.contains(buscador, na=False, case=False) |
            productos_filtrados['Talla'].str.contains(buscador, na=False, case=False)
        ]
    if familia_filtro != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Familia'] == familia_filtro]
    productos_filtrados = productos_filtrados[
        (productos_filtrados['Precio'] >= rango_precio[0]) & (productos_filtrados['Precio'] <= rango_precio[1])
    ]

    # Mostrar resultados
    if productos_filtrados.empty:
        st.warning("No se encontraron productos que coincidan con los filtros.")
    else:
        st.markdown("### Resultados del Catálogo:")
        for _, producto in productos_filtrados.iterrows():
            st.markdown(f"""
            <div style="
                border: 1px solid #ddd; 
                border-radius: 10px; 
                padding: 15px; 
                margin-bottom: 15px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
                display: flex; 
                justify-content: space-between; 
                align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #333;">{producto['CODIGO']}</h4>
                    <p style="margin: 0; color: #666;">{producto['Familia']} - {producto['Color']} - {producto['Talla']}</p>
                    <p style="margin: 0; font-weight: bold; color: #007BFF;">Precio: ${producto['Precio']:.2f}</p>
                    <p style="margin: 0; color: #555;">Inventario Disponible: {producto['Inventario']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Página de gestión de inventario
def pagina_gestion_inventario():
    global df  # Usa el DataFrame global
    st.title("📦 Gestión de Inventario")
    st.markdown("Añade o quita inventario de tus productos.")

    if df.empty:
        st.error("La base de datos de productos está vacía.")
        return

    # Selección de filtros
    familia = st.selectbox("Selecciona Familia", options=["Todos"] + list(df['Familia'].unique()))
    color = st.selectbox("Selecciona Color", options=["Todos"] + list(df['Color'].unique()))
    talla = st.selectbox("Selecciona Talla", options=["Todos"] + list(df['Talla'].unique()))

    productos_filtrados = df.copy()
    if familia != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Familia'] == familia]
    if color != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Color'] == color]
    if talla != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Talla'] == talla]

    producto_seleccionado = st.selectbox("Selecciona Producto", options=productos_filtrados['CODIGO'])

    # Formulario para actualizar inventario
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
            else:
                st.error(f"No hay suficiente inventario para quitar {cantidad} unidades.")

            # Guardar y recargar datos
            df = save_data(df, file_path)
        else:
            st.error("El producto seleccionado no existe en la base de datos.")

# Página de registro de ventas
def pagina_gestion_inventario():
    global df  # Asegúrate de que 'df' sea global
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
            
            # Guarda los cambios y recarga los datos
            save_data(df, file_path)
            df = load_data(file_path)  # Recargar los datos para que estén actualizados
        else:
            st.error("El producto seleccionado no existe en la base de datos.")

#VENTAS

def pagina_registro_ventas():
    global df, ventas_acumuladas
    st.title("🛒 Registro de Ventas")
    st.markdown("Registra las ventas de tus productos aquí.")

    if df.empty:
        st.error("La base de datos de productos está vacía.")
        return

    # Selección de filtros
    familia = st.selectbox("Selecciona Familia", options=["Todos"] + list(df['Familia'].unique()))
    color = st.selectbox("Selecciona Color", options=["Todos"] + list(df['Color'].unique()))
    talla = st.selectbox("Selecciona Talla", options=["Todos"] + list(df['Talla'].unique()))

    productos_filtrados = df.copy()
    if familia != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Familia'] == familia]
    if color != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Color'] == color]
    if talla != "Todos":
        productos_filtrados = productos_filtrados[productos_filtrados['Talla'] == talla]

    producto_seleccionado = st.selectbox("Selecciona Producto", options=productos_filtrados['CODIGO'])

    if not productos_filtrados.empty:
        producto_info = productos_filtrados[productos_filtrados['CODIGO'] == producto_seleccionado]
        st.write("Detalles del Producto:")
        st.table(producto_info[['CODIGO', 'Familia', 'Color', 'Talla', 'Inventario', 'Precio']])

    # Formulario para registrar venta
    with st.form("form_ventas"):
        cantidad = st.number_input("Cantidad Vendida", min_value=1, step=1)
        canal = st.selectbox("Canal de Venta", ["Whatsapp", "Instagram", "Showroom", "Shopify", "Puntos de Venta"])
        submit = st.form_submit_button("Registrar Venta")

        if submit:
            if producto_seleccionado in df['CODIGO'].values:
                idx = df[df['CODIGO'] == producto_seleccionado].index[0]
                if df.loc[idx, 'Inventario'] >= cantidad:
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
                    df = load_data(file_path)  # Recarga datos actualizados
                    st.success(f"Venta registrada: {cantidad} unidades de {producto_seleccionado} por {canal}.")
                else:
                    st.error(f"No hay suficiente inventario para vender {cantidad} unidades.")
            else:
                st.error("El producto seleccionado no existe en la base de datos.")

    # Historial de Ventas Recientes
    st.markdown("---")
    st.markdown("### Historial de Ventas Recientes:")
    if not ventas_acumuladas.empty:
        st.write(ventas_acumuladas.tail(5))
    else:
        st.info("No se han registrado ventas todavía.")

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
        productos_vendidos = ventas_con_info.groupby('CODIGO').agg({'Cantidad': 'sum'}).sort_values(by='Cantidad', ascending=False)
        top_producto = productos_vendidos.head(1).index[0]
        top_producto_cantidad = productos_vendidos.head(1)['Cantidad'].values[0]

        # Mostrar resumen de ventas en la parte superior
        st.markdown("### **Resumen de Ventas**")
        col1, col2, col3 = st.columns([1, 1, 1], gap="large")
        with col1:
            st.metric("Piezas Vendidas", total_ventas)
        with col2:
            st.metric("Utilidad Total", f"${total_utilidad:,.2f}")
        with col3:
            st.metric("Margen de Utilidad", f"{margen_utilidad:.2f}%")

        # Gráfico de pastel: Canales de venta
        st.markdown("### **Distribución por Canal**")
        canales_ventas = ventas_acumuladas.groupby('Canal')['Cantidad'].sum()
        fig1, ax1 = plt.subplots(figsize=(8, 8))
        colores_grises = sns.color_palette("Greys", len(canales_ventas))  # Tonos grises para el pastel
        canales_ventas.plot(
            kind='pie',
            ax=ax1,
            autopct='%1.1f%%',
            startangle=90,
            colors=colores_grises,
            wedgeprops={'edgecolor': 'black'}
        )
        ax1.set_ylabel("")  # Quitamos la etiqueta del eje Y
        ax1.set_title("Porcentaje de Ventas por Canal", fontsize=16, weight='bold', color="#333333")
        st.pyplot(fig1)

        # Gráfico de barras: Productos más vendidos
        st.markdown("### **Productos Más Vendidos**")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x=productos_vendidos.head(10).index,
            y=productos_vendidos.head(10)['Cantidad'],
            ax=ax2,
            palette="Greys_r",  # Barras en tonos grises
            edgecolor="black"
        )
        ax2.set_title("Top 10 Productos Más Vendidos", fontsize=16, weight='bold', color="#333333")
        ax2.set_xlabel("Código de Producto", fontsize=12, color="#555555")
        ax2.set_ylabel("Cantidad Vendida", fontsize=12, color="#555555")
        ax2.grid(visible=True, linestyle='--', alpha=0.5)
        st.pyplot(fig2)

        # Mención del producto más vendido
        st.markdown(f"**Producto Más Vendido:** {top_producto} con {top_producto_cantidad} unidades.")

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









