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
    imam = models.ForeignKey('Imam', on_delete=models.CASCADE)
    narrator = models.TextField()
    content = models.TextField()
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
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
    narration = models.ForeignKey(Narration, models.CASCADE)
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'NarrationSubject'

    def __str__(self):
        return self.subject


class NarrationFootnote(models.Model):
    narration = models.ForeignKey(Narration, models.CASCADE, related_name='footnote')
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


class ContentSummaryTree(models.Model):
    narration = models.ForeignKey(Narration, models.CASCADE, related_name='content_summary_tree')
    alphabet = models.CharField(max_length=200)
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


class NarrationSubjectVerse(models.Model):
    content_summary_tree = models.ForeignKey(ContentSummaryTree, models.CASCADE)
    quran_verse = models.ForeignKey(QuranVerse, models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'NarrationSubjectVerse'
        unique_together = (('content_summary_tree', 'quran_verse'),)


class NarrationVerse(models.Model):
    narration = models.ForeignKey(Narration, models.CASCADE)
    quran_verse = models.ForeignKey(QuranVerse, models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'NarrationVerse'
        unique_together = (('narration', 'quran_verse'),)


# //////////////////////////////// APIs:
#
# class Book1(models.Model):
#     name = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'Book1'
#
#     def __str__(self):
#         return self.name
#
#
# class Imam1(models.Model):
#     name = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'Imam1'
#
#     def __str__(self):
#         return self.name
#
#
# class Narration1(models.Model):
#     name = models.CharField(max_length=200)
#     imam = models.ForeignKey('Imam1', on_delete=models.CASCADE, related_name='narration')
#     book = models.ForeignKey('Book1', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'Narration1'
#
#     def __str__(self):
#         return self.name
#
#
# class NarrationSubject1(models.Model):
#     narration = models.ForeignKey('Narration1', models.CASCADE, related_name='subjects')
#     subject = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'NarrationSubject1'
#
#     def __str__(self):
#         return self.subject
#
#
# class NarrationFootnote1(models.Model):
#     # narration = models.ForeignKey(Narration, models.CASCADE)
#     expression = models.TextField()
#
#     class Meta:
#         db_table = 'NarrationFootnote1'
#
#     def __str__(self):
#         return self.expression
#
#
# class QuranVerse1(models.Model):
#     verse_content = models.TextField()
#
#     class Meta:
#         db_table = 'QuranVerse1'
#
#     def __str__(self):
#         return self.verse_content
#
#
# response = [
#     {
#         'alphabet': 'a',
#         'subjects': [
#             {
#                 'title': 'job',
#                 'subSubjects': [
#                     {
#                         'title': 'teaching',
#                         'content': [
#                             {
#                                 'summary': 'teaching is good',
#                                 'expression': 'teaching is a good activity that helps other people learn many things.'
#                             }
#                         ]
#                     }
#                 ]
#             }
#         ]
#     }
# ]
#
# a = [{
#     'alphabet': 'a',
#     'subject': 'job',
#     'subSubject': 'teaching',
#     'summary': 'teaching is good',
#     'expression': 'teaching is a good activity that helps other people learn many things.'
# },
#     {
#         'alphabet': 'a',
#         'subject_1': 'job',
#         'subject_2': 'teaching',
#         'summary': 'teaching is good',
#         'expression': 'teaching is a good activity that helps other people learn many things.'
#     }
# ]
#
# b = {
#     "alphabet": "b",
#     "subject_1": "bb1",
#     "subject_2": "teaching1",
#     "summary": "teaching is good1",
#     "expression": "teaching is a good activity that helps other people learn many things.1"
# }
#
# table = [
#     {
#         'alphabet': 'a',
#         'subject': 'airplane',
#         'sub_subject': 'sub_airplane1',
#         'expression': 'exp 1',
#         'summary': 'summary 1',
#     },
#     {
#         'alphabet': 'a',
#         'subject': 'airplane',
#         'sub_subject': 'sub_airplane1',
#         'expression': 'exp 2',
#         'summary': 'summary 2',
#     },
#     {
#         'alphabet': 'a',
#         'subject': 'airplane',
#         'sub_subject': 'sub_airplane2'
#         ,
#         'expression': 'exp 3',
#         'summary': 'summary 3',
#     },
#     {
#         'alphabet': 'a',
#         'subject': 'arrow',
#         'sub_subject': 'sub_arrow1'
#         ,
#         'expression': 'exp 2',
#         'summary': 'summary 2',
#     },
#     {
#         'alphabet': 'a',
#         'subject': 'arrow',
#         'sub_subject': 'sub_arrow2'
#         ,
#         'expression': 'exp 2',
#         'summary': 'summary 2',
#     },
#
#     {
#         'alphabet': 'b',
#         'subject': 'basket',
#         'sub_subject': 'sub_basket1'
#         ,
#         'expression': 'exp 21',
#         'summary': 'summary 21',
#     },
#     {
#         'alphabet': 'b',
#         'subject': 'basket',
#         'sub_subject': 'sub_basket2'
#         ,
#         'expression': 'exp 2',
#         'summary': 'summary 2',
#     },
#     {
#         'alphabet': 'b',
#         'subject': 'book',
#         'sub_subject': 'sub_book1'
#         ,
#         'expression': 'exp 20',
#         'summary': 'summary 20',
#     },
#     {
#         'alphabet': 'b',
#         'subject': 'book',
#         'sub_subject': 'sub_book2'
#         ,
#         'expression': 'exp 12',
#         'summary': 'summary 12',
#     }
#
# ]
#
# a = [
#     {
#         'alphabet': 'a',
#         'subjects': [
#             {
#                 'title': 'airplane',
#                 'sub_subjects': [
#                     {'title': 'sub_airplane1', 'content': [{'expression': 'exp 1', 'summary': 'summary 1'},
#                                                            {'expression': 'exp 2', 'summary': 'summary 2'}]},
#                     {'title': 'sub_airplane2', 'content': [{'expression': 'exp 3', 'summary': 'summary 3'}]}
#                 ]
#             },
#             {
#                 'title': 'arrow',
#                 'sub_subjects': [
#                     {'title': 'sub_arrow1', 'content': [{'expression': 'exp 2', 'summary': 'summary 2'}]},
#                     {'title': 'sub_arrow2', 'content': [{'expression': 'exp 2', 'summary': 'summary 2'}]}
#                 ]
#             }
#         ],
#     },
#     {
#         'alphabet': 'b',
#         'subjects': [
#             {
#                 'title': 'basket',
#                 'sub_subjects': [
#                     {'title': 'sub_basket1', 'content': [{'expression': 'exp 21', 'summary': 'summary 21'}]},
#                     {'title': 'sub_basket2', 'content': [{'expression': 'exp 2', 'summary': 'summary 2'}]}
#                 ]
#             },
#             {
#                 'title': 'book',
#                 'sub_subjects': [
#                     {'title': 'sub_book1', 'content': [{'expression': 'exp 20', 'summary': 'summary 20'}]},
#                     {'title': 'sub_book2', 'content': [{'expression': 'exp 12', 'summary': 'summary 12'}]}
#                 ]
#             },
#         ]
#     },
# ]
#
#
# class ContentSummaryTree1(models.Model):
#     # narration = models.ForeignKey(Narration, models.CASCADE)
#     alphabet = models.CharField(max_length=200)
#     subject = models.CharField(max_length=200)
#     sub_subject = models.CharField(max_length=200)
#     # subject_3 = models.CharField(max_length=200)
#     # subject_4 = models.CharField(max_length=200)
#     expression = models.TextField()
#     summary = models.TextField()
#
#     # created = models.DateTimeField(auto_now_add=True)
#     # modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'ContentSummaryTree1'
#
#     def __str__(self):
#         return self.expression
#
# # class NarrationSubjectVerse1(models.Model):
# #     # content_summary_tree = models.ForeignKey(ContentSummaryTree, models.CASCADE)
# #     # quran_verse = models.ForeignKey(QuranVerse, models.CASCADE)
# #     created = models.DateTimeField(auto_now_add=True)
# #     modified = models.DateTimeField(auto_now=True)
# #
# #     class Meta:
# #         db_table = 'NarrationSubjectVerse1'
# #         unique_together = (('content_summary_tree', 'quran_verse'),)
# #
# #
# # class NarrationVerse1(models.Model):
# #     # narration = models.ForeignKey(Narration, models.CASCADE)
# #     # quran_verse = models.ForeignKey(QuranVerse, models.CASCADE)
# #     created = models.DateTimeField(auto_now_add=True)
# #     modified = models.DateTimeField(auto_now=True)
# #
# #     class Meta:
# #         db_table = 'NarrationVerse1'
# #         unique_together = (('narration', 'quran_verse'),)
# #
