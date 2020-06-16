from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

def new(request):
    if request.method == 'POST':
        # Database에 저장
        # 1. 요청에 실려온 data 꺼내오기
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        form = ArticleForm(request.POST)
        
        # 2-1. data 유효성 검사
        if form.is_valid():
            # (ModelForm) 2-2. Database에 저장
            article = form.save()
            # # 2-2. 검증된 data 꺼내오기
            # title = form.cleaned_data.get('title')
            # content = form.cleaned_data.get('content')
            # # 2-3. Database에 저장
            # article = Article(title=title, content=content)
            # article.save()
            # 3. 저장된 data를 확인할 수 있는 곳으로 안내
            return redirect('articles:detail', article.pk)

    else: # GET
        # 작성 양식 보여주기
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/new.html', context)


def detail(request, pk):
    # Database에서 data 가져오기
    article = Article.objects.get(pk=pk)

    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


def delete(request, pk): # POST
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article.delete()
    return redirect('articles:index')

def edit(request, pk):
    # 1. Database에서 data 가져오기
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        # data 수정!
        
        # (ModelForm) 2-1. form에 data 집어넣기 + instance와 연결
        form = ArticleForm(request.POST, instance=article)
        # # 2-1. form에 data 집어넣기(검증 목적)
        # form = ArticleForm(request.POST)
        # 2-2. form에서 data 유효성 검사
        if form.is_valid():
            # (ModelForm) 2-3. Database에 저장
            article = form.save()
            # # 2-3. 검증된 data를 반영하기(저장)
            # article.title = form.cleaned_data.get('title')
            # article.content = form.cleaned_data.get('content')
            # article.save()
            # 3. 저장된 내용을 확인할 수 있는 페이지로 안내
            return redirect('articles:detail', article.pk)
    else:  
        # 수정 양식 보여주기!
        # (ModelForm) 2. Form에 data 채워 넣기
        form = ArticleForm(instance=article)
        # # 2. Form에 data 채워 넣기
        # form = ArticleForm(initial=article.__dict__)
    context = {
        'form': form,
    }
    return render(request, 'articles/edit.html', context)