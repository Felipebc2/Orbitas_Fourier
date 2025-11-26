#!/usr/bin/env python3
"""
CLI para plotagem de órbitas relativas entre corpos celestes usando Astropy
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric
from astropy.time import Time


def orbita(a=2, b=3, start="1966-08-30", end="2025-08-30"):
    """
    Plota a órbita relativa entre dois corpos celestes.
    
    Args:
        a: Índice do primeiro corpo celeste
        b: Índice do segundo corpo celeste
        start: Data de início (formato: "YYYY-MM-DD")
        end: Data de fim (formato: "YYYY-MM-DD")
    """
    ephemeris = 'de430'
    solar_system_ephemeris.set(ephemeris)
    corpos_solares = solar_system_ephemeris.bodies
    
    body2 = corpos_solares[a]
    body3 = corpos_solares[b]
    
    print(f"\n📍 Corpo 1: {body2}")
    print(f"📍 Corpo 2: {body3}")
    print(f"📅 Período: {start} até {end}")
    
    freq = 'D'
    times = pd.date_range(start=start, end=end, freq=freq)
    ts = Time(times)
    
    print(f"\n🔄 Calculando posições dos corpos celestes...")
    coordinates2 = get_body_barycentric(body2, ts)
    coordinates3 = get_body_barycentric(body3, ts)
    
    x2, y2, z2 = coordinates2.get_xyz() / 10**6
    x3, y3, z3 = coordinates3.get_xyz() / 10**6
    
    # Plotar órbita relativa
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(x2 - x3, y2 - y3, linewidth=2, color='blue', label=f'{body2} relativo a {body3}')
    ax.plot(0, 0, 'o', color='red', markersize=12, label=f'{body3} (centro)')
    
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f'Órbita Relativa: {body2} em relação a {body3}\n{start} a {end}', fontsize=16)
    ax.set_xlabel('X (milhões de km)', fontsize=12)
    ax.set_ylabel('Y (milhões de km)', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print('✅ Simulação concluída!')


def main():
    """Interface de linha de comando principal"""
    print("=" * 70)
    print("🌌 Simulação de Órbitas Relativas - Astropy Ephemerides 🌌")
    print("=" * 70)
    print()
    
    # Configurar ephemeris
    ephemeris = 'de430'
    solar_system_ephemeris.set(ephemeris)
    corpos_solares = solar_system_ephemeris.bodies
    
    # Listar corpos disponíveis
    print("Corpos celestes disponíveis:")
    for i, corpo in enumerate(corpos_solares):
        print(f"  {i}. {corpo}")
    print()
    
    # Escolher primeiro corpo
    while True:
        try:
            choice = input(f"Escolha o primeiro corpo (0-{len(corpos_solares)-1}): ").strip()
            corpo_idx_1 = int(choice)
            
            if 0 <= corpo_idx_1 < len(corpos_solares):
                corpo_1 = corpos_solares[corpo_idx_1]
                break
            else:
                print(f"!! Erro: Opção inválida! Escolha entre 0 e {len(corpos_solares)-1}.")
        except ValueError:
            print("!! Erro: Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            return
    
    print(f"\n✓ Primeiro corpo: {corpo_1}")
    
    # Escolher segundo corpo
    while True:
        try:
            choice = input(f"Escolha o segundo corpo (0-{len(corpos_solares)-1}): ").strip()
            corpo_idx_2 = int(choice)
            
            if 0 <= corpo_idx_2 < len(corpos_solares):
                corpo_2 = corpos_solares[corpo_idx_2]
                if corpo_idx_1 == corpo_idx_2:
                    print("!! Erro: Escolha um corpo diferente do primeiro!")
                    continue
                break
            else:
                print(f"!! Erro: Opção inválida! Escolha entre 0 e {len(corpos_solares)-1}.")
        except ValueError:
            print("!! Erro: Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            return
    
    print(f"✓ Segundo corpo: {corpo_2}")
    print()
    
    # Escolher data de início
    while True:
        try:
            start_date = input("Data de início (YYYY-MM-DD) [padrão: 1966-08-30]: ").strip()
            if not start_date:
                start_date = "1966-08-30"
            # Validar formato
            pd.to_datetime(start_date)
            break
        except:
            print("!! Erro: Formato de data inválido. Use YYYY-MM-DD.")
        
    # Escolher data de fim
    while True:
        try:
            end_date = input("Data de fim (YYYY-MM-DD) [padrão: 2025-08-30]: ").strip()
            if not end_date:
                end_date = "2025-08-30"
            # Validar formato
            pd.to_datetime(end_date)
            break
        except:
            print("!! Erro: Formato de data inválido. Use YYYY-MM-DD.")
    
    print("\n🚀 Gerando simulação...")
    
    # Executar simulação
    try:
        orbita(corpo_idx_1, corpo_idx_2, start_date, end_date)
        print("\n✨ Feche a janela do gráfico para sair.")
    except Exception as e:
        print(f"\n!! Erro ao gerar simulação: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

