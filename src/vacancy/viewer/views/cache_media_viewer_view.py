"""
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""
import os
import mimetypes
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class CacheMediaViewerView(View):
    """キャッシュメディアビューア"""

    @staticmethod
    def get_safe_viewer_path(base_dir, file_url):
        if not file_url:
            raise Http404

        real_base = os.path.abspath(base_dir)
        clean_rel_path = str(file_url).lstrip('/\\').replace('/', os.sep)
        target_path = os.path.abspath(os.path.join(real_base, clean_rel_path))

        if os.path.commonpath([real_base, target_path]) != real_base:
            raise Http404

        if not os.path.isfile(target_path):
            raise Http404

        return target_path

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user:
            raise Http404

        file_url = kwargs.get('file_url')
        if file_url:
            file_path = self.get_safe_viewer_path(settings.CACHE_FILE_DIR, file_url)
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
