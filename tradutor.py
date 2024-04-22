import sys
import speech_recognition as sr
from googletrans import LANGUAGES, Translator
from flask import Flask, render_template, request

app = Flask(__name__)

class TranslatorApp:
    @staticmethod
    def populate_language_combobox(combobox):
        for codigo_idioma, nome_idioma in LANGUAGES.items():
            combobox.append((f"{nome_idioma} ({codigo_idioma})", codigo_idioma))

    @staticmethod
    def traduzir_texto(texto, origem='pt', destino='en'):
        if texto is None:
            return "Texto vazio"
        translator = Translator()
        translated = translator.translate(texto, src=origem, dest=destino)
        return translated.text

    @staticmethod
    def ouvir_microfone():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Diga algo:")
            audio = recognizer.listen(source)
        
        try:
            texto = recognizer.recognize_google(audio, language='pt-BR')
            return texto
        except sr.UnknownValueError:
            print("Não foi possível entender a entrada de voz.")
            return None
        except sr.RequestError as e:
            print(f"Erro ao fazer a solicitação: {e}")
            return None

@app.route('/', methods=['GET', 'POST'])
def index():
    languages = [(f"{nome_idioma} ({codigo_idioma})", codigo_idioma) for codigo_idioma, nome_idioma in LANGUAGES.items()]
    if request.method == 'POST':
        if 'falar' in request.form:
            texto_a_traduzir = TranslatorApp.ouvir_microfone()
        else:
            texto_a_traduzir = request.form.get('texto_a_traduzir')
        
        selected_language = request.form.get('selected_language')
        selected_target_language = request.form.get('selected_target_language')

        if not texto_a_traduzir:
            translation = "Nenhum texto detectado."
        else:
            translation = TranslatorApp.traduzir_texto(texto_a_traduzir, origem=selected_language, destino=selected_target_language)

        return render_template('index.html', languages=languages, translation=translation, selected_language=selected_language, selected_target_language=selected_target_language)

    return render_template('index.html', languages=languages)

if __name__ == '__main__':
    app.run(debug=True)
