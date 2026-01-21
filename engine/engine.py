from class_infos import CLASS_INFOS
from engine_input_reading import ler_input
from narrative_tree import AdaptativeGraphNarrative, Branch
from player import Player
from combat import CombatLoop
from enemy import Enemy

def enviar_comando(comando: str, dado: str = ""):
    if dado:
        print(f"{comando}::{dado}", flush=True)
    else:
        print(comando, flush=True)

def escolher_caminho(no):
    escolha = ler_input()

    if escolha in no.choices:
        return no.choices[escolha]

    enviar_comando("ESCOLHA_INVALIDA")
    return None

def evento_combate(enemy, destino_vitoria):
    def _evento(player):
        enviar_comando("INICIO_DE_COMBATE")
        combate = CombatLoop(enemy)
        
        player.current_combat = combate
        player.in_battle = True
        
        def ao_vencer(p):
            p.move_to(destino_vitoria)
            
        combate.branch_vitoria = ao_vencer 
        
        combate.start(player)
    return _evento

def main_loop(player):
    processar_jogo(player, None)

    while True:
        entrada = ler_input()
        if not entrada: continue

        if player.in_battle:
            if entrada.startswith("COMBAT_CHOICE::"):
                partes = entrada.split("::")
                if len(partes) >= 3:
                    player.current_combat.step(player, partes[1], partes[2])
                    
                    if not player.in_battle:
                        processar_jogo(player, None) 
                continue

        processar_jogo(player, entrada)

def processar_jogo(player, entrada):
    no_atual = player.current_branch

    if entrada is None:
        no_atual.emitir_no()
        
        if no_atual.is_leaf():
            player.end_run()
            player.emitir_runs() 
            enviar_comando("FIM_DA_NARRATIVA")
            return

        enviar_comando("AGUARDANDO_ESCOLHA")
        player.aguardando_escolha = True
        return

    if entrada not in no_atual.choices:
        enviar_comando("ESCOLHA_INVALIDA")
        return

    escolha = no_atual.choices[entrada]
    player.aguardando_escolha = False

    if escolha.evento:
        escolha.evento(player)
        return

    if escolha.target:
        player.move_to(escolha.target)
        
        processar_jogo(player, None) 
        return

def run_game(nome_inicial=None, classe_inicial=None):
    if nome_inicial:
        nome = nome_inicial
    else:
        enviar_comando("INPUT", "NOME_HEROI")
        nome = ler_input()

    if classe_inicial:
        classe = classe_inicial
    else:
        enviar_comando("CLASSES_DISPONIVEIS", ",".join(CLASS_INFOS.keys()))
        classe = ler_input()

    if classe not in CLASS_INFOS:
        enviar_comando("ERRO", "Classe inválida")
        return

    # inicialização do player e da "árvore" narrativa
    player = Player(name=nome, class_type=classe)

    tree = AdaptativeGraphNarrative()

    # Inicializacao dos eventos de combate e os inimigos de cada um (tem 1 inimigo pra cada rota)
    bandido = Enemy("Bad Archer")
    ogro = Enemy("Orc Rei")

    # MARK: - Nós pós-combate
    ## Final Ogro
    final_rota_ogro = Branch(
        titulo="Como você quer terminar?",
        narrativa="Em sua frente está o ogro derrotado. Ele parece estender a mão em sua direção, mas você não tem certeza se ele está ainda tentando lutar ou pedindo por piedade. Você acaba com ele ou o poupa?",
    )

    poupar_ogro = Branch(
        titulo="Vou te poupar.",
        narrativa="Você aponta sua arma em direção a ele, espera por alguns segundos e então decide poupá-lo. Ele não parece agradecer e então desmaia. Por precaução, você parte o porrete dele e o deixa ali no chão.",
    )

    acabar_ogro = Branch(
        titulo="Você teve sua chance",
        narrativa="Você aponta sua arma em direção a ele e sem hesitar desfere um único e mortal golpe. O ogro não revida e sua história acaba ali mesmo. Você pega o porrete dele e segue em frente.",
    )

    tree.connect(origin=final_rota_ogro, key="1", texto="Poupar", target=poupar_ogro)
    tree.connect(
        origin=final_rota_ogro, key="2", texto="Acabar com ele", target=acabar_ogro
    )

    ## Final Bandido

    final_rota_bandido = Branch(
        titulo="Como você quer terminar?",
        narrativa="Em sua frente está o arqueiro derrotado. Ele parece estender a mão em sua direção, mas você não tem certeza se ele está ainda tentando lutar ou pedindo por piedade. Você acaba com ele ou o poupa?",
    )

    poupar_bandido = Branch(
        titulo="Vou te poupar.",
        narrativa="Você aponta sua arma em direção a ele, espera por alguns segundos e então decide poupá-lo. Ele não parece agradecer e então desmaia. Por precaução, você parte o arco dele e o deixa ali no chão da floresta.",
    )

    acabar_bandido = Branch(
        titulo="Você teve sua chance.",
        narrativa="Você aponta sua arma em direção a ele e sem hesitar desfere um único e mortal golpe. O arqueiro não revida e sua história acaba ali mesmo. Você pega o arco dele e segue em frente.",
    )

    combate_bandido = evento_combate(bandido, final_rota_bandido)
    combate_ogro = evento_combate(ogro, final_rota_ogro)

    tree.connect(
        origin=final_rota_bandido, key="1", texto="Poupar", target=poupar_bandido
    )
    tree.connect(
        origin=final_rota_bandido,
        key="2",
        texto="Acabar com ele",
        target=acabar_bandido,
    )

    # Criando a estrutura narrativa
    raiz = tree.create_root(
        titulo="Início",
        narrativa=f"""
Em uma vasta floresta amazônica, vinhas esverdeadas e névoas densas preenchem o ambiente. você, {player.name}, é um {player.class_type}, nascido nas Américas, aceitou um desafio de explorar terras estrangeiras, mas, por algum motivo, capangas atacaram o seu barco e te levaram a outro local sem que você conseguisse se defender. Ao acordar, uma luz de fim de tarde fracamente ilumina as árvores acima. Para todos os lados, existem vagalumes esverdeados cobertos pela névoa, mas do seu lado esquerdo, você enxerga uma luz amarelada, enquanto que em suas costas parece existir um caminho mais abaixo na floresta, mas levemente escurecido. Para onde você decide ir?
""",
    )

    #  MARK: -  Nivel 1
    luz = Branch(
        titulo="A luz",
        narrativa="Você caminha um pouco, com cautela, pois você passa por um pequeno riacho de correnteza calma e pedras lisas. Água limpa corre nele. Do outro lado da margem, você vê uma casa de madeira, a porta está entreaberta e aquela luz anterior certamente vinha dela. Você vai investigar a casa ou seguir a trilha próxima a ela?",
    )

    rota_ogro = Branch(
        titulo="Floresta abaixo",
        narrativa="Você desce o barranco com cuidado, você vê alguns cipós acima da sua cabeça e utiliza eles para estabilizar a descida. Você chega à base do barranco e percebe que você chegou em um local que parece um pântano, a névoa ficou ainda mais espessa, mas do que você imaginava que sequer fosse possível e a sua frente você vê um trajeto, do lado dele, alguns dos equipamentos dos homens que o atacaram. Você investiga ou segue pela rota?",
    )

    tree.connect(origin=raiz, key="1", texto="Seguir pela luz", target=luz)

    tree.connect(
        origin=raiz, key="2", texto="Seguir a floresta abaixo", target=rota_ogro
    )

    #  MARK: - Nível 2
    casa = Branch(
        titulo="Investigando a casa do bosque",
        narrativa="Você se aproxima devagar, caminhando levemente para não fazer tantos barulho ao pisar nas tábuas que rangem com o seu peso. Abre a porta e tenta chamar alguém. Nenhuma resposta, mas você percebe que o cômodo está revirado, alguns móveis estão caídos e uma janela, ao lado de uma cômoda com um pequeno rádio a pilha foi estilhaçada. Ao lado da janela, um homem está deitado, ferido, com a mão no ombro esquerdo. Você o ajuda ou foge?",
    )

    floresta = Branch(
        titulo="A floresta",
        narrativa="Você rapidamente avança pelo bosque, pois antes que se desse conta a noite começou a cair. A floresta que antes parecia misteriosa rapidamente tomou um tom sinistro e os vagalumes parecem ter sumido justo no momento em que a luz se tornou mais importante. Você para e tenta fazer algum tipo de iluminação ou procede pela mata na escuridão?",
    )

    tree.connect(origin=luz, key="1", texto="Investigar a casa", target=casa)

    tree.connect(origin=luz, key="2", texto="Seguir a trilha", target=floresta)

    #  MARK: - Nível 3
    ajuda_homem = Branch(
        titulo="'Decidi ajudar o homem ferido'",
        narrativa="Você avança rapidamente e logo está ao lado do homem. Ele tenta lhe falar algo, mas ele parece arrancar toda a força que possui apenas para permanecer consciente. Você vê que em seu ombro há uma grande hemorragia, provavelmente alguém o havia atacado. Nessas condições, não há mais como salvá-lo. Em seus últimos instantes, ele lhe diz apenas uma palavra: “Flecha”. Você fecha os olhos dele e então segue pelo caminho ao lado da casa.",
    )

    tree.connect(origin=casa, key="1", texto="Ajudar o homem", target=ajuda_homem)

    tree.connect(origin=casa, key="2", texto="Quero fugir", target=floresta)

    # MARK: - Nível 4
    tenta_iluminar = Branch(
        titulo="Tentando fazer uma iluminaçao decente.",
        narrativa="Você tenta procurar algum tipo de madeira, mas a maioria está úmida pela chuva da noite anterior e principalmente por conta da maldita névoa que não se dissipa. Depois de muito esforço, você consegue fazer uma pequena tocha. Não vai durar muito, mas vai ser útil. Você tenta fazer uma fogueira maior com essa tocha ou usa a iluminação dela para continuar caminhando",
    )

    floresta_escura = Branch(
        titulo="Vagando pela floresta escura",
        narrativa="Apenas com a pequena luz da tocha você caminha pela floresta, sem a trilha e com a pouca iluminação que lhe resta, a única coisa que lhe garante alguma coisa é a pura sorte. Contudo, justamente o oposto acontece: após um passo descuidado, você sente o chão ceder com o seu peso e então no instante seguinte você está tombando por um túnel que está lhe levando a sabe se lá onde no subterrâneo. Uma pancada forte e você está estirado no chão de uma caverna. Você se sente atordoado, mas uma pilha de carcaças amorteceu parte do impacto. Mas não há tempo para preocupações menores. Pois na sua frente, ameaçadoramente, um ogro lhe olha de cima para baixo. À batalha.",
    )

    tree.connect(
        origin=floresta_escura,
        key="1",
        texto="Avançar",
        target=None,
        evento=combate_ogro,
    )

    tree.connect(
        origin=floresta,
        key="1",
        texto="Tentar iluminar um pouco",
        target=tenta_iluminar,
    )

    tree.connect(
        origin=floresta, key="2", texto="Continuar caminhando", target=floresta_escura
    )

    # MARK: -  Rota do Bandido - Nível 5
    continuar_caminhando = Branch(
        titulo="Continuando a caminhada...",
        narrativa="A tocha queima rapidamente, cada segundo gasto é um segundo mais próximo das trevas lhe cercando. Você tenta procurar por mais madeira, junta uma patética quantidade, tenta fazer com que queimem, mas sem sucesso. A sua tocha apaga. Escuridão total. E o pior, você tem certeza que não está sozinho. 😳",
    )

    usar_tocha = Branch(
        titulo="Vou andar com a tocha",
        narrativa="Usando a luz criada pela tocha, você caminha pela floresta mais confidente, mas com a certeza que logo ela apagará. Primeiro você percebe um buraco na sua frente que desvia, em seguida usa as chamas para tentar afastar algo se movendo nos arbustos, talvez um lobo. Você não tem certeza, mas o mais importante, e talvez o mais assustador, um grande projétil vindo em sua direção. Você consegue iluminá-lo bem a tempo e desvia sem muito esforço. Estava apontado para o seu ombro. Quem disparou aquela flecha queria mais machucar do que apenas eliminá-lo. É então que um vulto desce da árvore e fica na sua frente. Um arqueiro encapuzado, frustrado por você ser o primeiro a desviar do ataque. À batalha!",
    )

    tree.connect(
        origin=tenta_iluminar,
        key="1",
        texto="Continuar caminhando",
        target=continuar_caminhando,
    )
    tree.connect(
        origin=tenta_iluminar,
        key="2",
        texto="Usar a tocha",
        target=usar_tocha,
        evento=combate_bandido,
    )

    #  MARK: - Rota do Bandido - Nível 6
    voce_nao_esta_sozinho = Branch(
        titulo="...Voce nao está sozinho",
        narrativa="No segundo que você chega a essa conclusão, você escuta um movimento nas árvores próximas, algo saltando entre elas, movendo-se rapidamente, leve como uma sombra, está claramente fixado em você. Até que subitamente para em uma instância ampla e depois relaxada. Então nesse momento você pensa “Flecha”. Você tenta bloquear ou sair do caminho?",
    )

    tree.connect(
        origin=continuar_caminhando,
        key="1",
        texto="Avançar",
        target=voce_nao_esta_sozinho,
    )

    #  MARK: - Rota do Bandido - Nível 7
    defender_flecha = Branch(
        titulo="Defender a flecha",
        narrativa="Em um reflexo rápido mas confiante, você impede que a enorme flecha lhe atinja no ombro, se tivesse lhe atingido, seria uma forma lenta e cruel de morrer. Mas a sua arma demonstrou-se forte o suficiente para não só aguentar o tranco, como também para enfrentar o homem encapuzado que agora está à sua frente, determinado a acabar com você aqui e agora! À batalha!",
    )

    tree.connect(
        origin=defender_flecha,
        key="1",
        texto="Avançar",
        target=None,
        evento=combate_bandido,
    )

    sair_caminho = Branch(
        titulo="Sair do caminho",
        narrativa="Em um movimento desajeitado e assustado, você sai do caminho da flecha no último segundo possível, ela passa raspando o seu ombro direito, e por pouco você escapa de um final cruel. Você tomba de lado, meio desajeitado, você tem quase certeza que deve ter torcido o tornozelo, mas não há tempo para choramingar. O inimigo está bem na sua frente e ele parece estar pronto para o combate! Recomponha-se, à batalha!",
    )

    tree.connect(
        origin=sair_caminho,
        key="1",
        texto="Avançar",
        target=None,
        evento=combate_bandido,
    )

    tree.connect(
        origin=voce_nao_esta_sozinho,
        key="1",
        texto="Sair do caminho",
        target=sair_caminho,
    )
    tree.connect(
        origin=voce_nao_esta_sozinho,
        key="2",
        texto="Defender a flecha",
        target=defender_flecha,
    )

    #  MARK: - Rota do ogro - Nível 2

    investigar_equipamento = Branch(
        titulo="Investigar equipamentos",
        narrativa="Ao aproximar-se você encontra alguns capacetes, alguns equipamentos, armas e cápsulas de bala no chão. Houve uma luta aqui, olhando mais em volta, você percebe que alguns passos, espaçados de maneira semi-aleatória seguiu adentro pelo pântano. Você decide segui-la.",
    )

    seguir_trajeto = Branch(
        titulo="Continuar trajeto",
        narrativa="Ao seguir pelo caminho, você encontra uma área curiosa, uma clareira. Em meio à região sombria do pântano, aquele local era bem iluminado e a neblina se reduzia em grande quantidade. Acima de você, a lua iluminava belamente as árvores, contudo, algo curioso lhe chama a atenção: um brilho vindo da mata. Primeiro um, depois, três, vários. Você fica parado esperando a aproximação ou se afasta?",
    )

    tree.connect(
        origin=rota_ogro,
        key="1",
        texto="Investigar equipamentos",
        target=investigar_equipamento,
    )
    tree.connect(
        origin=rota_ogro, key="2", texto="Continuar trajeto", target=seguir_trajeto
    )

    #  MARK: - Rota do ogro - Nível 3 -> Rota da Lua
    ficar_parado = Branch(
        titulo="Vou ficar parado.",
        narrativa="Lentamente o brilho se aproxima e então é possível identificá-los. Fogos fátuos! Criaturas encantadas que vagam durante a noite. Elas passam por você tranquilamente, praticamente ignorando sua presença. Mas então um dos fogos fátuos se aproxima e lhe diz algo rapidamente: “Saia daqui! Você está na zona de caça dele”, você fica confuso por um momento mas ele procede, “Já que você veio até aqui, a única saída é tentar passar justamente pelo covil, ao leste daqui, mas seja rápido. Acho que ele já está com fome outra vez.”  Então eles somem. Silêncio novamente. Você fica na clareira ou vai para um local mais isolado?",
    )

    se_afastar = Branch(
        titulo="Vou embora!",
        narrativa="Você decide sair da clareia e volta pela rota que você veio. Atrás de um tronco grande e caído você se esconde sem nenhum barulho e espera a grande multidão brilhante passar. Você então decide dormir ali mesmo. Encoberto pela escuridão, mas estranhamente não consegue ouvir o som de nenhum outro ser vivo. No meio da noite você vê uma grande criatura andando bem em frente ao tronco que você está escondido. Um calafrio desce a sua espinha. 😳\nNo dia seguinte, e já muito cansado de andar sem rumo, você continua pelo caminho e encontra a entrada de uma caverna, nela uma imensa criatura, um ogro, está olhando para você.Sem muito tempo para negociações ele imediatamente salta em você pronto para atacar. Coragem! À batalha!",
    )

    tree.connect(
        origin=se_afastar, key="1", texto="Avançar", target=None, evento=combate_ogro
    )

    tree.connect(
        origin=seguir_trajeto, key="1", texto="Ficar parado.", target=ficar_parado
    )
    tree.connect(origin=seguir_trajeto, key="2", texto="Me afastar", target=se_afastar)

    #  MARK: - Rota do ogro - Nível 3 -> Rota do Covil
    homem_covil = Branch(
        titulo="Seguir dentro do pantâno",
        narrativa="Você segue por um caminho mais discreto, por ali e percebe que aos poucos as pegadas vão sumindo, mas estranhamente, as cápsulas ainda estão presentes, como se o grupo estivesse sendo abatido aos poucos. Você prossegue e então percebe um covil a sua frente, na frente dele, há um homem que encostou-se ali. É um dos sequestradores que o atacou. Você se aproxima dele para tentar entender o que atacaria um grupo fortemente armado.",
    )

    tree.connect(
        origin=investigar_equipamento,
        key="1",
        texto="Seguindo dentro do pântano",
        target=homem_covil,
    )

    #  MARK: - Rota do ogro - Nível 4
    ficar_clareira = Branch(
        titulo="Quero ficar na clareira",
        narrativa="Você decide dormir na clareira, sob a luz da lua. Você pega no sono com dificuldade mas depois não tem mais problemas. A lua e as estrelas são as únicas olhando para você agora, não há mais ninguém. No dia seguinte, você segue o conselho do fogo fátuo e encontra um dos seus sequestradores feridos na entrada do covil. Você se aproxima dele ou o ignora?",
    )

    sair_clareira = Branch(
        titulo="Vou sair da clareira.",
        narrativa="Dado ao fato que a clareira estava muito iluminada, você prefere sair dela por receio de estar completamente exposto. Ali perto há um grande tronco escondido em uma área mais escura. Você decide ficar atrás dele, o escala devagar mas antes que consiga passar para o outro lado, algo lhe acerta na cabeça e você perde a consciência. Você acorda horas depois, em uma jaula. Na sua frente, um grande ogro faz alguma coisa que você não consegue compreender. Você tenta arrombar a jaula ou espera o momento de surpreendê-lo mais de perto?",
    )

    tree.connect(
        origin=ficar_parado, key="1", texto="Ficar na clareira.", target=ficar_clareira
    )
    tree.connect(origin=ficar_parado, key="2", texto="Me afastar", target=sair_clareira)

    # Convergëncia com o homem do covil - Direita - Clareira
    aproximar_homem_covil = Branch(
        titulo="Vou me aproximar.",
        narrativa="O homem está com a cabeça baixa e não parece responsivo quando você fala com ele. Ele não responde às suas perguntas e parece estar vivo apenas por um único fio de vida. Mas então ele levanta a cabeça e diz, em uma última tentativa de fazer algo digno, uma única palavra: “Atrás”. Em um ato reflexo, você sente algo e instintivamente agacha, apenas para ver uma grande mão passar onde o seu pescoço estava. Você rola, olha pra trás e ali está um grande ogro, aquele que o fogo fátuo falou. À batalha!",
    )

    ignorar_homem_ferido_covil = Branch(
        titulo="Não consigo lidar com isso agora",
        narrativa="Você ignora o homem à sua frente, olha em volta do covil, nada. Tenta abrir a porta devagar, mas então uma grande mão lhe agarra pelo pescoço e lhe lança para trás. Quando você se vira, um imenso Ogro pula em sua direção e tenta lhe acertar com um porrete. Você rola e então se levanta. Lute!",
    )

    tree.connect(
        origin=aproximar_homem_covil,
        key="1",
        texto="Avançar",
        target=None,
        evento=combate_ogro,
    )

    tree.connect(
        origin=ignorar_homem_ferido_covil,
        key="1",
        texto="Avançar",
        target=None,
        evento=combate_ogro,
    )

    tree.connect(
        origin=homem_covil,
        key="1",
        texto="Aproximar-se do homem ferido",
        target=aproximar_homem_covil,
    )
    tree.connect(
        origin=ficar_clareira,
        key="1",
        texto="Aproximar-se do homem ferido.",
        target=aproximar_homem_covil,
    )
    tree.connect(
        origin=ficar_clareira,
        key="2",
        texto="Ignorar homem",
        target=ignorar_homem_ferido_covil,
    )

    #  MARK: - Rota Ogro - Nível 5 - Rota da clareira - DIREITA
    arrombar_jaula = Branch(
        titulo="Vou arrombar a jaula!",
        narrativa="Usando a sua arma, você faz um movimento de alavanca e consegue quebrar a velha tranca que o mantinha preso. Cuidadosamente, você caminha devagar em direção ao ogro e percebe que ao lado dele há uma escada. Talvez esse seja o caminho indicado pelo fogo fátuo para fora dali? De todo modo, você terá que enfrentá-lo. À batalha!",
    )

    tentar_surpreender = Branch(
        titulo="Vou tentar surpreender",
        narrativa="Você espera várias horas, fingindo estar fraco e abatido, esperando o ogro abrir a jaula para tentar fazer algo com você. Então acontece: ele abre a jaula, você continua mole, e quando ele pega no seu braço e então você saca a sua arma e o ataca. Com a dor ele lança você contra a parede e então coloca a mão no ombro. Cambaleando, você se ergue, enquanto o ogro pega o seu porrete. Não há tempo para curativos. À batalha!.",
    )

    tree.connect(
        origin=arrombar_jaula,
        key="1",
        texto="Avançar",
        target=None,
        evento=combate_ogro,
    )

    tree.connect(
        origin=tentar_surpreender,
        key="1",
        texto="Avançar",
        target=None,
        evento=combate_ogro,
    )

    tree.connect(
        origin=sair_clareira, key="1", texto="Arrombar a jaula", target=arrombar_jaula
    )
    tree.connect(
        origin=sair_clareira,
        key="2",
        texto="Tentar surpreender",
        target=tentar_surpreender,
    )

    player.move_to(raiz)
    main_loop(player)
