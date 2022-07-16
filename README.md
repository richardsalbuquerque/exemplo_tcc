# Exemplo simples para construção de um perfil de densidade radial NFW, para um halo de matéria escura

Halos de matéria escura são estruturas em equilíbrio que estão gravitacionalmente ligadas, onde a densidade média de matéria escura é $200$ vezes a densidade crítica do Universo. Essas estruturas possibilitaram a formação de galáxias e aglomerados, que são os objetos mais luminosos encontrados no cosmos.
Podemos definir os halos como sendo uma região esfericamente simétrica com a densidade média, em um determinado redshift, igual a $200$ vezes a densidade crítica do Universo, $\bar{\rho}(z) = 200 \rho_{\rm crit}(z)$. A massa $M_{200}$ do halo está relacionada com o raio $r_{200}$ pela seguinte expressão:
\begin{equation}
    M_{200} = \frac{4 \pi}{3}r_{200}^3 200 \rho_{\rm crit}(z) ~,
\end{equation}
onde $M_{200}$ e $r_{200}$ também são conhecidos como a massa e o raio do virial, respectivamente. Como a densidade crítica do Universo, em um dado redshift, pode ser expressa por 
\begin{equation}
\rho_{\rm crit}(z) = \frac{3H^2(z)}{8 \pi G} ~,    
\end{equation}
podemos reescrever a equação da massa do virial como sendo:
\begin{equation}
    M_{200} = \frac{100 r_{200}^3 H^2(z)}{G} ~.
\end{equation}

Os halos de matéria escura provenientes das simulações numéricas podem ser caracterizados por um perfil radial de densidade, esfericamente simétrico, descrito pela seguinte relação \cite{navarro1997universal}:
%
\begin{equation}
    \rho (r) = \frac{\rho_s}{(r/r_s) (1 + r/r_s)^2} ~.  
    \label{eq_nfw}
\end{equation}
Onde, $r_s$ é um raio de escala e $\rho_s$ é um parâmetro adimensional de densidade característica \cite{navarro1997universal}. Analisando os valores extremos de $r_s$ no perfil NFW, temos que se $r << r_s$, o perfil se comporta como, $\rho \propto r^{-1}$ e se $r >> r_s$, então, $\rho \propto r^{-3}$. Portanto, $r_s$ é o raio que muda o formato da inclinação do perfil de densidade. 

