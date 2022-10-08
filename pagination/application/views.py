from django.shortcuts import render
from .models import Report
from django.core.paginator import Paginator

#----------[ Functions ]----------
def paginating_system(id_report, reports_list):
    current_report = Report.objects.get(pk = id_report)
    total_pages = Report.objects.count()
    current_page = 0

    for i in range(len(reports_list)):
        if reports_list[i].pk == id_report:
            current_page = i
            # Important: actually the page is i + 1,
            # because the list first ID is 0, but the first page is 1.
    paginator_index = current_page + 1
    around_less = current_page - 1
    around_more = current_page + 1
    max_boundary = total_pages - 1 # Avoid exceeding the list.

    #---[Shaping the paginator, 5 pages as maximum]---
    page_links = []

    # Always add the first page.
    page_links.append([
        reports_list[0], 1])

    # Add dots if we're in the 4th or higher page.
    if paginator_index > 3:
        page_links.append(["", "..."])

    # We add the Around Less if the Index is 3 or more.
    if paginator_index >= 3:
        page_links.append([
            reports_list[around_less], paginator_index - 1])

    # We add the current page if it isn't the minimum nor maximum.
    if (paginator_index > 1) and (paginator_index < total_pages):
        page_links.append([
            reports_list[current_page], paginator_index])

    # We add the Around More if we are below 2 from the maximum.
    if paginator_index < max_boundary:
        page_links.append([
            reports_list[around_more], paginator_index + 1])

    # Add dot if we're 2 below from the maximum.
    if paginator_index + 2 < total_pages:
        page_links.append(["", "..."])

    # We always add the Maximum Boundary.
    page_links.append([
        reports_list[max_boundary], total_pages])
    return [current_report, total_pages, current_page, page_links]
        
#----------[ Views ]----------
def index(request):
    return render(request, 'index.html')

def manual_paginating(request, id_report):
    reports_list = Report.objects.all().order_by('-pk')
    solution = paginating_system(id_report, reports_list)

    context = {
        'reports_list': reports_list,
        'current_report': solution[0],
        'total_pages': solution[1],
        'current_page': solution[2],
        'page_links': solution[3]
    }
    return render(request, 'manual_paginating.html', context)

def default_paginating(request):
    report_list = Report.objects.all().order_by('-pk')
    # The second parameter sets the reports amount per page.
    paginator = Paginator(report_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'default_paginating.html', context)
