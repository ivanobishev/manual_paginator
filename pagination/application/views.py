from django.shortcuts import render
from .models import Report

#----------[ Functions ]----------
def paginating_system(id_report, reports_list):
    try:
        current_report = Report.objects.get(pk = id_report)
    except:
        # Here we could prompt an error.
        pass
    else:
        total_pages = Report.objects.count()
        current_page = 0
        for i in range(len(reports_list)):
            if reports_list[i].pk == id_report:
                current_page = i
                # Important: actually the page is i + 1,
                # because the list first ID is 0,
                # but the first page 1.
        
        # We will display a maximum of five pages:
        around_less = current_page - 1
        around_more = current_page + 1
        max_boundary = total_pages - 1 # Avoid exceeding the list.


        #---[Shaping the paginator]---

        # We solve the list difference.
        paginator_index = current_page + 1

        page_links = []

        # Always add the first page.
        page_links.append([
            reports_list[0], 1
        ])

        # Add dot if we're in the 4th or higher page.
        if paginator_index > 3:
            page_links.append(["", "."])

        # We add the Around Less if the Index is 3 or more.
        if paginator_index >= 3:
            page_links.append([
                reports_list[around_less],
                paginator_index - 1
            ])
        
        # We add the current page if it isn't the minimum nor maximum.
        if (paginator_index > 1) and (paginator_index < total_pages):
            page_links.append([
                reports_list[current_page],
                paginator_index
            ])
        
        if paginator_index < max_boundary:
            page_links.append([
                reports_list[around_more],
                paginator_index + 1
            ])

        # Add dot if we're 2 below from the maximum.
        if paginator_index + 2 < total_pages:
            page_links.append(["", "."])

        page_links.append([
            reports_list[max_boundary],
            total_pages
        ])
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
