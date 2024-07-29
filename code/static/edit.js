function addItem(element, key) {
    var newItem = document.createElement('li');
    newItem.innerHTML = '<input type="text" placeholder="Add new item"><i class="fas fa-plus add-item" onclick="addItem(this, \'' + key + '\')"></i><i class="fas fa-minus remove-item" onclick="removeItem(this)"></i>';
    element.parentNode.parentNode.appendChild(newItem);
}

function removeItem(element) {
    element.parentNode.remove();
}

function saveData() {
    var data = {};
    var sections = document.querySelectorAll('.section');
    sections.forEach(function(section) {
        var key = section.querySelector('h2').innerText.toLowerCase();
        var value = parseSection(section.querySelector('.json-content').firstChild);
        data[key] = value;
    });

    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            alert('Data saved successfully!');
        } else {
            alert('Failed to save data.');
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving data.');
    });
}

function parseSection(element) {
    if (element.tagName === 'UL') {
        var list = [];
        element.querySelectorAll('li').forEach(function(li) {
            var input = li.querySelector('input');
            if (input) {
                list.push(input.value);
            }
        });
        return list;
    } else if (element.tagName === 'TABLE') {
        var table = [];
        var rows = element.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            var cells = row.querySelectorAll('td');
            var obj = {};
            cells.forEach(function(cell, index) {
                obj[element.querySelector('th:nth-child(' + (index + 1) + ')').innerText.toLowerCase()] = cell.querySelector('input').value;
            });
            table.push(obj);
        });
        return table;
    } else if (element.querySelector('input')) {
        return element.querySelector('input').value;
    }
    return null;
}
