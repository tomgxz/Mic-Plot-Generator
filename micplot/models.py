from django.db import models

class Show(models.Model):
    name =  models.CharField("Name",max_length=100)
    date = models.DateField("Date Started",default="",blank=True,null=True)
    
    created = models.DateTimeField(auto_now_add=True,editable=False)
    updated = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self): return self.name

class Act(models.Model):
    name = models.CharField("Name",max_length=100)

    show = models.ForeignKey(Show,on_delete=models.DO_NOTHING)
    
    created = models.DateTimeField(auto_now_add=True,editable=False)
    updated = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self): return self.name

class Mic(models.Model):
    packnumber = models.IntegerField("Mic Pack Number")
    mixchannel = models.IntegerField("Mixer Channel")

    show = models.ForeignKey(Show,on_delete=models.DO_NOTHING)
    
    created = models.DateTimeField(auto_now_add=True,editable=False)
    updated = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self): return f"{self.packnumber} / {self.mixchannel}"

class Scene(models.Model):
    number = models.IntegerField("Scene Number")

    act = models.ForeignKey(Act,on_delete=models.DO_NOTHING)
    
    created = models.DateTimeField(auto_now_add=True,editable=False)
    updated = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self): return f"Scene {self.number}"

class MicPos(models.Model):
    mic = models.ForeignKey(Mic,on_delete=models.DO_NOTHING)
    scene = models.ForeignKey(Scene,on_delete=models.DO_NOTHING)

    actor = models.CharField("Actor",max_length=100)
    speaking = models.IntegerField("Speaking",default=0)
    
    created = models.DateTimeField(auto_now_add=True,editable=False)
    updated = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self): 
        return "MP"
        return f"Mic {self.mic} at {self.scene}"