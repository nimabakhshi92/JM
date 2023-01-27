from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import pandas as pd
import numpy as np
import json
from .utils import conn
from .models import *
from .serializers import *

# def save_imam(request):
#     imams_names = [
#         'حضرت پیامبر صلی الله علیه و آله',
#         'حضرت امیرالمومنین علیه السلام',
#         'حضرت زهرا سلام الله علیها',
#         'امام حسن علیه السلام',
#         'امام حسین علیه السلام',
#         'امام سجاد علیه السلام',
#         'امام باقر علیه السلام',
#         'امام صادق علیه السلام',
#         'امام کاظم علیه السلام',
#         'امام رضا علیه السلام',
#         'امام جواد علیه السلام',
#         'امام هادی علیه السلام',
#         'امام حسن عسکری علیه السلام',
#         'امام زمان علیه السلام',
#         'نامشخص',
#     ]
#     for imam_name in imams_names:
#         imam = Imam(name=imam_name)
#         imam.save()

# Create your views here.
def save_narration_page(request):
    books = get_books()
    imams = get_Imams()
    quran_verse = list(QuranVerse.objects.all().order_by('surah_no', 'verse_no').values())
    print(quran_verse)
    surah_names = []
    for verse in quran_verse:
        if verse['surah_name'] not in surah_names:
            surah_names.append((verse['surah_name']))
    # print(surah_names)
    return render(request, 'ahadis/save_hadis.html',
                  {'books': books, 'masoumin': imams,
                   'summaries_counter': range(1, 71), 'subjects_counter': range(1, 31),
                   'summaries_ayat_counter': range(1, 71), 'summaries_containing_ayat_counter': range(1, 36),
                   'related_explanation_counter': range(1, 71),
                   'quran': {'quran': quran_verse},
                   'surah_names': surah_names,
                   })


def get_books():
    books = Book.objects.all().values()
    return books


def get_intersection_of_hadis_to_others(hadis, others):
    def get_intersection_of_hadis_to_1_other(hadis, other):
        def lambda_map(x):
            if x == ' ':
                return -1
            elif x in splited_other:
                return 1
            else:
                return 0

        splited_hadis = hadis.split(' ')
        splited_other = other.split(' ')
        intersection_boolean = [(word in splited_other) & (word != ' ') for word in splited_hadis]
        intersection = list(map(lambda_map, splited_hadis))
        intersection = np.array(intersection)
        intersection_percent = sum(intersection == 1) / sum(intersection != -1) * 100
        return intersection_percent, intersection

    for h in others:
        intersection_percent, intersection = get_intersection_of_hadis_to_1_other(hadis, h)
        if intersection_percent > 80:
            return intersection, h
    else:
        return None, None


def check_hadis_repetition(request):
    hadis_text = request.POST['HadisTextForRepetition']
    if not hadis_text:
        return HttpResponse('متن حدیث را وارد نکردید')
    else:
        ahadis = get_ahadis()['Had_Text'].to_list()
        intersection, other = get_intersection_of_hadis_to_others(hadis_text, ahadis)
        if intersection is None:
            return HttpResponse('این حدیث تکراری نیست')
        else:
            splited = np.array(hadis_text.split(' '))
            intersection_cond = list(map(lambda x: x == 1, intersection))
            intersection_hadis = ' '.join(splited[intersection_cond])

            result_text_1 = 'حدیث تکراری است. کلمات زیر در یک حدیث دیگر وجود دارد'
            result_text_2 = 'حدیثی که در دیتابیس وجود دارد ' + '\n'

            # return HttpResponse(f'{result_text_1} \n {intersection_hadis} \n\n\n {result_text_2} \n {other}')

    return render(request, 'ahadis/check_hadis_repetition.html',
                  {'result_text_1': result_text_1, 'result_text_2': result_text_2,
                   'intersection_hadis': intersection_hadis, 'other': other})


def save_narration(request):
    hadis_text = request.POST['HadisText']
    hadis_name = request.POST['HadisName']
    narrators = request.POST['HadisNarrators']
    book_vol_no = request.POST['BookVolNo']
    book_vol_no = int(book_vol_no) if book_vol_no else None
    book_page_no = request.POST['BookPageNo']
    book_page_no = int(book_page_no) if book_page_no else None
    book_narration_no = request.POST['BookHadisNo']
    book_narration_no = int(book_narration_no) if book_narration_no else None
    imam_id = int(request.POST['MasoumID'])
    book_id = int(request.POST['BookID'])

    imam = Imam.objects.get(id=imam_id)
    book = Book.objects.get(id=book_id)

    narration = Narration(name=hadis_name, narrator=narrators, content=hadis_text,
                          book_vol_no=book_vol_no, book_page_no=book_page_no,
                          book_narration_no=book_narration_no)
    narration.book = book
    narration.imam = imam
    narration.save()

    subjects = [request.POST[f'HadisSubject{i}'] for i in range(1, 31)]
    for subject in subjects:
        if subject:
            narration_subject = NarrationSubject(subject=subject)
            narration_subject.narration = narration
            narration_subject.save()

    related_explanation = [
        {
            'expression': request.POST[f'Expression{i}'],
            'explanation': request.POST[f'Explanation{i}']
        }
        for i in range(1, 71)
    ]
    for expression_explanation in related_explanation:
        expression = expression_explanation['expression']
        explanation = expression_explanation['explanation']
        if expression and explanation:
            narration_footnote = NarrationFootnote(expression=expression, explanation=explanation)
            narration_footnote.narration = narration
            narration_footnote.save()

    # ayat = [{'soore_name': request.POST[f'ContainingAyatSoore{i}'],
    #          'aye_no': request.POST[f'ContainingAyatAye{i}']} for i in range(1, 36)]
    #

    # ayat_summaries_in_fehrest = [{'alphabet': request.POST[f'FehrestSoore{i}'],
    #                               'subject': request.POST[f'FehrestAyeNo{i}'],
    #                               'summary': request.POST[f'FehrestAyeText{i}']} for i in range(1, 71)]

    summaries_in_fehrest = [
        {'alphabet': request.POST[f'Alphabet{i}'],
         'subject_1': request.POST[f'Subject{i}'],
         'subject_2': request.POST[f'Text1{i}'],
         'subject_3': request.POST[f'Text2{i}'],
         'subject_4': request.POST[f'Text3{i}'],
         'expression': request.POST[f'Text4{i}'],
         'summary': request.POST[f'Text5{i}'],
         'is_verse': request.POST.get(f'isVerse{i}'),
         'surah_name': request.POST.get(f'surah_name{i}'),
         'verse_no': request.POST.get(f'verse_no{i}'),
         } for i in range(1, 71)
    ]

    for item in summaries_in_fehrest:
        if item['subject_1'] and item['alphabet']:
            if not item['summary']:
                item['summaty'] = None
            content_summary_tree = ContentSummaryTree(alphabet=item['alphabet'],
                                                      subject_1=item['subject_1'],
                                                      subject_2=item['subject_2'],
                                                      subject_3=item['subject_3'],
                                                      subject_4=item['subject_4'],
                                                      expression=item['expression'],
                                                      summary=item['summary'])
            content_summary_tree.narration = narration
            content_summary_tree.save()

            is_verse = item['is_verse']
            if is_verse:
                surah_name = item['surah_name']
                verse_no = item['verse_no']
                quran_verse = QuranVerse.objects.get(surah_name=surah_name, verse_no=verse_no)
                narration_verse = NarrationVerse()
                narration_verse.narration = narration
                narration_verse.quran_verse = quran_verse
                narration_verse.save()

    # cursor = conn.cursor()
    # for item in ayat:
    #     if item['soore_name'] and item['aye_no']:
    #         # item['soore_name'] = item['soore_name'] if item['soore_name'] else 'NULL'
    #         cursor.execute(
    #             f"INSERT INTO dbo.[AyatInHadis](Had_ID, [AyaIH_SooreName], [AyaIH_AyeNo]) "
    #             f"VALUES({had_id}, N'{item['soore_name']}', {item['aye_no']})")
    # cursor.commit()
    # cursor.close()

    return HttpResponseRedirect(reverse('ahadis:save_hadis_page'))


def show(request, had_ids=None):
    # df_json = get_ahadis(had_ids, in_json_format=True)
    # fehrest_json = get_ahadis_fehrest(in_hierarchy_format=True)
    # ayat_fehrest_json = get_ayat_fehrest(in_hierarchy_format=True)
    # ayat_fehrest_serial_json = get_ayat_fehrest_serial(in_hierarchy_format=True)
    narrations = get_narrations()
    content_summary_tree, content_summary_df = get_content_summary_tree()
    verses_content_summary_tree, verses_content_summary_df = get_verses_content_summary_tree()
    ayat_fehrest_json = []
    ayat_fehrest_serial_json = []
    # return render(request, 'ahadis/show.html', {'ahadis': df_json, 'fehrest': fehrest_json,
    #                                             'ayat_fehrest': ayat_fehrest_json,
    #                                             'ayat_fehrest_serial': ayat_fehrest_serial_json})
    return render(request, 'ahadis/show.html', {'ahadis': narrations, 'fehrest': content_summary_tree,
                                                'ayat_fehrest': verses_content_summary_tree,
                                                'ayat_fehrest_serial': ayat_fehrest_serial_json})


def save_book_page(request):
    return render(request, 'ahadis/save_book.html')


def save_book(request):
    name = request.POST['Name']
    publisher = request.POST['Publisher']
    author = request.POST['Author']
    subject = request.POST['Subject']
    language = request.POST['Language']

    new_book = Book(name=name, publisher=publisher, author=author, subject=subject, language=language)
    new_book.save()

    return HttpResponseRedirect(reverse('ahadis:save_book_page'))


def search(request):
    word1 = request.POST['word1']
    word2 = request.POST['word2']
    word3 = request.POST['word3']
    word4 = request.POST['word4']

    word1 = word1 if word1 else ''
    word2 = word2 if word2 else ''
    word3 = word3 if word3 else ''
    word4 = word4 if word4 else ''

    subject1 = request.POST['subject1']
    subject2 = request.POST['subject2']
    subject3 = request.POST['subject3']
    subject4 = request.POST['subject4']

    subject1 = subject1 if subject1 else None
    subject2 = subject2 if subject2 else None
    subject3 = subject3 if subject3 else None
    subject4 = subject4 if subject4 else None

    df = get_ahadis()
    df = filter_ahadis(df, [word1, word2, word3, word4], [subject1, subject2, subject3, subject4])
    df_json_str = df.to_json(orient="records")
    df_json = json.loads(df_json_str)
    fehrest_json = get_ahadis_fehrest(in_hierarchy_format=True)
    return render(request, 'ahadis/show.html', {'ahadis': df_json, 'fehrest': fehrest_json})


def filter_ahadis(ahadis_df, words, requested_subjects):
    if len(ahadis_df) > 0:
        ahadis_df = ahadis_df[
            ahadis_df['Had_Text'].apply(lambda x: all([word in remove_arabic_characters(x) for word in words]))]
        subjects = get_ahadis_subjects()
        ahadis_df = filter_ahadis_to_requested_subjects(ahadis_df, subjects, requested_subjects)
    return ahadis_df


def filter_ahadis_from_fehrest(request):
    had_id = request.POST['had_id']
    had_id = had_id if had_id else None

    df_json = get_ahadis(had_id, in_json_format=True)

    fehrest_json = get_ahadis_fehrest(in_hierarchy_format=True)
    return render(request, 'ahadis/show.html', {'ahadis': df_json, 'fehrest': fehrest_json})


def filter_ahadis_from_fehrest_subject(request):
    args = {}
    alphabet = request.POST.get('alphabet')
    if alphabet:
        args['alphabet'] = alphabet
    subject_1 = request.POST.get('subject_1')
    if subject_1:
        args['subject_1'] = subject_1
    subject_2 = request.POST.get('subject_2')
    if subject_2:
        args['subject_2'] = subject_2
    subject_3 = request.POST.get('subject_3')
    if subject_3:
        args['subject_3'] = subject_3
    subject_4 = request.POST.get('subject_4')
    if subject_4:
        args['subject_4'] = subject_4
    narration_id = request.POST.get('narration_id')
    if narration_id:
        args['narration_id'] = narration_id

    filtered_content_summary_tree, filtered_content_summary_df = get_content_summary_tree(**args)
    content_summary_tree, content_summary_df = get_content_summary_tree()

    narration_ids = filtered_content_summary_df['narration_id'].unique().tolist()
    narrations = get_narrations(narration_ids)
    return render(request, 'ahadis/show.html', {'ahadis': narrations, 'fehrest': content_summary_tree})


def remove_arabic_characters(string):
    to_get_replaced_characters = 'آةيؤإأۀ'
    replacers = 'اهیوااه'

    saken_dar = 'بْنُ'
    saken = saken_dar[1]
    to_be_removed_characters = 'ءًٌٍَُِّ' + saken

    my_table = string.maketrans(to_get_replaced_characters, replacers, to_be_removed_characters)
    result = string.translate(my_table)
    return result


def get_ahadis(had_ids=None, in_json_format=False):
    if (had_ids is not None) and (not isinstance(had_ids, list)):
        had_ids = [had_id for had_id in had_ids]

    if had_ids is None:
        had_ids_query_string = ''
    else:
        had_ids_query_string = f" AND h.Had_ID in ( {','.join(list(map(str, had_ids)))} )"

    query = f"SELECT h.*, b.Boo_Title, b.Boo_Publisher from dbo.hadis h WITH(NOLOCK) " \
            f"INNER JOIN dbo.book b ON h.Boo_ID = b.Boo_ID " \
            f"WHERE 1=1 {had_ids_query_string}"
    result = pd.read_sql_query(query, conn)
    if in_json_format:
        result = result.to_json(orient="records")
        result = json.loads(result)
    return result


def get_narrations(narration_ids=None):
    # n = Narration.objects.all()
    # nr = Narration.objects.select_related('narrationsubject').all()
    # ns = NarrationSerializer(n, many=True)
    # narrations = Narration.objects.all().values('name', 'narrator', 'content', 'book_vol_no', 'book_page_no',
    #                                             'book_narration_no', 'imam__name', 'narrationsubject__subject',
    #                                             'book__name', 'book__publisher', 'narrationfootnote__expression')
    narrations = Narration.objects.all().values('id', 'name', 'narrator', 'content', 'book_vol_no', 'book_page_no',
                                                           'book_narration_no', 'imam__name', 'book__name',
                                                           'book__publisher',
                                                           )
    # narrations_serialized = NarrationSerializer(narrations, many=True).data
    narrations_df = pd.DataFrame(narrations)
    if narration_ids:
        narrations_df = narrations_df[narrations_df['id'].isin(narration_ids)]
    result = narrations_df.to_json(orient="records")
    result = json.loads(result)
    return result


def get_content_summary_tree_old():
    content_summary_tree = ContentSummaryTree.objects.all().values()
    result = pd.DataFrame(content_summary_tree)
    result_json = {
        alphabet:
            {
                subject1:
                    [
                        {'had_id': id, 'summary': summary} for id, summary in
                        zip(result['id'][result['subject_2'] == subject1],
                            result['summary'][result['subject_2'] == subject1])
                    ]
                for subject1 in result['subject_1'][result['alphabet'] == alphabet] if subject1
            }
        for alphabet in result['alphabet'].unique() if alphabet
    }
    result = result_json
    return result


def nest(df, prev):
    print(prev)
    if len(df.columns) == 1:
        return list(df.iloc[:, 0])
    first_col_name = df.columns[0]
    output = {
        key: nest(df[df[first_col_name] == key].drop(first_col_name, axis=1), prev)
        for key in df[first_col_name].unique() if key
    }
    return output


def get_content_summary_tree(**kwargs):
    content_summary_tree = ContentSummaryTree.objects.filter(**kwargs).values()
    result = pd.DataFrame(content_summary_tree)
    result.replace('', None, inplace=True)
    column_names = ['alphabet', 'subject_1', 'subject_2', 'subject_3', 'subject_4']
    for i in range(1, len(column_names)):
        result[column_names[i]].fillna(result[column_names[i - 1]], inplace=True)
    result_df = result[
        ['alphabet', 'subject_1', 'subject_2', 'subject_3', 'subject_4', 'narration_id', 'expression', 'summary']]
    result_nested_json = nest(result_df, {})

    return result_nested_json, result_df


def get_verses_content_summary_tree(**kwargs):
    content_summary_tree = ContentSummaryTree.objects.filter(**kwargs).values()
    result = pd.DataFrame(content_summary_tree)
    result.replace('', None, inplace=True)

    narration_verse = NarrationVerse.objects.all().values()
    narration_verse_df = pd.DataFrame(narration_verse)
    narration_verse_df.replace('', None, inplace=True)

    result = pd.merge(result, narration_verse_df, how='inner', on='narration_id')
    column_names = ['alphabet', 'subject_1', 'subject_2', 'subject_3', 'subject_4']
    for i in range(1, len(column_names)):
        result[column_names[i]].fillna(result[column_names[i - 1]], inplace=True)
    result_df = result[
        ['alphabet', 'subject_1', 'subject_2', 'subject_3', 'subject_4', 'narration_id', 'expression', 'summary']]
    result_nested_json = nest(result_df, {})

    return result_nested_json, result_df


def get_Imams():
    return Imam.objects.all().values()


def get_had_id_for_insert_to_hadis_table():
    ahadis = get_ahadis()
    if len(ahadis) == 0:
        return 1
    else:
        return max(ahadis['Had_ID']) + 1


def get_ahadis_subjects():
    query = 'select * from JanatolMava.dbo.HadisSubject'
    result = pd.read_sql_query(query, conn)
    return result


def get_ahadis_fehrest(in_hierarchy_format=False):
    query = 'select * from JanatolMava.dbo.HadisSummaryInFehrest'
    result = pd.read_sql_query(query, conn)
    if in_hierarchy_format and len(result) > 0:
        result_json = {
            alphabet:
                {
                    subject:
                        [
                            {'had_id': had_id, 'summary': summary} for had_id, summary in
                            zip(result['Had_ID'][result['HadSIF_subject'] == subject],
                                result['HadSIF_Summary'][result['HadSIF_subject'] == subject])
                        ]
                    for subject in result['HadSIF_subject'][result['HadSIF_Alphabet'] == alphabet]
                }
            for alphabet in result['HadSIF_Alphabet'].unique()
        }
        result = result_json
    return result


def get_ayat_fehrest(in_hierarchy_format=False):
    query = 'select * from JanatolMava.dbo.AyatSummaryInFehrest'
    result = pd.read_sql_query(query, conn)
    if in_hierarchy_format and len(result) > 0:
        result_json = {
            alphabet:
                {
                    subject:
                        {
                            aye_expression:
                                [
                                    {'had_id': had_id, 'aye_explanation': aye_explanation}
                                    for had_id, aye_explanation in
                                    zip(result['Had_ID'][result['AyaSIF_AyeExpression'] == aye_expression],
                                        result['AyaSIF_AyeExplanation'][
                                            result['AyaSIF_AyeExpression'] == aye_expression],
                                        )
                                ]
                            for aye_expression in
                            result['AyaSIF_AyeExpression'][(result['AyaSIF_Alphabet'] == alphabet)
                                                           and (result[
                                                                    'AyaSIF_Subject'] == subject)]
                        }
                    for subject in result['AyaSIF_Subject'][result['AyaSIF_Alphabet'] == alphabet]
                }
            for alphabet in result['AyaSIF_Alphabet'].unique()
        }
        result = result_json
    return result


def get_ayat_fehrest_serial(in_hierarchy_format=False):
    query = 'select * from JanatolMava.dbo.[AyatInHadis]'
    result = pd.read_sql_query(query, conn)
    if in_hierarchy_format and len(result) > 0:
        result_json = {
            sooreh_name: [aye_no for aye_no in result['AyaIH_AyeNo'][result['AyaIH_SooreName'] == sooreh_name].unique()]
            for sooreh_name in result['AyaIH_SooreName'].unique()
        }
        result = result_json
    return result


def filter_ahadis_to_requested_subjects(ahadis, subjects, requested_subjects):
    requested_subjects = list(filter(lambda x: x is not None, requested_subjects))
    if len(requested_subjects) > 0:
        subjects_test = subjects.groupby('Had_ID').apply(
            lambda x: any(~pd.Series(requested_subjects).isin(x['HadS_Subject'])))
        filtered_ahadis_ids = list(subjects_test.index[~subjects_test])
        filtered_ahadis = ahadis[ahadis['Had_ID'].isin(filtered_ahadis_ids)]
        return filtered_ahadis
    else:
        return ahadis