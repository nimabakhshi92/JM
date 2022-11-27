function showMoreBoxes1(){
    var obj = document.getElementById("MoreSummariesBoxes1");
    obj.style.display="none";
    var obj = document.getElementById("MoreSummariesBoxes2");
    obj.style.display="inline";
    var elements1 = document.querySelectorAll("#FehrestSummaryObject20~.FehrestSummaryObject");
    var elements2 = document.querySelectorAll("#ContainingAyatObject10 ~ .FehrestSummaryObject");
    var elements3 = document.querySelectorAll("#FehrestSummaryAyatObject20 ~ .FehrestSummaryObject");
    var elements4 = document.querySelectorAll("#RelatedExplanationObject20 ~ .FehrestSummaryObject");
    for (let i = 0; i < elements1.length; i++){
        if (i<20){
            elements1[i].style.display = "block";
            elements3[i].style.display = "block";
            elements4[i].style.display = "block";
            }
        if(i<10){
            elements2[i].style.display = "block";
        }
    }
}
function showMoreBoxes2(){
    var obj = document.getElementById("MoreSummariesBoxes2");
    obj.style.display="none";
    var elements1 = document.querySelectorAll("#FehrestSummaryObject40 ~ .FehrestSummaryObject");
    var elements2 = document.querySelectorAll("#ContainingAyatObject20 ~ .FehrestSummaryObject");
    var elements3 = document.querySelectorAll("#FehrestSummaryAyatObject40 ~ .FehrestSummaryObject");
    var elements4 = document.querySelectorAll("#RelatedExplanationObject40 ~ .FehrestSummaryObject");
    for (let i = 0; i < 30; i++){
        elements1[i].style.display = "block";
        elements3[i].style.display = "block";
        elements4[i].style.display = "block";
        if(i<15){
            elements2[i].style.display = "block";
        }
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