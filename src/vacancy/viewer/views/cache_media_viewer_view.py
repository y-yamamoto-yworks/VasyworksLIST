"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
import os
import mimetypes
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class CacheMediaViewerView(View):
    """
    キャッシュメディアビューア
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user:
            raise Http404

        file_url = kwargs.get('file_url')
        if file_url:
            file_path = os.path.join(settings.CACHE_FILE_DIR, file_url.replace('/', os.sep))
            file_name = self.get_file_name(file_url)

            file = None
            try:
                file = open(file_path, 'rb')
                content_type = self.get_content_type(file_url)

                response = HttpResponse(file.read(), content_type=content_type)
                if self.is_attachment(content_type):
                    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)

                file.close()
                return response

            except:
                if file:
                    file.close()
                raise Http404

        else:
            raise Http404

    @classmethod
    def get_content_type(cls, url: str):
        """ URLからContent-Typeを取得 """
        ans = ''
        if url:
            mimetype = mimetypes.guess_type(url)
            if mimetype:
                ans = mimetype[0]

        return ans

    @classmethod
    def get_file_name(cls, url: str):
        ans = ''
        if url:
            ans = url.rsplit('/', 1)[1]

        return ans

    @classmethod
    def is_attachment(cls, content_type):
        """ 指定のContent_Typeがダウンロード対象ならTrue  """
        ans = True
        if 'image/' in content_type:
            ans = False
        elif 'video/' in content_type:
            ans = False
        elif 'application/pdf' in content_type:
            ans = False

        return ans
