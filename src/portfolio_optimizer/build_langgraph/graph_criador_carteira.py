from langgraph.graph import END, StateGraph, START
from .nodes_criador_carteira import analista_avaliador_peso_carteira, should_continue, analista_criador_carteira, verify_weight_sum, verifica_tics_selecionados
from ..state_otputs.state_criador_carteira import StateCarteira


class BuildGraphCriadorCarteira:
    def __init__(self):
        self.graph = StateGraph(StateCarteira)

    def build(self):
        self.graph.add_node("analista_criador_carteira", analista_criador_carteira)
        self.graph.add_node("verify_weight_sum", verify_weight_sum)
        self.graph.add_node("verifica_tics_selecionados", verifica_tics_selecionados)
        self.graph.add_node("analista_avaliador_peso_carteira", analista_avaliador_peso_carteira)
        self.graph.set_entry_point("analista_criador_carteira")
        self.graph.add_edge("analista_criador_carteira", "verify_weight_sum")
        self.graph.add_edge("verify_weight_sum", "verifica_tics_selecionados")
        self.graph.add_edge("analista_avaliador_peso_carteira", "analista_criador_carteira")
        self.graph.add_conditional_edges("verifica_tics_selecionados", should_continue, {
            "analista_avaliador_peso_carteira": "analista_avaliador_peso_carteira",
            "END": END
        })
        return self.graph

    def compile(self):
        return self.build().compile()