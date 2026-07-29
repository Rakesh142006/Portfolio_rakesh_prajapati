document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      toggle.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        links.classList.remove('is-open');
        toggle.classList.remove('is-open');
      });
    });
  }

  // Scroll reveal
  var revealEls = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // Certificate image lightbox
  var certModal = document.getElementById('certModal');
  if (certModal) {
    var modalImage = document.getElementById('certModalImage');
    var modalTitle = document.getElementById('certModalTitle');
    var modalIssuer = document.getElementById('certModalIssuer');

    var openCertModal = function (trigger) {
      var image = trigger.dataset.certImage;
      var title = trigger.dataset.certTitle;
      var issuer = trigger.dataset.certIssuer;
      var date = trigger.dataset.certDate;

      modalImage.src = image;
      modalImage.alt = title;
      modalTitle.textContent = title;
      modalIssuer.textContent = issuer + (date ? ' · ' + date : '');

      certModal.classList.add('is-open');
      certModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    };

    var closeCertModal = function () {
      certModal.classList.remove('is-open');
      certModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    document.querySelectorAll('.cert-image-trigger').forEach(function (img) {
      img.addEventListener('click', function () { openCertModal(img); });
    });

    certModal.querySelectorAll('[data-close-modal]').forEach(function (el) {
      el.addEventListener('click', closeCertModal);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeCertModal();
    });
  }
});


const themeBtn=document.getElementById("themeToggle");

// Load theme
if(localStorage.getItem("theme")==="light"){
    document.body.classList.add("light-theme");
    themeBtn.innerHTML="☀️";
}else{
    themeBtn.innerHTML="🌙";
}

themeBtn.onclick=function(){

    document.body.classList.toggle("light-theme");

    if(document.body.classList.contains("light-theme")){

        localStorage.setItem("theme","light");
        themeBtn.innerHTML="☀️";

    }else{

        localStorage.setItem("theme","dark");
        themeBtn.innerHTML="🌙";

    }

}
