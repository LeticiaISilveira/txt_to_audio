import argparse
from pathlib import Path

from pdf_to_audio.pdf_reader import extract_text_from_pdf
from pdf_to_audio.speech import VOICE_TEST_PHRASES, play_wav, text_to_wav


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-to-audio",
        description="Converte um PDF em WAV ou reproduz um teste de voz com Kokoro.",
    )
    parser.add_argument(
        "pdf",
        type=Path,
        nargs="?",
        help="Caminho do arquivo PDF (nao use com --test-voice).",
    )
    parser.add_argument(
        "--test-voice",
        action="store_true",
        help="Gera e reproduz uma frase curta para testar a voz selecionada.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Destino do WAV (PDF: mesmo nome; teste: voice-test.wav).",
    )
    parser.add_argument(
        "--language",
        default="p",
        help="Codigo do idioma Kokoro (padrao: p, portugues brasileiro).",
    )
    parser.add_argument(
        "--voice",
        default="pf_dora",
        help="Codigo da voz Kokoro (padrao: pf_dora).",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Velocidade da fala (padrao: 1.0).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.speed <= 0:
        parser.error("--speed precisa ser maior que zero")

    if args.test_voice:
        if args.pdf is not None:
            parser.error("nao informe um PDF junto com --test-voice")
        if args.language not in VOICE_TEST_PHRASES:
            parser.error(
                "o teste de voz tem frases prontas para os idiomas 'p' e 'a'"
            )

        output_path = args.output or Path("voice-test.wav")
        if output_path.suffix.lower() != ".wav":
            parser.error("o arquivo de saida precisa ter extensao .wav")

        try:
            text_to_wav(
                text=VOICE_TEST_PHRASES[args.language],
                output_path=output_path,
                language=args.language,
                voice=args.voice,
                speed=args.speed,
            )
            play_wav(output_path)
        except RuntimeError as error:
            parser.error(str(error))
        print(f"Teste de voz salvo em: {output_path}")
        return

    if args.pdf is None:
        parser.error("informe um PDF ou use --test-voice")
    if not args.pdf.is_file():
        parser.error(f"arquivo PDF nao encontrado: {args.pdf}")
    if args.pdf.suffix.lower() != ".pdf":
        parser.error("o arquivo de entrada precisa ter extensao .pdf")

    output_path = args.output or args.pdf.with_suffix(".wav")
    if output_path.suffix.lower() != ".wav":
        parser.error("o arquivo de saida precisa ter extensao .wav")
    if output_path.resolve() == args.pdf.resolve():
        parser.error("o arquivo de saida nao pode substituir o PDF de entrada")

    try:
        text = extract_text_from_pdf(args.pdf)
    except ValueError as error:
        parser.error(str(error))

    text_to_wav(
        text=text,
        output_path=output_path,
        language=args.language,
        voice=args.voice,
        speed=args.speed,
    )
    print(f"Audio salvo em: {output_path}")
