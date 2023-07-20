import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageTemplate, Frame, NextPageTemplate, BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from lib.utils.graph import LearningTrackGraph
from lib.writing.files.pdf.graph import GraphFlowable
from lib.writing.files.BaseFileWriter import BaseFileWriter

class PDFWriter(BaseFileWriter):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.file_type = 'pdf'
        # self.canvas = canvas.Canvas(self.filename, pagesize=letter)

        # pdf specific attributes
        self.page_width, self.page_height = letter
        self.marginX = 50
        self.marginY = 50
        self.line_height = 9
        self.tab_width = 16
        self.max_content_height = self.page_height - 2 * self.marginY
        self.current_y = self.page_height - self.marginY
        self.current_x = 0
        self.current_line = ''
        self.current_page = 1
        self.font_size = 9
        self.font = "Helvetica"
        self.content = []
        self.paragraph_style = getSampleStyleSheet()['Normal']
        self.graph_page_dimensions = (2000, 4000) 
        # self._build()       

        # set text page layout
        # self.content.append(NextPageTemplate('textPage'))

    def __del__(self):
        self.build()


    def _setTextPageLayout(self, canvas: canvas.Canvas, doc: BaseDocTemplate) -> None:
        canvas.saveState()
        canvas.setPageSize(letter)
        canvas.restoreState()

    def _setGraphPageLayout(self, canvas: canvas.Canvas, doc: BaseDocTemplate) -> None:
        canvas.saveState()
        canvas.setPageSize(self.graph_page_dimensions)
        canvas.restoreState()

    def _set_page_templates(self) -> None:
        self.page_templates = [
            # larger page size for graph
            PageTemplate(id='graphPage', frames=[Frame( 0, 0, self.graph_page_dimensions[0], self.graph_page_dimensions[1], id='graphPage', leftPadding=0, topPadding=0, rightPadding=0, bottomPadding=0)], onPage=self._setGraphPageLayout),
            PageTemplate(id='textPage', frames=[Frame(self.marginX, self.marginY, self.page_width - 2 * self.marginX, self.page_height - 2 * self.marginY, id='textPage')], onPage=self._setTextPageLayout),
        ]
    
    def _reset_paragraph_style(self) -> None:
        self.paragraph_style = getSampleStyleSheet()['Normal']

    def get_file_stream(self):
        fs = io.BytesIO()
        self.doc = SimpleDocTemplate(fs, pagesize=letter, rightMargin=self.marginX, leftMargin=self.marginX,
                                      topMargin=self.marginY, bottomMargin=self.marginY,
                                      showBoundary=0 )
        self._set_page_templates()
        self.doc.addPageTemplates(self.page_templates)
        self.doc.build(self.content)
        fs.seek(0)
        return fs
    
    def build(self) -> None:
        """Builds the pdf file, printing the content to the file and saves it to the specified filename"""

        self.doc = SimpleDocTemplate(self.filename, pagesize=letter, rightMargin=self.marginX, leftMargin=self.marginX,
                                      topMargin=self.marginY, bottomMargin=self.marginY,
                                      showBoundary=0 )
        self._set_page_templates()
        self.doc.addPageTemplates(self.page_templates)
        self.doc.build(self.content)


    def write(self, text: str, indent: int=0) -> None:
        """Writes text to the pdf file, with an optional indent"""
        self.paragraph_style.leftIndent = indent * self.tab_width
        content = Paragraph(text, self.paragraph_style)
        self.content.append(content)
        self._reset_paragraph_style()

    #TODO: check key/val typing correctness
    def write_pair(self, key: str, value: str, indent: int=0) -> None:
        """Writes a key value pair to the pdf file, with an optional indent"""
        self.paragraph_style.leftIndent = indent * self.tab_width
        # self.paragraph_style.firstLineIndent = -1 * self.paragraph_style.leftIndent
        text = f'{key}: {value}'
        self.content.append(Paragraph(text, self.paragraph_style))
        self._reset_paragraph_style()

        
    def add_LearningTrack_graph(self, graph: LearningTrackGraph, key_mapping: dict) -> None:
        """Creates and adds a LearningTrackGraph to the pdf files contents"""
        gf = GraphFlowable(graph, key_mapping)
        self.graph_page_dimensions = gf.get_dimensions()

        # set page template to graph page, allows for larger page size
        self.content.append(NextPageTemplate('graphPage'))
        self.content.append(gf)
        self.content.append(NextPageTemplate('textPage'))


        
        
        