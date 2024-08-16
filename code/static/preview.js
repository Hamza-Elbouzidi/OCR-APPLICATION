function renderJsonItem(item, key = null) {
    if (item === null || item === undefined) {
        const p = document.createElement('p');
        p.textContent = 'No data available';
        return p;
    }

    if (typeof item === 'object' && !Array.isArray(item)) {
        const ul = document.createElement('ul');
        for (const [subkey, subvalue] of Object.entries(item)) {
            const li = document.createElement('li');
            const strong = document.createElement('strong');
            strong.textContent = `${subkey}: `;
            li.appendChild(strong);
            li.appendChild(renderJsonItem(subvalue, subkey));
            ul.appendChild(li);
        }
        return ul;
    } else if (Array.isArray(item)) {
        if (item.length > 0 && typeof item[0] === 'object') {
            const table = document.createElement('table');
            const thead = document.createElement('thead');
            const tbody = document.createElement('tbody');
            const trHead = document.createElement('tr');
            for (const header of Object.keys(item[0])) {
                const th = document.createElement('th');
                th.textContent = header.charAt(0).toUpperCase() + header.slice(1);
                trHead.appendChild(th);
            }
            thead.appendChild(trHead);
            for (const row of item) {
                const tr = document.createElement('tr');
                for (const cell of Object.values(row)) {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    tr.appendChild(td);
                }
                tbody.appendChild(tr);
            }
            table.appendChild(thead);
            table.appendChild(tbody);
            return table;
        } else {
            const ul = document.createElement('ul');
            for (const subitem of item) {
                const li = document.createElement('li');
                li.appendChild(renderJsonItem(subitem));
                ul.appendChild(li);
            }
            return ul;
        }
    } else {
        const input = document.createElement('input');
        input.type = 'text';
        input.value = item;
        return input;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const jsonDataContainer = document.getElementById('json-data-container');
    const jsonDataElement = document.getElementById('json-data');

    if (jsonDataElement && jsonDataElement.textContent) {
        try {
            const jsonData = JSON.parse(jsonDataElement.textContent);
            console.log('Parsed JSON Data:', jsonData);

            if (typeof jsonData === 'object' && jsonData !== null) {
                for (const [key, value] of Object.entries(jsonData)) {
                    const section = document.createElement('div');
                    section.classList.add('section');

                    const h2 = document.createElement('h2');
                    h2.textContent = key.charAt(0).toUpperCase() + key.slice(1);
                    section.appendChild(h2);

                    const jsonContent = document.createElement('div');
                    jsonContent.classList.add('json-content');
                    jsonContent.appendChild(renderJsonItem(value, key));

                    section.appendChild(jsonContent);
                    jsonDataContainer.appendChild(section);
                }
            } else {
                console.error('Expected JSON data to be an object, but received:', jsonData);
                const p = document.createElement('p');
                p.textContent = 'No data available';
                jsonDataContainer.appendChild(p);
            }
        } catch (error) {
            console.error('Error parsing JSON data:', error);
            const p = document.createElement('p');
            p.textContent = 'Error parsing JSON data';
            jsonDataContainer.appendChild(p);
        }
    } else {
        console.error('No JSON data found in the DOM element.');
        const p = document.createElement('p');
        p.textContent = 'No JSON data found';
        jsonDataContainer.appendChild(p);
    }
});
