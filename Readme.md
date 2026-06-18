# 🛡️ Posicionamento Ótimo de Ativos de Segurança (MVC)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NetworkX](https://img.shields.io/badge/networkx-%2300599C.svg?style=for-the-badge&logo=python&logoColor=white)

**Autores:** Yan Teixeira e Arthur Ramos  
**Projeto:** Análise de Algoritmos (DCC606) - Tema 12

**Orientador:** Herbert Oliveira 


---

## 📌 O que foi feito?
Desenvolvemos uma solução em **Python 3** utilizando **Algoritmos Genéticos** para resolver o problema da Cobertura Mínima de Vértices (MVC). 

A aplicação prática visa encontrar a forma mais barata e eficiente de espalhar câmeras de segurança (ou viaturas) por uma cidade, garantindo que **absolutamente todas as ruas sejam vigiadas** usando o menor número de câmeras possível.

---

## ⚙️ Como funciona?
O algoritmo gera possíveis soluções (cromossomos) onde cada gene representa um cruzamento da cidade (1 = com câmera, 0 = sem câmera). Ele evolui através de:
* **Seleção por Torneio:** Escolhe as melhores distribuições de câmeras.
* **Crossover e Mutação:** Mistura as ideias para achar posições melhores.
* **Reparo Heurístico (O diferencial):** Se o algoritmo criar uma solução falha (onde uma rua fica sem vigia), o nosso reparo age na mesma hora: ele instala uma câmera no cruzamento que conecta o maior número de ruas, maximizando o custo-benefício da prefeitura.

---

## 🧮 O Cálculo
O objetivo (Fitness) é simplesmente **minimizar a soma de câmeras instaladas**.

Para comprovar que o algoritmo realmente acha a solução ideal ou chega muito perto dela nos testes de estresse (DIMACS), usamos a regra matemática de que a Cobertura Mínima de um grafo equivale ao total de vértices menos o Conjunto Independente Máximo:

$$MVC(G) = |V| - MaxClique(\overline{G})$$

---

## 🚀 Como testar na sua máquina

**1. Instale as dependências:**
```bash
pip install networkx matplotlib numpy
