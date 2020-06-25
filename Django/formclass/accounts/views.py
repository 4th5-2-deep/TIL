from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserChangeForm, ProfileForm
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def signup(request):
    # 만약, 로그인이 되었다면 index로 돌려 보내기
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        # User 생성!
        # 1. POST로 넘어온 데이터 form에 넣기
        form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        # 2. form에서 유효성 검사
        if form.is_valid() and profile_form.is_valid():
            # 3. 유효하다면 database에 저장
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # Profile 생성
            # Profile.objects.create(user=user)
            # 3-1. 저장했다면, 해당 User로 로그인!
            auth_login(request, user)
            # 4. 저장 결과 확인이 가능한 페이지로 안내
            return redirect('articles:index')

    else:
        # User 생성 양식 보여주기
        form = UserCreationForm()
        # Profile 생성 양식 보여주기
        profile_form = ProfileForm()
    context = {
        'form': form,
        'profile_form': profile_form,
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
            return redirect(request.GET.get('next') or 'articles:index')
            # Quiz. 단축 평가
            # and -> False and True #=> False
            # or -> True or False #=> True
            # a = '' or 'apple' #=> apple
            # b = 'banana' or '' #=> banana

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


def delete(request): # POST
    # 만약 로그인이 안되어 있다면, index로 보내기
    if not request.user.is_authenticated:
        return redirect('articles:index')

    # User 삭제
    if request.method == 'POST':
        request.user.delete()

    return redirect('articles:index')


def edit(request):
    user = request.user
    if request.method == 'POST':
        # User 업데이트!
        # 1. POST로 넘어온 데이터 form에 넣기
        form = CustomUserChangeForm(request.POST, instance=user)
        # 2. form에서 데이터 검증하기
        if form.is_valid():
            # 3. 검증 통과하면, database에 저장
            form.save()
            # 4. 업데이트 결과 확인이 가능한 페이지로 안내
            return redirect('articles:index')
    else:
        # User 업데이트 양식 보여주기
        form = CustomUserChangeForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/edit.html', context)


def password(request):
    user = request.user
    if request.method == 'POST':
        # Password 변경!
        # 1. POST로 넘어온 data를 form에 넣기
        form = PasswordChangeForm(user, request.POST)
        # 2. form 유효성 검사
        if form.is_valid():
            # 3. 검사를 통과했다면, 저장!
            user = form.save()
            # 3-1. 저장 완료 후, 로그인 세션 유지!
            update_session_auth_hash(request, user)
            # 4. 어딘가로 돌려보내기
            return redirect('accounts:edit')
    else:
        # Password 변경 양식 보여주기
        form = PasswordChangeForm(user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password.html', context)


@login_required
def profile_detail(request):
    # 1:N - user.comment_set / comment.user
    # 1:1 - user.profile / profile.user
    profile = request.user.profile
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile_detail.html', context)


@login_required
def profile_edit(request):
    # 1. 현재 로그인 된 user의 profile 가져오기
    profile = request.user.profile

    if request.method == 'POST':
        # profile 업데이트
        # 1. POST로 넘어온 데이터 form에 넣기
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        # 2. form에서 유효성 검사
        if form.is_valid():
            # 3. 검사를 통과하면 저장
            form.save()
            # 4. 결과 확인이 가능한 페이지로 안내
            return redirect('accounts:profile_detail')
    else:
        # form에 profile 넣어서 양식 보여주기
        form = ProfileForm(instance=profile)
    context = {
        'form': form,
    }
    return render(request, 'accounts/profile_edit.html', context)


def profile(request, username):
    # username <- User가 들고 있음
    # User : Profile = 1 : 1
    # 1. profile.user.username
    profile = Profile.objects.get(user__username=username)
    # 2. User에서 username으로 user 찾고, user.profile
    # profile = get_user_model().objects.get(username=username).profile
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile_detail.html', context)
