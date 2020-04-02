from django.shortcuts import render

# Create your views here.

# from django.shortcuts import render_to_response

def index (request):
    return render(request, 'homepage/homepage.html')


# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# 	return render(request, "homepage/homepage.html")