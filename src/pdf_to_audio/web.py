import tempfile
from pathlib import Path

import gradio as gr

from pdf_to_audio.pdf_reader import extract_text_from_pdf
from pdf_to_audio.speech import VOICE_TEST_PHRASES, text_to_wav


VOICE_CHOICES = {
    "p": [
        ("Dora (feminina)", "pf_dora"),
        ("Alex (masculina)", "pm_alex"),
    ],
    "a": [
        ("Heart (feminina)", "af_heart"),
        ("Eric (masculina)", "am_eric"),
        ("Puck (masculina)", "am_puck"),
        ("Nicole (feminina)", "af_nicole"),
    ],
}


def voice_choices(language: str) -> list[tuple[str, str]]:
    return VOICE_CHOICES[language]


def update_voice_choices(language: str) -> gr.Dropdown:
    choices = voice_choices(language)
    return gr.Dropdown(choices=choices, value=choices[0][1])


def _temporary_audio_path() -> Path:
    return Path(tempfile.mkdtemp(prefix="pdf-to-audio-")) / "audio.wav"


def convert_pdf(
    pdf_path: str | None,
    language: str,
    voice: str,
    speed: float,
) -> str:
    if not pdf_path:
        raise gr.Error("Envie um arquivo PDF para começar.")

    source_path = Path(pdf_path)
    if source_path.suffix.lower() != ".pdf":
        raise gr.Error("O arquivo enviado precisa estar no formato PDF.")

    text = extract_text_from_pdf(source_path)
    output_path = _temporary_audio_path()
    text_to_wav(
        text=text,
        output_path=output_path,
        language=language,
        voice=voice,
        speed=speed,
    )
    return str(output_path)


def generate_voice_sample(language: str, voice: str, speed: float) -> str:
    output_path = _temporary_audio_path()
    text_to_wav(
        text=VOICE_TEST_PHRASES[language],
        output_path=output_path,
        language=language,
        voice=voice,
        speed=speed,
    )
    return str(output_path)


with gr.Blocks(title="PDF para Áudio") as demo:
    gr.Markdown(
        """
        # PDF para Áudio
        Envie um PDF com texto selecionável e gere um áudio com Kokoro TTS.
        PDFs digitalizados como imagem ainda precisam de OCR antes da conversão.
        """
    )

    with gr.Row():
        pdf_input = gr.File(
            label="Arquivo PDF",
            file_types=[".pdf"],
            type="filepath",
        )
        language_input = gr.Dropdown(
            label="Idioma",
            choices=[("Português", "p"), ("English", "a")],
            value="p",
        )

    with gr.Row():
        voice_input = gr.Dropdown(
            label="Voz",
            choices=voice_choices("p"),
            value="pf_dora",
        )
        speed_input = gr.Slider(
            label="Velocidade",
            minimum=0.5,
            maximum=2.0,
            value=1.0,
            step=0.1,
        )

    language_input.change(
        fn=update_voice_choices,
        inputs=language_input,
        outputs=voice_input,
    )

    with gr.Row():
        convert_button = gr.Button("Converter PDF", variant="primary")
        sample_button = gr.Button("Testar voz")

    audio_output = gr.Audio(
        label="Áudio gerado",
        type="filepath",
        format="wav",
        show_download_button=True,
    )
    convert_button.click(
        fn=convert_pdf,
        inputs=[pdf_input, language_input, voice_input, speed_input],
        outputs=audio_output,
    )
    sample_button.click(
        fn=generate_voice_sample,
        inputs=[language_input, voice_input, speed_input],
        outputs=audio_output,
    )
