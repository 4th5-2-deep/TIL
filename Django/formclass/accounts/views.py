from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout


def signup(request):
    # 만약, 로그인이 되었다면 index로 돌려 보내기
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        # User 생성!
        # 1. POST로 넘어온 데이터 form에 넣기
        form = UserCreationForm(request.POST)
        # 2. form에서 유효성 검사
        if form.is_valid():
            # 3. 유효하다면 database에 저장
            user = form.save()
            # 3-1. 저장했다면, 해당 User로 로그인!
            auth_login(request, user)
            # 4. 저장 결과 확인이 가능한 페이지로 안내
            return redirect('articles:index')

    else:
        # User 생성 양식 보여주기
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    # 만약, 로그인이 되었다면 index로 돌려 보내기
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        # User 검증 + 로그인
        # 1. POST로 넘어온 데이터 form에 넣기
        form = AuthenticationForm(request, request.POST)
        # 2. form 검증 (아이디, 비밀번호 맞음?)
        if form.is_valid():
            # 3. 맞으면, 로그인 시켜줌
            user = form.get_user()
            auth_login(request, user)
            # 4. 로그인 결과 확인이 가능한 페이지로 안내
            return redirect('articles:index')

    else:
        # User 로그인 창 보여주기
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout(request): # POST
    if request.method == 'POST':
        # Logout!
        auth_logout(request)
    return redirect('articles:index')
