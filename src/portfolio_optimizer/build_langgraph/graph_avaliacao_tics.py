from langgraph.graph import END, StateGraph
from .nodes_avaliacao_tics import get_data_fundamentalistas, analista_fundamentalista, avaliador_analista_fundamentalista, should_continue
from ..state_otputs.state_classificacao_tics import StateClassification



class BuildGraphAvaliacaoTics:
    def __init__(self):
        self.graph = StateGraph(StateClassification)
        
    def build(self):
        self.graph.add_node("coleta_fundamentalistas", get_data_fundamentalistas)
        self.graph.add_node("analise_fundamentalista", analista_fundamentalista)
        self.graph.add_node("avaliacao_analise", avaliador_analista_fundamentalista)
        self.graph.set_entry_point("coleta_fundamentalistas")
        self.graph.add_edge("coleta_fundamentalistas", "analise_fundamentalista")
        self.graph.add_edge("analise_fundamentalista", "avaliacao_analise")
        self.graph.add_conditional_edges("avaliacao_analise", should_continue, {
            "END": END,
            "analise_fundamentalista": "analise_fundamentalista"
        })
        return self.graph
    
    def compile(self):
        return self.build().compile()
        
