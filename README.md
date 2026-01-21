# World of Structure

Projeto realizado durante a disciplina de Estrutura de Dados I - Sistemas e Mídias Digitais (UFC).

## Sobre o projeto

O projeto é um protótipo de um RPG de turno, usando elementos de Tormenta e com sistema de combate em turnos.

### Tecnologia
Feito utilizando Tauri, que faz a comunicação e preocupação com a geração da aplicação em desktop. Frontend utilizando React e a engine (motor) utilizando Python.

<img src="https://github.com/ingrydf12/tormstructure-rpg/blob/rework/docs/projeto.png?raw=true">
<br>

A estrutura do projeto se basea em 3/4 estrutura de dados* que foram definidas como:
- Árvore AVL: Inventário de itens
- Pilha: Histórico de ações / avanço do player
- Fila / Lista: Ações durante combate de turno
- Grafo: Andamento de narrativa e decisão.

<b>Nota:</b> A estrutura de Grafo não foi passada durante a disciplina, mas foi necessária pro gancho narrativo. Feita com adaptações, para que pudesse suportar, uma ou duas opções.

Foi feito um <b>mapa narrativo</b>, descrevendo as duas rotas possíveis a serem feitas, bem elementos mais fortes em alguns pontos.

<img src="https://github.com/ingrydf12/tormstructure-rpg/blob/rework/docs/estrutura_daniel.png?raw=true">


## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)
