from django.shortcuts import render,redirect
from .models import Show,Act,Mic,Scene,MicPos
from .utils import getShowDict, verifyShow, verifyAct
from datetime import datetime

def index(request):
    shows = Show.objects.order_by("date").reverse()
    output = []

    for show in shows: output.append(getShowDict(show))

    return render(request,"index.html",{"shows":output})

def newshow(request):
    if request.method == "POST":
        showname = request.POST.get("show-name-input")
        showdate = request.POST.get("show-date-input")
        
        showdate = datetime.strptime(showdate,"%Y-%m-%d")

        newshow = Show(name=showname,date=showdate)
        newshow.save()

        return redirect("micplot:index")

    return render(request,"show-new.html")

def show(request,show_id,show_name):       
    return render(request,"show.html",{"show":verifyShow(show_id,show_name)})

def newact(request,show_id,show_name):
    showdict = verifyShow(show_id,show_name)

    if request.method == "POST":
        actname = request.POST.get("act-name-input")

        newact = Act(name=actname,show=showdict["original"])
        newact.save()

        return redirect("micplot:show",show_id,show_name)

    return render(request,"act-new.html",{"show":showdict})

def act(request,show_id,show_name,act_id):
    sortby = int(request.GET.get('sortby',0))
    # 0 = sort by mixing desk
    # 1 = sort by pack number

    showdict = verifyShow(show_id,show_name,sortmicsby=sortby)
    actdict = verifyAct(show_id,show_name,act_id)

    maxn = 0

    for mic in Mic.objects.filter(show=showdict["original"]):
        if mic.packnumber > maxn:
            maxn = mic.packnumber

    starting = [None for _ in range(maxn+1)]

    micpos = []

    micssorted = Mic.objects.filter(show=showdict["original"]).order_by("packnumber" if sortby else "mixchannel")

    for mic in micssorted:
        for mp in MicPos.objects.all().filter(mic=mic):
            if mp.mic.show == showdict["original"] and mp.scene.act == actdict["original"]:
                micpos.append(mp)

    for mp in micpos:
        if mp.mic.packnumber <= len(starting):
            if starting[mp.mic.packnumber] is not None:
                if mp.scene.number < starting[mp.mic.packnumber].scene.number:
                    if len(mp.actor) > 0:
                        starting[mp.mic.packnumber] = mp
            else: 
                if len(mp.actor) > 0:
                    starting[mp.mic.packnumber] = mp

    return render(request,"act.html",{"show":showdict,"act":actdict,"micpos":micpos,"startingmics":starting})

def createNewMic(show,micpack,mixchannel):
    newmic = Mic(show=show,packnumber=micpack,mixchannel=mixchannel)
    newmic.save()

def createNewScene(act,number):
    newscene = Scene(act=act,number=number)
    newscene.save()

def newmic(request,show_id,show_name):
    showdict = verifyShow(show_id,show_name)

    if request.method == "POST":
        micpack = request.POST.get("mic-pack-input")
        mixchannel = request.POST.get("mic-ch-input")

        createNewMic(showdict["original"],micpack,mixchannel)

        return redirect("micplot:show",show_id,show_name)

    return render(request,"mic-new.html",{"show":showdict})

def newscene(request,show_id,show_name,act_id):
    showdict = verifyShow(show_id,show_name)
    actdict = verifyAct(show_id,show_name,act_id)

    if request.method == "POST":
        scenenum = request.POST.get("scene-num-input")

        createNewScene(actdict["original"],scenenum)

        return redirect("micplot:act",show_id,show_name,act_id)

    return render(request,"scene-new.html",{"show":showdict,"act":actdict})

def newscenemultiple(request,show_id,show_name,act_id):
    showdict = verifyShow(show_id,show_name)
    actdict = verifyAct(show_id,show_name,act_id)

    if request.method == "POST":
        start = int(request.POST.get("scene-num-input"))
        count = int(request.POST.get("scene-count-input"))

        for i in range(start,start+count):
            if Scene.objects.filter(number=i,act=actdict["original"]): continue

            newscene = Scene(number=i,act=actdict["original"])
            newscene.save()

        return redirect("micplot:act",show_id,show_name,act_id)

    return render(request,"scene-new-multiple.html",{"show":showdict,"act":actdict})

def updateplot(request,show_id,show_name,act_id,mic_id,scene_id):
    assert request.method == "POST"

    assert int(request.POST.get("mic")) == mic_id
    assert int(request.POST.get("scene")) == scene_id

    actor=request.POST.get("actor")
    try: speaking=request.POST.get("speaking")
    except: speaking=2 if len(actor) > 0 else 0

    showdict = verifyShow(show_id,show_name)
    actdict = verifyAct(show_id,show_name,act_id)

    assert len(Mic.objects.filter(show=showdict["original"],pk=mic_id)) > 0 
    assert len(Scene.objects.filter(act=actdict["original"],pk=scene_id)) > 0 

    micposquery = MicPos.objects.filter(mic_id=mic_id,scene_id=scene_id)

    if len(micposquery) > 0:
        micposquery[0].actor = actor
        micposquery[0].speaking = speaking
        micposquery[0].save()
    else:
        newmicpos = MicPos(actor=actor,speaking=speaking,mic_id=mic_id,scene_id=scene_id)
        newmicpos.save()

    return redirect("/")