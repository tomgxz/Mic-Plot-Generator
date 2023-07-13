from docx import Document
from docx.shared import Pt,Cm
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.oxml.shared import OxmlElement

from .models import Mic,MicPos,Scene
from .utils import verifyShow, verifyAct

def set_cell_border(cell, **kwargs):
    """
    Set cell`s border
    Usage:

    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        start={"sz": 24, "val": "dashed", "shadow": "true"},
        end={"sz": 12, "val": "dashed"},
    )
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    # check for tag existnace, if none found, then create one
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)

    # list over all available tags
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)

            # check for tag existnace, if none found, then create one
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))

def set_cell_vertical_alignment(cell, align="center"): 
    try:   
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcValign = OxmlElement('w:vAlign')  
        tcValign.set(qn('w:val'), align)  
        tcPr.append(tcValign)
        return True 
    except Exception as e:
        print(e)           
        return False

def generateParamaters(showdict,actdict):
    maxn = len(Mic.objects.filter(show=showdict["original"]))

    blankrow = [None for _ in range(maxn+1)]
    starting = blankrow.copy()

    scenes = []
    micpos = []
    micmixmap = {}

    micssorted = Mic.objects.filter(show=showdict["original"]).order_by("mixchannel")
    for mic in enumerate(micssorted): micmixmap[str(mic[1].mixchannel)] = mic[0]

    for mic in micssorted:
        for mp in MicPos.objects.all().filter(mic=mic):
            if mp.mic.show == showdict["original"] and mp.scene.act == actdict["original"]:
                micpos.append(mp)

    for mp in micpos:
        if micmixmap[str(mp.mic.mixchannel)] <= len(starting):
            if starting[micmixmap[str(mp.mic.mixchannel)]] is not None:
                if mp.scene.number < starting[micmixmap[str(mp.mic.mixchannel)]].scene.number:
                    if len(mp.actor) > 0:
                        starting[micmixmap[str(mp.mic.mixchannel)]] = mp
            else: 
                if len(mp.actor) > 0:
                    starting[micmixmap[str(mp.mic.mixchannel)]] = mp

    for scene in enumerate(Scene.objects.filter(act=actdict["original"]).order_by("number")):
        scenes.append(blankrow.copy())
        scenes[scene[0]][0] = scene[1].number

        for mp in micpos:
            if mp.scene == scene[1] and mp.actor != "" and mp.actor is not None:
                scenes[scene[0]][micmixmap[str(mp.mic.mixchannel)]+1] = mp

    records = [
        ["Char",*list(map(lambda x: str(x.mixchannel),micssorted))],
        ["ACT 1",*list(map(lambda x: starting[micmixmap[str(x.mixchannel)]].actor if starting[micmixmap[str(x.mixchannel)]].actor is not None else "",micssorted))],
        *scenes,
    ]

    return records

def generateDocument(showdict):
    document = Document()

    style = document.styles["Normal"]
    font = style.font
    font.name = "Roboto"
    font.size = Pt(11)

    section = document.sections[-1]
    section.orientation = WD_ORIENT.LANDSCAPE

    #new_width, new_height = section.page_height, section.page_width
    #section.page_width = new_width
    #section.page_height = new_height
        
    section.page_width, section.page_height = section.page_height, section.page_width
    
    footer = section.footer

    p = footer.paragraphs[0]
    p.text = f"MIC PLOT - {showdict['name']} - {showdict['date'].year}".upper()

    return document

def createMicPlotDocument(show_id,show_name,act_id):

    showdict = verifyShow(show_id,show_name,sortmicsby=0)
    actdict = verifyAct(show_id,show_name,act_id)

    records = generateParamaters(showdict,actdict)
    document = generateDocument(showdict)

    p = document.add_paragraph(f"Mic plot for {actdict['name']} - SOUND DESK - ")

    table = document.add_table(len(records),len(records[0]))
    table.style = 'Table Grid'
    table.autofit = True
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    for r in enumerate(records[0]):
        c = table.cell(0,r[0])
        c.paragraphs[0].add_run(str(r[1])).bold=True

        paragraph = c.paragraphs[0]
        runs = paragraph.runs
        for run in runs: run.font.size=Pt(7)

        borderformat = {"sz": 16, "val": "single", "color": "#000000"} 

        set_cell_border(
            c,
            top=borderformat,
            bottom=borderformat,
            start=borderformat,
            end=borderformat,
        )

    for row in enumerate(records):
        if row[0] == 0: continue

        for r in enumerate(row[1]):
            c = table.cell(row[0],r[0])

            if r[1] not in [None,""]:

                if type(r[1]) == MicPos:
                    c.text = str(r[1].actor)
                    if r[1].speaking == 2:
                        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="cccccc"/>'.format(nsdecls('w'))))
                    elif r[1].speaking == 1:
                        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="bcbcbc"/>'.format(nsdecls('w'))))

                else:
                    if r[0] == 0: c.paragraphs[0].add_run(str(r[1])).bold=True
                    else: c.paragraphs[0].add_run(str(r[1]))

                paragraph = c.paragraphs[0]
                runs = paragraph.runs
                for run in runs: run.font.size=Pt(7)

            borderformat = {"sz": 6, "val": "single", "color": "#000000"}

            set_cell_border(
                c,
                top=borderformat,
                bottom=borderformat,
                start=borderformat,
                end=borderformat,
            )

    for column in table.columns:
        for cell in column.cells:
            cell._tc.tcPr.tcW.type = 'auto'
            set_cell_vertical_alignment(cell)

    for row in table.rows: row.height = Cm(.65)

    return document

createMicPlotDocument(2,"the_little_mermaid",2)