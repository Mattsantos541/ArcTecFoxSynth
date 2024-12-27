import streamlit as st
from config import COLORS

def apply_custom_styles():
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {COLORS['background']};
            color: {COLORS['text']};
        }}

        .logo-container {{
            position: relative;
            width: 300px;
            height: 300px;
            margin: 0 auto;
            animation: fadeIn 1.5s ease-in;
        }}

        .particle {{
            position: absolute;
            background: {COLORS['accent']};
            border-radius: 50%;
            pointer-events: none;
            opacity: 0;
        }}

        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: scale(0.8); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}

        @keyframes particle-animation {{
            0% {{ transform: translate(0, 0); opacity: 0; }}
            50% {{ opacity: 0.8; }}
            100% {{ transform: translate(var(--tx), var(--ty)); opacity: 0; }}
        }}

        .stButton>button {{
            background-color: {COLORS['primary']};
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
        }}

        .stTextInput>div>div>input {{
            border-radius: 5px;
            border: 1px solid {COLORS['secondary']};
        }}

        .stHeader {{
            background-color: {COLORS['primary']};
            padding: 1rem;
            border-radius: 5px;
            color: white;
        }}

        .stAlert {{
            background-color: {COLORS['accent']};
            border: 1px solid {COLORS['secondary']};
            border-radius: 5px;
            padding: 1rem;
        }}

        .metric-container {{
            background-color: white;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        </style>

        <script>
        function createParticle(container) {{
            const particle = document.createElement('div');
            particle.className = 'particle';

            const size = Math.random() * 6 + 2;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;

            const startX = Math.random() * 300;
            const startY = Math.random() * 300;
            particle.style.left = `${startX}px`;
            particle.style.top = `${startY}px`;

            const tx = (Math.random() - 0.5) * 200;
            const ty = (Math.random() - 0.5) * 200;
            particle.style.setProperty('--tx', `${tx}px`);
            particle.style.setProperty('--ty', `${ty}px`);

            particle.style.animation = `particle-animation ${Math.random() * 2 + 1}s linear infinite`;

            container.appendChild(particle);
            setTimeout(() => particle.remove(), 3000);
        }}

        function startParticleAnimation() {{
            const container = document.querySelector('.logo-container');
            if (container) {{
                setInterval(() => createParticle(container), 100);
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            startParticleAnimation();
        }});
        </script>
    """, unsafe_allow_html=True)

def display_logo():
    st.markdown(f"""
        <div class="logo-container">
            <img src="attached_assets/AF.jpg" style="width: 100%; height: 100%; object-fit: contain;">
        </div>
    """, unsafe_allow_html=True)