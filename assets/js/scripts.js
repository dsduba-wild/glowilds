var body = document.querySelector('body')
var menuTrigger = document.querySelector('#toggle-main-menu-mobile');
var menuContainer = document.querySelector('#main-menu-mobile');

menuTrigger.onclick = function() {
    var open = menuContainer.classList.toggle('open');
    menuTrigger.classList.toggle('is-active')
    body.classList.toggle('lock-scroll')
    menuTrigger.setAttribute('aria-expanded', open)
    // The open menu covers the page: keep Tab inside it instead of on hidden content
    document.querySelectorAll('#main, .footer, .sub-footer').forEach(function(el) { el.inert = open })
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && menuContainer.classList.contains('open')) {
        menuTrigger.click()
        menuTrigger.focus()
    }
})
