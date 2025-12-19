// Minimal keyboard support for the site nav (moved from base template)
document.addEventListener('DOMContentLoaded', function(){
  const menubar = document.querySelector('.site-menubar');
  if(!menubar) return;
  const navToggle = document.getElementById('nav-toggle');
  if(navToggle){
    navToggle.addEventListener('click', function(){
      const open = menubar.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  const topLinks = Array.from(menubar.querySelectorAll('.nav-link'));

  topLinks.forEach((link, idx) => {
    const navItem = link.closest('.nav-item');
    const dropdown = navItem ? navItem.querySelector('.dropdown') : null;

    link.addEventListener('keydown', function(e){
      if(e.key === 'ArrowDown' && dropdown){
        // open and focus first child
        const first = dropdown.querySelector('.dropdown-item');
        if(first){
          e.preventDefault();
          link.setAttribute('aria-expanded','true');
          first.focus();
        }
      } else if(e.key === 'ArrowRight'){
        e.preventDefault();
        const next = topLinks[(idx+1) % topLinks.length];
        next.focus();
      } else if(e.key === 'ArrowLeft'){
        e.preventDefault();
        const prev = topLinks[(idx-1+topLinks.length) % topLinks.length];
        prev.focus();
      }
    });

    if(dropdown){
      const items = Array.from(dropdown.querySelectorAll('.dropdown-item'));
      items.forEach((it, i)=>{
        it.addEventListener('keydown', function(e){
          if(e.key === 'ArrowDown'){
            e.preventDefault();
            if(i+1 < items.length) items[i+1].focus();
          } else if(e.key === 'ArrowUp'){
            e.preventDefault();
            if(i-1 >= 0) items[i-1].focus(); else link.focus();
          } else if(e.key === 'Escape'){
            e.preventDefault();
            link.focus();
            link.setAttribute('aria-expanded','false');
          }
        });
      });
    }
  });
});
