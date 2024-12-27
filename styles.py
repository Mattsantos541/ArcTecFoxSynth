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
            overflow: visible;
            z-index: 1000;
        }}

        .particle {{
            position: absolute;
            background: {COLORS['accent']};
            border-radius: 50%;
            pointer-events: none;
            opacity: 0;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            z-index: 999;
        }}

        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: scale(0.8) translateY(20px); }}
            100% {{ opacity: 1; transform: scale(1) translateY(0); }}
        }}

        @keyframes particle-animation {{
            0% {{ 
                transform: translate(0, 0);
                opacity: 0;
                width: 2px;
                height: 2px;
            }}
            50% {{ 
                opacity: 0.8;
                width: 4px;
                height: 4px;
            }}
            100% {{ 
                transform: translate(var(--tx), var(--ty));
                opacity: 0;
                width: 2px;
                height: 2px;
            }}
        }}

        .stButton>button {{
            background-color: {COLORS['primary']};
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }}

        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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

        .logo-image {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            position: relative;
            z-index: 1001;
        }}
        </style>

        <script>
        function createParticle(container) {{
            try {{
                const particle = document.createElement('div');
                particle.className = 'particle';

                const startX = Math.random() * 300;
                const startY = Math.random() * 300;
                particle.style.left = startX + 'px';
                particle.style.top = startY + 'px';

                const tx = (Math.random() - 0.5) * 400;
                const ty = (Math.random() - 0.5) * 400;
                particle.style.setProperty('--tx', tx + 'px');
                particle.style.setProperty('--ty', ty + 'px');

                const duration = Math.random() * 2 + 2;
                particle.style.animation = 'particle-animation ' + duration + 's linear';

                container.appendChild(particle);
                setTimeout(() => particle.remove(), duration * 1000);
            }} catch (error) {{
                console.error('Error creating particle:', error);
            }}
        }}

        function startParticleAnimation() {{
            try {{
                const container = document.querySelector('.logo-container');
                if (container) {{
                    setInterval(() => {{
                        for (let i = 0; i < 3; i++) {{
                            createParticle(container);
                        }}
                    }}, 200);
                }}
            }} catch (error) {{
                console.error('Error starting particle animation:', error);
            }}
        }}

        // Ensure DOM is fully loaded before starting animation
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', startParticleAnimation);
        }} else {{
            startParticleAnimation();
        }}
        </script>
    """, unsafe_allow_html=True)

def display_logo():
    st.markdown(f"""
        <div class="logo-container">
            <img src="attached_assets/AF.jpg" class="logo-image" alt="ArcTecFox Logo">
        </div>
    """, unsafe_allow_html=True)