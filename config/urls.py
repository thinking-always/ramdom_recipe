from django.contrib import admin
from django.urls import path, include
from random_recipe import views
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

def social_complete(request):
    #세션 로그인 상태(= allauth로 소셜 로그인 성공)라면 JWT 발급 후 프론트로 넘김
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    refresh = RefreshToken.for_user(request.user)
    #프론트 리다이렉트 (해시로 전달: 쿼리스트링보다 안전하고 간다)
    fe = "http//localhost:5173/social-complete"
    return redirect(f"{fe}#access={str(refresh.access_token)}&refresh={str(refresh)}")


urlpatterns = [
    path("admin/", admin.site.urls),
    #allauth: 웹용 로그인/회원가입/소셜 로그인
    path("accounts/", include("allauth.urls")),
    path('', views.home, name='home'),
    
    #dj-rest-auth: API 로그인/회원가입 (React 연동 대비)
    
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    
    #SimpleJWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("social/complete/", social_complete, name="social_complete"),
    
]
