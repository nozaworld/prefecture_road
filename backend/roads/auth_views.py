from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def _user_payload(user):
    """レスポンス用にユーザー情報を整形する（未ログインならis_authenticated=False）"""
    if user is not None and user.is_authenticated:
        return {'username': user.username, 'is_authenticated': True}
    return {'username': None, 'is_authenticated': False}


class CurrentUserView(APIView):
    """ログイン状態の確認用API。呼び出し時にCSRFトークンをCookieに発行する。"""

    permission_classes = [AllowAny]

    def get(self, request):
        get_token(request)
        return Response(_user_payload(request.user))


class LoginView(APIView):
    """セッションログイン。ユーザー登録機能は提供しない（ユーザー作成はDjango側のみ）。"""

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'ユーザー名またはパスワードが正しくありません。'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)
        return Response(_user_payload(user))


class LogoutView(APIView):
    """セッションログアウト。未ログインで呼んでも安全（何も起きない）。"""

    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response(_user_payload(request.user))
