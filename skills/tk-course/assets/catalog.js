(() => {
  'use strict';
  const input=document.getElementById('catalog-search'),cards=[...document.querySelectorAll('[data-catalog-card]')];
  const normalize=value=>value.normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
  const indexed=cards.map(card=>({card,text:normalize(card.dataset.search)}));
  function filter(){
    const terms=normalize(input.value).split(' ').filter(Boolean);let count=0;
    for(const item of indexed){item.card.hidden=!terms.every(term=>item.text.includes(term));if(!item.card.hidden)count++;}
    document.getElementById('catalog-count').textContent=`전체 ${cards.length}개 중 ${count}개 코스`;
    document.getElementById('catalog-empty').hidden=count>0;
    document.getElementById('catalog-empty-title').textContent=`'${input.value.trim()}'와 일치하는 코스가 없습니다.`;
    document.querySelector('.catalog-grid').hidden=count===0;
  }
  document.getElementById('catalog-clear').addEventListener('click',()=>{input.value='';filter();input.focus();});
  input.addEventListener('input',filter);filter();document.getElementById('catalog-search-controls').hidden=false;
})();
