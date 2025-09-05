from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

FRONTEND_URL = "http://localhost:5173/social-complete"

def social_complete(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")

    refresh = RefreshToken.for_user(request.user)
    access = str(refresh.access_token)
    refresh = str(refresh)

    resp = redirect(FRONTEND_URL)

    # ✅ 개발환경은 secure=False. 운영은 secure=True + HTTPS 필수
    resp.set_cookie(
        "access_token",
        access,
        httponly=True,
        samesite="Lax",
        secure=False,
        max_age=60 * 30,  # 30분
    )
    resp.set_cookie(
        "refresh_token",
        refresh,
        httponly=True,
        samesite="Lax",
        secure=False,
        max_age=60 * 60 * 24 * 7,  # 7일
    )
    
    return resp
    



def home(request):
    return render(request, "home.html")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })