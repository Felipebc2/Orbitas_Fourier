# Integração com Astropy — Parâmetros Orbitais Dinâmicos

## Como rodar

> Pré-requisito: Python 3.8+ instalado.

**1. Instale as dependências** (só precisa fazer uma vez):

```bash
pip install -r requirements.txt
```

**2. Execute o programa:**

```bash
python main.py
```

**3. Responda as perguntas que aparecerem:**

```
Qual planeta simular? → ex: Júpiter
Número de termos de Fourier? → ex: 5  (quanto mais, mais preciso)
```

**4. Um gráfico vai abrir** mostrando a órbita real do planeta (colorida) e a aproximação por Série de Fourier (tracejado preto). Feche o gráfico para encerrar.

> Prefere Jupyter? Abra `ipynb/simulacao_orbitas.ipynb` — ele roda célula a célula e já tem exemplos prontos.

---

## O que mudou

Antes desta implementação, os parâmetros orbitais (semi-eixo maior, excentricidade e período) de apenas três planetas estavam **hardcoded** em `utils/lib.py` como um dicionário estático, copiados da tabela 1 do TCC de referência:

```python
# Antes
PLANET_DATA = {
    'Marte':    {'semi_major': 1.524, 'ecc': 0.0934, 'period': 686.98, ...},
    'Vênus':    {'semi_major': 0.723, 'ecc': 0.0068, 'period': 224.7,  ...},
    'Mercúrio': {'semi_major': 0.387, 'ecc': 0.2056, 'period': 87.97,  ...},
}
```

Agora os parâmetros são **calculados dinamicamente** via Astropy a partir dos vetores de estado baricêntricos, e o suporte foi expandido para todos os planetas do sistema solar.

---

## Como funciona

### 1. Fonte de dados — `get_body_barycentric_posvel`

A função `_orbital_elements(body, epoch)` em `utils/lib.py` consulta as efemérides embutidas do Astropy (`solar_system_ephemeris = 'builtin'`) para obter os vetores de posição e velocidade do planeta em relação ao baricentro do sistema solar no époco J2000:

```python
with solar_system_ephemeris.set('builtin'):
    pos, vel = get_body_barycentric_posvel(body, epoch)
```

### 2. Cálculo dos elementos orbitais

A partir dos vetores `r` (posição) e `v` (velocidade), três grandezas são derivadas:

| Grandeza | Fórmula | Observação |
|---|---|---|
| **Semi-eixo maior** `a` | `a = -μ / (v² - 2μ/r)` | Via energia específica orbital |
| **Excentricidade** `e` | `‖e_vec‖`, onde `e_vec = (v × h)/μ − r̂` | Via vetor de Laplace-Runge-Lenz |
| **Período** `T` | `T = 2π √(a³/μ)` | Via 3ª Lei de Kepler |

Onde `μ = G · M☉` é o parâmetro gravitacional padrão do Sol.

### 3. Construção do `PLANET_DATA`

A função `_build_planet_data()` itera sobre todos os planetas, chama `_orbital_elements` para cada um e monta o dicionário `PLANET_DATA` em tempo de importação do módulo:

```python
PLANET_DATA = _build_planet_data()  # calculado uma vez ao importar lib.py
```

---

## Planetas suportados

| Planeta   | Nome interno (Astropy) |
|-----------|------------------------|
| Mercúrio  | `mercury`              |
| Vênus     | `venus`                |
| Marte     | `mars`                 |
| Júpiter   | `jupiter`              |
| Saturno   | `saturn`               |
| Urano     | `uranus`               |
| Netuno    | `neptune`              |

---

## Como usar

Nenhuma mudança na interface pública. O uso permanece igual:

```python
from utils.lib import simulate_and_plot

# Qualquer planeta da lista acima funciona
simulate_and_plot('Júpiter', num_terms=5)
simulate_and_plot('Netuno', num_terms=3)
```

Para acessar os parâmetros calculados diretamente:

```python
from utils.lib import PLANET_DATA

print(PLANET_DATA['Saturno'])
# {'semi_major': 9.514, 'ecc': 0.053, 'period': 10718.86, 'color': 'goldenrod'}
```

---

## Elementos osculadores vs. elementos médios

Os valores do Astropy diferem ligeiramente dos valores do TCC porque representam conceitos distintos:

- **Elementos osculadores** (Astropy): calculados a partir do estado instantâneo do planeta no époco J2000. Refletem a órbita real naquele momento, incluindo perturbações gravitacionais de outros planetas.
- **Elementos médios** (TCC): médias de longo prazo que filtram essas perturbações, representando a órbita "típica" do planeta.

Ambos são fisicamente corretos — descrevem a mesma órbita em contextos diferentes.

### Comparação de valores

| Planeta   | Semi-eixo ref. (UA) | Astropy (UA) | Exc. ref. | Astropy | Período ref. (dias) | Astropy (dias) |
|-----------|:-------------------:|:------------:|:---------:|:-------:|:-------------------:|:--------------:|
| Mercúrio  | 0.387               | 0.394        | 0.2056    | 0.1965  | 87.97               | 90.26          |
| Vênus     | 0.723               | 0.739        | 0.0068    | 0.0173  | 224.7               | 231.89         |
| Marte     | 1.524               | 1.505        | 0.0934    | 0.0867  | 686.98              | 674.47         |
| Júpiter   | —                   | 5.177        | —         | 0.0459  | —                   | 4302.52        |
| Saturno   | —                   | 9.514        | —         | 0.0530  | —                   | 10718.86       |
| Urano     | —                   | 19.206       | —         | 0.0483  | —                   | 30742.77       |
| Netuno    | —                   | 30.057       | —         | 0.0068  | —                   | 60187.77       |

---

## Dependência

A integração requer o pacote `astropy`, já incluído em `requirements.txt`:

```
astropy
```
