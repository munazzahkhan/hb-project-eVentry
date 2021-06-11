'use strict';


const addItem = document.querySelector('#add-item');

addItem.addEventListener('click', (evt) => {
    let itemsTable = document.getElementById('items-table');
    let numberOfRows = itemsTable.rows.length;
    let row = itemsTable.insertRow();
    let cell = row.insertCell();
    
    cell.innerHTML = `<p>Item name: <input type='text' name='name-${numberOfRows}'></p>
                      <p>Description: <textarea name='description-${numberOfRows}'></textarea></p>
                      <p>Upload an item image: <input type='file' name='file-${numberOfRows}' autocomplete='off' required></p>
                      <p>Link where to get it from: <input type='text' name='link-${numberOfRows}'></p>`;

    document.getElementById('number-of-items').value = numberOfRows + 1;
    // alert(document.getElementById('number-of-items').value)                   
})