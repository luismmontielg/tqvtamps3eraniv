__author__ = 'luismmontielg'

from django.core.exceptions import ObjectDoesNotExist
from django import forms

from rsvp.forms import RSVPForm
from rsvp.models import Guest, Event

class TQVRSVPForm(RSVPForm):
    event_id = forms.IntegerField(widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        if 'guest_class' in kwargs:
            self.guest_class = kwargs['guest_class']
            del(kwargs['guest_class'])
        else:
            self.guest_class = Guest
        super(RSVPForm, self).__init__(*args, **kwargs)
        self.event = None
        self.remove_field("comment")
        self.fields['email'].label = "Email"
        self.fields['name'].label = "Nombre"
        self.fields['attending'].label = "Atenderas?"
        self.fields['number_of_guests'].label = "Numero de invitados"

    def clean_email(self):
        return self.cleaned_data['email']

    def clean_event_id(self):
        event_id = self.cleaned_data['event_id']
        try:
            self.event = Event.objects.get(pk=event_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError, 'Error, No existe el evento'

    def clean_number_of_guests(self):
        if self.cleaned_data['number_of_guests'] < 0:
            raise forms.ValidationError, "El numero de invitados no puede ser negativo"
        return self.cleaned_data['number_of_guests']

    def remove_field(self, field): _remove_field(self, field)

    def save(self):
        guest, created = self.guest_class._default_manager.get_or_create(email=self.cleaned_data['email'],
                                                                            event=self.event)

        if self.cleaned_data['name']:
            guest.name = self.cleaned_data['name']

        guest.attending_status = self.cleaned_data['attending']
        guest.number_of_guests = self.cleaned_data['number_of_guests']
        guest.save()
        return guest

def _remove_field(form, field):
    if field in form.fields.keys():
        del form.fields[field]
