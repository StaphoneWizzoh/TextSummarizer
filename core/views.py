from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from io import BytesIO
import tempfile
import os

from .models import Summary
from .forms import SummaryForm
from .utils import extract_pdf, summarizer, extract_and_generate, create_pdf


def index(request):
    if request.method == "POST":
        summary_form = SummaryForm(request.POST, request.FILES)
        if summary_form.is_valid():
            summary = summary_form.save(commit=False)
            summary.owner = request.user

            summary.save()
            input_text = summary.input_text
            input_file = summary.input_file
            generated_text = ""

            if input_file:
                output_text = extract_and_generate(input_file.path)
                # output_text = extract_pdf(input_file.path)

                summary.generated_text = output_text

                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file_path = temp_file.name

                # Generate PDF
                create_pdf(output_text, temp_file_path)

                # Save temp_file to instance
                with open(temp_file_path, 'rb') as temp_file_content:
                    summary.generated_file.save(
                        "Generated_file.pdf", temp_file_content)

                # Remove temp file
                os.remove(temp_file_path)

                summary.save()
            else:
                output_text = summarizer(input_text)
                summary = Summary.objects.get(pk=summary.pk)
                summary.generated_text = output_text

                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file_path = temp_file.name

                # Generate PDF
                create_pdf(output_text, temp_file_path)

                # Save temp_file to instance
                with open(temp_file_path, 'rb') as temp_file_content:
                    summary.generated_file.save(
                        "Generated_file.pdf", temp_file_content)

                # Remove temp file
                os.remove(temp_file_path)

                summary.save()

            summary_detail_url = reverse_lazy(
                "detail", kwargs={"pk": summary.pk})
            return redirect(summary_detail_url)
    else:
        summary_form = SummaryForm()

    return render(request, 'core/index.html', {"form": summary_form})


def summary_list(request):
    summaries = Summary.objects.all()
    return render(request, 'core/list.html', {'summaries': summaries})


def tutorial(request):
    for name in request.POST:
        print("{}: {}".format(name, request.POST.getlist(name)))

    return render(request, "core/tutorial.html", {"method": request.method})


def vanilla_summary(request):
    if request.method == "POST":
        summary = Summary()
        owner = request.user or 1
        textInput = request.POST["textInput"]
        output_text = summarizer(textInput)

        if 'fileInput' in request.POST:
            fileInput = request.POST["fileInput"]
        summary(owner=owner,
                input_text=textInput,
                input_file=fileInput,
                generated_text=output_text,
                )
        summary.save()

    else:
        print("request is GET")

    return render(request, "core/vanilla.html")


class SummaryDetail(DetailView):
    model = Summary
    template_name = 'core/detail.html'
    context_object_name = "summary"
