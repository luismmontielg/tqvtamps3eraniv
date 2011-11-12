# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os

from django.db import models
from django.db.models import Q
from django.conf import settings

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Sum, Avg, Count

from django.db import utils as dbutils

import logging
import datetime
import hashlib
import time
from decimal import *

from rsvp.models import Event

class EventDetails(models.Model):
    event = models.OneToOneField(Event, verbose_name="evento", related_name="details")
    image = models.ImageField(upload_to="events")

    def __unicode__(self):
        return "Detalles para el evento " + self.event.title

    class Meta:
        verbose_name = "Detalles del evento"
        verbose_name_plural = "Detalles de los eventos"

class Activity(models.Model):
    event = models.ForeignKey(Event, verbose_name="evento")
    name = models.CharField("titulo", max_length=70)
    description = models.TextField('descripcion', blank=True)
    presenter = models.CharField("presentador", max_length=90,
                    default="---------", blank=True)
    start_time = models.DateTimeField("hora de inicio")
    end_time = models.DateTimeField("hora de finalizacion")
    enabled = models.BooleanField('Esta habilitada?', default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ("start_time",)


