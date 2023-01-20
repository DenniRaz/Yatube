from django.core.paginator import Page, Paginator


def pagination(request, object_list, per_page) -> Page:
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj