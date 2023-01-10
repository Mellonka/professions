let plots_btn = document.querySelector('.plots-btn');
let table_btn = document.querySelector('.table-btn');
let plots = document.querySelector('.plots-div');
let table = document.querySelector('.table-div');

plots_btn.onclick = function () {
    if (!plots_btn.classList.contains('btn-primary')){
        plots_btn.classList.add('btn-primary')
        plots_btn.classList.remove('btn-secondary')

        table_btn.classList.remove('btn-primary');
        table_btn.classList.add('btn-secondary');

        plots.classList.remove('d-none');
        table.classList.add('d-none');
    }
}

table_btn.onclick = function () {
    if (!table_btn.classList.contains('btn-primary')){
        table_btn.classList.add('btn-primary');
        table_btn.classList.remove('btn-secondary');

        plots_btn.classList.remove('btn-primary')
        plots_btn.classList.add('btn-secondary')

        plots.classList.add('d-none');
        table.classList.remove('d-none');
    }
}
