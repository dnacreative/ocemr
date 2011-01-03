
##########################################################################
#
#    This file is part of OCEMR.
#
#    OCEMR is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OCEMR is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OCEMR.  If not, see <http://www.gnu.org/licenses/>.
#
#
#########################################################################
#       Copyright 2011 Philip Freeman <philip.freeman@gmail.com>
##########################################################################
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest


from django.db.models import get_model, Q


@login_required
def lab_queue(request):
	"""
	"""
	from datetime import datetime, timedelta
	d_yesterday = datetime.today()-timedelta(1)
	d_now = datetime.today()

	from ocemr.models import Lab

	past_24h_q = Q(orderedDateTime__gt=d_yesterday)

	labs = Lab.objects.filter(past_24h_q).order_by('-orderedDateTime', '-id')
	return render_to_response('lab_queue.html', locals())

@login_required
def lab_start(request,id):
	"""
	"""
	from ocemr.models import Lab

	l = Lab.objects.get(pk=id)
	l.status = 'PEN'
	l.save()
	return render_to_response('close_window.html', {})

@login_required
def lab_cancel(request,id):
	"""
	"""
	from ocemr.models import Lab, LabNote

	l = Lab.objects.get(pk=id)
	l.status = 'CAN'
	l.save()
	ln = LabNote(lab=l, addedBy=request.user, note="Lab Canceled")
	ln.save()
	return render_to_response('close_window.html', {})

@login_required
def lab_fail(request,id):
	"""
	"""
	from ocemr.models import Lab

	l = Lab.objects.get(pk=id)
	l.status = 'FAI'
	l.save()
	return render_to_response('close_window.html', {})
#@login_required
#def lab_(request,id):
#	"""
#	"""
#	from ocemr.models import Lab
#
#	l = Lab.objects.get(pk=id)
#	l.status = ''
#	l.save()
#	return render_to_response('close_window.html', {})

@login_required
def lab_notate(request, id):
	"""
	"""
	from ocemr.models import LabNote, Lab, Visit
	from ocemr.forms import NewLabNoteForm

	labid=int(id)
	l=Lab.objects.get(pk=labid)

	if request.method == 'POST': # If the form has been submitted...
		form = NewLabNoteForm(l, request.user, request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			o = form.save()
			return HttpResponseRedirect('/close_window/')
	else:
		form = NewLabNoteForm(l, request.user) # An unbound form
	return render_to_response('popup_form.html', {
		'title': 'Add an Lab Note: %s'%(l.type.title),
		'form_action': '/lab/%d/notate/'%(l.id),
		'form': form,
	})

@login_required
def lab_complete(request, id):
	"""
	"""
	from ocemr.models import Lab
	from ocemr.forms import CompleteLabForm
	l = Lab.objects.get(pk=id)

	if request.method == 'POST':
		form = CompleteLabForm(request.POST)
		if form.is_valid():
			l.result = form.cleaned_data['result']
			l.status='COM'
			l.save()
			return HttpResponseRedirect('/close_window/')
	else:
		form = CompleteLabForm()
	return render_to_response('popup_form.html', {
		'title': 'Complete Lab: %s'%(l),
		'form_action': '/lab/%s/complete/'%(l.id),
		'form': form,
	})
