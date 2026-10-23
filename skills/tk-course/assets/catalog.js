(() => {
  'use strict';
  const input=document.getElementById('catalog-search'),cards=[...document.querySelectorAll('[data-catalog-card]')],grid=document.querySelector('.catalog-grid');
  const sort=document.getElementById('catalog-sort'),direction=document.getElementById('catalog-direction'),key='tigerkit-course-catalog:sort';
  const normalize=value=>value.normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
  const indexed=cards.map(card=>({card,text:normalize(card.dataset.search)}));let ascending=false;
  try{const saved=JSON.parse(localStorage.getItem(key));if(saved&&['recommended','created_at','updated_at'].includes(saved.sort)&&typeof saved.ascending==='boolean'){sort.value=saved.sort;ascending=saved.ascending;}}catch(_){}
  function reorder(save=false){
    const field=sort.value==='created_at'?'createdAt':'updatedAt';
    const ordered=[...cards].sort((a,b)=>{
      const tie=Number(a.dataset.recommended)-Number(b.dataset.recommended);
      if(sort.value==='recommended')return tie;
      const x=a.dataset[field],y=b.dataset[field];if(!x||!y)return x?-1:y?1:tie;
      return (ascending?x.localeCompare(y):y.localeCompare(x))||tie;
    });
    const fragment=document.createDocumentFragment();for(const card of ordered)fragment.append(card);grid.append(fragment);
    direction.disabled=sort.value==='recommended';direction.textContent=ascending?'오래된순':'최신순';direction.setAttribute('aria-pressed',String(ascending));
    if(save)try{localStorage.setItem(key,JSON.stringify({sort:sort.value,ascending}));}catch(_){}
  }
  function filter(){
    const terms=normalize(input.value).split(' ').filter(Boolean);let count=0;
    for(const item of indexed){item.card.hidden=!terms.every(term=>item.text.includes(term));if(!item.card.hidden)count++;}
    document.getElementById('catalog-count').textContent=`전체 ${cards.length}개 중 ${count}개 코스`;
    document.getElementById('catalog-empty').hidden=count>0;
    document.getElementById('catalog-empty-title').textContent=`'${input.value.trim()}'와 일치하는 코스가 없습니다.`;
    grid.hidden=count===0;
  }
  sort.addEventListener('change',()=>reorder(true));direction.addEventListener('click',()=>{ascending=!ascending;reorder(true);});
  document.getElementById('catalog-clear').addEventListener('click',()=>{input.value='';filter();input.focus();});
  input.addEventListener('input',filter);reorder();filter();document.getElementById('catalog-search-controls').hidden=false;
})();
