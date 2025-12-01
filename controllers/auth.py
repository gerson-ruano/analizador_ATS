import streamlit as st
import os
import time
from dotenv import load_dotenv
#from components.footer import footer

def init_session():
    """Inicialización centralizada de sesión - CON SINCRONIZACIÓN DE URL"""
    if "auth_initialized" not in st.session_state:
        load_dotenv()
        
        # SINCRONIZAR: Si hay query_params, actualizar session_state
        if 'user' in st.query_params and 'rol' in st.query_params:
            st.session_state.authenticated = True
            st.session_state.username = st.query_params['user']
            st.session_state.rol = st.query_params['rol']
            #print(f"✅ Sesión restaurada desde URL: {st.query_params['user']}")
        
        # SINCRONIZAR: Si hay session_state pero no query_params, agregarlos a la URL
        elif st.session_state.get('authenticated', False) and 'user' not in st.query_params:
            st.query_params['user'] = st.session_state.username
            st.query_params['rol'] = st.session_state.rol
            st.query_params['auth'] = 'true'
            #print(f"✅ Query_params agregados a URL: {st.session_state.username}")
        
        else:
            st.session_state.authenticated = False
            st.session_state.username = 'Invitado'
            st.session_state.rol = 'usuario'
            #print("🔐 No hay sesión activa")
        
        st.session_state.auth_initialized = True

def require_auth():
    """Para app.py (página principal)"""
    init_session()
    
    if not st.session_state.authenticated:
        show_login_screen()
        st.stop()
    
    return True

def require_page_auth():
    """Para páginas individuales - CON MANTENIMIENTO DE URL"""
    init_session()
    
    # SI ESTÁ AUTENTICADO PERO NO TIENE QUERY_PARAMS, AGREGARLOS
    if st.session_state.authenticated and 'user' not in st.query_params:
        st.query_params['user'] = st.session_state.username
        st.query_params['rol'] = st.session_state.rol
        st.query_params['auth'] = 'true'
        #print(f"🔄 Query_params agregados en página: {st.session_state.username}")
    
    if not st.session_state.authenticated:
        # REDIRECCIÓN MEJORADA
        st.markdown("""
        <div style='text-align: center; padding: 50px 20px;'>
            <h2 style='color: #005bea;'>🔐 Redirigiendo al login...</h2>
            <p>Por favor, inicia sesión para acceder a esta página.</p>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.switch_page("inicio.py")
        return False
    
    return True

def require_role(required_roles):
    """Verifica si el usuario tiene el rol requerido"""
    if not isinstance(required_roles, list):
        required_roles = [required_roles]
    
    # OBTENER ROL ACTUAL DE FORMA SEGURA
    user_role = st.session_state.get('rol', 'usuario')
    
    if user_role not in required_roles:
        st.error("❌ Acceso denegado")
        st.info(f"Se requiere rol de: {', '.join(required_roles)}")
        st.warning(f"Tu rol actual es: {user_role}")
        
        # Botón para volver al inicio
        if st.button("🏠 Volver al Inicio"):
            st.switch_page("inicio.py")
        
        st.stop()
    
    return True

def authenticate_env_users(username, password):
    """Autentica contra usuarios en .env"""
    init_session()
    allowed_users = os.getenv('ALLOWED_USERS', '')
    
    for user_info in allowed_users.split(','):
        parts = user_info.strip().split(':')
        if len(parts) >= 2:
            user = parts[0]
            pwd = parts[1]
            rol = parts[2] if len(parts) > 2 else 'usuario'
            
            if user == username and pwd == password:
                # ACTUALIZAR AMBOS: session_state Y query_params
                st.session_state.authenticated = True
                st.session_state.username = user
                st.session_state.rol = rol
                
                st.query_params['user'] = user
                st.query_params['rol'] = rol
                st.query_params['auth'] = 'true'
                
                #print(f"✅ Login exitoso: {user}, rol: {rol}")
                return {'authenticated': True, 'username': user, 'rol': rol}
    
    return {'authenticated': False}

def get_current_user():
    """Obtiene información del usuario actual"""
    init_session()
    
    # VERIFICAR SINCRONIZACIÓN
    if st.session_state.authenticated and 'user' not in st.query_params:
        st.query_params['user'] = st.session_state.username
        st.query_params['rol'] = st.session_state.rol
    
    return {
        'username': st.session_state.get('username', 'Invitado'),
        'rol': st.session_state.get('rol', 'usuario'),
        'authenticated': st.session_state.get('authenticated', False)
    }

def logout():
    """Cierra sesión completamente"""
    # Limpiar session_state
    st.session_state.authenticated = False
    st.session_state.username = 'Invitado'
    st.session_state.rol = 'usuario'
    
    # Limpiar query_params
    if 'user' in st.query_params:
        del st.query_params['user']
    if 'rol' in st.query_params:
        del st.query_params['rol']
    if 'auth' in st.query_params:
        del st.query_params['auth']
    
    st.success("👋 Sesión cerrada correctamente")
    time.sleep(1)
    st.rerun()

def show_login_screen():
    """Muestra la pantalla de login (tu código existente)"""
    st.set_page_config(
        page_title="Login",
        page_icon="✨", 
        layout="centered"
    )
    
    # Tu CSS existente...
    st.markdown("""
<style>
.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0,91,234,0.1);
    border: 1px solid #e6f0ff;
}
.login-header {
    text-align: center;
    margin-bottom: 1rem;
}

/* TARGET MUY ESPECÍFICO PARA EL BOTÓN DEL LOGIN */
div[data-testid="stForm"] button[data-testid="baseButton-primary"],
div[data-testid="stFormSubmitButton"] button,
form[data-testid="stForm"] button[kind="primary"] {
    background: linear-gradient(135deg, #005bea 0%, #0047b7 100%) !important;
    background-color: #005bea !important;
    border: 2px solid #005bea !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 16px !important;
    width: 100% !important;
}

/* ANULAR CUALQUIER ESTILO ROJO */
div[data-testid="stForm"] button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #0047b7 0%, #003a9c 100%) !important;
    border-color: #0047b7 !important;
}

ul[data-testid="stSidebarNavItems"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)
    
# Header
    st.markdown("""
    <div class="login-header">
        <h1 style='color: #005bea; margin-bottom: 10px;'>✨</h1>
        <h2 style='color: #005bea; margin: 0;'>Mejorador de CVS</h2>

    </div>
    """, unsafe_allow_html=True)

    # Formulario de login
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "👤 Usuario", 
            placeholder="Ingresa tu usuario",
            key="login_username"
        )
        password = st.text_input(
            "🔒 Contraseña", 
            type="password",
            placeholder="Ingresa tu contraseña", 
            key="login_password"
        )
        
        login_button = st.form_submit_button(
            "Ingresar",
            type="primary",
            
        )
        st.markdown("""
    <div class="login-header">
        <h5 style='color: #005bea; margin: 0;'>usuario:</h5>
        <h5 style='color: #054bya; margin: 0;'>prueba</h5>
        <h5 style='color: #005bea; margin: 0;'>password:</h5>
        <h5 style='color: #054bya; margin: 0;'>123</h5>
    </div>
    """, unsafe_allow_html=True)
        
        if login_button:
            if username and password:
                with st.spinner("Verificando credenciales..."):
                    result = authenticate_env_users(username, password)
                    
                    if result['authenticated']:
                        st.success(f"✅ Bienvenido, {result['username']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
            else:
                st.warning("⚠️ Por favor, completa todos los campos")

        

    