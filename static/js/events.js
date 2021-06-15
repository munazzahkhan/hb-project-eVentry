'use strict';


const addItem = document.querySelector('#add-item');

addItem.addEventListener('click', (evt) => {
    document.getElementById('number-of-items').value += 1;
})

// addItem.addEventListener('click', (evt) => {
//     let itemsTable = document.getElementById('items-table');
//     let numberOfRows = itemsTable.rows.length;
//     let rowHTML = `
//     <tr>
//         <td>
//             <div>
//                 <label>Item name: </label>
//                 <input id="name-${numberOfRows}" name="name" placeholder="Item Name" required type="text" value="">
//             </div>
//             <br>
//             <div>
//                 <label>Description: </label>
//                 <textarea id="item_description-${numberOfRows}" name="item_description" placeholder="Item description" required></textarea>
//             </div>
//             <br>
//             <div>
//                 <label>Upload an item image: </label>
//                 <input id="item_image-${numberOfRows}" name="item_image" required type="file">
//             </div>
//             <br>
//             <div>
//                 <label>Link where to get it from: </label>
//                 <input id="link-${numberOfRows}" name="link" placeholder="Item link/source" type="text" value="">
//             </div>
//         </td>
//     </tr>`;
//         itemsTable.innerHTML += rowHTML;
    
//  //   cell.innerHTML = `<p>Item name: <input type='text' name='name-${numberOfRows}'></p>
//  //                     <p>Description: <textarea name='description-${numberOfRows}'></textarea></p>
//  //                     <p>Upload an item image: <input type='file' name='file-${numberOfRows}' autocomplete='off' required></p>
//  //                     <p>Link where to get it from: <input type='text' name='link-${numberOfRows}'></p>`;

//     document.getElementById('number-of-items').value = numberOfRows + 1;        
// })