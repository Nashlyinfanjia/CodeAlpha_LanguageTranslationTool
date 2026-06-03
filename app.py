import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
import os

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LinguaNova AI",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===================== MODERN CSS STYLING =====================
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
        }
        
        .header-container {
            text-align: center;
            padding: 40px 20px 30px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-bottom: 3px solid #00d9ff;
        }
        
        .main-title {
            font-size: 48px;
            font-weight: 900;
            color: #00ffcc;
            text-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
            margin: 0;
            letter-spacing: 2px;
        }
        
        .tagline {
            font-size: 18px;
            color: #64748b;
            margin-top: 8px;
            font-style: italic;
            letter-spacing: 1px;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 2px solid #00d9ff;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
            color: #00ffcc;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 0px 8px 32px rgba(0, 217, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            box-shadow: 0px 12px 48px rgba(0, 255, 204, 0.4);
            transform: translateY(-2px);
        }
        
        .input-section {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
        }
        
        .result-box {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-left: 4px solid #00ffcc;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            font-size: 18px;
            color: #00ffcc;
            font-weight: 500;
        }
        
        .history-item {
            background: #1e293b;
            border-left: 4px solid #00d9ff;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            font-size: 14px;
        }
        
        .footer {
            text-align: center;
            color: #64748b;
            padding: 30px;
            border-top: 1px solid #334155;
            margin-top: 40px;
            font-size: 13px;
        }
        
        .error-box {
            background: #7f1d1d;
            border: 1px solid #dc2626;
            border-radius: 8px;
            padding: 15px;
            color: #fca5a5;
            margin: 10px 0;
        }
        
        .success-box {
            background: #064e3b;
            border: 1px solid #10b981;
            border-radius: 8px;
            padding: 15px;
            color: #a7f3d0;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">🌍 LinguaNova AI</h1>
        <p class="tagline">Translate. Understand. Speak the world.</p>
    </div>
""", unsafe_allow_html=True)

# ===================== FEATURE HIGHLIGHTS =====================
st.markdown("""
    <div class="feature-card">
        ⚡ 40+ Languages • 🧠 AI Auto Detection • 🎵 Voice Output • 💬 History
    </div>
""", unsafe_allow_html=True)

# ===================== LANGUAGE MAPPINGS =====================
languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Portuguese": "pt",
    "Italian": "it",
    "Dutch": "nl",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Malay": "ms",
    "Greek": "el",
    "Hebrew": "he",
    "Polish": "pl",
    "Czech": "cs",
    "Romanian": "ro",
    "Swedish": "sv",
    "Danish": "da",
    "Finnish": "fi",
    "Hungarian": "hu",
    "Ukrainian": "uk",
    "Norwegian": "no",
    "Persian": "fa",
    "Swahili": "sw"
}

# ===================== SESSION STATE INITIALIZATION =====================
if "history" not in st.session_state:
    st.session_state.history = []

if "last_translation" not in st.session_state:
    st.session_state.last_translation = None

# ===================== INPUT SECTION =====================
st.markdown('<div class="input-section">', unsafe_allow_html=True)

text = st.text_area("💬 Enter text to translate", placeholder="Type your text here...", height=120)

col1, col2, col3 = st.columns(3)

with col1:
    source_lang = st.selectbox("From", list(languages.keys()), label_visibility="collapsed")
    st.caption("Source Language")

with col2:
    target_options = [k for k in languages.keys() if k != "Auto Detect"]
    target_lang = st.selectbox("To", target_options, label_visibility="collapsed", key="target_lang")
    st.caption("Target Language")

with col3:
    tone = st.selectbox("Tone", ["Normal", "Formal", "Casual"], label_visibility="collapsed")
    st.caption("Translation Tone")

st.markdown('</div>', unsafe_allow_html=True)

# ===================== LANGUAGE DETECTION =====================
detected_lang_code = None
detected_lang_name = None

if text.strip():
    try:
        detected_lang_code = detect(text)
        # Map detected code to language name
        for lang_name, lang_code in languages.items():
            if lang_code == detected_lang_code:
                detected_lang_name = lang_name
                break
        if detected_lang_name:
            st.info(f"🧠 Auto-Detected Language: **{detected_lang_name}**")
    except Exception as e:
        st.warning("⚠️ Could not detect language automatically. Please select manually.")
        detected_lang_code = None
        detected_lang_name = None

# ===================== TRANSLATION FUNCTION =====================
def apply_tone(text, tone_type):
    """Apply tone modifications to translated text."""
    if tone_type == "Formal":
        return f"Kindly note: {text}. We appreciate your attention to this matter."
    elif tone_type == "Casual":
        return f"Hey! {text.lower()} 😄"
    else:
        return text

def generate_audio(text, lang_code):
    """Generate audio file safely using gTTS."""
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_file = "voice.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        return None

def read_audio_file(file_path):
    """Safely read audio file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return f.read()
    except Exception:
        return None
    return None

# ===================== TRANSLATE BUTTON =====================
if st.button("🚀 Translate Now", use_container_width=True):
    if not text.strip():
        st.warning("⚠️ Please enter text to translate.")
    else:
        try:
            # Get source language code
            src_code = languages[source_lang]
            
            # If Auto Detect is selected, use detected language
            if src_code == "auto":
                if detected_lang_code:
                    src_code = detected_lang_code
                else:
                    st.error("❌ Could not auto-detect language. Please select manually.")
                    st.stop()
            
            # Get target language code
            target_code = languages[target_lang]
            
            # Perform translation
            translator = GoogleTranslator(source=src_code, target=target_code)
            translated_text = translator.translate(text)
            
            # Apply tone
            display_text = apply_tone(translated_text, tone)
            
            # Store in session state
            st.session_state.last_translation = {
                "original": text,
                "translated": translated_text,
                "display": display_text,
                "source": source_lang,
                "target": target_lang,
                "tone": tone
            }
            
            # ===================== DISPLAY RESULT =====================
            st.markdown(f'<div class="success-box">✨ Translation Complete!</div>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="result-box">{display_text}</div>', unsafe_allow_html=True)
            
            # ===================== AUDIO OUTPUT =====================
            st.markdown("### 🎵 Audio Output")
            audio_col1, audio_col2 = st.columns([1, 1])
            
            with audio_col1:
                if st.button("🔊 Generate Audio", use_container_width=True):
                    with st.spinner("Generating audio..."):
                        audio_path = generate_audio(translated_text, target_code)
                        if audio_path:
                            audio_data = read_audio_file(audio_path)
                            if audio_data:
                                st.audio(audio_data, format="audio/mp3")
                                st.success("✅ Audio generated successfully!")
                            else:
                                st.error("❌ Failed to read audio file.")
                        else:
                            st.error("❌ Failed to generate audio. Check your internet connection.")
            
            with audio_col2:
                # ===================== DOWNLOAD =====================
                st.download_button(
                    label="📥 Download Text",
                    data=translated_text,
                    file_name="LinguaNova_translation.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # ===================== SAVE TO HISTORY =====================
            st.session_state.history.append({
                "original": text,
                "translated": translated_text,
                "source": source_lang,
                "target": target_lang,
                "tone": tone
            })
        
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Translation Failed: {str(e)}</div>', unsafe_allow_html=True)
            st.info("💡 Troubleshooting Tips:\n- Check your internet connection\n- Make sure Google Translator service is accessible\n- Try with a shorter text\n- Verify the source and target languages are correct")

# ===================== HISTORY SECTION =====================
st.markdown("---")
st.subheader("💬 Translation History")

if not st.session_state.history:
    st.write("📭 No translations yet. Start translating to see history!")
else:
    # Display last 10 translations
    for idx, item in enumerate(reversed(st.session_state.history[-10:])):
        st.markdown(f"""
        <div class="history-item">
            <strong>🧑 You ({item['source']} → {item['target']}):</strong><br>
            {item['original']}<br><br>
            <strong>🤖 LinguaNova:</strong><br>
            {item['translated']}
        </div>
        """, unsafe_allow_html=True)

# ===================== FOOTER =====================
st.markdown("""
    <div class="footer">
        <p>🌍 Built with Streamlit | LinguaNova AI v1.0</p>
        <p style="font-size: 11px; margin-top: 10px;">Powered by Google Translate, langdetect, and gTTS</p>
    </div>
""", unsafe_allow_html=True)