from django.db import models

# Create your models here.
class PDFFile(models.Model):
    request_id = models.IntegerField(db_column="rid",verbose_name="用户提交时随机产生一个id，用于下载文件的凭证")
    file =models.FileField(upload_to="pdf",db_column="file")
    class Meta:
        db_table = "pdfdb"