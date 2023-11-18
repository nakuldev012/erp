import io
import os
from posixpath import splitext
import ssl
import uuid
from urllib.request import urlretrieve
from django.forms import ValidationError
from datetime import datetime

from mferp.common.constant import TZ

import requests
from django.core.files import File
from django.db import models
from PIL import Image
# from mferp.mastertableconfig.models import AbstractTime
from mferp.auth.user.models import Account
from mferp.common.constant import MAX_FILE_SIZE
from mferp.common.errors import ForbiddenErrors

ssl._create_default_https_context = ssl._create_unverified_context


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/<upload_type>/year/month/day/<sub_dir>/<filename>
    sub_dir = "/{}".format(instance.sub_dir) if instance.sub_dir else ""
    date = datetime.now(tz=TZ).strftime("%Y/%m/%d")
    year, month, day = date.split("/")
    exts = ('jpg', 'jpeg', 'png',)
    ext = filename.split(".")[-1]
    check_extension(ext)
    if ext in exts:
        filename = ".".join(filename.split(".")[:-1])
        return os.path.join(year,month,day,"uploads","Image",sub_dir, f"{filename[:450]}.{ext}")
    else:
        filename = ".".join(filename.split(".")[:-1])
        return os.path.join(year,month,day,"uploads","document",sub_dir, f"{filename[:450]}.{ext}")

def check_extension(ext):
        allowed_exts = ('jpg', 'jpeg', 'png', 'svg', 'pdf', 'zip')
        ext = ext.lower()
        if ext not in allowed_exts:
            raise ForbiddenErrors("Allowed file types: {0}".format(allowed_exts))
        ext_map = {
			'.jpeg': '.jpg'
		}
        return ext_map.get(ext) or ext    

# def validate_file_size(value):
# 	video_allowed_ext = ('.mp4', '.mov')
# 	_, ext = os.path.splitext(value.name)

# 	limit_kb = get_int_config('upload.max_video_size_kb' if ext in video_allowed_ext else 'upload.max_file_size_kb')
# 	if value.size > limit_kb * 1024:
# 		raise exceptions.ValidationError('File too large. Size should not exceed {0} MiB'.format(limit_kb/1024))



class UploadedFile(models.Model):

    upload = models.FileField(upload_to=user_directory_path, max_length=500 )
    height = models.PositiveIntegerField(blank=True, null=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    sub_dir = models.CharField(max_length=100, null=True, blank=True, default="")
    ext = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        related_name="uploaded_files",
        null=True,
        blank=True,
    )
    thumbnail = models.FileField(
        upload_to=user_directory_path, max_length=500, null=True, blank=True
    )

    def clean(self):
        super().clean()

        if self.upload:
            if self.upload.size > MAX_FILE_SIZE:
                raise ForbiddenErrors(f"File size should not exceed {MAX_FILE_SIZE//(1024*1024)} MB")

    def save(self, *args, **kwargs):
        self.clean()  # Perform the size validation before saving

        if self.upload and self.upload.name.lower().endswith(('.jpg', '.jpeg', '.png',)):
            try:
                with Image.open(self.upload) as img:
                    self.height, self.width = img.size
            except Exception as e:
                # Handle exceptions if the file is not a valid image or there are other issues
                pass
        _, ext = splitext(self.upload.name)
        self.ext = ext

        super().save(*args, **kwargs)

  

    # def __str__(self):
    #     return str(self.upload)

    # @staticmethod
    # def resize(img, var):
    #     size = img.resize(
    #         (int(img.width / var), int(img.height / var)), Image.ANTIALIAS
    #     )
    #     return size


    