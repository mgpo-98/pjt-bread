
from django.shortcuts import render
from django.core.paginator import Paginator
from reviews.models import Review
from random import choice
# Create your views here.

def bread(request):
    bread_menu_list = ['마늘빵','코끼리빵','크로와상','공갈빵','단팥빵','슈크림빵','도넛','케이크','식빵']
    bread_menu_img = {
        '마늘빵' : 'https://recipe1.ezmember.co.kr/cache/recipe/2018/02/12/89b45644b695a32c06d4a8ed8b59db3d1.jpg',
        '코끼리빵' : 'https://img.insight.co.kr/static/2021/01/04/1200/8tj15no99ovpy2sljg1d.jpg',
        '크로와상' : 'https://t1.daumcdn.net/cfile/tistory/99E151455C75F80620',
        '공갈빵' : 'https://img.bakingschool.co.kr/data/recipe/recipe_main/1800/1782_recipe_main_015a',
        '단팥빵' : 'https://sitem.ssgcdn.com/29/91/03/item/1000034039129_i1_1200.jpg',
        '슈크림빵' : 'https://image.utoimage.com/preview/cp907097/2020/06/202006001067_500.jpg',
        '도넛' : 'http://www.astronomer.rocks/news/photo/201811/86623_11543_4134.jpeg',
        '케이크' : 'https://img.danawa.com/prod_img/500000/515/433/img/14433515_1.jpg?shrink=330:330&_v=20210610094425',
        '식빵' : 'https://img.maisonkorea.com/2017/09/msk_59cc9cb6ad4ba-1024x682.jpg',
    }
    bread_menu = choice(bread_menu_list)
    bread_img = bread_menu_img[bread_menu]
    context = {
        'bread_menu' : bread_menu,
        'bread_img' : bread_img,
    }
    return render(request, 'base.html', context)


def home(request):
    reviews = Review.objects.order_by('-pk')

    page = request.GET.get('page', '1')
    paginator = Paginator(reviews, 4)
    posts = paginator.get_page(page)

    context= {
        'reviews' : reviews,
        'posts' : posts,
    }

    return render(request, 'home.html', context)