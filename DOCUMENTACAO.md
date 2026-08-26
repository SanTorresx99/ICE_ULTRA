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

## 🛠️ Arquivos Alterados
* [`Medidas_Ranking.tmdl`](file:///C:/Users/a.alves/Downloads/ICE_ULTRA/ICE_ULTRA.SemanticModel/definition/tables/Medidas_Ranking.tmdl): Contém as medidas Base64, lógica do rodapé dinâmico de metas e clientes alcançados no visual `Ranking_Sellers_HTML`.
* [`DOCUMENTACAO.md`](file:///C:/Users/a.alves/Downloads/ICE_ULTRA/DOCUMENTACAO.md): Atualizado com as novas regras de negócio do rodapé dinâmico.
