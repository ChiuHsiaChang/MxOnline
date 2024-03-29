from datetime import datetime

from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import CourseOrg

from DjangoUeditor.models import UEditorField

#1. 设计表结构有几个重要的点
"""
实体1 <关系> 实体2
课程 章节 视频 课程资源
"""
#2. 实体的具体字段
#3. 每个字段的类型，是否必填

class Course(BaseModel):
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="課程機構")
    name = models.CharField(verbose_name="課程名", max_length=500)
    #desc = UEditorField(verbose_name="課程詳情", width=600, height=300, imagePath="courses/ueditor/images/",
    #                     filePath="courses/ueditor/files/", default="")
    #desc = models.CharField(verbose_name="課程描述", max_length=5000)
    students = models.IntegerField(default=0, verbose_name='學習人數')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人數')
    click_nums = models.IntegerField(default=0, verbose_name="點擊數")
    category = models.CharField(default=u"後端開發", max_length=20, verbose_name="課程類別")
    #tag = models.CharField(default="", verbose_name="課程標簽", max_length=10)
    is_classics = models.BooleanField(default=False, verbose_name="是否經典")
    detail = UEditorField(verbose_name="課程詳情", width=600, height=300, imagePath="courses/ueditor/images/",
                           filePath="courses/ueditor/files/", default="")
    is_banner = models.BooleanField(default=False, verbose_name="是否廣告位")
    image = models.CharField(max_length=1000, verbose_name=u"封面圖")

    class Meta:
        verbose_name = "課程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}'>".format(self.image.url))
    show_image.short_description = "圖片"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/course/{}'>跳轉</a>".format(self.id))
    go_to.short_description = "跳轉"


class BannerCourse(Course):
    class Meta:
        verbose_name = "輪播課程"
        verbose_name_plural = verbose_name
        proxy = True


class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    tag = models.CharField(max_length=100, verbose_name="標簽")

    class Meta:
        verbose_name = "課程標簽"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="課程") 
     #on_delete表示对应的外键数据被删除后，当前的数据应该怎么办
    name = models.CharField(max_length=500, verbose_name="章節名")

    class Meta:
        verbose_name = "課程章節"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="章節", on_delete=models.CASCADE)
    name = models.CharField(max_length=500, verbose_name=u"視頻名")
    url = models.CharField(max_length=1000, verbose_name=u"訪問地址")

    class Meta:
        verbose_name = "視頻"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name