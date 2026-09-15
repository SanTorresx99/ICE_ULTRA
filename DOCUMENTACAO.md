# Documentação do Projeto - Painel de Ranking Dinâmico HTML (ICE & PETRA ULTRA)

Esta documentação descreve o estado atual do projeto de visualização HTML dinâmico no Power BI, detalhando as regras de negócio aplicadas, a arquitetura de arquivos TMDL e as soluções técnicas implementadas.

---

## 🚀 Arquitetura de Imagens e Performance (Base64)

Para contornar as restrições de segurança do Power BI com o protocolo `file:///` e garantir o funcionamento offline e em nuvem (Power BI Service), todas as imagens originais foram convertidas para strings Base64 e injetadas no modelo por meio de **medidas independentes** na tabela `Medidas_Ranking`:

* **`[PetraBase64]`**: Imagem da garrafa Petra Ultra com fundo transparente (redimensionada para 73 KB).
* **`[IceLimBase64]`**: Imagem da Ice Limão.
* **`[IceCajuBase64]`**: Imagem da Ice Caju (redimensionada de 3.6 MB para 79 KB).
* **`[IceFrAmBase64]`**: Imagem da Ice Frutas Amarelas.
* **`[IceFrVmBase64]`**: Imagem da Ice Frutas Vermelhas.
* **`[IceBase64]`**: Medida de compatibilidade que aponta por padrão para `[IceLimBase64]`.

---

## 🎨 Showcase 3D Dinâmico de Produtos

O painel esquerdo exibe as imagens das garrafas de acordo com a seleção de produto ativa no filtro (`OpcaoSel`):

1. **Ação Total (ICE + ULTRA - Opção 1)**:
   * Exibe as garrafas de **Ice Caju**, **Ice Frutas Vermelhas (FR.VM)** e a **Petra Ultra** em um carrossel 3D rotativo.
2. **Somente ICE (Opção 2)**:
   * Exibe **todos os 4 sabores** de Ice (Limão, Caju, Frutas Amarelas e Frutas Vermelhas) rotacionando em formato carrossel.
3. **Somente PETRA (Opção 3)**:
   * Exibe apenas a garrafa da **Petra Ultra com tamanho gigante (460px)** flutuando livremente com um brilho dourado premium.

### 🔄 Lógica do Carrossel 3D (CSS)
Para evitar que as garrafas extrapolassem os limites da tela (550px), o layout flexível linear foi substituído por posicionamento absoluto com **sobreposição de camadas no eixo X**.
A rotação contínua e a sensação de profundidade são controladas por um ciclo de animação CSS e atrasos (`animation-delay`) dessincronizados:
* A garrafa que rotaciona para o centro ganha luminosidade total (`brightness(1.05)`), aumenta de escala (`scale(1.15)`) e recebe uma sombra dourada brilhante (`drop-shadow` de 30px).
* As garrafas que se movem para as laterais encolhem (`scale(0.8)`), recuam no `z-index` e escurecem (`brightness(0.6)`), dando efeito de plano de fundo.

---

## 📊 Lista de Ranking e Linha Proporcional

O painel direito apresenta a lista dos vendedores com foco na legibilidade e proporcionalidade:

* **Posicionamento Vertical Inteligente**: O nome do vendedor agora fica posicionado **abaixo** de sua respectiva barra dourada. Isso liberou espaço horizontal, permitindo nomes longos sem cortes bruscos.
* **Proporcionalidade Estrita das Linhas**: O 1º colocado sempre terá 100% de preenchimento horizontal. Os demais colocados têm suas barras calculadas pela fórmula:
  $$\text{Largura} = \left(\frac{\text{Vendas do Vendedor}}{\text{Vendas do 1º Colocado}}\right) \times 100$$
* **Correção de Decimal (Bug de Locale)**: O Power BI Desktop em português formata decimais usando vírgulas (ex: `49,5%`), o que invalida regras de largura no CSS. Foi aplicada a correção via DAX utilizando `SUBSTITUTE(FORMAT(Pct, "0.0"), ",", ".")` para forçar o ponto decimal exigido pelos navegadores.
* **Otimização de Espaço (TOP 10)**: Badges e espaçamentos internos foram reduzidos para que o TOP 10 caibe integralmente na tela de 1240x680px sem a necessidade de rolagem.

---

## 🚀 Regras de Negócio e Dinâmicas do Rodapé (HTML)

Recentemente, foram adicionadas validações e indicadores dinâmicos ao rodapé do painel para refletir com mais precisão o progresso da equipe:

### 🏆 Critério Dinâmico de Parabenização
Para evitar parabenizações incorretas (como quando um supervisor é filtrado e possui poucas vendas totais), foi implementada uma validação condicional:
* **Condição**: Média de caixas vendidas por vendedor maior ou igual a **50** OU pelo menos um vendedor individual com vendas maior ou igual a **50**.
* **Resultado**: 
  * Se a condição for atendida, exibe a palavra **"PARABENS"**.
  * Se a condição não for atendida, exibe a mensagem de incentivo **"Vamos acelerar!"**.

### 👥 Indicador de Clientes Alcançados
O rodapé agora totaliza dinamicamente o número total de clientes únicos alcançados pela ação, respeitando a seleção de produto ativa:
* **Ação Total**: Utiliza a medida `[QTD CLI TOTAL ACAO]`.
* **Somente ICE**: Utiliza a medida `[TOTAL CLI ICE]`.
* **Somente Petra**: Utiliza a medida `[TOTAL PETRA ULTRA]`.

O formato final do rodapé consolidou-se em:
`Total da ação: X caixas — Y clientes alcançados — [Mensagem Condicional]`

---

---

---

## 📱 Versão HTML Mobile Verticalizada (Modo "Light Screen")

Com base nos mockups verticais incluídos (`Modelo_ICE.jpeg` e `Modelo_Ultra_Mobile.jpeg`), foi desenvolvida uma solução verticalizada focada na experiência de visualização por smartphones e telas portáteis:

### 🌟 Características da Versão Mobile:
1. **Modo "Light Screen" (Tema Claro Otimizado)**:
   * Desenvolvido especialmente para telas de celulares e ambientes com iluminação diurna.
   * Fundo claro suave (`#f1f5f9`), cartões brancos com elevação suave (`box-shadow`), tipografia de alto contraste (`#0f172a` / `#475569`).
   * Paleta temática adaptativa: Dourado quente para **Petra Ultra**, Rubi/Vermelho para **Crystal Ice**.
   * Inclui alternador interativo de tema (**☀️ Light / 🌙 Dark**) para comparação com os mockups escuros originais.

2. **Linhas Sutis de Campo de Futebol no Background**:
   * Marca d'água vetorial discreta (`opacity: 0.07`), elegante e sem poluição visual.
   * Reproduz geometricamente:
     * Linhas limites do campo com escanteios nos 4 cantos.
     * Linha de meio-campo com círculo central e ponto central.
     * Grande área e pequena área superior e inferior.
     * Marca da cal (pênalti) e meia-lua da grande área.
     * Traves e gols superior e inferior com detalhes sutis da rede em linhas pontilhadas.

3. **Repartição Dinâmica dos Vendedores em Lotes (Tabela de Liga / Futebol)**:
   * **Critério de Ativação**:
     * Se a quantidade de vendedores ativos for **$\ge 5$**, a divisão em 5 categorias é aplicada automaticamente.
     * Se a quantidade for **$< 5$** (ex: filtro por equipe/supervisor pequeno), os marcadores e divisores são **omitidos**, exibindo apenas o ranking limpo normal.
   * **As 5 Categorias Dinâmicas**:
     * 🏆 **G4 • Libertadores**: Top 4 colocados (1º ao 4º) com destaque nobre e vaga direta.
     * 🥈 **G-Nº • Pré-Libertadores**: 1/4 do total de vendedores (ex: até o G10 se forem 40 vendedores).
     * ⚽ **G-Nº • Sul-Americana**: 2/4 do total de vendedores (50% superior restante).
     * ⚠️ **Zona de Rebaixamento**: 3/4 do total de vendedores (alerta de perigo).
     * 🔻 **Série B • Rebaixados**: Últimos colocados (restante até o final, necessitam reagir).
   * **Marcadores Visuais**: Banners divisores de categoria estilizados com cores temáticas e selos em miniatura (*pills*) em cada linha de vendedor (`G4`, `Pré-Lib`, `Sula`, `Rebaixamento`, `Série B`).

4. **Padrão Verticalizado Fiel aos Mockups**:
   * **Header de Destaque**: Título "Ranking da Ação", nome do produto com efeito gradiente metálico e badge de período ("✦ Realizado dos dias 14/08 a 01/09 ✦").
   * **Showcase Hero com Garrafa Flutuante**: Garrafa do produto ativo com animação fluida de flutuação 3D, gotas de condensação e halo de brilho suave.
   * **Pódios e Medalhas (TOP 3)**:
     * 1º Lugar: Medalha de Ouro 🥇 com fita e linha destacada.
     * 2º Lugar: Medalha de Prata 🥈 com fita e linha destacada.
     * 3º Lugar: Medalha de Bronze 🥉 com fita e linha destacada.
     * 4º ao 15º: Badges circulares limpos.
   * **Tabela de Vendedores**: Colunas `#`, `Vendedor`, `Caixas` e `Posit.`, além de barra de progresso proporcional calculada com base no 1º colocado.
   * **2 Grandes Blocos de KPI**:
     * **Total de Caixas** com ícone temático de engradado (826 / 1.600 / 2.426).
     * **Total de Positivações** com gráfico de barras ascendente e seta 📈 (428 / 643 / 1.071).

5. **Lógica Dinâmica de Parabenização e Slogan**:
   * Validação condicional: Média >= 50 OU Venda Máxima >= 50.
   * Título: **"PARABÉNS A TODOS OS VENDEDORES!"** quando atingida a meta de incentivo, ou **"VAMOS ACELERAR!"** em caso contrário.
   * Slogan motivacional: `— Juntos somos mais fortes! —` em tipografia cursiva elegante (`Dancing Script` / `Caveat`).
   * Resumo de rodapé com total de caixas e clientes alcançados.

---

---

## 🏆 Tabelão Único Brasileirão - Página Completa PBIP (1280x720)

Para atender a demanda de acompanhamento pelas equipes de supervisores em tela cheia (formato padrão PBIP de **1280px de largura por 720px de altura**), foi desenvolvido um painel integrado em formato de tabela de classificação do Campeonato Brasileiro:

### 🌟 Especificações e Recursos:
1. **Background de Campo de Futebol Suave ("Verde Claro" & Discreto)**:
   * Fundo gradiente em verde suave de gramado (`#edf7ed` a `#e2efe4`), com listras verticais sutis de corte de grama (*mowing stripes*).
   * Marca d'água vetorial de campo de futebol em paisagem 1280x720 com linhas em branco e cinza suave (`opacity: 0.12`), traves laterais com rede pontilhada, grandes e pequenas áreas, círculos e arcos de escanteio.

2. **⚙️ 3 Motores de Cálculo do Ranking (Interativos)**:
   A classificação dos vendedores e a composição dos lotes esportivos podem ser alternadas dinamicamente entre 3 critérios:
   * **Motor 1: Volume de Produtos Vendidos (Caixas)**:
     * Ordenação decrescente pela quantidade total de caixas vendidas.
     * Barra proporcional dourada/verde relativa ao 1º colocado.
   * **Motor 2: Quantidade de Clientes Atingidos (Positivações)**:
     * Ordenação decrescente pelo número de clientes únicos positivados.
   * **Motor 3: % de Clientes Atingidos (Cobertura da Carteira)**:
     * Fórmula:
       $$\% \text{ Atingido} = \left(\frac{\text{Clientes Alcançados}}{\text{Clientes da Base}}\right) \times 100$$
     * Barra e badge com cores dinâmicas de performance:
       * **Verde ($\ge 40\%$)**: Alta cobertura de clientes.
       * **Âmbar ($25\% \text{ a } 39.9\%$)**: Média cobertura.
       * **Vermelho ($< 25\%$)**: Baixa cobertura / Alerta.

3. **Aproveitamento Total do Espaço Horizontal (1280px)**:
   * Colunas amplas e organizadas:
     * `#` (Posição com medalhas 🥇, 🥈, 🥉 e badges).
     * `Zona Brasileirão` (Tags proeminentes de classificação).
     * `Vendedor` (Nome completo sem cortes bruscos).
     * `Supervisor` (Identificação da equipe em tag cinza elegante).
     * `Volume (Cx)` (Volume numérico e barra proporcional).
     * `Clientes Posit.` (Quantidade de positivações).
     * `Base Clientes` (Tamanho da carteira cadastrada do vendedor).
     * `% Atingido Base` (Percentual de cobertura com mini-gauge).
     * `Status / Tag` (Tags dinâmicas de futebol ajustadas para 170px com fonte compacta 0.68rem e sem overlap: 🏆 **INVICTO**, ⚡ **MELHOR NO VOL**, 🎯 **CAMISA 10**, 🔥 **NO ATAQUE**, 🛡️ **EM JOGO**, 🏠 **PERDENDO EM CASA**, ❓ **CADÊ O TÉCNICO?**).

4. **Divisão Dinâmica em 5 Categorias do Brasileirão**:
   * Mantém a regra matemática estabelecida:
     * 🏆 **G4 • Libertadores**: Posições 1 a 4 (Classificação direta).
     * 🥈 **G-Nº • Pré-Libertadores**: 5º até $\approx 1/4$ do total (Ex: G14 em 54 vendedores).
     * ⚽ **G-Nº • Sul-Americana**: Até $\approx 2/4$ do total (Ex: G27 em 54 vendedores).
     * ⚠️ **Zona de Rebaixamento**: Até $\approx 3/4$ do total (Ex: Z41 em 54 vendedores).
     * 🔻 **Série B • Rebaixados**: Últimos colocados (restante).
5. **Alinhamento do Critério Oficial VEND-PED (RCA do Pedido)**:
   * **Objetivo**: Garantir que todo RCA que emitiu pedido faturado participe legitimamente do ranking oficial e das estatísticas apuradas.
   * **Critério de Inclusão**: O filtro considera todos os vendedores com vendas faturadas no período (`[@Sales] > 0`). Supervisores que também atuam comercialmente emitindo pedidos sob sua própria matrícula (como Ermeson Barbosa de Souza, 1º lugar geral com 169 caixas) são plenamente reconhecidos no ranking.
   * **Implementação**:
     * DAX: `FILTER(RawSellers, [@Sales] > 0)` aplicado em `[Ranking_Brasileirao_HTML]`, `[Ranking_Mobile_HTML]` e `[Ranking_Sellers_HTML]`.
     * Mockups JS: `.filter(s => s.sales > 0)`.
     * Suporte nos 3 visuais HTML à alternância dinâmica entre **Volume de Vendas (Caixas)** e **Quantidade de Clientes Positivados** via `Filtro_Ranking_Motor`.

6. **Arquitetura Responsiva e Alta Densidade de Visualização**:
   * **Responsividade Fluida 100% x 100%**:
     * Remove larguras e alturas fixas de pixel (`width: 100%; height: 100%; min-width: 920px; min-height: 540px;`).
     * Permite aumentar livremente as dimensões da página PBIP no Power BI (ex: $1600 \times 900$, $1920 \times 1080$ Full HD, ou páginas longas verticais como $1280 \times 1400$), ocupando todo o espaço sem cortes nem sobras brancas.
     * **Grid CSS Fluido**: Colunas principais usam `minmax(..., fr)` (como nome do vendedor e supervisor), expandindo proporcionalmente conforme a largura aumenta.
     * **Marca d'água Vetorial Escalável**: SVG com `preserveAspectRatio="none"` e coordenadas percentuais normalizadas, adaptando o desenho do gramado e traves a qualquer proporção de tela.
   * **Otimização de Espaço Vertical (Mais Vendedores na Tela)**:
     * Cabeçalho compacto reduzido para 56px e rodapé para 36px.
     * Altura de linha otimizada para ~32px (em vez dos ~48px anteriores).
     * **Capacidade de Visualização Simultânea**:
       * Em **720px**: de 6-7 vendedores visíveis para **17+ vendedores simultâneos** sem rolagem.
       * Em **900px**: **22+ vendedores simultâneos**.
       * Em **1080px (Full HD)**: **28+ vendedores simultâneos**.
       * Em **1400px (Página longa)**: **37+ vendedores simultâneos**.
     * Seletor interativo de densidade no mockup (`Compacto 17+` vs `Ultra 21+`).

7. **Estrutura de Páginas do Relatório PBIP**:
   * **`Ranking Geral`** (`1304 x 750`): Página widescreen com a tabela fluida do Brasileirão (`[Ranking_Brasileirao_HTML]`), ocupando 100% da área com alta densidade (17+ vendedores simultâneos), 3 motores de cálculo e coluna de Zona ampliada para 150px (zero overlap na tag *PRÉ-LIBERTADORES*).
   * **`Mobile`** (`720 x 1280`): Página verticalizada otimizada para smartphones (`[Ranking_Mobile_HTML]`) no modo light screen com divisões de zonas.
   * **`Rankin`** (`1280 x 720`): Visão desktop clássica com tabela à esquerda e cartazes/KPIs à direita (`[Ranking_Sellers_HTML]`).
   * **`Audit`** (`1280 x 720`): Página de conferência e auditoria de dados.
   * **`Info`** (`1280 x 720`): Instruções e regras da campanha.

---

## 🚀 Nova Campanha Comercial (Regras a partir de 01/09/2026)

Para a nova fase da campanha comercial, foi implementada uma arquitetura modular de isolamento histórico, preservando integralmente o fechamento oficial de Agosto/2026 e adicionando novas medidas e páginas dedicadas:

### 📦 Novos Produtos e Preços Mínimos de Corte:
1. **Crystal Ice**:
   * **Produtos Incluídos**: `16000`, `16001`, `200168`, `201670`, `201681`, `201910`.
   * **Preço Mínimo**: Preços a partir de **R$ 45,00** (`VLRUNITARIO >= 45.00`) entram no cálculo do volume (redução do corte anterior de R$ 53,00).
2. **Petra Ultra & Linha Especial**:
   * **Produto 16395 (Petra Ultra)**: Preço a partir de **R$ 65,40** (`VLRUNITARIO >= 65.40`) entra no volume (redução do corte anterior de R$ 73,00).
   * **Produto 15143**: Incluído no grupo com preço a partir de **R$ 51,08** (`VLRUNITARIO >= 51.08`).

### 🏛️ Preservação Histórica e Snapshot CSV de Agosto/2026:
* **Snapshot Oficial**: [`SNAPSHOT_FECHAMENTO_AGOSTO_2026.csv`](file:///C:/Users/a.alves/Downloads/ICE_ULTRA/SNAPSHOT_FECHAMENTO_AGOSTO_2026.csv) gerado previamente em UTF-8 com BOM e ponto-e-vírgula contendo o extrato auditado de todos os 64 vendedores, volumes e clientes de Agosto/2026 (2.320 caixas, 875 clientes únicos alcançados).
* **Páginas e Medidas de Agosto**: Mantidas inalteradas (`Ranking Geral`, `Mobile`, `Rankin`, `Audit`, `Info`), garantindo fidelidade aos bônus do RH e à apresentação executiva.

### ⚙️ Novas Medidas Modulares V2:
* `[QTD_ICE_PRECO_V2]`: Volume faturado dos 6 códigos de Ice com preço unitário $\ge$ R$ 45,00.
* `[QTD_P_ULTRA_PRECO_V2]`: Volume faturado do código 16395 ($\ge$ R$ 65,40) somado ao código 15143 ($\ge$ R$ 51,08).
* `[QTD_ACAO_ULTRACRYSTAL_V2]`: Volume consolidado da nova ação (`[QTD_ICE_PRECO_V2] + [QTD_P_ULTRA_PRECO_V2]`).
* `[TOTAL CLI ICE V2]`, `[TOTAL PETRA ULTRA V2]`, `[QTD CLI TOTAL ACAO V2]`: Contagem distinta de clientes positivados com as novas regras.
* `[Ranking_Brasileirao_HTML_V2]`, `[Ranking_Mobile_HTML_V2]`, `[Ranking_Sellers_HTML_V2]`: Visuais dinâmicos HTML atualizados apontando para as novas medidas e com período padrão a partir de 01/09/2026.

### 📑 Novas Páginas no Power BI PBIP:
1. **`Ranking Geral (Novo)`** (`1304 x 1150`): Tabela completa responsiva do Brasileirão com as regras V2 e 3 motores de cálculo.
2. **`Rankin (Novo)`** (`1280 x 720`): Visão desktop clássica com showcase 3D de garrafas e ranking horizontal proporcional com as novas regras V2.
3. **`Mobile (Novo)`** (`720 x 1280`): Painel verticalizado light screen para smartphones com divisões de zonas esportivas sob as regras V2.
4. **`Audit (Novo)`** (`1280 x 720`): Matriz de conferência analítica contendo os 8 códigos de produto e faixas de preço unitário faturadas a partir de 01/09/2026.

---

## 🛠️ Arquivos e Entregáveis
* [`SNAPSHOT_FECHAMENTO_AGOSTO_2026.csv`](file:///C:/Users/a.alves/Downloads/ICE_ULTRA/SNAPSHOT_FECHAMENTO_AGOSTO_2026.csv): Snapshot oficial auditado de fechamento de Agosto/2026.
* [`Dim_Calendario.tmdl`](file:///C:/Users/a.alves/Downloads/ICE_ULTRA/ICE_ULTRA.SemanticModel/definition/tables/Dim_Calendario.tmdl): Novas medidas de corte de volume V2.
* [`_Medidas_Winthor.tmdl`](file:///C:/Users/a.alves/Downloads/ICE_ULTRA/ICE_ULTRA.SemanticModel/definition/tables/_Medidas_Winthor.tmdl): Novas medidas de clientes e volume total V2.
* [`Medidas_Ranking.tmdl`](file:///C:/Users/a.alves/Downloads/ICE_ULTRA/ICE_ULTRA.SemanticModel/definition/tables/Medidas_Ranking.tmdl): Medidas HTML V2 para Desktop, Mobile e Brasileirão.
* [`pages.json`](file:///C:/Users/a.alves/Downloads/ICE_ULTRA/ICE_ULTRA.Report/definition/pages/pages.json): Registro e ordenação das páginas com destaque para as novas visualizações.




