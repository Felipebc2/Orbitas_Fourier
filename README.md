# Simulação de Órbitas Planetárias com Série de Fourier

Este projeto simula órbitas planetárias usando aproximações por Série de Fourier, baseado em um TCC da Maria Faria na Pasta Others.

## 🚀 Como usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o programa

```bash
python main.py
```

### 3. Escolher opções

O programa irá perguntar:
- **Qual planeta simular**: Mercúrio, Vênus, Marte, Júpiter, Saturno, Urano ou Netuno
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

## 🪐 Comparações

Os parâmetros orbitais são calculados dinamicamente via Astropy (`get_body_barycentric_posvel`) usando as efemérides embutidas no époco J2000, em vez de valores fixos no código.

| Planeta   | Semi-eixo ref. (UA) | Astropy (UA) | Exc. ref. | Astropy | Período ref. (dias) | Astropy (dias) |
|-----------|:-------------------:|:------------:|:---------:|:-------:|:-------------------:|:--------------:|
| Mercúrio  | 0.387               | 0.394        | 0.2056    | 0.1965  | 87.97               | 90.26          |
| Vênus     | 0.723               | 0.739        | 0.0068    | 0.0173  | 224.7               | 231.89         |
| Marte     | 1.524               | 1.505        | 0.0934    | 0.0867  | 686.98              | 674.47         |
| Júpiter   | ---                 | 5.177        | ---       | 0.0459  | ---                 | 4302.52        |
| Saturno   | ---                 | 9.514        | ---       | 0.0530  | ---                 | 10718.86       |
| Urano     | ---                 | 19.206       | ---       | 0.0483  | ---                 | 30742.77       |
| Netuno    | ---                 | 30.057       | ---       | 0.0068  | ---                 | 60187.71       |

As diferenças existem porque o TCC usa **elementos médios** (médias de longo prazo) enquanto o Astropy calcula **elementos osculadores instantâneos** no époco J2000 - ambos são fisicamente corretos e representam a mesma órbita em contextos diferentes.

## 🎓 Conceitos

- **Órbita elíptica**: Trajetória natural dos planetas ao redor do Sol
- **Série de Fourier**: Método matemático para aproximar funções periódicas usando senos e cossenos
- **Termos de Fourier**: Quanto mais termos, melhor a aproximação
- **Elementos osculadores**: Parâmetros orbitais instantâneos calculados a partir dos vetores de posição e velocidade
- **Elementos médios**: Parâmetros tabelados que representam a órbita média filtrada de perturbações gravitacionais
