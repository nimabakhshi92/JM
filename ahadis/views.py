from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import pyodbc
import pandas as pd
import numpy as np
import json
from .utils import conn



# Create your views here.
def save_hadis_page(request):
    df = pd.read_sql_query('select * from dbo.Book', conn)
    df_json_str = df.to_json(orient="records")
    df_json = json.loads(df_json_str)

    masoumin = get_masoumin()
    return render(request, 'ahadis/save_hadis.html',
                  {'books': df_json, 'masoumin': masoumin,
                   'summaries_counter': range(1, 71), 'subjects_counter': range(1, 16),
                   'summaries_ayat_counter': range(1, 71), 'summaries_containing_ayat_counter': range(1, 36),
                   'related_explanation_counter': range(1, 71)})


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


def save_hadis(request):
    hadis_text = request.POST['HadisText']
    hadis_text = hadis_text if hadis_text else 'NULL'
    hadis_name = request.POST['HadisName']
    hadis_name = hadis_name if hadis_name else 'NULL'
    masoum_id = request.POST['MasoumID']
    masoum_id = masoum_id if masoum_id else 'NULL'
    hadis_narrators = request.POST['HadisNarrators']
    hadis_narrators = hadis_narrators if hadis_narrators else 'NULL'
    book_vol_no = request.POST['BookVolNo']
    book_vol_no = book_vol_no if book_vol_no else 'NULL'
    book_page_no = request.POST['BookPageNo']
    book_page_no = book_page_no if book_page_no else 'NULL'
    book_hadis_no = request.POST['BookHadisNo']
    book_hadis_no = book_hadis_no if book_hadis_no else 'NULL'

    book_id = request.POST['BookID']

    subjects = [request.POST[f'HadisSubject{i}'] for i in range(1, 16)]

    ayat = [{'soore_name': request.POST[f'ContainingAyatSoore{i}'],
             'aye_no': request.POST[f'ContainingAyatAye{i}']} for i in range(1, 36)]

    related_explanation = [{'expression': request.POST[f'Expression{i}'],
                            'explanation': request.POST[f'Explanation{i}']} for i in range(1, 71)]

    ayat_summaries_in_fehrest = [{'alphabet': request.POST[f'FehrestSoore{i}'],
                                  'subject': request.POST[f'FehrestAyeNo{i}'],
                                  'summary': request.POST[f'FehrestAyeText{i}']} for i in range(1, 71)]

    summaries_in_fehrest = [{'alphabet': request.POST[f'Alphabet{i}'],
                             'subject': request.POST[f'Subject{i}'],
                             'summary': request.POST[f'Text{i}']} for i in range(1, 71)]

    had_id = get_had_id_for_insert_to_hadis_table()

    cursor = conn.cursor()
    cursor.execute(
        "insert into dbo.Hadis(Had_ID, Had_Text, Had_Title, MasoumID, Had_Narrators, "
        "Boo_ID, Had_BookVolNo, Had_BookPageNo, Had_BookHadisNo) "
        f"values({had_id}, N'{hadis_text}', N'{hadis_name}', {masoum_id}, N'{hadis_narrators}', "
        f"{book_id}, {book_vol_no}, {book_page_no}, {book_hadis_no})")

    cursor.commit()
    cursor.close()

    cursor = conn.cursor()
    for subject in subjects:
        if subject:
            cursor.execute(f"INSERT INTO dbo.HadisSubject(Had_ID, HadS_Subject) VALUES({had_id}, N'{subject}')")
    cursor.commit()
    cursor.close()

    cursor = conn.cursor()
    for item in summaries_in_fehrest:
        if item['subject'] and item['alphabet']:
            item['summary'] = item['summary'] if item['summary'] else 'NULL'
            cursor.execute(
                f"INSERT INTO dbo.HadisSummaryInFehrest(Had_ID, HadSIF_Alphabet, HadSIF_subject, HadSIF_Summary) "
                f"VALUES({had_id}, N'{item['alphabet']}', N'{item['subject']}', N'{item['summary']}')")
    cursor.commit()
    cursor.close()

    cursor = conn.cursor()
    for item in ayat:
        if item['soore_name'] and item['aye_no']:
            # item['soore_name'] = item['soore_name'] if item['soore_name'] else 'NULL'
            cursor.execute(
                f"INSERT INTO dbo.[AyatInHadis](Had_ID, [AyaIH_SooreName], [AyaIH_AyeNo]) "
                f"VALUES({had_id}, N'{item['soore_name']}', {item['aye_no']})")
    cursor.commit()
    cursor.close()

    return HttpResponseRedirect(reverse('ahadis:save_hadis_page'))


def show(request, had_ids=None):
    df_json = get_ahadis(had_ids, in_json_format=True)
    fehrest_json = get_ahadis_fehrest(in_hierarchy_format=True)
    ayat_fehrest_json = get_ayat_fehrest(in_hierarchy_format=True)
    ayat_fehrest_serial_json = get_ayat_fehrest_serial(in_hierarchy_format=True)
    return render(request, 'ahadis/show.html', {'ahadis': df_json, 'fehrest': fehrest_json,
                                                'ayat_fehrest': ayat_fehrest_json,
                                                'ayat_fehrest_serial': ayat_fehrest_serial_json})


def save_book_page(request):
    return render(request, 'ahadis/save_book.html')


def save_book(request):
    name = request.POST['Name']
    publisher = request.POST['Publisher']
    author = request.POST['Author']
    subject = request.POST['Subject']
    language = request.POST['Language']

    cursor = conn.cursor()
    cursor.execute("insert into dbo.Book(Boo_Title, Boo_Author, Boo_Publisher, Boo_Language, Boo_Subject) "
                   f"values(N'{name}', N'{author}', N'{publisher}', N'{language}', N'{subject}')")
    cursor.commit()
    cursor.close()

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
    subject = request.POST['Subject']
    subject = subject if subject else None

    fehrest = get_ahadis_fehrest()
    had_ids = fehrest['Had_ID'][fehrest['HadSIF_subject'] == subject].unique()

    df_json = get_ahadis(had_ids, in_json_format=True)

    fehrest_json = get_ahadis_fehrest(in_hierarchy_format=True)
    return render(request, 'ahadis/show.html', {'ahadis': df_json, 'fehrest': fehrest_json})


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


def get_masoumin():
    query = 'select * from JanatolMava.dbo.Masoum'
    result = pd.read_sql_query(query, conn)
    result = result.to_json(orient="records")
    result = json.loads(result)
    return result


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
