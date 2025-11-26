#!/usr/bin/env python3
"""
Exemplo rápido de uso da biblioteca
"""
from utils.lib import simulate_and_plot

# Exemplo 1: Marte com 3 termos
print("🪐 Simulando Marte com 3 termos de Fourier...")
simulate_and_plot('Marte', num_terms=3)