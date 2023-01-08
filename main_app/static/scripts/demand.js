let plots_btn = document.querySelector('.btn.plots');
let tables_btn = document.querySelector('.btn.tables');
let plots = document.querySelector('div.plots');
let tables = document.querySelector('div.tables');

plots_btn.onclick = function () {
    if (!plots_btn.classList.contains('btn-primary')){
        plots_btn.classList.add('btn-primary')
        plots_btn.classList.remove('btn-secondary')

        tables_btn.classList.remove('btn-primary');
        tables_btn.classList.add('btn-secondary');

        plots.classList.remove('d-none');
        tables.classList.add('d-none');
    }
}

tables_btn.onclick = function () {
    if (!tables_btn.classList.contains('btn-primary')){
        tables_btn.classList.add('btn-primary');
        tables_btn.classList.remove('btn-secondary');

        plots_btn.classList.remove('btn-primary')
        plots_btn.classList.add('btn-secondary')

        plots.classList.add('d-none');
        tables.classList.remove('d-none');
    }
}
