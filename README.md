# Simulação de Órbitas Planetárias com Série de Fourier

Este projeto simula órbitas planetárias usando aproximações por Série de Fourier, baseado em um TCC da Maria Faria na Pasta Others.

## 🚀 Como usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o programa

```bash
python cli.py
```

### 3. Escolher opções

O programa irá perguntar:
- **Qual planeta simular**: Marte, Vênus ou Mercúrio
- **Número de termos de Fourier**: Recomendado entre 3-10 termos

### 4. Visualizar resultado

Um gráfico será exibido mostrando:
- **Órbita Real** (colorida): A órbita elíptica calculada usando as leis de Kepler
- **Aproximação de Fourier** (linha tracejada preta): A órbita reconstruída usando a série de Fourier

Quanto mais termos de Fourier você usar, mais precisa será a aproximação!

## 📂 Estrutura do projeto

```
idp/
├── utils/
│   └── lib.py
├── others/
│   └── original.ipynb
│   └── TCC - Maria Farias_Final.pdf
├── tests/
│   └── exemplo.py
├── main.py
├── requirements.txt
└── README.md
```

## 🎓 Conceitos

- **Órbita elíptica**: Trajetória natural dos planetas ao redor do Sol
- **Série de Fourier**: Método matemático para aproximar funções periódicas usando senos e cossenos
- **Termos de Fourier**: Quanto mais termos, melhor a aproximação (mas mais lenta a computação)