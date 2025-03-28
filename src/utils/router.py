class Router:
    def __init__(self):
        self.pages = {
            "Home": self._load_home,
            # "Energia": self._load_energy,
            # "Ambiental": self._load_environmental
        }

    def navigate(self, page_name, data):
        """Carrega a página selecionada com os dados fornecidos"""
        if page_name in self.pages:
            self.pages[page_name](data)
        else:
            self._load_error_page()

    def _load_home(self, data):
        from views.home_view import HomeView

        view = HomeView()
        view.display(data)

    # def _load_energy(self, data):
    #     from views.energy_view import EnergyView
    #     view = EnergyView()
    #     view.display(data)

    # def _load_environmental(self, data):

    #     from views.environmental_view import EnvironmentalView
    #     view = EnvironmentalView()
    #     view.display(data)

    def _load_error_page(self):
        import streamlit as st

        st.error("Página não encontrada")
