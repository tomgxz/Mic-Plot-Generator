from docx import Document
from docx.shared import Pt,Cm
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.oxml.shared import OxmlElement

from msoffice2pdf import convert
import pythoncom,os

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

def generateParamaters(showdict,actdict,sortby=0):
    assert sortby in [0,1]

    # sortby=0 -> mic mixer channel
    # sortby=1 -> mic pack number

    sortbytext = "packnumber" if sortby > 0 else "mixchannel"

    maxn = len(Mic.objects.filter(show=showdict["original"]))

    blankrow = [None for _ in range(maxn+1)]
    starting = blankrow.copy()

    scenes = []
    micpos = []
    micmixmap = {}

    micssorted = Mic.objects.filter(show=showdict["original"]).order_by(sortbytext)
    for mic in enumerate(micssorted): 
        field = str(mic[1].packnumber if sortby > 0 else mic[1].mixchannel) 
        micmixmap[field] = mic[0]

    for mic in micssorted:
        for mp in MicPos.objects.all().filter(mic=mic):
            if mp.mic.show == showdict["original"] and mp.scene.act == actdict["original"]:
                micpos.append(mp)

    for mp in micpos:
        field = str(mp.mic.packnumber if sortby > 0 else mp.mic.mixchannel) 
        if micmixmap[field] <= len(starting):
            if starting[micmixmap[field]] is not None:
                if mp.scene.number < starting[micmixmap[field]].scene.number:
                    if len(mp.actor) > 0:
                        starting[micmixmap[field]] = mp
            else: 
                if len(mp.actor) > 0:
                    starting[micmixmap[field]] = mp

    for scene in enumerate(Scene.objects.filter(act=actdict["original"]).order_by("number")):
        scenes.append(blankrow.copy())
        scenes[scene[0]][0] = scene[1].number

        for mp in micpos:
            if mp.scene == scene[1] and mp.actor != "" and mp.actor is not None:
                field = str(mp.mic.packnumber if sortby > 0 else mp.mic.mixchannel) 
                scenes[scene[0]][micmixmap[field]+1] = mp

    records = [
        ["Char",*list(map(lambda x: str(x.packnumber if sortby > 0 else x.mixchannel),micssorted))],
        ["ACT 1",*list(map(lambda x: starting[micmixmap[str(x.packnumber if sortby > 0 else x.mixchannel)]].actor if starting[micmixmap[str(x.packnumber if sortby > 0 else x.mixchannel)]].actor is not None else "",micssorted))],
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

def createMicPlotDocument(show_id,show_name):

    showdict = verifyShow(show_id,show_name,sortmicsby=0)
    document = generateDocument(showdict)

    # create two copies in the document, one that sorts by mixer channel (0)
    # and one that sorts by mic pack number (1)
    for sortby in [0,1]:

        # generate a copy for each act
        for actdict in showdict["acts"]:

            # get the table data for the act, based on the sortby value
            records = generateParamaters(showdict,actdict,sortby)

            pagetitle = f"Mic plot for {actdict['name']} - SOUND DESK - "
            if sortby > 0: pagetitle = f"Mic plot for {actdict['name']} - "

            p = document.add_paragraph(pagetitle)

            # create table
            table = document.add_table(len(records),len(records[0]))
            table.style = 'Table Grid'
            table.autofit = True
            table.alignment = WD_TABLE_ALIGNMENT.LEFT

            # create header row with thicker border
            for r in enumerate(records[0]):
                # create cell and set text
                c = table.cell(0,r[0])
                c.paragraphs[0].add_run(str(r[1])).bold=True

                # set font size of cell
                paragraph = c.paragraphs[0]
                runs = paragraph.runs
                for run in runs: run.font.size=Pt(7)

                borderformat = {"sz": 16, "val": "single", "color": "#000000"} 

                # set border to be thicker than others (16px)
                set_cell_border(
                    c,
                    top=borderformat,
                    bottom=borderformat,
                    start=borderformat,
                    end=borderformat,
                )

            # create rows for each scene (and starting mics)
            for row in enumerate(records):
                # ignore first row (generated in the header)
                if row[0] == 0: continue

                # iterate through cells
                for r in enumerate(row[1]):
                    c = table.cell(row[0],r[0])

                    # ensure the cell has content
                    if r[1] not in [None,""]:

                        # if it is a MicPos type (ie not a starting character cell)
                        if type(r[1]) == MicPos:
                            # set cell content to actor
                            if sortby != 1: c.text = str(r[1].actor)
                            else:

                                closest = float("inf")
                                for next in MicPos.objects.filter(mic=r[1].mic):
                                    if next.scene.number <= r[1].scene.number: continue
                                    if next.scene.number < closest: closest = next.scene.number

                                try:
                                    next = MicPos.objects.filter(
                                        mic=r[1].mic,
                                        scene=Scene.objects.filter(act=actdict["original"],number=closest)[0]
                                    )[0]

                                    if next.actor != r[1].actor and next.actor not in [None,""]:
                                        c.text = f"TO {next.actor}"

                                except IndexError: # no micpos matching said query
                                    pass

                                except OverflowError: # closest still = infinity
                                    pass

                            # lookup next MicPos
                            # if actor is not this actor
                            # next cell needs to have that text

                            # set cell background based on speaking type
                            speakingxml = r'<w:shd {} w:fill="cccccc"/>'.format(nsdecls('w'))
                            if r[1].speaking == 1: r'<w:shd {} w:fill="bcbcbc"/>'.format(nsdecls('w'))
                            c._tc.get_or_add_tcPr().append(parse_xml(speakingxml))

                        # if it is a string (ie a starting character cell)
                        else:
                            # set text to record content
                            if r[0] == 0: c.paragraphs[0].add_run(str(r[1])).bold=True
                            else: c.paragraphs[0].add_run(str(r[1]))

                        # set cell font size
                        paragraph = c.paragraphs[0]
                        runs = paragraph.runs
                        for run in runs: run.font.size=Pt(7)

                    borderformat = {"sz": 6, "val": "single", "color": "#000000"}

                    # set thin border (6px)
                    set_cell_border(
                        c,
                        top=borderformat,
                        bottom=borderformat,
                        start=borderformat,
                        end=borderformat,
                    )

            # set columns width to fit content & page
            for column in table.columns:
                for cell in column.cells:
                    cell._tc.tcPr.tcW.type = 'auto'
                    set_cell_vertical_alignment(cell)

            # set row height
            for row in table.rows: row.height = Cm(.65)

            # add page break if not last act
            if actdict != showdict["acts"][-1]: document.add_page_break()
        
        # add page break if not last sort function
        if sortby != 1: document.add_page_break()

    return document

def fileToPDF(path):
    output = convert(source=os.path.abspath("demo.docx"), output_dir=os.path.abspath("."), soft=0)
    if os.path.isfile("demo.pdf"): os.remove("demo.pdf")
    os.rename(output,"demo.pdf")

def saveAsDOCX(document):
    document.save("demo.docx")
    return "demo.docx"

pythoncom.CoInitialize()

