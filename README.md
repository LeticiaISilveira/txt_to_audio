# PDF to Audio

Aplicativo de linha de comando que extrai o texto de um PDF e gera um arquivo WAV com o Kokoro TTS. O projeto
separa leitura do PDF, sintese de voz e interface de terminal.

## Requisitos

- Python 3.10 ou superior
- `espeak-ng`, necessario pelo Kokoro:
  - macOS: `brew install espeak-ng`
  - Ubuntu/Debian: `sudo apt-get install espeak-ng`

## Instalacao

Na raiz do projeto, crie e ative um ambiente virtual e instale o aplicativo:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

No Windows, ative o ambiente com `.venv\Scripts\activate`.

## Uso

Converta um PDF para WAV:

```bash
pdf-to-audio ./meu-livro.pdf
```

Por padrao, o audio e salvo ao lado do PDF, com o mesmo nome. Para escolher
outro destino, voz, idioma ou velocidade:

```bash
pdf-to-audio ./meu-livro.pdf \
  --output ./audios/meu-livro.wav \
  --language p \
  --voice pf_dora \
  --speed 1.0
```

O idioma e a voz precisam ser compativeis. Para portugues brasileiro, use
`--language p` com uma voz portuguesa, como `pf_dora` ou `pm_alex`. As vozes
`af_heart`, `am_eric`, `am_puck` e `af_nicole` do teste sao vozes em ingles
americano (`--language a`).

Para ver todas as opcoes:

```bash
pdf-to-audio --help
```

O PDF precisa conter texto selecionavel. Arquivos digitalizados como imagem
precisam passar por OCR antes; OCR ainda nao faz parte deste app.

## Estrutura

```text
.
├── examples/
│   └── voice_preview.py       # Gera amostras das vozes em ingles do teste
├── src/
│   └── pdf_to_audio/
│       ├── cli.py             # Argumentos e fluxo da aplicacao
│       ├── pdf_reader.py      # Extracao de texto do PDF
│       └── speech.py          # Geracao de WAV com Kokoro
├── tests/
│   └── test_pdf_reader.py
└── pyproject.toml
```

O arquivo original era uma exportacao de notebook do Colab, com comandos
`!pip`, interfaces do IPython e experimentos separados de XTTS/OmniVoice.
Esses comandos nao sao Python executavel localmente; o fluxo Kokoro relevante
foi aproveitado no app e no exemplo de vozes. Os experimentos de clonagem nao
foram incluidos na conversao PDF para audio.
