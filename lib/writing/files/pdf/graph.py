from typing import Tuple
from collections import deque
from reportlab.pdfgen import canvas
from reportlab.platypus import Flowable
from reportlab.lib import colors
from textwrap import wrap

from lib.parsing.Branch import Branch
from lib.parsing.Step import Step

import grandalf.graphs as gr
import grandalf.layouts as layouts
import grandalf.routing as routing

from lib.utils.graph import LearningTrackGraph

nodeTypeColorMap = {
    'quizStep': colors.Color(0.3, 0.75, 0.93),
    'learningActivityStep': colors.Color(0.2, 0.32, 0.8),
}

class NodeView(object):
    def __init__(self, width: int = 150, height: int = 50):
        self.w = width
        self.h = height


class GraphFlowable(Flowable):
    def __init__(self, graph: LearningTrackGraph, key_mapping:dict) -> None:
        """Initialises the GraphFlowable object, which is a Flowable object that can be added to a reportlab canvas.
        Uses the grandalf library to get the correct layout coordinates for the nodes and edges of the graph.
        Key mapping is needed to link the printed nodes to the correct step inside the pdf file.
        """
        
        super().__init__()
        self.lt_graph = graph
        self.width = 2000
        self.height = 4000
        self.default_node_width = 150
        self.default_node_height = 50
        self.key_mapping = key_mapping

        self.paddingX = 100
        self.paddingY = 100

        self.x_gap = self.default_node_width / 2
        self.y_gap = self.default_node_height / 2

        self.gr_nodes_dict = {}
        self.gr_edges = []

        # self.edges = []
        self._build_graph()

    def _build_graph(self) -> None:
        self._build_gr_nodes()
        self._build_gr_edges()
        self._set_gr_layout()
        self._translate_gr_coordinates()
        self._translate_gr_edges_to_node_center()
        self._flip_gr_y_coordinates()
        self._add_padding_to_gr_coordinates()
        self._set_width_and_height()
        # self._add_padding_to_gr_coordinates(100, 100)

        # for node in self.gr_nodes_dict.values():
        #     print(node.view.xy)
    
    def get_dimensions(self) -> Tuple[int, int]:
        return (self.width, self.height)
    
    def _set_width_and_height(self) -> None:
        """Sets the width and height of the graph flowable based on the coordinates of the nodes.
        Uses the nodes to get the max x and y coordinates of the graph visualisation."""
        max_x = max(node.view.xy[0] for node in self.gr_nodes_dict.values())
        max_y = max(node.view.xy[1] for node in self.gr_nodes_dict.values())
        self.width = max_x + self.default_node_width + self.paddingX
        self.height = max_y + self.default_node_height + self.paddingY
    
    def _set_gr_layout(self) -> layouts.SugiyamaLayout:
        """Sets the x, y coordinates of the nodes of the graph and adds edge lines using the grandalf library."""
        vertices = self.gr_nodes_dict.values()
        edges = self.gr_edges
        g = gr.Graph(vertices, edges)
        for v in vertices: v.view = NodeView()
        for e in edges: e.view = routing.EdgeViewer()
        layout = layouts.SugiyamaLayout(g.C[0])
        layout.xspace = self.x_gap
        layout.yspace = self.y_gap
        # layout.route_edge = routing.route_with_lines
        layout.init_all()
        layout.draw() # sets the x and y coordinates of the vertices
        # layout.draw_edges()
        return layout

    def _add_padding_to_gr_coordinates(self) -> None:
        """Adds padding to the x and y coordinates of the nodes and edges."""
        for node in self.gr_nodes_dict.values():
            node.view.xy = (node.view.xy[0] + self.paddingX, node.view.xy[1] + self.paddingY)

        for edge in self.gr_edges:
            for idx, point in enumerate(edge.view._pts):
                edge.view._pts[idx] = (point[0] + self.paddingX, point[1] + self.paddingY)

    def _flip_gr_y_coordinates(self) -> None:
        """Flips the y coordinates of the nodes and edges to conform to the reportlab coordinate system."""
        y_max = max(node.view.xy[1] for node in self.gr_nodes_dict.values())
        for node in self.gr_nodes_dict.values():
            node.view.xy = (node.view.xy[0], y_max - node.view.xy[1])

        for edge in self.gr_edges:
            for idx, point in enumerate(edge.view._pts):
                edge.view._pts[idx] = (point[0], y_max - point[1])

    def _translate_gr_edges_to_node_center(self) -> None:
        """Translate the edges to the center of the nodes
        ONLY WORKS IF ALL NODES HAVE THE SAME DIMENSIONS"""
        for edge in self.gr_edges:
            for idx, point in enumerate(edge.view._pts):
                edge.view._pts[idx] = (point[0] + self.default_node_width / 2, point[1] - self.default_node_height / 2)

    def _translate_gr_coordinates(self) -> None:
        """Translates the coordinates of the nodes and edges to start at (0, 0)."""
        min_x = min(node.view.xy[0] for node in self.gr_nodes_dict.values())
        min_y = min(node.view.xy[1] for node in self.gr_nodes_dict.values())

        for node in self.gr_nodes_dict.values():
            node.view.xy = (node.view.xy[0] - min_x, node.view.xy[1] - min_y)
        
        for edge in self.gr_edges:
            for idx, point in enumerate(edge.view._pts):
                edge.view._pts[idx] = (point[0] - min_x, point[1] - min_y)


    def _build_gr_nodes(self) -> None:
        # TODO no deque
        root_node = self.lt_graph.get_root_node()
        # self._add_other_node(root_node)
        
        queue = deque([root_node])
        
        while queue:
            node = queue.popleft()
            if node.id in self.gr_nodes_dict: # already added
                continue
            
            #if start or end node
            if node.id == 'end' or node.id == 'start':
                self._add_other_node(node)
            else:
                self._add_step_node(node)
                
            branches = self.lt_graph.get_child_branches(node.id)
            
            for idx, branch in enumerate(branches):
                # process branch 
                if branch.scoreRange is not None:
                  # if there is no score range, then there is no need for a branch node
                  self._add_branch_node(branch, node.id)


                # process child
                child = self.lt_graph.get_step_by_id(branch.childStepId)
                queue.append(child)


    def _add_branch_node(self, branch: Branch, parentId: str) -> None:
        scoreRange = branch.scoreRange
        id = (parentId, branch.childStepId, 0)
        while id in self.gr_nodes_dict:
            id = (parentId, branch.childStepId, id[2] + 1)

        text = f'{scoreRange.start} - {scoreRange.end}' if scoreRange.end != scoreRange.start else f'{scoreRange.start}'
        node = gr.Vertex({'id': id, 'text': text, 'link': None, 'type': 'branch'})
        self.gr_nodes_dict[id] = node
    
    def _add_other_node(self, node: Step) -> None:
        # start/end node
        text = node.title
        _node = gr.Vertex({'id': node.id, 'text': text, 'link': None, 'type': 'other'})
        self.gr_nodes_dict[node.id] = _node

    def _add_step_node(self, step: Step) -> None:
        # check if node already exists
        if step.id in self.gr_nodes_dict:
            return
        text = step.title
        link = step.id
        step_type = step.type
        node = gr.Vertex({'id': step.id, 'text': text, 'link': link, 'type': 'step', 'stepType': step_type})
        self.gr_nodes_dict[step.id] = node

    def _build_gr_edges(self) -> None:
        for id, node in self.gr_nodes_dict.items():
            if node.data['type'] == 'branch': 
                start_node_id = id[0]
                start_node = self.gr_nodes_dict[start_node_id]
                end_node_id = id[1]
                end_node = self.gr_nodes_dict[end_node_id]

                self.gr_edges.append(gr.Edge(start_node, node))
                self.gr_edges.append(gr.Edge(node, end_node))
            else:
              branches = self.lt_graph.get_child_branches(id)
              for branch in branches:
                  if branch.scoreRange is None:
                      # Direct link, no branch node present
                      child = self.lt_graph.get_step_by_id(branch.childStepId)
                      child_node = self.gr_nodes_dict[child.id]
                      self.gr_edges.append(gr.Edge(node, child_node))
                  # else:
                  #     # Branch node present
                  #     child = self.lt_graph.get_step_by_id(branch.childStepId)
                  #     child_node = self.gr_nodes_dict[child.id]
                  #     branch_node_id = (id, branch.childStepId, 0)
                  #     while branch_node_id in self.gr_nodes_dict:
                  #         branch_node = self.gr_nodes_dict[branch_node_id]
                  #         self.gr_edges.append(gr.Edge(node, branch_node))
                  #         self.gr_edges.append(gr.Edge(branch_node, child_node))
                  #         branch_node_id = (id, branch.childStepId, branch_node_id[2] + 1)

    def _draw_edges(self, canvas) -> None:
        for edge in self.gr_edges:
            self._draw_edge(edge, canvas)

    def _draw_edge(self, edge, canvas) -> None:
        canvas.setLineWidth(2)
        canvas.setStrokeColor(colors.black)
        node1, node2 = edge.v

        line_pts = edge.view._pts
        # lines = [ (list(line_pts[i]).extend(list(line_pts[i+1]))) for i in range(len(line_pts) - 1)]
        lines = []
        for i in range(len(line_pts) - 1):
            line = [line_pts[i][0], line_pts[i][1], line_pts[i+1][0], line_pts[i+1][1]]
            lines.append(line)

        canvas.lines(lines)


    def _draw_nodes(self, canvas: canvas.Canvas) -> None:
        for node in self.gr_nodes_dict.values():
            self._draw_node(node, canvas)
    
    def _draw_node(self, node: gr.Vertex, canvas: canvas.Canvas) -> None:
        x, y = node.view.xy
        width, height = node.view.w, node.view.h

        text = node.data['text']
        link = self.key_mapping[node.data['link']] if node.data['link'] is not None else None
        border_color = colors.black
        border_width = 1
        fill_color = nodeTypeColorMap[node.data['stepType']] if node.data['type'] == 'step' else colors.Color(0.3, 0.75, 0.93)
        fill_color = colors.Color(0.2, 0.32, 0.8) if node.data['type'] == 'other' else fill_color
        font_color = colors.white
        font_size = 9
        node_drawer = NodeDrawer(x, y, width, height, text, link, border_color, border_width, fill_color, font_color, font_size)
        node_drawer.draw(canvas)

    def wrap(self, availWidth: int, availHeight: int) -> Tuple[int, int]:
        return self.width, self.height
    
    def draw(self) -> None:
        # self.canv.setPageSize((self.width, self.height))
        self._draw_edges(self.canv)
        self._draw_nodes(self.canv)
        
    
class NodeDrawer():
    def __init__(self, x: int, y: int, width:int, height: int, text:str, link:str=None, border_color:colors.Color=colors.black, border_width:int=0, fill_color:colors.Color=colors.Color(0.3, 0.75, 0.93), font_color:colors.Color=colors.white, font_size:int=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.link = link
        self.border_color = border_color
        self.border_width = border_width
        self.fill_color = fill_color
        self.font_color = font_color
        self.font_size = font_size


    def get_center(self) -> Tuple[int, int]:
        return (self.x + self.width / 2, self.y + self.height / 2)
    
    def _draw_text(self, canvas: canvas.Canvas) -> None:
        canvas.setFontSize(self.font_size)
        canvas.setFillColor(self.font_color)

        text_x, text_y = self.x + self.width / 2, self.y + self.height / 2 - self.font_size / 4

        # Make sure text fits in node, otherwise introduce line breaks
        if canvas.stringWidth(self.text) > self.width:
            available_width_in_chars = self.width / canvas.stringWidth('a')
            available_width_in_chars -= 4 # Leave some space for padding
            _wrap = wrap(self.text, width=available_width_in_chars)
            if len(_wrap) > self.height / self.font_size:
                # remove lines that don't fit
                _wrap = _wrap[:int(self.height / self.font_size)-1] # -1 to leave padding in y direction
                _wrap[-1] = _wrap[-1][:3] + '...'
            text_y = text_y + ((len(_wrap)-1) * self.font_size) / 2 # Adjust starting y position to center text
            for idx, line in enumerate(_wrap):
                canvas.drawCentredString(text_x, text_y - (idx * self.font_size), line)
            return

        canvas.drawCentredString(text_x, text_y, self.text)
        
    def _draw_rect(self, canvas: canvas.Canvas) -> None:
        canvas.setStrokeColor(self.border_color)
        canvas.setFillColor(self.fill_color)
        canvas.setLineWidth(self.border_width)
        canvas.rect(self.x, self.y, self.width, self.height, fill=self.fill_color != colors.transparent)
        

    def draw(self, canvas: canvas.Canvas) -> None:
        self._draw_rect(canvas)
        self._draw_text(canvas)
        
        # Add link to node visual
        if self.link:
            canvas.linkAbsolute('test_fill', self.link, (self.x, self.y, self.x + self.width, self.y + self.height))
