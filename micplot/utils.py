from django.shortcuts import render as _render
from django.shortcuts import redirect as _redirect
from django.shortcuts import get_object_or_404

from django.http import Http404
from .models import Show,Act,Mic,Scene
import re

def verifyShow(show_id,show_name,sortmicsby=0):
    show = get_object_or_404(Show,pk=show_id)
    showdict = getShowDict(show,sortmicsby=sortmicsby)
    if show_name != showdict["reducedname"]: raise Http404
    
    return showdict

def verifyAct(show_id,show_name,act_id):
    verifyShow(show_id,show_name)

    act = get_object_or_404(Act,pk=act_id)
    actdict = getActDict(act)
    
    return actdict

def getSceneDict(scene:Scene):
    return {
        "original":scene,
        "id":scene.pk,
        "number":scene.number,
        "created":scene.created,
        "updated":scene.updated
    }

def getMicDict(mic:Mic):
    return {
        "original":mic,
        "id":mic.pk,
        "pack":mic.packnumber,
        "channel":mic.mixchannel,
        "created":mic.created,
        "updated":mic.updated
    }

def getShowDict(show:Show,sortmicsby=0):
    acts = Act.objects.filter(show=show)
    actsdicts = []
    for act in acts: actsdicts.append(getActDict(act))

    mics = Mic.objects.filter(show=show).order_by("packnumber" if sortmicsby else "mixchannel")
    micsdicts = []
    for mic in mics: micsdicts.append(getMicDict(mic))

    return {
        "original":show,
        "id":show.pk,
        "name":show.name,
        "reducedname":re.sub('[^0-9a-zA-Z]+', '_', show.name.lower()),
        "created":show.created,
        "updated":show.updated,
        "date":show.date,
        "acts":actsdicts if len(actsdicts) > 0 else None,
        "mics":micsdicts if len(micsdicts) > 0 else None
    }

def getActDict(act:Act):
    scenes = Scene.objects.filter(act=act)
    scenesdicts = []
    for scene in scenes: scenesdicts.append(getSceneDict(scene))

    return {
        "original":act,
        "id":act.pk,
        "name":act.name,
        "reducedname":re.sub('[^0-9a-zA-Z]+', '_', act.name.lower()),
        "created":act.created,
        "updated":act.updated,
        "scenes":scenesdicts if len(scenesdicts) > 0 else None
    }

def getReferrer(request):
    try: return request.session["referrer"]
    except KeyError: return None

def setReferrer(request,referrer):
    request.session["referrer"] = referrer

def render(request,path,options={},*a,referrer="",**k):
    if referrer not in [None,""]: setReferrer(request,referrer)
    return _render(request,path,options,*a,*k)

def redirect(request,to,*a,referrer="",**k):    
    if referrer not in [None,""]: setReferrer(request,referrer)
    return _redirect(to,*a,*k)
