const el = document.getElementById('quran-data').textContent
const quran = JSON.parse(el)['quran'];
console.log('allInputs')

function setCharAt(str,index,chr) {
    if(index > str.length-1) return str;
    return str.substring(0,index) + chr + str.substring(index+1);
}

const selectSurah = function(i){
    clearSurahSelection(i)
    const verse_no = document.getElementById('verse_no'+i)
    const surah_name = document.getElementById('surah_name'+i).value
    const verses = quran.filter((verse)=>verse.surah_name === surah_name)
    for(let i = 0; i<verses.length; i++){
        let child = document.createElement('option')
        child.textContent = verses[i].verse_no
        verse_no.appendChild(child)
    }
    setVerseContent(i)

}

const clearSurahSelection = function(i){
    const verse_no = document.getElementById('verse_no'+i)
      verse_no.innerHTML = '';
}

const setVerseContent = function(i){
    const surah_name = document.getElementById('surah_name'+i).value
    const verse_no = document.getElementById('verse_no'+i)
    const verse_text_el = document.getElementById('verse_text'+i)
    const verses = quran.filter((verse)=>verse.surah_name === surah_name)
    selectedVerse = verses.filter((verse)=>verse.verse_no == verse_no.value)[0]
    selectedVerseText = selectedVerse.verse_content
    verse_text_el.value = selectedVerseText
}
const changeVerseAvailablity = function(i){
    const surah_name = document.getElementById('surah_name'+i)
    console.log(surah_name.value)
    let isDisabled = surah_name.disabled
    console.log(isDisabled)
    surah_name.disabled = !isDisabled
    console.log(surah_name.disabled)
    const verse_no = document.getElementById('verse_no'+i)
    isDisabled = verse_no.disabled
    verse_no.disabled = !isDisabled
}
const fillFootnotesAutomatically = ()=>{
    for(let i=1; i<1000; i++){
        let e = document.getElementById('Expression'+i)
        if(e){
            e.value = ''
        }
    }
    console.log('user_verse_text')
    let user_verse_text = document.getElementById('HadisText').value
    console.log(user_verse_text)
    if(user_verse_text){
        let i = 1
        while(true){
            if(user_verse_text.indexOf('@')===-1)
                break

                let idx1 = user_verse_text.indexOf('@')
                user_verse_text = setCharAt(user_verse_text, idx1, 'a')
                console.log(idx1)
                 if(user_verse_text.indexOf('@')===-1)
                break

                let idx2 = user_verse_text.indexOf('@')
                user_verse_text = setCharAt(user_verse_text, idx2, 'a')
                console.log(idx2)
                let note = user_verse_text.substring(idx1+1, idx2)
                let expressionEl = document.getElementById('Expression'+i)
                expressionEl.value = note
                i++
        }
    }
}

function copy(i){
    console.log(i)
    let names = ["Alphabet", 'Subject', 'Text1', 'Text2', 'Text3']
    for(let j=0; j<names.length; j++ ){
        document.getElementById(names[j]+i).value = document.getElementById(names[j]+Math.floor(i-1)).value
    }
}

let classes = ['.fehrest-subject-input','.fehrest-input','.InputOne','.InputSubject']

classes.forEach(className=>{
const allInputs = document.querySelectorAll(className)
console.log(allInputs)
allInputs.forEach((input)=>{
    const defaultWidth = input.style.width
    input.addEventListener('mouseenter', ()=>{
    let newWidth = (input.value.length + 1) * 8
    if(newWidth>140)
        input.style.width = newWidth + 'px'
    })
    input.addEventListener('mouseleave', ()=>{
        input.style.width = defaultWidth
    })
})

})

for(let i=1; i<1000; i++){
    document.getElementById('surah_name'+i).addEventListener('change', ()=>selectSurah(i))
    document.getElementById('verse_no'+i).addEventListener('change', ()=>setVerseContent(i))
    document.getElementById('isVerse'+i).addEventListener('change', ()=>changeVerseAvailablity(i))
    document.getElementById('copy'+i).addEventListener('click', ()=>copy(i))
    selectSurah(i)
}

fillFootnotesAutomatically()


