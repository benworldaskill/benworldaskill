

from .form import ContactForm
from .models import Post, Category, Projects, ProjectCategory
from django.db.models import Count, Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
import logging
from django.core.mail import EmailMessage


logger = logging.getLogger(__name__)
# Create your views here.


# views.py


def home(request):
    posts = Post.objects.filter(is_published=True)
    category = request.GET.get("category")
    if category:
        posts = posts.filter(category_id=category)
    return render(request, "home.html", {
        "posts": posts,
        "categories": Category.objects.all(),
        "active_category": category,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    return render(request, "post_detail.html", {"post": post})


def contact_me(request):

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid:
            saved = contact_form.save()
            messages.success(
                request,
                "Thanks! Your message has been sent, I'll reply within 24hrs.")
            return redirect('contact')
        if settings.CONTACT_NOTIFY_EMAIL:
            try:
                EmailMessage(
                    subject=f"New message from{saved.name}",
                    body=(
                        f"Name: {saved.name}\n"
                        f"Email: {saved.email}\n"
                        f"phone: {saved.phone or '-'}\n\n"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_NOTIFY_EMAIL],
                    reply_to=[saved.email],
                ).send()
            except Exception:
                logger.exception('Contact email failed')

        messages.success(
            request, "Thanks! your message has been sent, I'll reply in 24hrs time")
        return redirect('contact')

    else:
        contact_form = ContactForm()

    return render(request, 'contact.html', {'contact_form': contact_form})


def projects(request):
    items = Projects.objects.filter(
        is_published=True).select_related("category")
    active_category = request.GET.get("category")
    if active_category:
        items = items.filter(category_id=active_category)

    categories = ProjectCategory.objects.annotate(
        total=Count("projects", filter=Q(projects__is_published=True))
    )

    return render(request, "projects.html", {
        "projects": items,
        "categories": categories,
        "active_category": active_category,
        "all_count": Projects.objects.filter(is_published=True).count(),
    })


def project_detail(request, pk):
    project = get_object_or_404(
        Projects.objects.prefetch_related("gallery"),
        pk=pk, is_published=True,
    )
    return render(request, "project_detail.html", {"project": project})


def blog(request):
    blogs = Post.objects.filter(is_published=True)
    category = request.GET.get("category")
    if category:
        blogs = blogs.filter(category_id=category)

    return render(request, "blog.html", {
        "blogs": blogs,
        "categories": Category.objects.all(),
        "active_category": category,
    })


def about(requests):
    return render(requests, "about.html")


def build_query(terms, fields):

    query = Q()
    for term in terms:
        term_q = Q()
        for field in fields:
            term_q |= Q(**{f"{field}__icontains": term})
        query &= term_q
    return query


def search(request):
    query = request.GET.get("q", "").strip()
    post_results = []
    project_results = []

    if query:
        terms = query.split()

        post_results = list(
            Post.objects.filter(is_published=True)
            .filter(build_query(terms, ["title", "description", "body", "author", "category__name"]))
            .distinct()[:24]
        )
        project_results = list(
            Projects.objects.filter(is_published=True)
            .filter(build_query(terms, ["title", "description", "tech_stack", "category__name"]))
            .distinct()[:24]
        )

    return render(request, "search.html", {
        "query": query,
        "posts": post_results,
        "projects": project_results,
        "total": len(post_results) + len(project_results),
    })
