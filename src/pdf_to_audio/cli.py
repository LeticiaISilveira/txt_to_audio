import argparse
from pathlib import Path

from pdf_to_audio.pdf_reader import extract_text_from_pdf
from pdf_to_audio.speech import text_to_wav


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-to-audio",
        description="Converte o texto de um PDF em um arquivo WAV com Kokoro.",
    )
    parser.add_argument("pdf", type=Path, help="Caminho do arquivo PDF.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Destino do WAV (padrao: mesmo nome do PDF).",
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

    if not args.pdf.is_file():
        parser.error(f"arquivo PDF nao encontrado: {args.pdf}")
    if args.pdf.suffix.lower() != ".pdf":
        parser.error("o arquivo de entrada precisa ter extensao .pdf")
    if args.speed <= 0:
        parser.error("--speed precisa ser maior que zero")

    output_path = args.output or args.pdf.with_suffix(".wav")
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
