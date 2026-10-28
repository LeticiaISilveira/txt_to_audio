---
title: PDF to Audio
emoji: 🔊
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: app.py
python_version: "3.12"
---

# PDF to Audio

Aplicativo de linha de comando que extrai o texto de um PDF e gera um arquivo WAV com o Kokoro TTS. O projeto
separa leitura do PDF, sintese de voz, interface de terminal e interface web (wip).

## Requisitos

- Python 3.10, 3.11 ou 3.12. O Kokoro usado pelo projeto ainda nao oferece as
  versoes necessarias para Python 3.13 ou superior.
- `espeak-ng`, necessario pelo Kokoro:
  - macOS: `brew install espeak-ng`
  - Ubuntu/Debian: `sudo apt-get install espeak-ng`

## Instalacao

### Instalar para usar o comando

#### macOS

Instale os requisitos do sistema e o `pipx`:

```bash
brew install python@3.12 espeak-ng pipx
pipx ensurepath
```

#### Linux (Ubuntu/Debian)

Instale Python 3.12, o suporte a ambientes virtuais, `espeak-ng`, `pipx` e Git:

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv espeak-ng pipx git
pipx ensurepath
```

Se sua versao do Ubuntu/Debian nao disponibilizar `python3.12`, instale o
Python 3.12 por uma fonte apropriada para sua distribuicao antes de continuar.

Em distribuicoes Fedora, instale os pacotes equivalentes (`python3.12`,
`espeak-ng`, `pipx` e `git`) com `dnf` antes de executar os comandos do `pipx`.

Depois de instalar os requisitos do seu sistema, abra um novo terminal,
execute `pipx ensurepath` se necessario e instale o app diretamente do GitHub:

```bash
pipx install --python python3.12 \
  "git+https://github.com/LeticiaISilveira/txt_to_audio.git"
```

Depois, o comando fica disponivel de qualquer pasta:

```bash
pdf-to-audio --test-voice
pdf-to-audio "/caminho/para/seu-arquivo.pdf"
```

Para atualizar para a versao mais recente:

```bash
pipx upgrade pdf-to-audio
```

### Instalar para desenvolvimento

Na raiz do projeto, crie o ambiente virtual com Python 3.12 e instale as
dependencias. Para instalar tambem a interface Gradio, use o extra `web`:

```bash
python3.12 -m venv .venv312
source .venv312/bin/activate
python -m pip install -e ".[web]"
```

Use `.venv312` para manter o ambiente isolado. No Windows, crie o ambiente
com `py -3.12 -m venv .venv` e ative-o com `.venv\Scripts\activate`.
