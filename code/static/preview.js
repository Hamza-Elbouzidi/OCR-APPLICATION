function renderJsonItem(item) {
    if (typeof item === 'object' && !Array.isArray(item)) {
        const ul = document.createElement('ul');
        for (const [key, value] of Object.entries(item)) {
            const li = document.createElement('li');
            const strong = document.createElement('strong');
            strong.textContent = `${key}: `;
            li.appendChild(strong);
            li.appendChild(renderJsonItem(value));
            ul.appendChild(li);
        }
        return ul;
    } else if (Array.isArray(item)) {
        if (item.length > 0 && typeof item[0] === 'object') {
            const table = document.createElement('table');
            const thead = document.createElement('thead');
            const tbody = document.createElement('tbody');
            const trHead = document.createElement('tr');
            for (const key of Object.keys(item[0])) {
                const th = document.createElement('th');
                th.textContent = key.charAt(0).toUpperCase() + key.slice(1);
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
        return document.createTextNode(item);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const jsonDataContainer = document.getElementById('json-data-container');
    const jsonData = JSON.parse(document.getElementById('json-data').textContent);

    for (const [key, value] of Object.entries(jsonData)) {
        const section = document.createElement('div');
        section.classList.add('section');
        const h2 = document.createElement('h2');
        h2.textContent = key.charAt(0).toUpperCase() + key.slice(1);
        section.appendChild(h2);
        const jsonContent = document.createElement('div');
        jsonContent.classList.add('json-content');
        jsonContent.appendChild(renderJsonItem(value));
        section.appendChild(jsonContent);
        jsonDataContainer.appendChild(section);
    }
});