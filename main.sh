cd ./chatbot && ./load_kb.sh && cd ..
python -m chatbot build
export TWILIO_AUTH_TOKEN=6e41fd5c5be903def94f9e7efaaa15ed
export TWILIO_ACCOUNT_SID=AC090860c33f406130a009592dbd376709
python whatsapp_bot_server.py
