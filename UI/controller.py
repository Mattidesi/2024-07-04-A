import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        years = self._model.getYears()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    def fillDDShapes(self,e):

        self._view.ddshape.options.clear()
        shapes = self._model.getShapes(self._view.ddyear.value)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        if self._view.ddyear.value is None or self._view.ddshape.value is None:
            self._view.txt_result1.controls.append(ft.Text("Inserisci una forma e un anno!", color='red'))
            self._view.update_page()
            return
        self._model.buildGraph(self._view.ddyear.value, self._view.ddshape.value)

        nNodes, nEdges = self._model.getGraphDetails()
        totConnesse = self._model.getTotConnesse()
        largestConnessa = self._model.largestConnessa()

        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nNodes}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.txt_result1.controls.append(ft.Text(f"il grafo ha: {totConnesse} componenti connesse"))

        self._view.update_page()

        for e in largestConnessa:
            self._view.txt_result1.controls.append(ft.Text(e))
            self._view.update_page()

    def handle_path(self, e):
        pass
