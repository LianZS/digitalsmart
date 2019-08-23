from django.db import models


# Create your models here.
class PDFFile(models.Model):
    id = models.UUIDField(primary_key=True, db_column="id", verbose_name="用户提交时唯一产生uuid，用于下载文件的凭证", editable=False)
    file = models.FileField(upload_to="pdf", db_column="file")

    class Meta:
        db_table = "pdfdb"
