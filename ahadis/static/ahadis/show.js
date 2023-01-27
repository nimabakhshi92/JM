function showAyatSubject(){
    var obj = document.getElementById("AyatSubject");
    obj.style.display="block";
    var obj = document.getElementById("AyatSerial");
    obj.style.display="none";
    document.getElementById("AyatSubjectButton").style.backgroundColor = 'green';
    document.getElementById("AyatSerialButton").style.backgroundColor = '#EEE';
}
function showAyatSerial(){
    var obj = document.getElementById("AyatSubject");
    obj.style.display="none";
    var obj = document.getElementById("AyatSerial");
    obj.style.display="block";
    document.getElementById("AyatSubjectButton").style.backgroundColor = '#EEE';
    document.getElementById("AyatSerialButton").style.backgroundColor = 'green';
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