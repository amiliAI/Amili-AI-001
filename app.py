import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import tempfile
import os

# API Key
API_KEY = "AIzaSyDBYrye_IhG5fcZzqQjOaPLP0iL9zenqfY"
genai.configure(api_key=API_KEY)

# Model နာမည်ကို models/ မပါဘဲ ဒီအတိုင်းပဲ ရေးပါမယ်
# ဒါက Google API တိုင်းမှာ အလုပ်လုပ်ရမယ့် နာမည်ပါ
model = genai.GenerativeModel('gemini-pro')

st.title("🇲🇲 AI Myanmar Voice")

if prompt := st.chat_input("မေးခွန်းရိုက်ပါ..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # အခြေခံအကျဆုံး response နည်းလမ်းကို သုံးပါမယ်
            response = model.generate_content(prompt, stream=False)
            ai_text = response.text
            st.markdown(ai_text)
            
            async def speak(text):
                communicate = edge_tts.Communicate(text, "my-MM-NilarNeural")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    await communicate.save(tmp.name)
                    return tmp.name
            
            audio_path = asyncio.run(speak(ai_text))
            with open(audio_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            os.remove(audio_path)
            
        except Exception as e:
            # Error တက်ရင် အဖြေရှာရလွယ်အောင် Error စာသားကို အကုန်ပြပါမယ်
            st.error(f"Error: {str(e)}")
            st.warning("Google API က Model ကို ရှာမတွေ့တာ ဖြစ်နိုင်ပါတယ်။")
            
