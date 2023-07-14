function showMoreBoxes1(){
    var obj = document.getElementById("MoreSummariesBoxes1");
    obj.style.display="none";
    var obj = document.getElementById("MoreSummariesBoxes2");
    obj.style.display="inline";
    var elements1 = document.querySelectorAll("#FehrestSummaryObject20~.FehrestSummaryObject");
    var elements4 = document.querySelectorAll("#RelatedExplanationObject20 ~ .FehrestSummaryObject");
    for (let i = 0; i < elements1.length; i++){
        if (i<20){
            elements1[i].style.display = "block";
            elements4[i].style.display = "block";
            }
    }
}
function showMoreBoxes2(){
    var obj = document.getElementById("MoreSummariesBoxes2");
    obj.style.display="none";
    var elements1 = document.querySelectorAll("#FehrestSummaryObject40 ~ .FehrestSummaryObject");
    var elements4 = document.querySelectorAll("#RelatedExplanationObject40 ~ .FehrestSummaryObject");
    for (let i = 0; i < 30; i++){
        elements1[i].style.display = "block";
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