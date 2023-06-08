document.querySelector('.menu-toggle').addEventListener('click', function() {
    document.querySelector('aside').classList.toggle('collapsed');
  });


  
const nombreMenuElement = document.getElementById("nombreMenu");

const menuItems = document.querySelectorAll(".nav-item");

for (let i = 0; i < menuItems.length; i++) {
    menuItems[i].addEventListener("click", (event) => {
        const menuTitle = event.currentTarget.innerText;
        nombreMenuElement.innerText = menuTitle;
    });
}


document.getElementById('file-upload').addEventListener('change', handleFileSelect, false);

function handleFileSelect(event) {
  const files = event.target.files;
  procesar_comprobante(files);
}


const dropZone = document.querySelector('.drop-zone');

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    // Realizar las acciones necesarias con el archivo
});



document.getElementById('file-upload').addEventListener('change', handleFileSelect, false);

function handleFileSelect(event) {
    const files = event.target.files;
    const tableRow = document.getElementById('table-row');
    const arrastrarText = document.getElementById('arrastrar');

    if (files.length > 0) {
        const fileName = files[0].name;
        const fileSize = files[0].size;

        const tableBody = document.getElementById('table-body');
        const newRow = document.createElement('tr');

        const newFileNameCell = document.createElement('td');
        newFileNameCell.textContent = fileName;

        const newFileSizeCell = document.createElement('td');
        newFileSizeCell.textContent = fileSize;

        newRow.appendChild(newFileNameCell);
        newRow.appendChild(newFileSizeCell);

        tableBody.appendChild(newRow);

        document.getElementById('file-name').textContent = fileName;

        tableRow.removeAttribute('hidden'); // Mostrar la fila

        arrastrarText.style.display = 'none'; // Ocultar el texto de arrastrar
    } else {
        tableRow.setAttribute('hidden', ''); // Ocultar la fila

        arrastrarText.style.display = 'block'; // Mostrar el texto "Arrastrar y soltar"
    }
}



