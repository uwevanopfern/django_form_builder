from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import is_user_authenticated
from forms_builder.forms.models import Form
from .forms import FormForForm
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from forms_builder.forms.signals import form_invalid, form_valid
from django.conf import settings
from forms_builder.forms.utils import split_choices
try:
    from django.urls import reverse
except ImportError:
    # For Django 1.8 compatibility
    from django.core.urlresolvers import reverse
from email_extras.utils import send_mail_template
from forms_builder.forms.settings import EMAIL_FAIL_SILENTLY

@is_user_authenticated
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, 'food/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def forms(request):
    context =  {"forms": get_forms()}
    return render(request, 'food/forms.html',context)

def form_sent(request):
    return render(request, 'food/form_sent.html')


class FormDetail(TemplateView):

    template_name = "food/form_details.html"

    def get_context_data(self, **kwargs):
        context = super(FormDetail, self).get_context_data(**kwargs)
        published = Form.objects.published(for_user=self.request.user)
        context["form"] = get_object_or_404(published, slug=kwargs["slug"])
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        login_required = context["form"].login_required
        if login_required and not request.user.is_authenticated:
            path = urlquote(request.get_full_path())
            bits = (settings.LOGIN_URL, REDIRECT_FIELD_NAME, path)
            return redirect("%s?%s=%s" % bits)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        published = Form.objects.published(for_user=request.user)
        form = get_object_or_404(published, slug=kwargs["slug"])
        form_for_form = FormForForm(form, RequestContext(request),
                                    request.POST or None,
                                    request.FILES or None)
        if not form_for_form.is_valid():
            form_invalid.send(sender=request, form=form_for_form)
        else:
            # Attachments read must occur before model save,
            # or seek() will fail on large uploads.
            attachments = []
            for f in form_for_form.files.values():
                f.seek(0)
                attachments.append((f.name, f.read()))
            entry = form_for_form.save()
            form_valid.send(sender=request, form=form_for_form, entry=entry)
            self.send_emails(request, form_for_form, form, entry, attachments)
            if not self.request.is_ajax():
                return redirect(form.redirect_url or
                    reverse("form_sent", kwargs={"slug": form.slug}))
        context = {"form": form, "form_for_form": form_for_form}
        return self.render_to_response(context)

    def render_to_response(self, context, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            json_context = json.dumps({
                "errors": context["form_for_form"].errors,
                "form": context["form_for_form"].as_p(),
                "message": context["form"].response,
            })
            if context["form_for_form"].errors:
                return HttpResponseBadRequest(json_context,
                    content_type="application/json")
            return HttpResponse(json_context, content_type="application/json")
        return super(FormDetail, self).render_to_response(context, **kwargs)

    def send_emails(self, request, form_for_form, form, entry, attachments):
        subject = form.email_subject
        if not subject:
            subject = "%s - %s" % (form.title, entry.entry_time)
        fields = []
        for (k, v) in form_for_form.fields.items():
            value = form_for_form.cleaned_data[k]
            if isinstance(value, list):
                value = ", ".join([i.strip() for i in value])
            fields.append((v.label, value))
        context = {
            "fields": fields,
            "message": form.email_message,
            "request": request,
        }
        email_from = form.email_from or settings.DEFAULT_FROM_EMAIL
        email_to = form_for_form.email_to()
        if email_to and form.send_email:
            send_mail_template(subject, "form_response", email_from,
                               email_to, context=context,
                               fail_silently=EMAIL_FAIL_SILENTLY)
        headers = None
        if email_to:
            headers = {"Reply-To": email_to}
        email_copies = split_choices(form.email_copies)
        if email_copies:
            send_mail_template(subject, "form_response_copies", email_from,
                               email_copies, context=context,
                               attachments=attachments,
                               fail_silently=EMAIL_FAIL_SILENTLY,
                               headers=headers)

form_detail = FormDetail.as_view()


@login_required(login_url='login')
def home(request):
    clients = User.objects.all()
    clients = clients.filter(is_admin=False)
    user = User.objects.get(username=request.user)
    auth_forms = user.forms.all()
    context = {'clients': clients, 'auth_forms': auth_forms}
    return render(request, 'food/home.html', context)


@login_required(login_url='login')
def client_details(request, pk):
    client = get_client(pk=pk)
    client_forms = client.forms.all()
    forms = get_forms()
    context = {'client': client, 'client_forms': client_forms}
    return render(request, 'food/client_details.html', context)

def get_forms():
    return Form.objects.all()

def get_client(pk):
    client = User.objects.get(pk=pk)
    return client
