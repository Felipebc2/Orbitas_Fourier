"""
Biblioteca para simulação de órbitas planetárias usando Série de Fourier
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris
from astropy.time import Time
from astropy import units as u
from astropy import constants as const


_PLANET_NAMES = {
    'Mercúrio': 'mercury',
    'Vênus':    'venus',
    'Marte':    'mars',
    'Júpiter':  'jupiter',
    'Saturno':  'saturn',
    'Urano':    'uranus',
    'Netuno':   'neptune',
}

_PLANET_COLORS = {
    'Mercúrio': 'gray',
    'Vênus':    'orange',
    'Marte':    'red',
    'Júpiter':  'peru',
    'Saturno':  'goldenrod',
    'Urano':    'lightblue',
    'Netuno':   'royalblue',
}


def _orbital_elements(body: str, epoch: Time) -> tuple:
    """Calcula (semi-eixo maior em UA, excentricidade, período em dias) a partir
    dos vetores de estado baricêntricos fornecidos pelo Astropy."""
    with solar_system_ephemeris.set('builtin'):
        pos, vel = get_body_barycentric_posvel(body, epoch)

    r_vec = pos.xyz.to(u.m).value
    v_vec = vel.xyz.to(u.m / u.s).value

    mu = (const.G * const.M_sun).to(u.m**3 / u.s**2).value

    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)

    # Semi-eixo maior via energia específica: ε = v²/2 − μ/r → a = −μ/(2ε)
    a_m = -mu / (v**2 - 2 * mu / r)
    a_au = (a_m * u.m).to(u.au).value

    # Excentricidade via vetor de Laplace-Runge-Lenz
    h_vec = np.cross(r_vec, v_vec)
    e_vec = np.cross(v_vec, h_vec) / mu - r_vec / r
    ecc = np.linalg.norm(e_vec)

    # Período via 3ª lei de Kepler: T = 2π√(a³/μ)
    period_days = (2 * np.pi * np.sqrt(a_m**3 / mu) * u.s).to(u.day).value

    return a_au, ecc, period_days


def _build_planet_data() -> dict:
    epoch = Time('J2000')
    data = {}
    for pt_name, body in _PLANET_NAMES.items():
        a, ecc, period = _orbital_elements(body, epoch)
        data[pt_name] = {
            'semi_major': a,
            'ecc': ecc,
            'period': period,
            'color': _PLANET_COLORS[pt_name],
        }
    return data


PLANET_DATA = _build_planet_data()


def calculate_real_orbit(semi_major, ecc, num_points=1000):
    """
    Calcula as coordenadas x e y de uma órbita elíptica.
    
    Args:
        semi_major: Semi-eixo maior da órbita (em UA)
        ecc: Excentricidade da órbita
        num_points: Número de pontos para calcular a órbita
        
    Returns:
        tuple: (x, y, r) - coordenadas cartesianas e raio
    """
    theta = np.linspace(0, 2 * np.pi, num_points)
    r = semi_major * (1 - ecc**2) / (1 + ecc * np.cos(theta))
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, r


def calculate_fourier_coefficients(x_real, y_real, num_terms):
    """
    Calcula os coeficientes de Fourier a_n, b_n, c_n e d_n
    a partir das coordenadas da órbita real.
    
    Args:
        x_real: Array com coordenadas x da órbita real
        y_real: Array com coordenadas y da órbita real
        num_terms: Número de termos da série de Fourier
        
    Returns:
        tuple: (a_n, b_n, c_n, d_n) - coeficientes de Fourier
    """
    num_points = len(x_real)
    time = np.linspace(0, 2 * np.pi, num_points)

    a_n = np.zeros(num_terms + 1)
    b_n = np.zeros(num_terms + 1)
    c_n = np.zeros(num_terms + 1)
    d_n = np.zeros(num_terms + 1)

    # Coeficientes para n = 0 (média)
    a_n[0] = np.mean(x_real)
    c_n[0] = np.mean(y_real)

    # Coeficientes para n > 0
    for n in range(1, num_terms + 1):
        a_n[n] = (2 / num_points) * np.sum(x_real * np.cos(n * time))
        b_n[n] = (2 / num_points) * np.sum(x_real * np.sin(n * time))
        c_n[n] = (2 / num_points) * np.sum(y_real * np.cos(n * time))
        d_n[n] = (2 / num_points) * np.sum(y_real * np.sin(n * time))

    return a_n, b_n, c_n, d_n


def reconstruct_fourier_orbit(a_n, b_n, c_n, d_n, num_terms, num_points=1000):
    """
    Reconstrói a órbita usando os coeficientes de Fourier.
    
    Args:
        a_n, b_n, c_n, d_n: Coeficientes de Fourier
        num_terms: Número de termos da série de Fourier
        num_points: Número de pontos para reconstruir a órbita
        
    Returns:
        tuple: (x_fourier, y_fourier) - coordenadas da órbita reconstruída
    """
    time = np.linspace(0, 2 * np.pi, num_points)
    x_fourier = a_n[0] * np.ones_like(time)
    y_fourier = c_n[0] * np.ones_like(time)

    for n in range(1, num_terms + 1):
        x_fourier += a_n[n] * np.cos(n * time) + b_n[n] * np.sin(n * time)
        y_fourier += c_n[n] * np.cos(n * time) + d_n[n] * np.sin(n * time)

    return x_fourier, y_fourier


def simulate_and_plot(planet_name, num_terms=3):
    """
    Função principal para simular e plotar as órbitas.
    
    Args:
        planet_name: Nome do planeta ('Marte', 'Vênus' ou 'Mercúrio')
        num_terms: Número de termos da série de Fourier (padrão: 3)
    """
    if planet_name not in PLANET_DATA:
        raise ValueError(f"Planeta '{planet_name}' não encontrado. Escolha entre: {list(PLANET_DATA.keys())}")
    
    pdata = PLANET_DATA[planet_name]

    # Gerar a órbita real
    x_real, y_real, r_real = calculate_real_orbit(pdata['semi_major'], pdata['ecc'])

    # Calcular os coeficientes de Fourier a partir da órbita real
    a_n, b_n, c_n, d_n = calculate_fourier_coefficients(x_real, y_real, num_terms)

    # Reconstruir a órbita de Fourier
    x_fourier, y_fourier = reconstruct_fourier_orbit(a_n, b_n, c_n, d_n, num_terms)

    # Plotar as órbitas
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x_real, y_real, label='Órbita Real', color=pdata['color'], linewidth=2)
    ax.plot(x_fourier, y_fourier, '--', label=f'Fourier ({num_terms} termos)', color='black', linewidth=2)
    ax.plot(0, 0, 'o', color='gold', markersize=10, label='Sol')

    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f'Órbitas de {planet_name} (Aproximação por Fourier)', fontsize=16)
    ax.set_xlabel('X (UA)')
    ax.set_ylabel('Y (UA)')
    ax.legend()
    ax.grid(True)
    plt.show()

