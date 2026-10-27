/* ===== Links & UTM – hier zentral pflegen =====
       TODO: echte Ziel-URLs eintragen (Produktseiten per PZN je Packungsgröße).
       Solange ein Wert leer ist, führt der Button zur offiziellen Produktseite. */
    const LINKS={
      productInfo:'https://www.klein-naturarznei.de/produkte/oxacant-sedativ-liquid.html',
      locator:'',       // z. B. Apothekenfinder (aponet.de o. Ä.)
      shopApotheke:'',  // z. B. https://www.shop-apotheke.com/arzneimittel/<PZN>/...
      docmorris:''      // z. B. https://www.docmorris.de/<produkt>/<PZN>
    };
    const UTM={utm_source:'herzzeit',utm_medium:'advertorial',utm_campaign:'oxacant_sedativ_liquid'};
    window.dataLayer=window.dataLayer||[];
    const track=(event,params={})=>window.dataLayer.push({event,...params});
    document.querySelectorAll('[data-link]').forEach(a=>{
      const base=LINKS[a.dataset.link]||LINKS.productInfo;
      try{const u=new URL(base);Object.entries(UTM).forEach(([k,v])=>u.searchParams.set(k,v));u.searchParams.set('utm_content',a.dataset.track||a.dataset.link);a.href=u.toString();}catch(e){a.href=base;}
    });
    document.addEventListener('click',e=>{const a=e.target.closest('[data-track]');if(a)track('cta_click',{cta_id:a.dataset.track,cta_target:a.dataset.link||a.getAttribute('href')});});

    const bar=document.getElementById('progress');
    addEventListener('scroll',()=>{const max=document.documentElement.scrollHeight-innerHeight;bar.style.width=(max>0?scrollY/max*100:0)+'%'},{passive:true});
    const quiz=document.getElementById('stress-check-form');
    const steps=[...quiz.querySelectorAll('.quiz-step')];
    const next=document.getElementById('quiz-next');
    const back=document.getElementById('quiz-back');
    const actions=document.getElementById('quiz-actions');
    const feedback=document.getElementById('quiz-feedback');
    const quizResult=document.getElementById('quiz-result');
    const resultTitle=document.getElementById('quiz-result-title');
    const resultCopy=document.getElementById('quiz-result-copy');
    const resultCta=document.getElementById('quiz-result-cta');
    const count=document.getElementById('quiz-count');
    const track2=document.getElementById('quiz-progress');
    let current=0;

    function showStep(index){
      current=index;
      steps.forEach((step,i)=>step.hidden=i!==current);
      back.hidden=current===0;
      next.textContent=current===steps.length-1?'Einordnung anzeigen':'Weiter';
      count.textContent=`Frage ${current+1} von ${steps.length}`;
      track2.style.width=`${(current+1)/steps.length*100}%`;
      feedback.textContent='';
    }

    const RESULTS={
      low:{title:'Nur wenige Belastungssignale',copy:'Ihre Antworten sprechen derzeit für wenige der beschriebenen Alltagssignale. Wenn Sie wissen möchten, warum Stress manchmal am Herzen spürbar wird, lesen Sie weiter.',cta:'Zusammenhang verstehen'},
      mid:{title:'Ihr Muster: Anspannung, die auch körperlich spürbar wird',copy:'Mehrere Ihrer Antworten betreffen Herzschlag, Abschalten und Erholung zugleich. Das passt zu einem häufigen Muster: Belastung bleibt nicht im Kopf, sondern zeigt sich auch im Herz-Kreislauf-System. Wie das zusammenhängt und was Sie selbst tun können, erfahren Sie unten.',cta:'Zusammenhang verstehen'},
      high:{title:'Die Belastung scheint deutlich spürbar',copy:'Bitte lassen Sie anhaltende, neue oder unklare Herzbeschwerden zuerst ärztlich abklären – dieses Ergebnis ist keine Diagnose. Ist eine organische Ursache ausgeschlossen, finden Sie unten Hintergründe und konkrete Schritte für mehr Ruhe im Alltag.',cta:'Hintergründe lesen'}
    };
    function finishQuiz(){
      const data=new FormData(quiz);
      const score=['q1','q2','q3','q4','q5'].reduce((sum,name)=>sum+Number(data.get(name)),0);
      const band=score<=4?'low':score<=9?'mid':'high';
      steps[current].hidden=true;
      actions.hidden=true;
      feedback.hidden=true;
      quizResult.hidden=false;
      count.textContent='Ihre Einordnung';
      track2.style.width='100%';
      resultTitle.textContent=RESULTS[band].title;
      resultCopy.textContent=RESULTS[band].copy;
      resultCta.textContent=RESULTS[band].cta;
      track('quiz_complete',{quiz_score:score,quiz_band:band});
    }

    next.addEventListener('click',()=>{
      const chosen=steps[current].querySelector('input:checked');
      if(!chosen){feedback.textContent='Bitte wählen Sie eine Antwort aus.';return;}
      if(current===0)track('quiz_start');
      if(current<steps.length-1)showStep(current+1);else finishQuiz();
    });
    back.addEventListener('click',()=>showStep(Math.max(0,current-1)));
    quiz.addEventListener('change',()=>{feedback.textContent=''});
    document.getElementById('quiz-restart').addEventListener('click',()=>{
      quiz.reset();
      quizResult.hidden=true;
      actions.hidden=false;
      feedback.hidden=false;
      showStep(0);
    });

    const readingTriggers=[...document.querySelectorAll('.reading-tab-trigger')];
    const readingPanels=[...document.querySelectorAll('.reading-panel')];
    const activateReadingTab=(index,moveFocus=false)=>{
      readingTriggers.forEach((trigger,i)=>{
        const active=i===index;
        trigger.setAttribute('aria-selected',String(active));
        trigger.tabIndex=active?0:-1;
      });
      readingPanels.forEach((panel,i)=>{
        const active=i===index;
        panel.classList.toggle('is-active',active);
        panel.hidden=!active;
      });
      if(moveFocus)readingTriggers[index].focus();
    };
    readingTriggers.forEach((trigger,index)=>{
      trigger.addEventListener('pointerenter',(event)=>{
        if(event.pointerType==='mouse')activateReadingTab(index);
      });
      trigger.addEventListener('click',()=>activateReadingTab(index));
      trigger.addEventListener('focus',()=>activateReadingTab(index));
      trigger.addEventListener('keydown',(event)=>{
        let nextIndex;
        if(event.key==='ArrowDown'||event.key==='ArrowRight')nextIndex=(index+1)%readingTriggers.length;
        if(event.key==='ArrowUp'||event.key==='ArrowLeft')nextIndex=(index-1+readingTriggers.length)%readingTriggers.length;
        if(event.key==='Home')nextIndex=0;
        if(event.key==='End')nextIndex=readingTriggers.length-1;
        if(nextIndex!==undefined){event.preventDefault();activateReadingTab(nextIndex,true);}
      });
    });
    activateReadingTab(0);

