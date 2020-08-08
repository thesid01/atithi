cd ./chatbot && ./load_kb.sh && cd ..
python -m chatbot build
export TWILIO_AUTH_TOKEN=
export TWILIO_ACCOUNT_SID=
python whatsapp_bot_server.py
