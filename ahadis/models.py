from django.db import models


# class Narration(models.Model):
#     narration_text = models.CharField(max_length=20000)
#     # date = models.DateTimeField('date')

class Book(models.Model):
    name = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    source_type = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Book'

    def __str__(self):
        return self.name


class Imam(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Imam'

    def __str__(self):
        return self.name


class Narration(models.Model):
    name = models.CharField(max_length=200)
    imam = models.ForeignKey('Imam', models.DO_NOTHING)
    narrator = models.CharField(max_length=200)
    content = models.TextField()
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)
    # book = models.ForeignKey('Book', on_delete=models.DO_NOTHING, related_name="narrations",
    #                          related_query_name="narration")
    book_vol_no = models.IntegerField()
    book_page_no = models.IntegerField()
    book_narration_no = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Narration'

    def __str__(self):
        return self.name


class NarrationSubject(models.Model):
    narration = models.ForeignKey(Narration, models.DO_NOTHING)
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'NarrationSubject'

    def __str__(self):
        return self.subject


class NarrationFootnote(models.Model):
    narration = models.ForeignKey(Narration, models.DO_NOTHING)
    expression = models.TextField()
    explanation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'NarrationFootnote'

    def __str__(self):
        return self.expression


class QuranVerse(models.Model):
    part_no = models.IntegerField()
    page_no = models.IntegerField()
    surah_no = models.IntegerField()
    verse_no = models.IntegerField()
    surah_name = models.CharField(max_length=100)
    verse_content = models.TextField()

    class Meta:
        db_table = 'QuranVerse'

    def __str__(self):
        return self.verse_content


class NarrationVerse(models.Model):
    narration = models.ForeignKey(Narration, models.DO_NOTHING)
    quran_verse = models.ForeignKey(QuranVerse, models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'NarrationVerse'
        unique_together = (('narration', 'quran_verse'),)


class ContentSummaryTree(models.Model):
    narration = models.ForeignKey(Narration, models.DO_NOTHING)
    alphabet = models.CharField(max_length=5)
    subject_1 = models.CharField(max_length=200)
    subject_2 = models.CharField(max_length=200)
    subject_3 = models.CharField(max_length=200)
    subject_4 = models.CharField(max_length=200)
    expression = models.TextField()
    summary = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ContentSummaryTree'

    def __str__(self):
        return self.expression
