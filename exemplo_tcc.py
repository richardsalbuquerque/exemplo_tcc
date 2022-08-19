# Importando as bibliotecas necessárias

import numpy as np
import matplotlib.pylab as plt
import pynbody
from scipy.optimize import curve_fit

plt.rcParams.update({'font.size': 15})

# Carregando os arquivos que contém a simulação e o catálogo de halos, respectivamente

simulacao = pynbody.load('snapshot_070')

catalogo_halos = np.loadtxt('exemplo_perfil_NFW.ascii')

# Calculando a densidade crítica do Universo
densidade_critica = pynbody.analysis.cosmology.rho_crit(simulacao, z=None)

# Definindo os vetores com as posições em coordenadas retangulares, 
#          massa do halo e raio do halo / retirando os halos sem massa

m200c = catalogo_halos[:,27]
x     = catalogo_halos[:, 8][np.where(m200c>0)[0]]
y     = catalogo_halos[:, 9][np.where(m200c>0)[0]]
z     = catalogo_halos[:,10][np.where(m200c>0)[0]]
m200c = catalogo_halos[:,27][np.where(m200c>0)[0]]
rvir  = catalogo_halos[:, 4][np.where(m200c>0)[0]]

# Definindo os vetores com as posições em coordenadas retangulares, 
#          massa do halo e raio do halo / retirando os halos sem massa

m200c = catalogo_halos[:,27]
x     = catalogo_halos[:, 8][np.where(m200c>0)[0]]
y     = catalogo_halos[:, 9][np.where(m200c>0)[0]]
z     = catalogo_halos[:,10][np.where(m200c>0)[0]]
m200c = catalogo_halos[:,27][np.where(m200c>0)[0]]
rvir  = catalogo_halos[:, 4][np.where(m200c>0)[0]]

print(f'Digite um número entre 0 e {len(m200c)} para construir um perfil de densidade NFW')
i = int(input())

# Transladando o halo para o centro do Universo

halo_x = simulacao.dm['x'] - x[i]
halo_y = simulacao.dm['y'] - y[i]
halo_z = simulacao.dm['z'] - z[i]

# Excluindo as partículas que não pertencem ao halo

nao_percence_ao_halo = np.where(np.sqrt(halo_x**2 + halo_y**2 + halo_z**2) < rvir[i]/1000)
halo_x = halo_x[nao_percence_ao_halo]
halo_y = halo_y[nao_percence_ao_halo]
halo_z = halo_z[nao_percence_ao_halo]

# Definindo que o centro do halo também é o centro do Universo que foi transladado

centro_halo_x = 0
centro_halo_y = 0
centro_halo_z = 0

# Calculando a densidade média e o raio médio, em escala logarítmica

numero_cascas_esfericas = 30           # Definindo a quantidade de cascas esféricas [pode ser alterado].
raio_maximo             = rvir[i]/1000 # Mpc [mesma unidade de (x, y, z)]
densidade               = []           # Esse vetor será preenchido com a densidade média das cascas esféricas 
raio1_log               = 0.005        # Esse é o logaritmo do primeiro raio


passo_entre_raio1_e_raio2 = np.log10(raio_maximo/raio1_log) / numero_cascas_esfericas # Definindo a distância entre 
                                                                                      #    as cascas esféricas
raio_medio_log            = []                                                        # Raio médio entre as cascas
distancia_do_centro       = np.sqrt(halo_x**2 + halo_y**2 + halo_z**2)                # Distância de cada partícula
                                                                                      #    ao centro do halo
# O 'for' no Python é utilizado para realização de processos repetitivos     
for n in range(0,numero_cascas_esfericas):     # Repete os cálculos de acordo com a quantidade de cascas esféricas
    
    raio2_log = 10**( np.log10( raio1_log ) + passo_entre_raio1_e_raio2 ) # O raio 2, da casca esférica,
                                                                          #     é o raio 1  mais um passo
    
    raio_medio_log.append(  ( raio2_log + raio1_log )/2  )          # O raio médio é a média entre o raio 1 e o 2,
                                                                    #      em escala logatimica
        
    volume_casca_esferica = ( 4/3 ) * np.pi * ( raio2_log**3 - raio1_log**3 ) # Volume entre os raios 1 e 2
    
    # Abaixo calculo a quantidade de partículas contidas na casca esférica        
    quantidade_particulas = len(np.where( (distancia_do_centro > raio1_log)&(distancia_do_centro <= raio2_log) )[0] )
    
    massa_casca_esferica = quantidade_particulas * simulacao.dm['mass'][0] # A massa da casca esférica é a 
                                                                           #     quantidade de partículas contidas
                                                                           #     entre o raio 1 e 2 vezes
                                                                           #     a massa de cada partícula
                
    densidade.append(massa_casca_esferica/volume_casca_esferica)    # Carregando o vetor densidade
    raio1_log = raio2_log    # Evoluindo o valor de raio 1

# Correção das unidades
densidade      = np.array(densidade)*((3.0856778570831*10**24)**-3)*(1.989*10**33)*10**10 #  h^2 g/cm^3
raio_medio_log = 1000*np.array(raio_medio_log) # h^-1 kpc

# Ajuste do perfil de densidade radial de Navarro–Frenk–White

def func(r, rho_s, r_s):
        return rho_s/((r/r_s)*(1 + r/r_s)**2) # Formato funcional do perfil

    
parametros, cov = curve_fit(func, raio_medio_log, densidade, p0 = [1e-26, 60], sigma = densidade) # Necessário para
                                                                                                # realizar o ajuste
rho_s   = parametros[0]   # Parâmetro ajustado
r_s     = parametros[1]   # Parâmetro ajustado

ajuste_nfw_x   = np.linspace(raio_medio_log[0], raio_medio_log[-1],1000) # Vetor criado para construir o gráfico
ajuste_nfw_y   = func(ajuste_nfw_x, rho_s, r_s)                          # Vetor criado para construir o gráfico

# Gerando o gráfico do perfil de densidade radial de Navarro–Frenk–White

fig, ax = plt.subplots(figsize=(10, 7))

plt.scatter(raio_medio_log[::2], densidade[::2], color='red')                       # Pontos vermelhos
plt.plot(ajuste_nfw_x, ajuste_nfw_y, color='blue', label='Ajueste do perfil NFW')   # Curva azul

plt.title(f'Perfil de densidade do halo {i}')
plt.xlabel('R [h$^{-1}$ kpc]')
plt.ylabel('ρ [h${^2}$ g cm$^{-3}$]')
plt.xscale("log")   # Escala logarítmica
plt.yscale("log")   # Escala logarítmica
plt.legend(loc='upper right')
plt.show()

# Estatísticas avançadas

print('ESTATÍSTICAS AVANÇADAS')
print(f'A massa do halo escolhido é: {np.around(m200c[i]/0.67):.2e} M_sol')
print(f'O raio do halo escolhido é: {np.around(rvir[i]/0.67)} kpc')
print(f'O parâmetro de concentração do halo escolhido é: {np.around(rvir[i]/r_s, 2)}')
porcentagem_massa = m200c[i]*100/(np.sum(simulacao.dm['mass'])*10**10)
print(f'Esse halo tem {porcentagem_massa:.2e}% da massa total da simulação')
porcentagem_volume = 100*(4/3)*np.pi*(rvir[i]/1000)**3/10**3
print(f'Esse halo tem {porcentagem_volume:.2e}% do volume total da simulação')
print('')
print('Tenha um bom dia!')
