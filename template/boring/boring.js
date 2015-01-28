window.onload = set_header_offset;
window.onresize = set_header_offset;

function set_header_offset() {
    var header_height = document.getElementById('header').clientHeight;
    var section = document.getElementById('section');
    section.style.marginTop = (header_height + "px");
}
