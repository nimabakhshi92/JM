function showVerses(){
    var obj = document.getElementById("FehrestAyat");
    obj.style.display="block";
    var obj = document.getElementById("Fehrest");
    obj.style.display="none";
    var obj = document.getElementById("FehrestAyatMozuee");
    obj.style.display="none";
    document.getElementById("AyatSubjectButton1").style.backgroundColor = 'green';
    document.getElementById("AyatSubjectButton2").style.backgroundColor = 'green';
    document.getElementById("AyatSubjectButton3").style.backgroundColor = 'green';

    document.getElementById("RevayatSubjectButton1").style.backgroundColor = 'white';
    document.getElementById("RevayatSubjectButton2").style.backgroundColor = 'white';
    document.getElementById("RevayatSubjectButton3").style.backgroundColor = 'white';

    document.getElementById("AyatSubjectSubjectButton1").style.backgroundColor = 'white';
    document.getElementById("AyatSubjectSubjectButton2").style.backgroundColor = 'white';
    document.getElementById("AyatSubjectSubjectButton3").style.backgroundColor = 'white';
}
function showAyatSubject(){
    var obj = document.getElementById("FehrestAyatMozuee");
    obj.style.display="block";
    var obj = document.getElementById("FehrestAyat");
    obj.style.display="none";
    var obj = document.getElementById("Fehrest");
    obj.style.display="none";
    document.getElementById("AyatSubjectSubjectButton1").style.backgroundColor = 'green';
    document.getElementById("AyatSubjectSubjectButton2").style.backgroundColor = 'green';
    document.getElementById("AyatSubjectSubjectButton3").style.backgroundColor = 'green';

    document.getElementById("AyatSubjectButton1").style.backgroundColor = 'white';
    document.getElementById("AyatSubjectButton2").style.backgroundColor = 'white';
    document.getElementById("AyatSubjectButton3").style.backgroundColor = 'white';

    document.getElementById("RevayatSubjectButton1").style.backgroundColor = 'white';
    document.getElementById("RevayatSubjectButton2").style.backgroundColor = 'white';
    document.getElementById("RevayatSubjectButton3").style.backgroundColor = 'white';
}

function showRevayatSubject(){
    var obj = document.getElementById("FehrestAyatMozuee");
    obj.style.display="none";
    var obj = document.getElementById("FehrestAyat");
    obj.style.display="none";
    var obj = document.getElementById("Fehrest");
    obj.style.display="block";
    document.getElementById("RevayatSubjectButton1").style.backgroundColor = 'green';
    document.getElementById("RevayatSubjectButton2").style.backgroundColor = 'green';
    document.getElementById("RevayatSubjectButton3").style.backgroundColor = 'green';

    document.getElementById("AyatSubjectButton1").style.backgroundColor = 'white';
    document.getElementById("AyatSubjectButton2").style.backgroundColor = 'white';
    document.getElementById("AyatSubjectButton3").style.backgroundColor = 'white';

    document.getElementById("AyatSubjectSubjectButton1").style.backgroundColor = 'white';
    document.getElementById("AyatSubjectSubjectButton2").style.backgroundColor = 'white';
    document.getElementById("AyatSubjectSubjectButton3").style.backgroundColor = 'white';
}
function showMoreBoxes2(){
    var obj = document.getElementById("MoreSummariesBoxes2");
    obj.style.display="none";
    var elements1 = document.querySelectorAll("#FehrestSummaryObject40 ~ .FehrestSummaryObject");
    var elements3 = document.querySelectorAll("#FehrestSummaryAyatObject40 ~ .FehrestSummaryObject");
    var elements4 = document.querySelectorAll("#RelatedExplanationObject40 ~ .FehrestSummaryObject");
    for (let i = 0; i < 30; i++){
        elements1[i].style.display = "block";
        elements3[i].style.display = "block";
        elements4[i].style.display = "block";
    }
}
function showRepeatBox(){
    var obj = document.getElementById("RepeatBoxDiv");
    obj.style.display="block";
}
function closeRepeatBox(){
    var obj = document.getElementById("RepeatBoxDiv");
    obj.style.display="none";
}
showRevayatSubject()