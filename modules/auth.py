import streamlit as st
import bcrypt
import os
from pathlib import Path
import base64

def check_password(input_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña coincide con el hash usando bcrypt.
    
    Args:
        input_password: Contraseña en texto plano ingresada por el usuario
        hashed_password: Hash bcrypt almacenado en variable de entorno
    
    Returns:
        True si la contraseña es correcta, False en caso contrario
    """
    try:
        return bcrypt.checkpw(
            input_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def is_authenticated() -> bool:
    """
    Verifica si el usuario está autenticado en la sesión actual.
    
    Returns:
        True si el usuario está autenticado, False en caso contrario
    """
    return st.session_state.get('authenticated', False)


def logout():
    """Cierra la sesión del usuario."""
    st.session_state.authenticated = False
    st.rerun()


def render_login_page():
    """
    Renderiza la pantalla de login minimalista.
    Usa el toggle nativo de Streamlit para mostrar/ocultar contraseña.
    """
    password_hash = os.getenv('APP_PASSWORD_HASH')
    
    if not password_hash:
        st.error("Error de Configuración: No se ha configurado APP_PASSWORD_HASH")
        st.code("python -m scripts.generate_password_hash 'TuContraseña'", language="bash")
        st.stop()
    
    # Cargar logo
    logo_path = Path(__file__).parent.parent / "assets" / "Logo-Acuicultura.png"
    logo_html = ''
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_data}" style="width: 80px; height: 80px; object-fit: contain;" />'
    
    # CSS para todo en un solo contenedor blanco
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            * {{ font-family: 'Inter', sans-serif; }}
            
            .stApp {{ 
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            }}
            
            #MainMenu, footer, header {{ visibility: hidden; }}
            
            /* Contenedor principal = tarjeta blanca */
            .block-container {{
                max-width: 400px !important;
                margin: 8vh auto 0 auto !important;
                padding: 2.5rem 2rem !important;
                background: white !important;
                border-radius: 16px !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08) !important;
            }}
            
            /* Input */
            .stTextInput > label {{ display: none !important; }}
            .stTextInput > div > div > input {{
                border: 2px solid #e2e8f0 !important;
                border-radius: 10px !important;
                padding: 0.875rem 1rem !important;
                font-size: 0.9375rem !important;
                background: #f8fafc !important;
            }}
            .stTextInput > div > div > input:focus {{
                border-color: #0284c7 !important;
                box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.1) !important;
                background: white !important;
            }}
            
            /* Ocultar tooltip "Press Enter to apply" */
            .stTextInput [data-testid="InputInstructions"] {{
                display: none !important;
            }}
            
            /* Botón primario */
            .stButton > button[kind="primary"] {{
                width: 100% !important;
                background: linear-gradient(135deg, #0e7490 0%, #0284c7 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.875rem !important;
                font-weight: 600 !important;
                font-size: 0.9375rem !important;
                box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
                margin-top: 1rem !important;
            }}
            .stButton > button[kind="primary"]:hover {{
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 16px rgba(2, 132, 199, 0.35) !important;
            }}
        </style>
        
        <!-- Header: Logo y Título -->
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="margin-bottom: 1rem;">{logo_html}</div>
            <h1 style="margin: 0 0 0.25rem 0; font-size: 1.5rem; font-weight: 700; color: #0f172a;">Monitor Biofloc</h1>
            <p style="margin: 0; color: #64748b; font-size: 0.875rem;">Lab. Cultivos Crustáceos - UCN</p>
        </div>

        
        <!-- Separador -->
        <div style="height: 1px; background: #e2e8f0; margin-bottom: 1.5rem;"></div>
        
        <!-- Label del campo -->
        <p style="margin: 0 0 0.5rem 0; font-weight: 600; color: #334155; font-size: 0.875rem;">Contraseña de Acceso</p>
    """, unsafe_allow_html=True)

    
    # Formulario con st.form para que Enter funcione
    with st.form("login_form"):
        password = st.text_input(
            "Contraseña",
            type="password",
            key="password_input",
            placeholder="Ingresa tu contraseña",
            label_visibility="collapsed"
        )
        
        submitted = st.form_submit_button("Iniciar Sesión", type="primary", use_container_width=True)
        
        if submitted:
            if password:
                if check_password(password, password_hash):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")
            else:
                st.warning("Ingresa tu contraseña")
    
    # Info al final
    st.markdown("""
        <div style="margin-top: 1.5rem; padding: 0.75rem; background: #f8fafc; border-radius: 8px; border-left: 3px solid #0284c7;">
            <p style="margin: 0; font-size: 0.8rem; color: #475569; display: flex; align-items: center; gap: 0.5rem;">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                <span><strong>Sistema protegido:</strong> Autenticación requerida</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

